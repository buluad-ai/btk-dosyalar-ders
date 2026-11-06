# -*- coding: utf-8 -*-
"""Gerçek boyutlu CSV: sikayetler.csv (600 satır) okuma, tür dönüşümü, boş hücreler.

NE ÖĞRETİYOR?
    - csv.DictReader: her satır bir sözlük, başlıklar anahtar (Excel'de ilk satır başlık)
    - CSV'den gelen HER DEĞER METİNDİR: "7" ile 7 farklıdır
    - Boş hücre ("") ile sıfır (0) farklıdır: boş = bilinmiyor
    - Durum sayımı (Excel: EĞERSAY), koşullu ortalama (ORTALAMAEĞER), koşullu toplam (ETOPLA)

    Sabahki 03_csv_okuma.py küçük veriyle (36 satır) aynı işi yapıyordu.
    Şimdi aynı yöntem 600 satırlık şikâyet verisine uygulanıyor: kod neredeyse aynı!

NASIL ÇALIŞTIRILIR?
    python gun03/10_sikayet_csv_okuma.py

BEKLENEN ÇIKTI (kısaltılmış):
    Sütunlar: ['sikayet_no', 'tarih', 'il', ...]
    Toplam şikâyet: 600
    Durumlara göre: {'Reddedildi': 89, 'Çözüldü': 415, 'İşlemde': 96}
    Boş çözüm süresi: 96
    Çözülenlerin ortalama süresi: 9.60 gün
    Toplam itiraz tutarı: ... TL (160 kayıtta)
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# newline="" : csv modülünün satır sonlarını kendisi yönetmesi için gerekli (resmî öneri).
with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    okuyucu = csv.DictReader(dosya)
    print("Sütunlar:", okuyucu.fieldnames)
    kayitlar = list(okuyucu)          # tüm satırları listeye al (dosya kapanmadan önce!)

print("Toplam şikâyet:", len(kayitlar))
print("İlk kayıt:", kayitlar[0])
# Dikkat: ilk kayıtta 'cozum_suresi_gun': '7' -> tırnak içinde, yani METİN.

# ---------------------------------------------------------------------------
# 1) Sayım: durumlara göre (Excel: EĞERSAY veya PivotTable "Say")
# ---------------------------------------------------------------------------
durumlar = {}
for kayit in kayitlar:
    durum = kayit["durum"]
    durumlar[durum] = durumlar.get(durum, 0) + 1
print("Durumlara göre:", durumlar)

# ---------------------------------------------------------------------------
# 2) Tür dönüşümü ve boş hücreler
# ---------------------------------------------------------------------------
# İşlemdeki kayıtlarda çözüm süresi BOŞTUR (""), çünkü henüz çözülmediler.
# int("") -> ValueError: invalid literal for int() with base 10: ''
# Bu yüzden önce boş mu diye bakıyoruz. Boşu 0 yapmak YANLIŞ olur:
# ortalamayı yapay olarak düşürür ("0 günde çözüldü" demek olur).
bos_sure = 0
cozulen_sureler = []
for kayit in kayitlar:
    metin = kayit["cozum_suresi_gun"]
    if metin == "":
        bos_sure += 1
        continue                      # bu kaydı atla, döngünün başına dön
    if kayit["durum"] == "Çözüldü":
        cozulen_sureler.append(int(metin))   # metin -> tam sayı

print("Boş çözüm süresi:", bos_sure)
ortalama = sum(cozulen_sureler) / len(cozulen_sureler)
print(f"Çözülenlerin ortalama süresi: {ortalama:.2f} gün")   # Excel: ORTALAMAEĞER

# ---------------------------------------------------------------------------
# 3) Ondalıklı sayı: itiraz tutarı (yalnızca fatura itirazlarında dolu)
# ---------------------------------------------------------------------------
# CSV'de ondalık ayırıcı NOKTA: "2404.26". float("2404,26") hata verir!
# Türkçe Excel'den gelen dosyalarda virgül görürseniz: float(metin.replace(",", "."))
toplam_tutar = 0.0
dolu_tutar = 0
for kayit in kayitlar:
    if kayit["itiraz_tutari_tl"] != "":
        toplam_tutar += float(kayit["itiraz_tutari_tl"])
        dolu_tutar += 1
print(f"Toplam itiraz tutarı: {toplam_tutar:,.2f} TL ({dolu_tutar} kayıtta)")   # Excel: ETOPLA
# :,.2f -> binlik ayırıcı virgül, 2 ondalık (İngilizce biçim: 1,234.56)

# ---------------------------------------------------------------------------
# 4) Memnuniyet puanı (1-5) - boşlar hariç ortalama
# ---------------------------------------------------------------------------
puanlar = [int(k["memnuniyet"]) for k in kayitlar if k["memnuniyet"] != ""]
print(f"Memnuniyet: {len(puanlar)} puan, ortalama {sum(puanlar) / len(puanlar):.2f} / 5")
