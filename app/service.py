from typing import List
from .models import HNEntry
from .wordutils import count_words


def filter_long_titles_sort_by_comments(entries: List[HNEntry]) -> List[HNEntry]:
    longs = [e for e in entries if count_words(e.title) > 5]
    return sorted(longs, key=lambda e: (-e.comments, -e.points, e.rank))


def filter_short_titles_sort_by_points(entries: List[HNEntry]) -> List[HNEntry]:
    shorts = [e for e in entries if count_words(e.title) <= 5]
    return sorted(shorts, key=lambda e: (-e.points, -e.comments, e.rank))
