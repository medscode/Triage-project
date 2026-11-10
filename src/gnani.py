"""Thin wrappers over the two Gnani REST endpoints. Nothing here is invented: see docs/API_FACTS.md."""
import time
import requests
from . import config as C


def _headers():
    if not C.API_KEY:
        raise SystemExit("GNANI_API_KEY missing. Copy .env.example to .env and paste your key.")
    return {"X-API-Key-ID": C.API_KEY}


def _post(**kw):
    # Docs: accounts may be limited to 1 active request at a time -> 429 RATE_LIMITED. So: sequential + retry.
    for attempt in range(5):
        r = requests.post(timeout=90, **kw)
        if r.status_code == 429:
            time.sleep(2 * (attempt + 1))
            continue
        return r
    return r


def tts(text, voice, speed=1.0, language=None):
    body = {
        "text": text, "voice": voice, "model": C.TTS_MODEL,
        "language": language or C.TTS_LANGUAGE, "speed": speed,  # speed range 0.85-1.15 (VERIFIED)
        "audio_config": {"sample_rate": C.SAMPLE_RATE, "num_channels": 1, "sample_width": 2,
                         "encoding": "linear_pcm", "container": "wav"},
    }
    r = _post(url=C.TTS_URL, headers={**_headers(), "Content-Type": "application/json"}, json=body)
    if r.status_code != 200:
        raise RuntimeError(f"TTS failed {r.status_code}: {r.text[:300]}")
    return r.content


def stt(path, model=None, language_code="hi-IN"):
    """Returns (text, raw_json). model: 'v2.5' (default) or 'v3.0' (uses indic-auto)."""
    model = model or C.STT_MODEL
    data = {"language_code": language_code}
    if model == "v3.0":
        data = {"language_code": "indic-auto", "model": "prisma-v3.0"}  # VERIFIED: indic-auto only on v3.0
    with open(path, "rb") as f:
        r = _post(url=C.STT_URL, headers=_headers(), files={"audio_file": (path.name, f, "audio/wav")}, data=data)
    if r.status_code != 200:
        raise RuntimeError(f"STT failed {r.status_code}: {r.text[:300]}")
    raw = r.json()
    # UNVERIFIED which key holds the text (SDK uses "transcript"; some docs show "text"). Handle both, keep raw.
    text = raw.get("transcript") or raw.get("text") or ""
    return text, raw
