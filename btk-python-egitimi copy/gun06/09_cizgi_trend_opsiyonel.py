# -*- coding: utf-8 -*-
"""Çizgi grafiği: aylık şikâyet trendi (data/sikayetler.csv).

NE ÖĞRETİYOR?
    - ZAMAN sorusu -> çizgi grafik. x ekseni zaman sırasıyla ilerler.
    - Tarih metninden ay çıkarma: "2026-03-14"[:7] -> "2026-03"
    - Ay numarasını Türkçe kısa ada çevirme (Oca, Şub, Mar ...)
    - ax.plot(x, y, marker="o") ve en yüksek noktaya not düşme (annotate)
    - İki seri: tüm şikâyetler ve yalnızca "İnternet Hızı" -> lejant (legend)

    Excel karşılığı: Ekle > Çizgi Grafik. Ay sütununu kendiniz SOLDAN(A2;7) ile üretip
    PivotTable'da "Satırlar = ay" yapmakla aynı işi görür.

NASIL ÇALIŞTIRILIR?
    python gun06/09_cizgi_trend_opsiyonel.py

BEKLENEN ÇIKTI:
    En yoğun ay: Haz (87 şikâyet)
    Grafik kaydedildi: outputs/gun06/09_aylik_trend.png
"""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("ATLANDI: matplotlib kurulu değil — B planı: 17_svg_cizgi_aylik.py")
    sys.exit(0)

AY_ADLARI = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

toplam = Counter(k["tarih"][:7] for k in kayitlar)                       # {"2026-01": 64, ...}
hiz = Counter(k["tarih"][:7] for k in kayitlar if k["kategori"] == "İnternet Hızı")

aylar = sorted(toplam)            # "2026-01" < "2026-02" ... metin sırası = zaman sırası (YYYY-AA biçimi sayesinde)
etiketler = [AY_ADLARI[int(ay[5:7]) - 1] for ay in aylar]   # "2026-03" -> 3 -> "Mar"
toplam_degerler = [toplam[ay] for ay in aylar]
hiz_degerler = [hiz[ay] for ay in aylar]   # Counter, olmayan ay için 0 döndürür (hata vermez)

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(etiketler, toplam_degerler, marker="o", linewidth=2, color="#167d9a", label="Tüm şikâyetler")
ax.plot(etiketler, hiz_degerler, marker="o", linewidth=2, color="#eb6834", label="Yalnızca İnternet Hızı")

# En yüksek ayı bul ve üstüne not yaz.
en_yuksek = max(range(len(aylar)), key=lambda i: toplam_degerler[i])   # en büyük değerin SIRA numarası
ax.annotate(f"En yüksek: {toplam_degerler[en_yuksek]}",
            xy=(en_yuksek, toplam_degerler[en_yuksek]),            # okun ucu (nokta)
            xytext=(en_yuksek - 1.6, toplam_degerler[en_yuksek] + 8),  # yazının yeri
            arrowprops={"arrowstyle": "->", "color": "#555555"})

ax.set_title("Aylık şikâyet sayısı, 2026")
ax.set_xlabel("Ay")
ax.set_ylabel("Şikâyet sayısı (adet)")
ax.set_ylim(0, max(toplam_degerler) * 1.25)   # 0'dan başlatmak dalgalanmayı abartmamızı engeller
ax.grid(axis="y", color="#e5e5e2")            # açık gri yardımcı çizgiler
ax.legend(frameon=False)                      # iki seri var -> lejant şart
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()

cikti = ROOT / "outputs" / "gun06"
cikti.mkdir(parents=True, exist_ok=True)
fig.savefig(cikti / "09_aylik_trend.png", dpi=150)
# plt.show()
plt.close(fig)

print(f"En yoğun ay: {etiketler[en_yuksek]} ({toplam_degerler[en_yuksek]} şikâyet)")
print("Grafik kaydedildi: outputs/gun06/09_aylik_trend.png")
