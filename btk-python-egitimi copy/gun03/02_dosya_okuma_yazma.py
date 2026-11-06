# -*- coding: utf-8 -*-
"""Dosya yolu ve UTF-8. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

cikti = ROOT / "outputs" / "gun03"
cikti.mkdir(parents=True, exist_ok=True)
dosya = cikti / "not.txt"
dosya.write_text("Türkçe: ölçüm, başvuru, süre\n", encoding="utf-8")
print(dosya.read_text(encoding="utf-8").strip())
print("Dosya kaydedildi:", dosya.name)
