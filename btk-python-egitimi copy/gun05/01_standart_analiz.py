# -*- coding: utf-8 -*-
"""Standart kütüphane ile analiz. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

from statistics import mean, median
# Tamamlanma süresi yalnızca kapanmış başvurularda ölçülür.
sureler = [int(k["islem_suresi"]) for k in kayitlar if k["durum"] == "Kapali"]
print("Kapalı kayıt:", len(sureler))
print(f"Ortalama: {mean(sureler):.2f}")
print(f"Medyan: {median(sureler):.2f}")
print("Aralık:", min(sureler), max(sureler))
