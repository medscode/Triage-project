# API facts (read this before touching src/gnani.py)

Source: docs.gnani.ai, checked 2026-11-10. If a thing is not on this page, DO NOT invent it — run
`python scripts/00_probe_api.py` and read the real response, or ask the human.

## TTS (Timbre) — VERIFIED
- `POST https://api.vachana.ai/api/v1/tts/inference`, header `X-API-Key-ID`, JSON body, response = raw audio bytes.
- Body: `text`, `voice`, `model` (`timbre-v2.5` | `timbre-v3.0`), `language` (`auto`, `hi-IN`, `en-IN`, `hi-en` Hinglish …),
  `speed` (0.85–1.15), `audio_config` {`sample_rate`, `num_channels`, `sample_width`, `encoding`, `container`}.
- Voices are per model. Documented v2.5 examples: Nalini (Hindi), Deepak (Hindi), Kaveri (English), Poorvi (Hinglish).
- Numbers/IDs should be written as spoken words in the text (docs: "Input Formatting Guide").
- Errors: flat `{"success":false,"message":...}`; auth/rate errors `{"detail":{"error_code":...}}`; 429 = only 1 active request.
- NOT supported/documented for REST: SSML. We use `speed` for panic vs calm instead.

## STT (Prisma) — VERIFIED
- `POST https://api.vachana.ai/stt/v3`, multipart: `audio_file`, `language_code` (e.g. `hi-IN`), optional `model=prisma-v3.0`.
- `language_code=indic-auto` works ONLY with `prisma-v3.0`. Default (no model) = Prisma v2.5.
- Clip limit 60 s (ideal ≤ 30 s). Formats: WAV, MP3, OGG, FLAC, AAC, M4A.

## UNVERIFIED (handle defensively)
- Which JSON key holds the text: the official SDK reads `result["transcript"]`; code accepts `transcript` or `text` and stores the raw JSON.
- Whether Hinglish in Devanagari + embedded Latin words (our scripts) is spoken well by `language=auto`: listen to the audio; try `hi-en` via `TTS_LANGUAGE`.
- How Prisma renders English words / our fictional place names (Devanagari vs Latin) → fix by adding variants to `src/lexicon.py` GAZETTEER.

## Project rules for any AI agent working here
1. Synthetic calls only. Never add real emergency recordings or real people's data.
2. Urgency comes from life-threat content, never from tone, volume or exclamation marks.
3. Unsure or location missing → flag and escalate to a human; never drop a call. A human always dispatches.
4. Never tune rules on `data/heldout.json`. Report its score as-is.
5. No new features beyond README "IN SCOPE". No database, auth, maps, live streaming.
6. Label every demo "SYNTHETIC CALLS". Call numbers a "synthetic pre-pilot benchmark".
7. Don't invent API fields, voice names or statistics. Cite or leave out.
