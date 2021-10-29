from dataclasses import dataclass
@dataclass
class SpeakingData:
    txt: str
    sec: float

@dataclass
class ListeningData:
    txt: str
    is_final: bool
