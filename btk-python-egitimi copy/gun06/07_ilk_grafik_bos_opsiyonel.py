# -*- coding: utf-8 -*-
"""CANLI KODLAMA İSKELETİ: Matplotlib ile ilk grafik (öğrenci doldurur).

NE ÖĞRETİYOR?
    Bu dosya ÇALIŞIR ama "çirkin" bir grafik üretir: başlık yok, eksen adı yok,
    değer etiketi yok. TODO yazan satırları sırayla tamamlayıp her adımda dosyayı
    yeniden çalıştırın ve PNG'yi tekrar açın. Grafiğin nasıl iyileştiğini görün.
    Tamamlanmış hali: 07_ilk_grafik_opsiyonel.py (önce kendiniz deneyin).

NASIL ÇALIŞTIRILIR?
    python gun06/07_ilk_grafik_bos_opsiyonel.py

BEKLENEN ÇIKTI:
    İskelet çalıştı: outputs/gun06/07_iskelet.png
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
    sayilar = Counter(satir["kategori"] for satir in csv.DictReader(dosya))

# TODO 1: Kategorileri büyükten küçüğe sıralayın.
#         İpucu: sayilar.most_common() size [("Fatura", 160), ...] listesini verir.
kategoriler = list(sayilar.keys())
adetler = list(sayilar.values())

fig, ax = plt.subplots(figsize=(9, 4.5))
cubuklar = ax.bar(kategoriler, adetler)

# TODO 2: Başlık ekleyin.          İpucu: ax.set_title("...")
# TODO 3: Eksen adlarını ve BİRİMİ yazın. İpucu: ax.set_xlabel("..."), ax.set_ylabel("... (adet)")
# TODO 4: Y eksenini 0'dan başlatın.     İpucu: ax.set_ylim(bottom=0)
# TODO 5: Çubukların üstüne değerleri yazın. İpucu: ax.bar_label(cubuklar)
# TODO 6: Rengi tek, sade bir renge çevirin. İpucu: ax.bar(..., color="#167d9a")

fig.tight_layout()
cikti = ROOT / "outputs" / "gun06"
cikti.mkdir(parents=True, exist_ok=True)
fig.savefig(cikti / "07_iskelet.png", dpi=150)
# plt.show()   # Ekranda görmek isterseniz # işaretini kaldırın (pencere kapanınca script devam eder)
plt.close(fig)
print("İskelet çalıştı: outputs/gun06/07_iskelet.png")
