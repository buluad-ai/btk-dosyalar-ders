# -*- coding: utf-8 -*-
"""Temel ve ek alıştırmanın bağımsız örnek çözümü."""
# Değişken adları, koşullar ve dosya yollarını örneklerle karşılaştırın.
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))
def birim_filtrele(veri, kod):
    return [k for k in veri if k["birim_kodu"] == kod]

for kod in ["A", "B", "X"]:
    sonuc = birim_filtrele(kayitlar, kod)
    if sonuc:
        print(kod, len(sonuc), "kayıt")
    else:
        print(kod, "için kayıt bulunamadı")
