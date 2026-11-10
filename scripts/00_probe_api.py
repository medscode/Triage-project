import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config as C

"""STEP 0: check key, ffmpeg, one TTS call, one STT call. Prints raw STT JSON so you can see the real response keys."""
import shutil
from src import gnani

print("ffmpeg:", "found" if shutil.which("ffmpeg") else "MISSING")
print("api key set:", bool(C.API_KEY))
wav = gnani.tts("नमस्ते, यह एक टेस्ट है।", voice="Nalini")
p = C.AUDIO_CLEAN / "probe.wav"
p.write_bytes(wav)
print("TTS ok:", len(wav), "bytes ->", p)
text, raw = gnani.stt(p)
print("STT text:", text)
print("STT raw JSON:", json.dumps(raw, ensure_ascii=False, indent=2))
