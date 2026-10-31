# -*- coding: utf-8 -*-
"""Gruplama ve CSV raporu. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

from collections import Counter
sayilar = Counter(k["birim_kodu"] for k in kayitlar)
cikti = ROOT / "outputs" / "gun05"
cikti.mkdir(parents=True, exist_ok=True)
with (cikti / "birim_ozeti.csv").open("w", encoding="utf-8-sig", newline="") as dosya:
    yazici = csv.writer(dosya)
    yazici.writerow(["birim", "adet"])
    yazici.writerows(sorted(sayilar.items()))
print("Rapor toplamı:", sum(sayilar.values()))
print("CSV ayıracı virgüldür; Excel'de Veri > Metin/CSV yoluyla açılabilir.")
