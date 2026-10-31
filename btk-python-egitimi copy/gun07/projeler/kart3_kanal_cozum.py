# -*- coding: utf-8 -*-
"""PROJE KARTI 3 — Referans çözüm: "Hangi kanal daha hızlı çözüm alıyor?"

NE ÖĞRETİYOR?
    - Doğru alt küme: süre yalnızca "Çözüldü" kayıtlarda anlamlı.
    - Ortalama + medyan + kayıt sayısı birlikte verilir (tek sayı yanıltabilir).
    - "Fark yok" da bir BULGUDUR: kanallar arasındaki fark 1 günden azsa
      "kanal belirleyici değil" demek dürüst sonuçtur.
    - Karıştırıcı etken (kategori karışımı): Kapsama şikâyetleri (~18 gün) hangi
      kanaldan çok geliyorsa o kanal "yavaş" görünür. Bu yüzden kategori içinde de
      karşılaştırırız: her kategoride en hızlı kanal hangisi?

NASIL ÇALIŞTIRILIR?
    python gun07/projeler/kart3_kanal_cozum.py

BEKLENEN ÇIKTI:
    En hızlı kanal (ortalama): Çağrı Merkezi 9.27 gün
    En hızlı ile en yavaş arası fark: 0.69 gün
    Çıktılar: outputs/gun07/projeler/kart3_kanal.csv, kart3_kanal.svg
"""
import csv
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "gun06"))
from svg_cizim import yatay_bar_svg                    # noqa: E402

CIKTI = ROOT / "outputs" / "gun07" / "projeler"
CIKTI.mkdir(parents=True, exist_ok=True)

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    cozulen = [k for k in csv.DictReader(dosya) if k["durum"] == "Çözüldü"]

# Kanal -> süre listesi (Excel: kanal sütununa göre grupla)
sureler = {}
for k in cozulen:
    sureler.setdefault(k["kanal"], []).append(int(k["cozum_suresi_gun"]))   # setdefault: yoksa boş liste aç

satirlar = [{"kanal": kanal, "cozulen": len(liste), "ortalama_gun": round(statistics.mean(liste), 2),
             "medyan_gun": float(statistics.median(liste))} for kanal, liste in sureler.items()]
satirlar.sort(key=lambda s: (s["ortalama_gun"], s["kanal"]))              # hızlıdan yavaşa

print(f"{'Kanal':<15} {'Çözülen':>8} {'Ortalama':>9} {'Medyan':>7}")
for s in satirlar:
    print(f"{s['kanal']:<15} {s['cozulen']:>8} {s['ortalama_gun']:>9} {s['medyan_gun']:>7}")
fark = satirlar[-1]["ortalama_gun"] - satirlar[0]["ortalama_gun"]
print(f"En hızlı kanal (ortalama): {satirlar[0]['kanal']} {satirlar[0]['ortalama_gun']} gün")
print(f"En hızlı ile en yavaş arası fark: {fark:.2f} gün")

# Kategori içinde karşılaştırma: her kategori için en hızlı kanal
print("\nKategori içinde en hızlı kanal (en az 5 kayıtlı kanallar):")
kategoriler = sorted({k["kategori"] for k in cozulen})
for kategori in kategoriler:
    adaylar = []
    for kanal in sureler:
        liste = [int(k["cozum_suresi_gun"]) for k in cozulen if k["kategori"] == kategori and k["kanal"] == kanal]
        if len(liste) >= 5:
            adaylar.append((statistics.mean(liste), kanal, len(liste)))
    if adaylar:
        ort, kanal, n = min(adaylar)
        print(f"  {kategori:<14} -> {kanal} ({ort:.1f} gün, {n} kayıt)")
print("Sonuç: kanal farkı küçük ve kategoriye göre değişiyor; kanal tek başına belirleyici görünmüyor.")

with (CIKTI / "kart3_kanal.csv").open("w", encoding="utf-8-sig", newline="") as dosya:
    yazici = csv.DictWriter(dosya, fieldnames=list(satirlar[0]), delimiter=";")
    yazici.writeheader()
    yazici.writerows(satirlar)
svg = yatay_bar_svg([s["kanal"] for s in satirlar], [s["ortalama_gun"] for s in satirlar],
                    baslik="Kanala göre ortalama çözüm süresi", birim="gün",
                    alt_not="Yalnızca Çözüldü kayıtlar. Fark 1 günden az.")
(CIKTI / "kart3_kanal.svg").write_text(svg, encoding="utf-8")
print("Çıktılar: outputs/gun07/projeler/kart3_kanal.csv, kart3_kanal.svg")
