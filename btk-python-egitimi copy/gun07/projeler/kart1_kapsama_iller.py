# -*- coding: utf-8 -*-
"""PROJE KARTI 1 — Referans çözüm: "Kapsama şikâyetleri hangi illerde yoğun?"

NE ÖĞRETİYOR?
    "Yoğun" iki farklı anlama gelebilir; iyi bir analiz İKİSİNİ de gösterir:
      a) ADET  : en çok Kapsama şikâyeti hangi ilden geliyor?  (büyük il hep önde)
      b) PAY   : ilin kendi şikâyetleri içinde Kapsama yüzde kaç? (iller adil karşılaştırılır)
    Ayrıca küçük sayılara dikkat: 34 şikâyetli bir ilde 6 kayıt %17.6 eder; 1-2 kayıt
    oranı çok oynatır. Rapora "kayıt sayısı az" notu düşmek analistin görevidir.

    Excel karşılığı: PivotTable (Satır=il, Sütun=kategori, Değer=Say) + "Satır toplamının %'si".

NASIL ÇALIŞTIRILIR?
    python gun07/projeler/kart1_kapsama_iller.py

BEKLENEN ÇIKTI:
    Adet olarak en yoğun il: İstanbul (20)
    Pay olarak en yoğun il: Erzurum (%17.6)
    Çıktılar: outputs/gun07/projeler/kart1_kapsama.csv, kart1_kapsama_payi.svg
"""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # gun07/projeler -> gun07 -> proje kökü
sys.path.insert(0, str(ROOT / "gun06"))              # hazır SVG çizim aleti
from svg_cizim import yatay_bar_svg                  # noqa: E402

CIKTI = ROOT / "outputs" / "gun07" / "projeler"
CIKTI.mkdir(parents=True, exist_ok=True)

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

toplam = Counter(k["il"] for k in kayitlar)                                   # ildeki tüm şikâyetler
kapsama = Counter(k["il"] for k in kayitlar if k["kategori"] == "Kapsama")    # ildeki Kapsama şikâyetleri

satirlar = []
for il, il_toplam in toplam.items():
    pay = kapsama[il] / il_toplam * 100
    satirlar.append({"il": il, "kapsama": kapsama[il], "toplam": il_toplam, "pay_yuzde": round(pay, 1),
                     "not": "kayıt az, dikkatli yorumla" if kapsama[il] < 10 else ""})
satirlar.sort(key=lambda s: s["pay_yuzde"], reverse=True)       # paya göre büyükten küçüğe

print(f"{'İl':<10} {'Kapsama':>8} {'Toplam':>7} {'Pay %':>6}  Not")
for s in satirlar:
    print(f"{s['il']:<10} {s['kapsama']:>8} {s['toplam']:>7} {s['pay_yuzde']:>6}  {s['not']}")

en_adet = max(satirlar, key=lambda s: s["kapsama"])
print(f"Adet olarak en yoğun il: {en_adet['il']} ({en_adet['kapsama']})")
print(f"Pay olarak en yoğun il: {satirlar[0]['il']} (%{satirlar[0]['pay_yuzde']})")

with (CIKTI / "kart1_kapsama.csv").open("w", encoding="utf-8-sig", newline="") as dosya:
    yazici = csv.DictWriter(dosya, fieldnames=list(satirlar[0]), delimiter=";")
    yazici.writeheader()
    yazici.writerows(satirlar)
svg = yatay_bar_svg([s["il"] for s in satirlar], [s["pay_yuzde"] for s in satirlar],
                    baslik="Kapsama şikâyetlerinin il içindeki payı", birim="%", vurgula=satirlar[0]["il"],
                    alt_not="Pay = ildeki Kapsama / ildeki tüm şikâyetler. Sentetik veri.")
(CIKTI / "kart1_kapsama_payi.svg").write_text(svg, encoding="utf-8")
print("Çıktılar: outputs/gun07/projeler/kart1_kapsama.csv, kart1_kapsama_payi.svg")
