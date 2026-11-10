import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config as C

"""STEP 2: for each call make 3 versions: clean / snr10 / snr0 (white noise), all squashed to phone quality."""
from src import audio

for wav in sorted(C.AUDIO_CLEAN.glob("*.wav")):
    if wav.stem == "probe":
        continue
    x, rate = audio.read_wav(wav)
    for level, snr in C.SNR_DB.items():
        tmp = C.AUDIO_FINAL / f"_tmp_{wav.stem}.wav"
        audio.write_wav(tmp, x if snr is None else audio.add_noise(x, snr, seed=7), rate)
        audio.phone_filter(tmp, C.AUDIO_FINAL / f"{wav.stem}_{level}.wav")
        tmp.unlink()
    print("degraded", wav.stem)
