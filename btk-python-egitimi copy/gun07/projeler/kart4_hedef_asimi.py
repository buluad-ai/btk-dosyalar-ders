# -*- coding: utf-8 -*-
"""PROJE KARTI 4 — Referans çözüm: "Hangi operatör hedef çözüm süresini en çok aşıyor?"

NE ÖĞRETİYOR?
    - İKİ KAYNAĞI BİRLEŞTİRME: şikâyetler CSV'de, kategori hedefleri Excel'in
      "Hedefler" sayfasında. Her şikâyete kendi kategorisinin hedefini getiririz
      (Excel: DÜŞEYARA / pandas: merge / SQL: JOIN). Burada sözlükle yapıyoruz.
    - Excel dosyasını paketsiz okumak: gun07/basit_xlsx.py
    - Oran hesabı: hedefi aşan çözüm / tüm çözülen.
    - Operatör x kategori çapraz tablosu: sorun her kategoride mi, tek kategoride mi?

NASIL ÇALIŞTIRILIR?
    python gun07/projeler/kart4_hedef_asimi.py

BEKLENEN ÇIKTI:
    Hedef aşım oranı en yüksek operatör: Operatör C
    Çıktılar: outputs/gun07/projeler/kart4_hedef.csv, kart4_hedef.svg
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "gun06"))
sys.path.insert(0, str(ROOT / "gun07"))
from basit_xlsx import xlsx_oku                        # noqa: E402
from svg_cizim import yatay_bar_svg                    # noqa: E402

CIKTI = ROOT / "outputs" / "gun07" / "projeler"
CIKTI.mkdir(parents=True, exist_ok=True)

# DÜŞEYARA tablosu: {"Fatura": 7, "Kapsama": 20, ...}
hedef = {s["kategori"]: s["hedef_gun"] for s in xlsx_oku(ROOT / "data" / "btk_ornek_veri.xlsx", "Hedefler")}

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    cozulen = [k for k in csv.DictReader(dosya) if k["durum"] == "Çözüldü"]
for k in cozulen:
    k["asti"] = int(k["cozum_suresi_gun"]) > hedef[k["kategori"]]   # True/False yeni sütun

operatorler = sorted({k["operator"] for k in cozulen})
kategoriler = sorted(hedef)
satirlar = []
for op in operatorler:
    grup = [k for k in cozulen if k["operator"] == op]
    satir = {"operator": op, "cozulen": len(grup), "asan": sum(k["asti"] for k in grup)}
    satir["asim_yuzde"] = round(satir["asan"] / satir["cozulen"] * 100, 1)
    for kat in kategoriler:                   # çapraz tablo sütunları
        alt = [k for k in grup if k["kategori"] == kat]
        satir[kat] = round(sum(k["asti"] for k in alt) / len(alt) * 100) if alt else ""
    satirlar.append(satir)
satirlar.sort(key=lambda s: s["asim_yuzde"], reverse=True)

print("Hedefler:", ", ".join(f"{k} {v} gün" for k, v in hedef.items()))
print(f"{'Operatör':<12} {'Çözülen':>8} {'Aşan':>5} {'Aşım %':>7}")
for s in satirlar:
    print(f"{s['operator']:<12} {s['cozulen']:>8} {s['asan']:>5} {s['asim_yuzde']:>7}")
print("\nKategori bazında aşım % (satır: operatör):")
print(" " * 12 + "".join(f"{kat:>15}" for kat in kategoriler))
for s in satirlar:
    print(f"{s['operator']:<12}" + "".join(f"{s[kat]:>15}" for kat in kategoriler))
print(f"Hedef aşım oranı en yüksek operatör: {satirlar[0]['operator']}")

with (CIKTI / "kart4_hedef.csv").open("w", encoding="utf-8-sig", newline="") as dosya:
    yazici = csv.DictWriter(dosya, fieldnames=list(satirlar[0]), delimiter=";")
    yazici.writeheader()
    yazici.writerows(satirlar)
svg = yatay_bar_svg([s["operator"] for s in satirlar], [s["asim_yuzde"] for s in satirlar],
                    baslik="Hedef çözüm süresini aşan çözüm payı", birim="%", vurgula=satirlar[0]["operator"],
                    alt_not="Hedefler: btk_ornek_veri.xlsx > Hedefler sayfası. Yalnızca Çözüldü kayıtlar.")
(CIKTI / "kart4_hedef.svg").write_text(svg, encoding="utf-8")
print("Çıktılar: outputs/gun07/projeler/kart4_hedef.csv, kart4_hedef.svg")
