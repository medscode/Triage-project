import unicodedata


def norm(t: str) -> str:
    """Lowercase, NFC, drop punctuation/symbols but KEEP Devanagari vowel signs (a plain \\w regex would delete them)."""
    t = unicodedata.normalize("NFC", t or "").lower()
    t = "".join(" " if unicodedata.category(c)[0] in "PS" else c for c in t)
    return " ".join(t.split())
