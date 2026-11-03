"""
CSE Aspirant - Unified Music Search Engine
"""
import asyncio
from typing import List
import urllib.parse
from music.track import Track
from core.logger import logger

class MusicSearchEngine:
    async def search(self, query: str, requester_id: int, requester_name: str, limit: int = 5) -> List[Track]:
        query = query.strip()
        logger.info(f"Music search query: '{query}' by {requester_name}")
        
        # If query is direct audio/stream URL
        if query.startswith("http://") or query.startswith("https://"):
            return [
                Track(
                    title=f"Web Stream: {urllib.parse.urlparse(query).path.split('/')[-1] or 'Live Stream'}",
                    uri=query,
                    duration=0,
                    requester_id=requester_id,
                    requester_name=requester_name,
                    is_live=True,
                    source="Direct Stream"
                )
            ]

        try:
            import yt_dlp
        except ImportError:
            logger.error("yt-dlp is required for song-name searches")
            return []

        target = query if query.startswith(("http://", "https://")) else f"ytsearch{limit}:{query}"
        options = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "format": "bestaudio/best",
            "skip_download": True,
        }

        def resolve():
            with yt_dlp.YoutubeDL(options) as downloader:
                return downloader.extract_info(target, download=False)

        try:
            info = await asyncio.to_thread(resolve)
        except Exception as exc:
            logger.warning(f"Unable to resolve audio query: {exc}")
            return []

        entries = info.get("entries") or [info]
        results: List[Track] = []
        for entry in entries[:limit]:
            if not entry or not entry.get("url"):
                continue
            results.append(
                Track(
                    title=entry.get("title") or query,
                    uri=entry["url"],
                    duration=int(entry.get("duration") or 0),
                    requester_id=requester_id,
                    requester_name=requester_name,
                    is_live=bool(entry.get("is_live")),
                    source="YouTube" if "youtube" in (entry.get("webpage_url") or "") else "Direct Stream",
                )
            )
        return results

search_engine = MusicSearchEngine()
