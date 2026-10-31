# -*- coding: utf-8 -*-
"""Tarihe göre çizgi grafiği."""
from pathlib import Path
from collections import Counter
from datetime import date, timedelta
import csv
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data/basvurular.csv").open(encoding="utf-8", newline="") as f:
    gunluk = Counter(date.fromisoformat(k["tarih"]) for k in csv.DictReader(f))
# Eksik gün varsa 0 olarak ekle; tarihleri metin sırasına bırakma.
baslangic, bitis = min(gunluk), max(gunluk)
gunler = [baslangic + timedelta(days=i) for i in range((bitis-baslangic).days+1)]
noktalar = []
for i, gun in enumerate(gunler):
    noktalar.append(f"{60+i*22},{240-gunluk[gun]*70}")
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="760" height="340">
<rect width="760" height="340" fill="white"/>
<text x="40" y="30" font-size="22">Günlük başvuru sayısı</text>
<path d="M60 80 V240 H680" fill="none" stroke="black"/>
<text x="30" y="245">0</text><text x="30" y="175">1</text><text x="30" y="105">2</text>
<polyline points="{' '.join(noktalar)}" fill="none" stroke="#167d9a" stroke-width="3"/>
<text x="50" y="270">{baslangic.isoformat()}</text><text x="570" y="270">{bitis.isoformat()}</text>
<text x="40" y="310">Her nokta bir gün. Adet değişimi; nedensellik göstermez.</text></svg>"""
cikti = ROOT / "outputs/gun06"
cikti.mkdir(parents=True, exist_ok=True)
(cikti / "gunluk.svg").write_text(svg, encoding="utf-8")
print("Gün sayısı:", len(gunler))
print("Günlük toplam:", sum(gunluk.values()))
