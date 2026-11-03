"""
CSE Aspirant - Payment & UTR Submission Commands
"""
from typing import Dict, Any, Optional
from payments.gateway import payment_gateway
from payments.reconciliation import reconciliation_engine
from core.config import config
from bot.keyboards.inline import inline_kb

async def handle_pay(user_id: int, plan: str = "PREMIUM") -> Dict[str, Any]:
    amount = 499.0 if plan.upper() == "PRO" else 199.0
    invoice = payment_gateway.generate_payment_invoice(user_id, plan, amount)
    
    bank = invoice["bank_neft"]
    text = (
        f"💳 **CSE ASPIRANT PAYMENT INVOICE ({invoice['plan']})**\n\n"
        f"💵 **Payable Amount**: `₹{amount:.2f}`\n\n"
        "⚡ **Option 1: UPI Transfer**\n"
        f"• UPI VPA: `{invoice['upi_id']}`\n"
        f"• Direct Link: [Click to Pay via UPI]({invoice['upi_intent']})\n\n"
        "🏛 **Option 2: NEFT / IMPS Bank Transfer**\n"
        f"• Bank: {bank['bank_name']}\n"
        f"• Account: `{bank['account_number']}`\n"
        f"• IFSC: `{bank['ifsc_code']}`\n"
        f"• Name: {bank['account_name']}\n\n"
        "💳 **Option 3: Debit/Credit Card**\n"
        f"• [Open Secure Payment Portal]({invoice['card_gateway_url']})\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📌 **After Payment**:\n"
        "Submit the 12-digit Bank Reference / UTR Number:\n"
        "`/submit_utr <12_digit_utr>`\n"
        "(You can also attach a screenshot with the caption)"
    )
    return {"text": text}

async def handle_submit_utr(user_id: int, utr: str, screenshot_url: Optional[str] = None) -> Dict[str, Any]:
    if not utr:
        return {"text": "⚠️ Please provide your 12-digit UTR! Example: `/submit_utr 421098234812`"}

    try:
        record = await reconciliation_engine.process_submission(
            user_id=user_id,
            utr=utr,
            amount=199.0,
            method="UPI",
            screenshot_url=screenshot_url
        )
        return {
            "text": (
                f"✅ **UTR Received!** (`{record.utr}`)\n\n"
                "Your payment submission has been queued for bank statement reconciliation.\n"
                "Once approved by the owner, your subscription will activate and your **NextGen API Key** will be automatically sent to your DM!"
            ),
            "owner_notify": {
                "owner_id": config.bot.owner_id,
                "text": f"💰 New Payment Submission: UTR `{record.utr}` by user `{user_id}` (Amount: ₹{record.amount})",
                "reply_markup": {"inline_keyboard": inline_kb.payment_review(record.utr)}
            }
        }
    except Exception as e:
        return {"text": f"❌ Error: {str(e)}"}

