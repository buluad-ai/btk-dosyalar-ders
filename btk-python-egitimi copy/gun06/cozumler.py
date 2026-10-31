# -*- coding: utf-8 -*-
"""Temel ve ek alıştırmanın bağımsız örnek çözümü."""
# Değişken adları, koşullar ve dosya yollarını örneklerle karşılaştırın.
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))
from collections import Counter
sayilar = Counter(k["durum"] for k in kayitlar)
for durum, adet in sorted(sayilar.items()):
    print(f"{durum}: {'#' * adet} {adet} ({adet / len(kayitlar):.0%})")
