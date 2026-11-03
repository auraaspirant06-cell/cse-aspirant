"""
CSE Aspirant - Global Exception & Error Handlers
"""
import traceback
from typing import Dict, Any
from core.logger import logger
from error_handling.exceptions import CSEAspirantException

def format_error_response(error: Exception) -> Dict[str, Any]:
    if isinstance(error, CSEAspirantException):
        return {
            "success": False,
            "error_code": error.code,
            "message": error.message
        }
    return {
        "success": False,
        "error_code": "UNHANDLED_EXCEPTION",
        "message": "An unexpected error occurred. Please try again later."
    }

async def handle_bot_error(chat_id: int, error: Exception, send_message_fn):
    logger.error(f"Bot execution error in chat {chat_id}: {error}\n{traceback.format_exc()}")
    user_msg = "⚠️ An error occurred while executing your request."
    if isinstance(error, CSEAspirantException):
        user_msg = f"⚠️ {error.message}"
    try:
        await send_message_fn(chat_id, user_msg)
    except Exception as send_err:
        logger.error(f"Failed to deliver error message to chat {chat_id}: {send_err}")
