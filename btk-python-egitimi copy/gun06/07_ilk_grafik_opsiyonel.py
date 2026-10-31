# -*- coding: utf-8 -*-
"""Matplotlib ile ilk düzgün grafik: kategori bazında şikâyet (TAMAMLANMIŞ hali).

NE ÖĞRETİYOR?
    1) fig, ax = plt.subplots()  -> "fig" kağıt, "ax" o kağıttaki çizim alanı.
    2) ax.bar(...)               -> çubukları çiz.
    3) İyi grafik kuralları: başlık, eksen etiketleri, BİRİM, 0'dan başlayan eksen,
       tek renk, değer etiketi (bar_label), Türkçe karakterler.
    4) fig.savefig(..., dpi=150) -> PNG dosyasına kaydet; plt.close(fig) -> belleği boşalt.
    Canlı kodlama iskeleti: 07_ilk_grafik_bos_opsiyonel.py (TODO'ları sınıfta doldurun).

    Excel karşılığı: Veriyi seç > Ekle > Sütun Grafiği > Grafik Başlığı / Eksen Başlıkları
    > Veri Etiketleri. Burada her tıklama bir satır koddur; bir kez yazınca her ay
    aynı grafiği tek komutla yeniden üretirsiniz.

NASIL ÇALIŞTIRILIR?
    python gun06/07_ilk_grafik_opsiyonel.py

BEKLENEN ÇIKTI:
    Grafik kaydedildi: outputs/gun06/07_kategori_bar.png
    (matplotlib yoksa: ATLANDI: matplotlib kurulu değil — B planı: 18_svg_yatay_bar.py)
"""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    import matplotlib.pyplot as plt   # "plt" kısaltması dünya çapında standarttır
except ImportError:
    print("ATLANDI: matplotlib kurulu değil — B planı: 18_svg_yatay_bar.py")
    sys.exit(0)   # 0 = "hata yok" çıkışı; ders paketsiz yoldan devam eder

# --- Veriyi hazırla (pandas gerekmez; csv modülü yeterli) -----------------------
with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    sayilar = Counter(satir["kategori"] for satir in csv.DictReader(dosya))

# Büyükten küçüğe sırala: okur en büyüğü ilk bakışta görsün.
sirali = sayilar.most_common()                       # [("Fatura", 160), ...]
kategoriler = [ad for ad, adet in sirali]            # x ekseni yazıları
adetler = [adet for ad, adet in sirali]              # çubuk boyları

# --- Grafiği çiz ----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.5))   # figsize = (genişlik, yükseklik) inç cinsinden
cubuklar = ax.bar(kategoriler, adetler, color="#167d9a")   # TEK renk: renk anlam taşımıyorsa çoğaltma

ax.set_title("Kategoriye göre şikâyet sayısı (Ocak–Eylül 2026)")
ax.set_xlabel("Şikâyet kategorisi")
ax.set_ylabel("Şikâyet sayısı (adet)")   # BİRİM parantez içinde: adet, gün, Mbps ...
ax.set_ylim(bottom=0)                     # Çubuk grafiği DAİMA 0'dan başlar
ax.bar_label(cubuklar, padding=3)        # Her çubuğun üstüne değerini yaz
ax.spines[["top", "right"]].set_visible(False)   # Gereksiz çerçeve çizgilerini kaldır

fig.tight_layout()   # Yazılar taşmasın diye kenar boşluklarını otomatik ayarla

cikti = ROOT / "outputs" / "gun06"
cikti.mkdir(parents=True, exist_ok=True)
fig.savefig(cikti / "07_kategori_bar.png", dpi=150)   # dpi: inç başına nokta (150 = rapora yeter)
# plt.show()   # Ekranda pencere olarak görmek isterseniz bu satırın başındaki # işaretini silin.
plt.close(fig)   # Döngüde çok grafik çizerken belleğin şişmesini önler

print("En çok şikâyet:", kategoriler[0], adetler[0])
print("Grafik kaydedildi: outputs/gun06/07_kategori_bar.png")
