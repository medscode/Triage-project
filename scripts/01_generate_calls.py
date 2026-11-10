import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config as C

"""STEP 1: Timbre TTS -> one clean WAV per scripted call (dev + held-out). Sequential on purpose (rate limit)."""
import time
from src import gnani

for fname in ("calls.json", "heldout.json"):
    for c in json.loads((C.ROOT / "data" / fname).read_text(encoding="utf-8")):
        out = C.AUDIO_CLEAN / f"{c['id']}.wav"
        if out.exists():
            print("skip", out.name); continue
        out.write_bytes(gnani.tts(c["text"], c["voice"], c["speed"]))
        print("made", out.name); time.sleep(1)
