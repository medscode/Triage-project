"""Add white noise at a target SNR, then squash to phone quality (8 kHz mono, 300-3400 Hz) with ffmpeg or scipy."""
import shutil
import subprocess
import wave
import numpy as np

try:
    import scipy.signal as signal
except ImportError:
    signal = None


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        assert w.getsampwidth() == 2 and w.getnchannels() == 1, "expected 16-bit mono WAV"
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64), w.getframerate()


def write_wav(path, x, rate):
    x = np.clip(x, -32768, 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(x.tobytes())


def add_noise(x, snr_db, seed=0):
    rng = np.random.default_rng(seed)
    p_sig = np.mean(x ** 2) + 1e-9
    p_noise = p_sig / (10 ** (snr_db / 10))
    return x + rng.normal(0, np.sqrt(p_noise), size=x.shape)


def phone_filter(src, dst):
    if shutil.which("ffmpeg"):
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ar", "8000", "-ac", "1",
             "-af", "highpass=f=300,lowpass=f=3400", str(dst)],
            check=True
        )
        return
    if signal is not None:
        x, rate = read_wav(src)
        target_rate = 8000
        if rate != target_rate:
            gcd = int(np.gcd(rate, target_rate))
            up = target_rate // gcd
            down = rate // gcd
            x = signal.resample_poly(x, up, down)
            rate = target_rate
        # Bandpass filter 300-3400 Hz at 8000 Hz
        sos = signal.butter(4, [300, 3400], btype="bandpass", fs=rate, output="sos")
        x_filtered = signal.sosfilt(sos, x)
        write_wav(dst, x_filtered, rate)
        return
    raise SystemExit("Neither ffmpeg nor scipy is available to filter audio.")
