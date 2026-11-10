# Emergency Call Triage (synthetic pre-pilot)

## What is this, in plain words
A 112-style call-taker hears panicked, noisy, Hindi-English mixed calls. This app is a **second pair of ears**:
it turns each call's audio into text, pulls out **what happened, where, how urgent**, and shows a **ranked queue**
so the worst case is on top. A human always makes the dispatch decision.

Key demo idea: **the loudest caller is not the most urgent.** A calm man saying "my father is unconscious" outranks an
angry neighbour shouting about parking, because urgency is scored from *life-threat words*, not tone.

## How big are we building (scope)
IN SCOPE (tonight):
- 4 scripted fake calls (+2 held-out calls we never tune on), voiced by Gnani Timbre (TTS)
- noise added at 3 levels (clean / 10 dB / 0 dB) + phone-line squashing
- Gnani Prisma (STT) transcribes each version
- hand-written rules extract type, location (fictional place list), urgency score, flags
- one static dashboard: ranked queue, noise slider, accuracy chart, audio players
- a 60-second screen-recorded demo

OUT OF SCOPE: real recordings, live streaming, maps, login, database, auto-dispatch, deployment, extra languages,
any claim of real-world accuracy. This is a small honest benchmark, not a product.

## Pipeline
```
data/calls.json ──01 Timbre TTS──► audio/clean/*.wav ──02 noise+phone filter──► audio/final/<id>_<level>.wav
        ──03 Prisma STT──► results/transcripts_<model>.json ──04 rules+metrics──► results/results.json ──► web/index.html
```

## Files
| Path | What it does |
|---|---|
| `data/calls.json` | 4 call scripts + the true answer for each |
| `data/heldout.json` | 2 extra calls, written after rules are frozen; never tune on them |
| `src/config.py` | URLs, model names, noise levels, folders |
| `src/gnani.py` | the only code that talks to Gnani (TTS + STT) |
| `src/audio.py` | add noise at a given SNR, phone filter via ffmpeg |
| `src/textnorm.py` | text cleaning that keeps Devanagari intact |
| `src/lexicon.py` | keyword lists, threat weights, fictional gazetteer, urgency thresholds |
| `src/extract.py` | turns a transcript into type / location / score / flags |
| `src/metrics.py` | word error rate |
| `scripts/00_probe_api.py` … `04_extract_and_eval.py` | the pipeline steps |
| `run_all.py` | runs everything (`--oracle` = no API) |
| `web/index.html` | dashboard (reads `results/results.json`) |
| `tests/test_extract.py` | checks rules on the scripts, "loud ≠ urgent", escalation flags |
| `docs/API_FACTS.md` | verified vs unverified API facts + rules for AI agents |

## Run it
```bash
pip install -r requirements.txt          # also needs ffmpeg installed
cp .env.example .env                     # paste GNANI_API_KEY
pytest -q                                # offline, should pass
python run_all.py --oracle               # offline: dashboard works, numbers are NOT real accuracy
python -m http.server 8000               # open http://localhost:8000/web/index.html

python scripts/00_probe_api.py           # FIRST real step: confirms key, TTS, STT, shows real response keys
python run_all.py                        # real run: TTS -> noise -> STT -> rules -> results
python scripts/03_transcribe.py v3.0 && python scripts/04_extract_and_eval.py v3.0   # compare Prisma v3.0
```

## Likely first problems (and where to fix)
1. STT writes place names in a different spelling → add variants in `src/lexicon.py`.
2. TTS Hinglish sounds odd → try `TTS_LANGUAGE=hi-en` in `.env` and regenerate (delete `audio/`).
3. Rules miss a word → add it, then re-run `04`. Don't touch `heldout.json` text to make it pass.

## Known weakness already found (use it in the red-team slide)
Held-out call `h1_fall` says breathing is *fine* ("सांस चल रही है"), but the keyword rule still adds breathing points, so it scores
critical instead of high (over-triage). Over-triage is the safe direction, but it is a real failure: keyword rules ignore negation.
Do NOT edit the rules just to fix this one held-out call; show it as a limitation, or write 2 fresh held-out calls first.

## Honest framing for judges
"Synthetic pre-pilot benchmark on 4 + 2 scripted calls. Rules are hand-written. Low confidence or missing location
escalates to a human." Cite any 112 statistic as *reported*, with its source and year, never as one national number.
