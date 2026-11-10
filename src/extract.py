from .textnorm import norm
from . import lexicon as L


def _has(padded, term):
    return f" {norm(term)} " in padded


def _sum(padded, table):
    return sum(w for t, w in table.items() if _has(padded, t))


def extract(text: str) -> dict:
    padded = f" {norm(text)} "
    scores = {k: sum(_has(padded, t) for t in v) for k, v in L.TYPES.items()}
    best = max(scores.values())
    winners = [k for k, v in scores.items() if v == best]
    etype = winners[0] if best > 0 and len(winners) == 1 else "unknown"

    places = [name for name, variants in L.GAZETTEER.items() if any(_has(padded, v) for v in variants)]
    score = _sum(padded, L.THREAT) + _sum(padded, L.VULNERABLE) + _sum(padded, L.COUNTS)
    urgency = "critical" if score >= L.CRITICAL_AT else "high" if score >= L.HIGH_AT else "low"

    flags = []
    if not places:
        flags.append("location missing -> ask caller")
    low_conf = etype == "unknown" or len(padded.split()) < 5
    if low_conf:
        flags.append("low confidence -> escalate to human")
    return {"type": etype, "type_scores": scores, "locations": places, "urgency_score": score,
            "urgency": urgency, "flags": flags, "low_confidence": low_conf}
