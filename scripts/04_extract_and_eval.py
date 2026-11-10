import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config as C

"""STEP 4: rules + metrics -> results/results.json (what the dashboard reads).
Usage: python scripts/04_extract_and_eval.py [v2.5|v3.0]     (uses real Prisma transcripts)
       python scripts/04_extract_and_eval.py --oracle        (no API: runs rules on the script text itself;
                                                              proves the rules + dashboard work, NOT an accuracy claim)"""
from src.extract import extract
from src.metrics import wer

oracle = "--oracle" in sys.argv
model = next((a for a in sys.argv[1:] if not a.startswith("--")), C.STT_MODEL)
tr = {} if oracle else json.loads((C.RESULTS / f"transcripts_{model}.json").read_text(encoding="utf-8"))
calls = []
for setname, fname in (("dev", "calls.json"), ("heldout", "heldout.json")):
    for c in json.loads((C.ROOT / "data" / fname).read_text(encoding="utf-8")):
        by = {}
        for level in C.LEVELS:
            text = c["text"] if oracle else tr[c["id"]][level]["transcript"]
            e = extract(text)
            e["transcript"] = text
            e["wer"] = None if oracle else wer(c["text"], text)
            e["audio"] = f"audio/final/{c['id']}_{level}.wav"
            by[level] = e
        calls.append({"id": c["id"], "set": setname, "label": c["label"], "tone": c["tone"], "script": c["text"],
                      "true": {"type": c["true_type"], "urgency": c["true_urgency"], "location": c["true_location"]},
                      "by_level": by})

def metrics(setname):
    out = {}
    for level in C.LEVELS:
        rows = [(c["true"], c["by_level"][level]) for c in calls if c["set"] == setname]
        n = len(rows)
        if not n: continue
        wers = [r["wer"] for _, r in rows if r["wer"] is not None]
        out[level] = {"n": n,
                      "type_acc": sum(t["type"] == r["type"] for t, r in rows) / n,
                      "urgency_acc": sum(t["urgency"] == r["urgency"] for t, r in rows) / n,
                      "location_acc": sum(t["location"] in r["locations"] for t, r in rows) / n,
                      "mean_wer": sum(wers) / len(wers) if wers else None}
    return out

res = {"mode": "oracle_script_text" if oracle else f"prisma_{model}", "levels": C.LEVELS, "calls": calls,
       "metrics": {"dev": metrics("dev"), "heldout": metrics("heldout")}}
(C.RESULTS / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote results/results.json | mode:", res["mode"])
print(json.dumps(res["metrics"], indent=1))
