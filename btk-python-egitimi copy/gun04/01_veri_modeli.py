# -*- coding: utf-8 -*-
"""Veri modeli ve benzersiz kimlik. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

# Bir satır = bir başvuru; birim_kodu başka tablodaki birime bağlanır.
kimlikler = [kayit["basvuru_no"] for kayit in kayitlar]
if len(kimlikler) != len(set(kimlikler)):
    raise ValueError("Tekrarlayan başvuru kimliği var")
print("Benzersiz kimlik:", len(set(kimlikler)))
# Birleştirmede birimler tablosunda birim kodu da benzersiz olmalı.
