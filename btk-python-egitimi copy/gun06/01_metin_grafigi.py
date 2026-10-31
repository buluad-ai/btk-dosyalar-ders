# -*- coding: utf-8 -*-
"""Grafiğe giriş: metin sütunları. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

from collections import Counter
sayilar = Counter(k["kategori"] for k in kayitlar)
for kategori, adet in sorted(sayilar.items()):
    print(f"{kategori:8} {'#' * adet} {adet}")
print("Her # bir başvurudur.")
