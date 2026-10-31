# -*- coding: utf-8 -*-
"""Paketsiz SVG sütun grafiği. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

from collections import Counter
from html import escape
sayilar = Counter(k["kategori"] for k in kayitlar)
cikti = ROOT / "outputs" / "gun06"
cikti.mkdir(parents=True, exist_ok=True)
# SVG bir metin dosyasıdır; tarayıcıda açılır. Hazır çizim şablonunu uyarlıyoruz.
parcalar = ['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="340" viewBox="0 0 720 340">',
            '<rect width="720" height="340" fill="white"/>',
            '<text x="30" y="35" font-size="22">Kategoriye göre başvuru sayısı</text>']
for sira, (kategori, adet) in enumerate(sorted(sayilar.items())):
    y = 90 + sira * 70
    parcalar.append(f'<text x="20" y="{y+25}" font-size="18">{escape(kategori)}</text>')
    parcalar.append(f'<rect x="120" y="{y}" width="{adet*20}" height="36" fill="#167d9a"/>')
    parcalar.append(f'<text x="{130+adet*20}" y="{y+25}" font-size="18">{adet}</text>')
parcalar.append('<text x="20" y="320" font-size="15">Ölçek: 20 piksel = 1 başvuru; başlangıç = 0.</text></svg>')
(cikti / "kategori.svg").write_text("\n".join(parcalar), encoding="utf-8")
print("Grafik: outputs/gun06/kategori.svg")
