"""
Unit Tests for Payment System, Fraud Prevention & Activation
"""
import pytest
from payments.utr_validator import utr_validator
from payments.gateway import payment_gateway
from payments.reconciliation import reconciliation_engine
from payments.owner_approval import owner_approval
from database.repository import repo
from error_handling.exceptions import PaymentReconciliationError

def test_utr_validator():
    assert utr_validator.validate("421098234812") is True
    assert utr_validator.validate("SBIN1234567890") is True
    assert utr_validator.validate("") is False
    assert utr_validator.validate("short") is False
    assert utr_validator.validate("invalid@symbol!!") is False

def test_payment_gateway_invoice():
    inv = payment_gateway.generate_payment_invoice(user_id=123, plan="PREMIUM", amount=199.0)
    assert inv["amount"] == 199.0
    assert "upi://" in inv["upi_intent"]
    assert "SBIN" in inv["bank_neft"]["ifsc_code"]

@pytest.mark.asyncio
async def test_payment_submission_and_duplicate_prevention():
    user_id = 999
    utr = "UTRTEST123456"

    # 1. First submission should succeed as PENDING
    record = await reconciliation_engine.process_submission(
        user_id=user_id,
        utr=utr,
        amount=199.0,
        method="UPI",
        screenshot_url="https://audit.storage/ss1.png"
    )
    assert record.status == "PENDING"
    assert record.utr == utr

    # 2. Duplicate submission with same UTR must be rejected
    with pytest.raises(PaymentReconciliationError):
        await reconciliation_engine.process_submission(
            user_id=888,
            utr=utr,
            amount=199.0,
            method="UPI"
        )

@pytest.mark.asyncio
async def test_owner_approval_and_key_delivery():
    user_id = 555
    utr = "UTRAPPROVE789012"

    await reconciliation_engine.process_submission(user_id=user_id, utr=utr, amount=499.0, method="NEFT")
    
    # Owner approves the payment
    approval_res = await owner_approval.approve(utr=utr, approver_id=100)
    assert approval_res["tier"] == "PRO"
    assert approval_res["api_key"].startswith("csea_pro_")
    assert approval_res["rate_limit"] == 1000

    # Verify user record in repository
    user = await repo.get_user(user_id)
    assert user.tier == "PRO"


@pytest.mark.asyncio
async def test_repeated_approval_does_not_issue_another_key_or_subscription():
    utr = "UTRREPEAT123456"
    await reconciliation_engine.process_submission(user_id=556, utr=utr, amount=199.0, method="UPI")

    first = await owner_approval.approve(utr=utr, approver_id=100)
    second = await owner_approval.approve(utr=utr, approver_id=100)

    assert first["status"] == "ACTIVE"
    assert second["status"] == "ALREADY_ACTIVE"
    assert second["api_key"] is None
    assert len(repo._subscriptions) == 1

