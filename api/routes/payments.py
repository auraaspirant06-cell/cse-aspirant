"""
CSE Aspirant - Payment Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from api.schemas import PaymentSubmitRequest, BaseResponse
from api.auth import verify_api_key
from database.models import ApiKeyRecord
from core.config import config
from payments.gateway import payment_gateway
from payments.reconciliation import reconciliation_engine

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])

@router.get("/invoice/{user_id}", response_model=BaseResponse)
async def get_invoice(
    user_id: int,
    plan: str = Query("PREMIUM", pattern="^(PREMIUM|PRO)$"),
    amount: float = Query(199.0, gt=0, le=1_000_000),
):
    inv = payment_gateway.generate_payment_invoice(user_id, plan, amount)
    return BaseResponse(data=inv)

@router.post("/submit", response_model=BaseResponse)
async def submit_utr(req: PaymentSubmitRequest, auth: ApiKeyRecord = Depends(verify_api_key)):
    is_admin = auth.user_id == config.bot.owner_id or auth.user_id in config.bot.sudo_users
    if req.user_id != auth.user_id and not is_admin:
        raise HTTPException(status_code=403, detail="API keys may submit payments only for their owner.")
    record = await reconciliation_engine.process_submission(
        user_id=req.user_id,
        utr=req.utr,
        amount=req.amount,
        method=req.method,
        screenshot_url=req.screenshot_url
    )
    return BaseResponse(
        message="UTR submitted successfully. Pending owner bank statement reconciliation.",
        data={"utr": record.utr, "status": record.status}
    )

