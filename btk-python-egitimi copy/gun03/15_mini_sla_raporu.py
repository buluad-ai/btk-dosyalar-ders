# -*- coding: utf-8 -*-
"""Gün 3 mini proje (tamamlanmış): kategori bazında SLA (hedef süre) aşım raporu.

NE ÖĞRETİYOR?
    15_mini_sla_raporu_bos.py iskeletinin doldurulmuş hâli. Günün tüm konuları:
    kendi modülümüzü import, fonksiyon, CSV okuma, boş hücre, sözlükle gruplama
    (Excel PivotTable'ın elle yapılmış hâli), oran hesabı ve CSV'ye yazma.

NASIL ÇALIŞTIRILIR?
    python gun03/15_mini_sla_raporu.py

BEKLENEN ÇIKTI (kısaltılmış):
    Kategori        Hedef  Çözülen  Aşan   Oran
    Fatura              7      ...   ...   ...%
    ...
    Toplam çözülen: 415
    Rapor: outputs/gun03/sla_raporu.csv
"""
import csv
from pathlib import Path

import yardimcilar

ROOT = Path(__file__).resolve().parents[1]
cikti = ROOT / "outputs" / "gun03"
cikti.mkdir(parents=True, exist_ok=True)

HEDEFLER = {"Fatura": 7, "İnternet Hızı": 10, "Kesinti": 5,
            "Taahhüt/İptal": 15, "Numara Taşıma": 3, "Kapsama": 20}

kayitlar = yardimcilar.csv_oku("sikayetler.csv")

# Sözlük üreteci: her kategori için sıfırlanmış sayaç sözlüğü
ozet = {kategori: {"cozulen": 0, "asan": 0} for kategori in HEDEFLER}

for kayit in kayitlar:
    if kayit["durum"] != "Çözüldü":                                   # TODO 1
        continue
    sure = yardimcilar.sayiya_cevir(kayit["cozum_suresi_gun"], int)   # TODO 2
    hedef = HEDEFLER[kayit["kategori"]]                               # TODO 3
    ozet[kayit["kategori"]]["cozulen"] += 1                           # TODO 4
    if yardimcilar.sla_asildi_mi(sure, hedef):
        ozet[kayit["kategori"]]["asan"] += 1

# TODO 5: tablo hâlinde yazdır ve oranı hesapla
satirlar = []
print(f"{'Kategori':<15} {'Hedef':>5} {'Çözülen':>8} {'Aşan':>5} {'Oran':>7}")
for kategori, sayac in ozet.items():
    oran = round(100 * sayac["asan"] / sayac["cozulen"], 1) if sayac["cozulen"] else None
    satirlar.append({"kategori": kategori, "hedef_gun": HEDEFLER[kategori],
                     "cozulen": sayac["cozulen"], "asan": sayac["asan"], "asim_orani": oran})
    print(f"{kategori:<15} {HEDEFLER[kategori]:>5} {sayac['cozulen']:>8} {sayac['asan']:>5} {oran:>6}%")

# Kontrol toplamı: kategorilerin toplamı tüm çözülenlere eşit olmalı
print("Toplam çözülen:", sum(s["cozulen"] for s in satirlar))

# TODO 6: CSV'ye yaz
rapor = cikti / "sla_raporu.csv"
with open(rapor, "w", encoding="utf-8-sig", newline="") as f:
    yazici = csv.DictWriter(f, fieldnames=["kategori", "hedef_gun", "cozulen", "asan", "asim_orani"])
    yazici.writeheader()
    yazici.writerows(satirlar)
print("Rapor:", rapor.relative_to(ROOT).as_posix())

# Sonucu yorumlayın: Hangi kategoride hedef en sık aşılıyor? Hedef mi gerçekçi değil,
# yoksa süreç mi yavaş? Veri tek başına "neden"i söylemez; soru sordurur.
