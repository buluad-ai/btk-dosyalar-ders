# -*- coding: utf-8 -*-
"""Paketsiz paylaşılabilir HTML raporu. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

from collections import Counter
from html import escape
sayilar = Counter(k["kategori"] for k in kayitlar)
satirlar = "".join(f"<tr><td>{escape(ad)}</td><td>{adet}</td></tr>" for ad, adet in sorted(sayilar.items()))
# escape, verinin HTML etiketi olarak yorumlanmasını önler.
html = f"""<!doctype html><html lang="tr"><meta charset="utf-8">
<title>BTK Eğitim Raporu</title><style>body{{font:20px sans-serif;max-width:850px;margin:50px auto}}td,th{{padding:12px;border-bottom:1px solid #ddd}}</style>
<h1>Başvuru özeti</h1><p>Sentetik veri • Toplam {len(kayitlar)} başvuru</p>
<table><tr><th>Kategori</th><th>Başvuru sayısı</th></tr>{satirlar}</table>
<p>Bu tablo adetleri gösterir; hizmet kalitesini tek başına ölçmez.</p></html>"""
cikti = ROOT / "outputs" / "gun07"
cikti.mkdir(parents=True, exist_ok=True)
(cikti / "rapor.html").write_text(html, encoding="utf-8")
print("Rapor: outputs/gun07/rapor.html")
