"""Thin wrappers over the Gnani REST endpoints. All network calls are restricted to this module."""
import time
import requests
from . import config as C


def _headers():
    if not C.API_KEY:
        raise RuntimeError("GNANI_API_KEY missing. Copy .env.example to .env and paste your key.")
    return {"X-API-Key-ID": C.API_KEY}


def _post(**kw):
    """Sequential POST with automatic retry on 429 (rate limit)."""
    for attempt in range(5):
        r = requests.post(timeout=90, **kw)
        if r.status_code == 429:
            time.sleep(2 * (attempt + 1))
            continue
        return r
    return r


def tts(text: str, voice: str, speed: float = 1.0, language: str = None) -> bytes:
    """Timbre TTS: Synthesize speech from text. Returns raw WAV bytes."""
    body = {
        "text": text,
        "voice": voice,
        "model": C.TTS_MODEL,
        "language": language or C.TTS_LANGUAGE,
        "speed": float(speed),  # Valid range: 0.85 - 1.15
        "audio_config": {
            "sample_rate": C.SAMPLE_RATE,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav",
        },
    }
    r = _post(url=C.TTS_URL, headers={**_headers(), "Content-Type": "application/json"}, json=body)
    if r.status_code != 200:
        raise RuntimeError(f"TTS request failed ({r.status_code}): {r.text[:300]}")
    return r.content


def stt(path, model: str = None, language_code: str = None) -> tuple[str, dict]:
    """Prisma STT: Transcribe audio file. Returns (transcript_text, raw_json)."""
    model = model or C.STT_MODEL
    lang = language_code or C.STT_LANGUAGE

    data = {"language_code": lang}
    if model in ("v3.0", "prisma-v3.0"):
        data["model"] = "prisma-v3.0"

    with open(path, "rb") as f:
        r = _post(
            url=C.STT_URL,
            headers=_headers(),
            files={"audio_file": (path.name, f, "audio/wav")},
            data=data,
        )

    if r.status_code != 200:
        raise RuntimeError(f"STT request failed ({r.status_code}): {r.text[:300]}")

    raw = r.json()

    # Robust fallback parsing across API variants
    text = raw.get("transcript") or raw.get("text")
    if not text and isinstance(raw.get("data"), dict):
        text = raw["data"].get("transcript") or raw["data"].get("text")
    if not text and isinstance(raw.get("result"), dict):
        text = raw["result"].get("transcript") or raw["result"].get("text")

    return str(text or "").strip(), raw
