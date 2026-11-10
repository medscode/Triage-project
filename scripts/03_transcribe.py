import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config as C

"""STEP 3: Prisma STT on every degraded file. Usage: python scripts/03_transcribe.py [v2.5|v3.0]
Saves results/transcripts_<model>.json (text + raw API JSON)."""
import time
from src import gnani

model = sys.argv[1] if len(sys.argv) > 1 else C.STT_MODEL
ids = [c["id"] for f in ("calls.json", "heldout.json") for c in json.loads((C.ROOT / "data" / f).read_text(encoding="utf-8"))]
out = {}
for cid in ids:
    out[cid] = {}
    for level in C.LEVELS:
        text, raw = gnani.stt(C.AUDIO_FINAL / f"{cid}_{level}.wav", model=model)
        out[cid][level] = {"transcript": text, "raw": raw}
        print(cid, level, "->", text[:60]); time.sleep(1)
(C.RESULTS / f"transcripts_{model}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
