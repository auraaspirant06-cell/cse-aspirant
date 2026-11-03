"""
CSE Aspirant - Payment Owner Approval Workflow
"""
from typing import Dict, Any
from core.config import config
from payments.activation import activation_service
from core.logger import logger

class OwnerApprovalWorkflow:
    def format_owner_notification(self, utr: str, user_id: int, amount: float, method: str, screenshot_url: str = None) -> str:
        return (
            "💰 **NEW PAYMENT SUBMISSION FOR APPROVAL**\n\n"
            f"👤 **User ID**: `{user_id}`\n"
            f"💳 **Method**: `{method}`\n"
            f"💵 **Amount**: `₹{amount:.2f}`\n"
            f"🔢 **UTR / Ref**: `{utr}`\n"
            f"📷 **Screenshot**: {screenshot_url or 'None Provided'}\n\n"
            "⚠️ *Verify UTR directly with bank statements before approving.*"
        )

    async def approve(self, utr: str, approver_id: int) -> Dict[str, Any]:
        logger.info(f"Owner {approver_id} approved payment UTR {utr}")
        return await activation_service.activate_and_deliver_keys(utr, approved_by=approver_id)

owner_approval = OwnerApprovalWorkflow()

