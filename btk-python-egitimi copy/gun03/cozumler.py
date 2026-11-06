# -*- coding: utf-8 -*-
"""Temel ve ek alıştırmanın bağımsız örnek çözümü."""
# Değişken adları, koşullar ve dosya yollarını örneklerle karşılaştırın.
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))
acik = [k for k in kayitlar if k["durum"] == "Acik"]
print("Açık:", len(acik))
cikti = ROOT / "outputs" / "gun03"
cikti.mkdir(parents=True, exist_ok=True)
with (cikti / "acik.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=kayitlar[0].keys())
    w.writeheader()
    w.writerows(acik)
