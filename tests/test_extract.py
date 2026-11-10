import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.extract import extract

ROOT = Path(__file__).resolve().parent.parent
CALLS = json.loads((ROOT / "data" / "calls.json").read_text(encoding="utf-8"))  # dev set only; held-out is REPORTED, never asserted/tuned


def test_rules_on_scripts():
    for c in CALLS:
        e = extract(c["text"])
        assert e["type"] == c["true_type"], c["id"]
        assert e["urgency"] == c["true_urgency"], c["id"]
        assert c["true_location"] in e["locations"], c["id"]


def test_loud_is_not_urgent():
    by = {c["id"]: extract(c["text"]) for c in CALLS}
    assert by["c4_parking"]["urgency_score"] < by["c2_chest"]["urgency_score"]


def test_missing_location_and_low_confidence_flags():
    e = extract("हेलो मदद")
    assert any("ask caller" in f for f in e["flags"]) and e["low_confidence"]
