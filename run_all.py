"""Run the whole pipeline: python run_all.py [--oracle]   (--oracle = skip all API calls)"""
import subprocess, sys
py = sys.executable
steps = [["scripts/04_extract_and_eval.py", "--oracle"]] if "--oracle" in sys.argv else [
    ["scripts/01_generate_calls.py"], ["scripts/02_degrade_audio.py"],
    ["scripts/03_transcribe.py"], ["scripts/04_extract_and_eval.py"]]
for s in steps:
    print("==>", *s); subprocess.run([py, *s], check=True)
print("Done. Now: python -m http.server 8000  and open http://localhost:8000/web/index.html")
