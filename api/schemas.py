"""
CSE Aspirant - API Request and Response Schemas
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional

class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Operation completed successfully."
    data: Optional[Dict[str, Any]] = None

class ApiKeyCreateRequest(BaseModel):
    user_id: int = Field(gt=0)
    tier: Literal["FREE", "PREMIUM", "PRO"] = "FREE"

class ApiKeyRevokeRequest(BaseModel):
    key: str

class MusicPlayRequest(BaseModel):
    chat_id: int
    query_or_url: str
    requester_id: int
    requester_name: str = "API User"

class PaymentSubmitRequest(BaseModel):
    user_id: int = Field(gt=0)
    utr: str = Field(min_length=10, max_length=22, pattern=r"^[A-Za-z0-9]+$")
    amount: float = Field(gt=0, le=1_000_000)
    method: Literal["UPI", "NEFT", "CARD"] = "UPI"
    screenshot_url: Optional[str] = None

class AIQueryRequest(BaseModel):
    prompt: str
    mode: str = "general"  # general, math, code, summarize

