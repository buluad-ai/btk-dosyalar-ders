# -*- coding: utf-8 -*-
"""PROJE KARTI 2 — Referans çözüm: "Fiber paketler vaat edilen hızı veriyor mu?"

NE ÖĞRETİYOR?
    - Soruyu ÖLÇÜLEBİLİR hale getirmek: "vaat edilen hızı vermek" = ölçülen indirme
      hızı, paket hızının en az %80'i (bu eşik bizim tanımımız; raporda açıkça yazılır).
    - Oran sütunu türetmek: oran = indirme / paket  (Excel'de yeni sütun: =F2/E2)
    - Paket hızına göre kırılım: 100 Mbps paket ile 1000 Mbps paket aynı davranmayabilir.
    - Ortalama yerine MEDYAN: birkaç uç ölçüm sonucu çarpıtmasın.

NASIL ÇALIŞTIRILIR?
    python gun07/projeler/kart2_fiber_vaat.py

BEKLENEN ÇIKTI:
    Fiber ölçüm: 139 | %80 eşiğini geçen: %24
    Çıktılar: outputs/gun07/projeler/kart2_fiber.csv, kart2_fiber_esik.svg
"""
import csv
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "gun06"))
from svg_cizim import sutun_svg                        # noqa: E402

ESIK = 0.80          # "vaat edilen hızı veriyor" tanımı: paketin en az %80'i
CIKTI = ROOT / "outputs" / "gun07" / "projeler"
CIKTI.mkdir(parents=True, exist_ok=True)

with (ROOT / "data" / "hiz_olcumleri.csv").open(encoding="utf-8", newline="") as dosya:
    olcumler = list(csv.DictReader(dosya))

fiber = [o for o in olcumler if o["teknoloji"] == "Fiber"]
for o in fiber:
    o["oran"] = float(o["indirme_mbps"]) / float(o["paket_hizi_mbps"])   # yeni "hesaplanmış sütun"

gecen = [o for o in fiber if o["oran"] >= ESIK]
print(f"Fiber ölçüm: {len(fiber)} | %{ESIK * 100:.0f} eşiğini geçen: %{len(gecen) / len(fiber) * 100:.0f}")

# Paket hızına göre kırılım (PivotTable: Satır = paket_hizi_mbps)
paketler = sorted({int(o["paket_hizi_mbps"]) for o in fiber})
satirlar = []
for paket in paketler:
    grup = [o for o in fiber if int(o["paket_hizi_mbps"]) == paket]
    satirlar.append({
        "paket_mbps": paket,
        "olcum": len(grup),
        "medyan_indirme_mbps": round(statistics.median(float(o["indirme_mbps"]) for o in grup), 1),
        "medyan_oran_yuzde": round(statistics.median(o["oran"] for o in grup) * 100, 1),
        "esigi_gecen_yuzde": round(sum(o["oran"] >= ESIK for o in grup) / len(grup) * 100, 1),
    })

print(f"{'Paket':>6} {'Ölçüm':>6} {'Medyan Mbps':>12} {'Medyan oran %':>14} {'Eşiği geçen %':>14}")
for s in satirlar:
    print(f"{s['paket_mbps']:>6} {s['olcum']:>6} {s['medyan_indirme_mbps']:>12} "
          f"{s['medyan_oran_yuzde']:>14} {s['esigi_gecen_yuzde']:>14}")
print("Yorum: düşük paketlerde vaat büyük ölçüde tutuyor; 500 ve 1000 Mbps paketlerde ölçülen hız vaadin çok altında.")
print("Sınırlılık: ölçüm koşulları (Wi-Fi/kablo, cihaz) veride yok; sentetik veri.")

with (CIKTI / "kart2_fiber.csv").open("w", encoding="utf-8-sig", newline="") as dosya:
    yazici = csv.DictWriter(dosya, fieldnames=list(satirlar[0]), delimiter=";")
    yazici.writeheader()
    yazici.writerows(satirlar)
svg = sutun_svg([f"{s['paket_mbps']} Mbps" for s in satirlar], [s["esigi_gecen_yuzde"] for s in satirlar],
                baslik="Fiber: vaat edilen hızın %80'ini alan ölçüm payı", y_etiketi="Ölçüm payı (%)",
                alt_not="Her sütun bir paket hızı. Eşik: indirme >= paket x 0.80")
(CIKTI / "kart2_fiber_esik.svg").write_text(svg, encoding="utf-8")
print("Çıktılar: outputs/gun07/projeler/kart2_fiber.csv, kart2_fiber_esik.svg")
