"""
CSE Aspirant - Multi-Method Payment Request Generator (UPI, NEFT, Cards)
"""
from typing import Dict, Any
import urllib.parse

class PaymentGateway:
    def __init__(self):
        self.upi_id = "cse-aspirant@upi"
        self.merchant_name = "CSE Aspirant Academy"
        self.bank_details = {
            "bank_name": "State Bank of India",
            "account_name": "CSE ASPIRANT EDUTECH",
            "account_number": "394829104829",
            "ifsc_code": "SBIN0001234",
            "branch": "New Delhi Main Branch"
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
            "card_gateway_url": f"https://pay.cse-aspirant.org/checkout?order=CSE-{user_id}",
            "instructions": (
                "1. Pay via UPI, NEFT or Card.\n"
                "2. Note the 12-digit Bank Reference / UTR Number.\n"
                "3. Submit via `/submit_utr <12_digit_utr>` with optional screenshot."
            )
        }

payment_gateway = PaymentGateway()

