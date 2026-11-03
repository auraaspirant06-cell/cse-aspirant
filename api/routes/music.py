"""
CSE Aspirant - NextGen Music API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from api.schemas import MusicPlayRequest, BaseResponse
from api.auth import verify_api_key
from database.models import ApiKeyRecord
from music.multi_group import multi_player_manager
from music.search import search_engine

router = APIRouter(prefix="/api/v1/music", tags=["Music Engine"])

@router.post("/play", response_model=BaseResponse)
async def play_audio(req: MusicPlayRequest, auth: ApiKeyRecord = Depends(verify_api_key)):
    tracks = await search_engine.search(req.query_or_url, req.requester_id, req.requester_name)
    if not tracks:
        raise HTTPException(status_code=404, detail="No matching audio tracks found.")
    
    player = multi_player_manager.get_player(req.chat_id)
    played_track = await player.play(tracks[0])
    return BaseResponse(
        message=f"Queued track '{played_track.title}'",
        data={"track": played_track.to_dict(), "player_status": player.get_status()}
    )

@router.post("/pause/{chat_id}", response_model=BaseResponse)
async def pause_audio(chat_id: int, auth: ApiKeyRecord = Depends(verify_api_key)):
    player = multi_player_manager.get_player(chat_id)
    paused = await player.pause()
    return BaseResponse(message="Playback paused." if paused else "Player not playing.")

@router.post("/resume/{chat_id}", response_model=BaseResponse)
async def resume_audio(chat_id: int, auth: ApiKeyRecord = Depends(verify_api_key)):
    player = multi_player_manager.get_player(chat_id)
    resumed = await player.resume()
    return BaseResponse(message="Playback resumed." if resumed else "Player not paused.")

@router.post("/skip/{chat_id}", response_model=BaseResponse)
async def skip_audio(chat_id: int, auth: ApiKeyRecord = Depends(verify_api_key)):
    player = multi_player_manager.get_player(chat_id)
    next_track = await player.skip()
    return BaseResponse(
        message="Skipped to next track." if next_track else "Queue completed.",
        data={"current": next_track.to_dict() if next_track else None}
    )

@router.get("/status/{chat_id}", response_model=BaseResponse)
async def get_player_status(chat_id: int):
    player = multi_player_manager.get_player(chat_id)
    return BaseResponse(data=player.get_status())

