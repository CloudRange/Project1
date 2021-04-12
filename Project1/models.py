from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Artist:
    id: str
    name: str
    genres: List[str]

@dataclass
class AudioFeatures:
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
    id: str
        
@dataclass
class Track:
    id: str
    name: str
    artists: List[Artist]
    audio_features: AudioFeatures