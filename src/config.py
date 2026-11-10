"""All settings in one place. Values marked VERIFIED come from docs.gnani.ai (checked 2026-11-10)."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GNANI_API_KEY", "")
BASE = "https://api.vachana.ai"
TTS_URL = BASE + "/api/v1/tts/inference"   # VERIFIED: POST, JSON body, returns raw audio bytes
STT_URL = BASE + "/stt/v3"                 # VERIFIED: POST, multipart (audio_file, language_code, optional model)
TTS_MODEL = "timbre-v2.5"                  # VERIFIED: also valid: timbre-v3.0
TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "auto")  # VERIFIED values: auto, hi-IN, en-IN, hi-en, ...
SAMPLE_RATE = 16000                        # VERIFIED allowed: 8000,16000,22050,24000,44100,48000
STT_MODEL = os.getenv("STT_MODEL", "v2.5") # "v2.5" = default (omit model field); "v3.0" = prisma-v3.0

LEVELS = ["clean", "snr10", "snr0"]        # clean = phone-quality only; snr10 / snr0 = + noise at that SNR in dB
SNR_DB = {"clean": None, "snr10": 10, "snr0": 0}

AUDIO_CLEAN = ROOT / "audio" / "clean"
AUDIO_FINAL = ROOT / "audio" / "final"
RESULTS = ROOT / "results"
for d in (AUDIO_CLEAN, AUDIO_FINAL, RESULTS):
    d.mkdir(parents=True, exist_ok=True)
