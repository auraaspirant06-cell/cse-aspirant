"""
CSE Aspirant - Music Track Data Structure
"""
from dataclasses import dataclass, field
import uuid

@dataclass
class Track:
    title: str
    uri: str
    duration: int  # in seconds
    requester_id: int
    requester_name: str
    track_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    thumbnail: str = "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400"
    is_live: bool = False
    source: str = "YouTube"

    def to_dict(self):
        return {
            "track_id": self.track_id,
            "title": self.title,
            "uri": self.uri,
            "duration": self.duration,
            "requester_name": self.requester_name,
            "thumbnail": self.thumbnail,
            "is_live": self.is_live,
            "source": self.source
        }
