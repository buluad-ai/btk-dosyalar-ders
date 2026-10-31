"""Ders dosyalarını ortak bir komutla çalıştırır; paket kurmaz.

python run_lesson.py --list
python run_lesson.py gun01/01_merhaba.py
python run_lesson.py --framework

Windows'ta 'python' yerine 'py' kullanılabilir. VS Code Run Python File da uygundur.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def interpreter(folder: str) -> Path:
    relative = "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
    candidate = ROOT / folder / relative
    return candidate if candidate.exists() else Path(sys.executable)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", nargs="?")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--framework", action="store_true", help="İsteğe bağlı yerel Streamlit paneli")
    args, extra = parser.parse_known_args()
    if args.list or (not args.script and not args.framework):
        manifest = json.loads((ROOT / "data/lesson_manifest.json").read_text(encoding="utf-8"))
        for entry in manifest:
            print(f"{entry['file']:<43} {entry['title']}" + (" [optional]" if entry['optional'] else ""))
        return 0
    if args.framework:
        python = interpreter(".venv-analytics")
        command = [str(python), "-m", "streamlit", "run",
                   str(ROOT / "gun07/04_streamlit_opsiyonel.py"),
                   "--server.address", "127.0.0.1", "--server.port", "8501",
                   "--browser.gatherUsageStats", "false"]
        print("Yerel panel: http://127.0.0.1:8501 — Durdurmak için Ctrl+C", flush=True)
    else:
        script = (ROOT / args.script).resolve()
        if not script.is_relative_to(ROOT) or not script.is_file() or script.suffix != ".py":
            parser.error("Eğitim klasöründeki geçerli bir .py dosyasını seçin.")
        command = [str(interpreter(".venv")), str(script), *extra]
    try:
        return subprocess.call(command, cwd=ROOT)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
