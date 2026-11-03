"""
CSE Aspirant - Payment Endpoints
"""
from fastapi import APIRouter, HTTPException
from api.schemas import PaymentSubmitRequest, BaseResponse
from payments.gateway import payment_gateway
from payments.reconciliation import reconciliation_engine

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])

@router.get("/invoice/{user_id}", response_model=BaseResponse)
async def get_invoice(user_id: int, plan: str = "PREMIUM", amount: float = 199.0):
    inv = payment_gateway.generate_payment_invoice(user_id, plan, amount)
    return BaseResponse(data=inv)

@router.post("/submit", response_model=BaseResponse)
async def submit_utr(req: PaymentSubmitRequest):
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

