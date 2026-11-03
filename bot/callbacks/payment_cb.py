"""
CSE Aspirant - Payment & Promotion Callback Handlers
"""
from typing import Dict, Any
from payments.owner_approval import owner_approval
from promotion.reviewer import promotion_reviewer
from core.config import config

class PaymentCallbackHandler:
    async def handle_approval(self, callback_data: str, user_id: int) -> str:
        # Expected format: pay_approve_<utr> or pay_reject_<utr>
        parts = callback_data.split("_")
        if len(parts) != 3 or parts[1] not in {"approve", "reject"} or not parts[2]:
            return "Invalid payment review action."
        if user_id != config.bot.owner_id and user_id not in config.bot.sudo_users:
            return "⛔ Payment review is restricted to the owner or sudo users."
        action = parts[1]
        utr = parts[2]
        
        if action == "approve":
            res = await owner_approval.approve(utr, approver_id=user_id)
            if res["status"] == "ALREADY_ACTIVE":
                return f"ℹ️ Payment `{utr}` was already approved; no new key was issued."
            return f"✅ Payment `{utr}` Approved! User `{res['user_id']}` upgraded to {res['tier']}. Key: `{res['api_key']}`"
        await owner_approval.reject(utr, approver_id=user_id)
        return f"❌ Payment `{utr}` Rejected."

class PromoCallbackHandler:
    async def handle_review(self, callback_data: str, user_id: int) -> str:
        # Expected format: promo_approve_<promo_id> or promo_reject_<promo_id>
        parts = callback_data.split("_")
        action = parts[1]
        promo_id = parts[2]
        
        res = await promotion_reviewer.review(promo_id, action, owner_id=user_id)
        if res and res.status == "APPROVED":
            return f"✅ Promotion `{promo_id}` approved for publication."
        return f"❌ Promotion `{promo_id}` rejected."

payment_cb_handler = PaymentCallbackHandler()
promo_cb_handler = PromoCallbackHandler()

