"""
CSE Aspirant - API Request and Response Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Operation completed successfully."
    data: Optional[Dict[str, Any]] = None

class ApiKeyCreateRequest(BaseModel):
    user_id: int
    tier: str = Field(default="FREE", description="FREE, PREMIUM, or PRO")

class ApiKeyRevokeRequest(BaseModel):
    key: str

class MusicPlayRequest(BaseModel):
    chat_id: int
    query_or_url: str
    requester_id: int
    requester_name: str = "API User"

class PaymentSubmitRequest(BaseModel):
    user_id: int
    utr: str
    amount: float
    method: str = "UPI"
    screenshot_url: Optional[str] = None

class AIQueryRequest(BaseModel):
    prompt: str
    mode: str = "general"  # general, math, code, summarize

