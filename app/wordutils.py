def normalize_token(token: str) -> str:
    # We quit simbols, we let only letters (accents includes)
    return "".join(ch for ch in token if ch.isalpha())


def count_words(title: str) -> int:
    tokens = title.split()
    normalized = [normalize_token(t) for t in tokens]
    return sum(1 for t in normalized if t)
