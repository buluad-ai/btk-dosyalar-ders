# -*- coding: utf-8 -*-
"""Sıralı yatay çubuk (barh): il bazında şikâyet sayısı.

NE ÖĞRETİYOR?
    - Kategori adları uzunsa veya çoksa (8 il) YATAY çubuk daha okunaklıdır:
      yazılar yan yatmaz, üst üste binmez.
    - Sıralama: büyükten küçüğe. barh alttan yukarı çizdiği için listeyi
      KÜÇÜKTEN büyüğe verip en büyüğü en üste getiririz (sık yapılan şaşırtmaca).
    - Vurgu rengi: hepsi gri-mavi, anlatmak istediğimiz tek çubuk turuncu.
      Renk "süs" değil, "mesaj" taşımalı.

    Excel karşılığı: Çubuk grafik (yatay) + "Veriyi Sırala (Z'den A'ya)" + tek bir
    veri noktasını seçip dolgu rengini değiştirmek.

NASIL ÇALIŞTIRILIR?
    python gun06/08_sirali_barh_opsiyonel.py

BEKLENEN ÇIKTI:
    En yoğun il: İstanbul (185)
    Grafik kaydedildi: outputs/gun06/08_il_barh.png
"""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("ATLANDI: matplotlib kurulu değil — B planı: 18_svg_yatay_bar.py")
    sys.exit(0)

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    il_sayilari = Counter(satir["il"] for satir in csv.DictReader(dosya))

# Küçükten büyüğe sırala -> barh en büyüğü EN ÜSTE koyar.
# sorted(..., key=lambda ikili: ikili[1]) : "ikilinin 2. elemanına (adede) göre sırala"
sirali = sorted(il_sayilari.items(), key=lambda ikili: ikili[1])
iller = [il for il, adet in sirali]
adetler = [adet for il, adet in sirali]
en_yogun = iller[-1]                       # listenin son elemanı = en büyük

# Her çubuğun rengi: en yoğun il turuncu, diğerleri ana renk.
renkler = ["#eb6834" if il == en_yogun else "#167d9a" for il in iller]

fig, ax = plt.subplots(figsize=(8, 5))
cubuklar = ax.barh(iller, adetler, color=renkler)
ax.bar_label(cubuklar, padding=3)          # değerler çubuğun ucunda
ax.set_title("İl bazında şikâyet sayısı (Ocak–Eylül 2026)")
ax.set_xlabel("Şikâyet sayısı (adet)")
ax.set_xlim(left=0)                        # yatay çubukta da başlangıç 0
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()

cikti = ROOT / "outputs" / "gun06"
cikti.mkdir(parents=True, exist_ok=True)
fig.savefig(cikti / "08_il_barh.png", dpi=150)
# plt.show()
plt.close(fig)

print(f"En yoğun il: {en_yogun} ({adetler[-1]})")
print("Not: İstanbul nüfusu en büyük il; adet tek başına 'en sorunlu il' demek değildir.")
print("Grafik kaydedildi: outputs/gun06/08_il_barh.png")
