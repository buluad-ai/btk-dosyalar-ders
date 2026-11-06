# -*- coding: utf-8 -*-
"""Gün 3 ek alıştırmalarının çözümleri (ALISTIRMALAR.md: Temel T1-T3, Orta O1-O3, İleri İ1-İ3).

NASIL ÇALIŞTIRILIR?
    python gun03/cozumler_ek.py

BEKLENEN ÇIKTI (kısaltılmış):
    T1 KDV dahil toplam: 6219.93 TL
    T2 e-Devlet şikâyeti: 195
    T3 İzmir CSV satırı: 68
    O1 Ankara: (107, 80, 8.7)
    ...
    İ3 İş günü (02.03.2026-16.03.2026): 11
Öğrenciye önce kendi çözümünü yazdırın; bu dosyayı karşılaştırma için açın.
"""
import csv
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import yardimcilar as y

ROOT = Path(__file__).resolve().parents[1]
CIKTI = ROOT / "outputs" / "gun03"
CIKTI.mkdir(parents=True, exist_ok=True)
kayitlar = y.csv_oku("sikayetler.csv")

# ===========================================================================
# TEMEL
# ===========================================================================
# T1: Üç itiraz tutarının KDV dahil toplamı (modüldeki kdv_ekle ile)
tutarlar = [2404.26, 1952.36, 826.66]
print(f"T1 KDV dahil toplam: {sum(y.kdv_ekle(t) for t in tutarlar):.2f} TL")

# T2: e-Devlet kanalından gelen şikâyet sayısı (Excel: EĞERSAY)
print("T2 e-Devlet şikâyeti:", sum(1 for k in kayitlar if k["kanal"] == "e-Devlet"))

# T3: İzmir şikâyetlerini Excel'de açılabilir CSV'ye yaz ve geri oku
izmir = [k for k in kayitlar if k["il"] == "İzmir"]
with open(CIKTI / "izmir.csv", "w", encoding="utf-8-sig", newline="") as f:
    yazici = csv.DictWriter(f, fieldnames=list(kayitlar[0]))
    yazici.writeheader()
    yazici.writerows(izmir)
with open(CIKTI / "izmir.csv", encoding="utf-8-sig", newline="") as f:
    print("T3 İzmir CSV satırı:", len(list(csv.DictReader(f))))


# ===========================================================================
# ORTA
# ===========================================================================
# O1: Birden çok değer döndüren fonksiyon
def il_ozeti(kayitlar, il):
    """(toplam, çözülen, çözülenlerin ortalama süresi) döndürür."""
    secilen = [k for k in kayitlar if k["il"] == il]
    sureler = [int(k["cozum_suresi_gun"]) for k in secilen if k["durum"] == "Çözüldü"]
    ort = round(sum(sureler) / len(sureler), 1) if sureler else None
    return len(secilen), len(sureler), ort


print("O1 Ankara:", il_ozeti(kayitlar, "Ankara"))
toplam, cozulen, ort = il_ozeti(kayitlar, "Bursa")
print(f"O1 Bursa: {toplam} şikâyet, {cozulen} çözülen, ortalama {ort} gün")

# O2: Haziran şikâyetlerinin hafta günü dağılımı ve en yoğun gün
haziran = [date.fromisoformat(k["tarih"]) for k in kayitlar if k["tarih"].startswith("2026-06")]
gunler = Counter(y.gun_adi(t) for t in haziran)
en_yogun, adet = gunler.most_common(1)[0]
print(f"O2 Haziran: {len(haziran)} şikâyet, en yoğun gün {en_yogun} ({adet})")

# O3: Paket hızının %50'sinin altında kalan ölçümleri say, log dosyasına yaz
olcumler = y.csv_oku("hiz_olcumleri.csv")
dusuk = [o for o in olcumler
         if y.hiz_yuzdesi(float(o["indirme_mbps"]), int(o["paket_hizi_mbps"])) < 50]
with open(CIKTI / "dusuk_hiz_log.txt", "w", encoding="utf-8") as f:
    for o in dusuk:
        yuzde = y.hiz_yuzdesi(float(o["indirme_mbps"]), int(o["paket_hizi_mbps"]))
        f.write(f"{o['tarih']} {o['il']} {o['operator']} %{yuzde}\n")
print("O3 Paketin %50 altındaki ölçüm:", len(dusuk))


# ===========================================================================
# İLERİ
# ===========================================================================
# İ1: Kural tablosuyla doğrulama + gerekçe sayımlarını JSON'a yazma
KURALLAR = {
    "tarih_gecersiz": lambda k: not _tarih_gecerli(k["tarih"]),
    "kategori_bos": lambda k: k["kategori"].strip() == "",
    "sure_sayi_degil": lambda k: k["cozum_suresi_gun"] != "" and not k["cozum_suresi_gun"].lstrip("-").isdigit(),
    "sure_negatif": lambda k: k["cozum_suresi_gun"].startswith("-"),
    "memnuniyet_aralik_disi": lambda k: k["memnuniyet"] != "" and not 1 <= int(k["memnuniyet"]) <= 5,
}


def _tarih_gecerli(metin):
    try:
        date.fromisoformat(metin)
    except ValueError:
        return False
    return True


kirli = y.csv_oku("sikayetler_kirli.csv")
gerekceler = Counter()
for k in kirli:
    for ad, kural in KURALLAR.items():
        if kural(k):
            gerekceler[ad] += 1
(CIKTI / "kural_sayimlari.json").write_text(
    json.dumps(dict(gerekceler), ensure_ascii=False, indent=2), encoding="utf-8")
print("İ1 Kural ihlalleri:", dict(sorted(gerekceler.items())))


# İ2: Birden çok il için tek seferde rapor (parametre listesi)
def il_raporu(iller=("Ankara", "İzmir")):
    for il in iller:
        toplam, cozulen, ort = il_ozeti(kayitlar, il)
        print(f"İ2 {il}: {toplam} şikâyet, çözüm oranı %{100 * cozulen / toplam:.1f}")


il_raporu()


# İ3: Excel TAMİŞGÜNÜ benzeri: iki tarih arasındaki iş günü (iki uç dahil, hafta sonu hariç)
def is_gunu_sayisi(baslangic, bitis):
    gun = baslangic
    sayac = 0
    while gun <= bitis:
        if gun.weekday() < 5:          # 0-4: Pazartesi-Cuma
            sayac += 1
        gun += timedelta(days=1)
    return sayac


print("İ3 İş günü (02.03.2026-16.03.2026):", is_gunu_sayisi(date(2026, 3, 2), date(2026, 3, 16)))
