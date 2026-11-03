"""
CSE Aspirant - Payment Reconciliation & Fraud Detection Engine
"""
from typing import Dict, Any, Optional
from database.repository import repo
from database.models import PaymentRecord
from payments.utr_validator import utr_validator
from error_handling.exceptions import PaymentReconciliationError
from core.logger import logger

class ReconciliationEngine:
    async def process_submission(
        self,
        user_id: int,
        utr: str,
        amount: float,
        method: str,
        screenshot_url: Optional[str] = None
    ) -> PaymentRecord:
        clean_utr = utr.strip().upper()
        if not utr_validator.validate(clean_utr):
            raise PaymentReconciliationError(f"Invalid UTR/Transaction format: '{utr}'. Must be 10-22 alphanumeric characters.")

        # Check duplicate
        existing = await repo.get_payment(clean_utr)
        if existing:
            raise PaymentReconciliationError(f"Duplicate transaction detected! UTR {clean_utr} already exists.")

        # Record payment as PENDING owner reconciliation
        # Note: Screenshots are stored for audit only; never trusted as confirmation!
        record = await repo.submit_payment(
            utr=clean_utr,
            user_id=user_id,
            amount=amount,
            method=method,
            screenshot_url=screenshot_url
        )
        logger.info(f"Payment submission staged for owner approval: UTR {clean_utr} (User {user_id})")
        return record

reconciliation_engine = ReconciliationEngine()

