from dataclasses import dataclass


@dataclass(frozen=True)
class HNEntry:
    rank: int
    title: str
    points: int
    comments: int
