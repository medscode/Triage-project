import sys
import json
import shutil
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import config as C
from src import gnani

print("=" * 60)
print("00_PROBE_API: Gnani Timbre TTS & Prisma STT Verification")
print("=" * 60)

# 1. Verify API Key
if not C.API_KEY:
    print("\n[ERROR] GNANI_API_KEY is missing!")
    print("Please create a .env file from .env.example:")
    print("  cp .env.example .env")
    print("And paste your GNANI_API_KEY inside .env.\n")
    sys.exit(1)

masked_key = C.API_KEY[:4] + "..." + C.API_KEY[-4:] if len(C.API_KEY) > 8 else "***"
print(f"[OK] GNANI_API_KEY detected: {masked_key}")

# 2. Check Audio Processing Tools
has_ffmpeg = bool(shutil.which("ffmpeg"))
print(f"[*] Audio backend - ffmpeg: {'FOUND' if has_ffmpeg else 'NOT FOUND (using scipy fallback)'}")

# 3. Test Timbre TTS
test_phrase = "नमस्ते, यह आपातकालीन 112 सेवा का एक टेस्ट है।"
print(f"\n[*] Sending TTS probe request (voice='Nalini', text='{test_phrase}')...")
try:
    wav_bytes = gnani.tts(test_phrase, voice="Nalini", speed=1.0)
    probe_path = C.AUDIO_CLEAN / "probe.wav"
    probe_path.write_bytes(wav_bytes)
    print(f"[OK] Timbre TTS succeeded: received {len(wav_bytes)} bytes -> saved to {probe_path.relative_to(ROOT)}")
except Exception as e:
    print(f"[FAIL] Timbre TTS error: {e}")
    sys.exit(1)

# 4. Test Prisma STT
print(f"\n[*] Sending STT probe request (model='{C.STT_MODEL}', lang='{C.STT_LANGUAGE}')...")
try:
    text, raw_json = gnani.stt(probe_path, model=C.STT_MODEL, language_code=C.STT_LANGUAGE)
    print(f"[OK] Prisma STT succeeded!")
    print(f"[*] Extracted transcript: \"{text}\"")
    print(f"\n[*] Exact STT response JSON keys: {list(raw_json.keys())}")
    print("\n[*] Full raw STT JSON response:")
    print(json.dumps(raw_json, ensure_ascii=False, indent=2))
except Exception as e:
    print(f"[FAIL] Prisma STT error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("PROBE PASSED: Both Timbre TTS and Prisma STT are fully operational!")
print("=" * 60)
