"""
CSE Aspirant - Multi-Method Payment Request Generator (UPI, NEFT, Cards)
"""
from typing import Dict, Any
import urllib.parse
from core.config import config

class PaymentGateway:
    def __init__(self):
        self.upi_id = config.payment.upi_id
        self.merchant_name = config.payment.merchant_name
        self.bank_details = {
            "bank_name": config.payment.bank_name,
            "account_name": config.payment.account_name,
            "account_number": config.payment.account_number,
            "ifsc_code": config.payment.ifsc_code,
            "branch": config.payment.bank_branch,
        }

    def generate_payment_invoice(self, user_id: int, plan: str, amount: float) -> Dict[str, Any]:
        upi_payload = {
            "pa": self.upi_id,
            "pn": self.merchant_name,
            "am": f"{amount:.2f}",
            "cu": "INR",
            "tn": f"CSE-{plan.upper()}-{user_id}"
        }
        upi_intent = f"upi://pay?{urllib.parse.urlencode(upi_payload)}"
        
        return {
            "plan": plan.upper(),
            "amount": amount,
            "upi_id": self.upi_id,
            "upi_intent": upi_intent,
            "bank_neft": self.bank_details,
            "card_gateway_url": f"{config.payment.checkout_url.rstrip('/')}/checkout?order=CSE-{user_id}",
            "instructions": (
                "1. Pay via UPI, NEFT or Card.\n"
                "2. Note the 12-digit Bank Reference / UTR Number.\n"
                "3. Submit via `/submit_utr <12_digit_utr>` with optional screenshot."
            )
        }

payment_gateway = PaymentGateway()

