# -*- coding: utf-8 -*-
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

# DictReader alanları metin verir; hesaplamadan önce int'e dönüştür.
toplam = 0
for kayit in kayitlar:
    toplam += int(kayit["islem_suresi"])
print("Kayıt:", len(kayitlar))
print("Süre toplamı:", toplam)
