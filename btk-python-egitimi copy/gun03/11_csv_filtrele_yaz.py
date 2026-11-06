# -*- coding: utf-8 -*-
"""Filtreleyip yeni CSV yazma: Excel'de düzgün açılan dosya (utf-8-sig ve noktalı virgül).

NE ÖĞRETİYOR?
    - Excel'deki Otomatik Filtre'nin Python karşılığı: if ile satır seçmek
    - csv.DictWriter ile başlıklı yeni CSV yazmak
    - utf-8-sig: Excel'in Türkçe karakterleri doğru göstermesi için
    - Türkçe Windows Excel'i için ";" ayırıcılı ve ondalığı virgüllü sürüm

    NEDEN utf-8-sig?
      Excel, CSV'ye çift tıklanınca dosyanın kodlamasını tahmin eder. Dosyanın
      başında görünmez bir işaret (BOM) yoksa Türkçe karakterleri bozabilir:
      "İstanbul" -> "Ä°stanbul". encoding="utf-8-sig" bu işareti ekler.
      Python ve Power BI bu işareti sorunsuz okur.

    NEDEN noktalı virgül?
      Türkçe bölge ayarlı Windows'ta ondalık ayırıcı VİRGÜLDÜR (12,5). Bu yüzden
      Excel CSV'de sütun ayırıcı olarak ";" bekler. Virgüllü CSV'ye çift
      tıklayınca tüm satır tek sütunda görünebilir. İki seçenek:
        a) Excel > Veri > Metinden/CSV'den ile içe aktarıp ayırıcıyı seçmek
        b) Dosyayı ";" ayırıcıyla yazmak (aşağıda ikinci dosya)

NASIL ÇALIŞTIRILIR?
    python gun03/11_csv_filtrele_yaz.py

BEKLENEN ÇIKTI:
    Filtre: Ankara + İnternet Hızı
    Seçilen satır: ...
    Yazıldı: outputs/gun03/ankara_internet_hizi.csv
    Yazıldı: outputs/gun03/ankara_internet_hizi_excel_tr.csv
    Geri okunan satır: ... (başlık hariç)
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cikti = ROOT / "outputs" / "gun03"
cikti.mkdir(parents=True, exist_ok=True)

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

# ---------------------------------------------------------------------------
# 1) Filtre (Excel: Otomatik Filtre -> il = Ankara VE kategori = İnternet Hızı)
# ---------------------------------------------------------------------------
IL = "Ankara"
KATEGORI = "İnternet Hızı"
secilenler = []
for kayit in kayitlar:
    if kayit["il"] == IL and kayit["kategori"] == KATEGORI:
        secilenler.append(kayit)
print(f"Filtre: {IL} + {KATEGORI}")
print("Seçilen satır:", len(secilenler))

# ---------------------------------------------------------------------------
# 2) Standart CSV (virgül + utf-8-sig): Python, Power BI ve içe aktarma için
# ---------------------------------------------------------------------------
dosya1 = cikti / "ankara_internet_hizi.csv"
# newline="" yazmazsak Windows'ta satırlar arasında BOŞ SATIR oluşur (klasik hata).
with open(dosya1, "w", encoding="utf-8-sig", newline="") as f:
    yazici = csv.DictWriter(f, fieldnames=list(kayitlar[0].keys()))
    yazici.writeheader()             # başlık satırı
    yazici.writerows(secilenler)     # tüm seçili satırlar
print("Yazıldı:", dosya1.relative_to(ROOT).as_posix())

# ---------------------------------------------------------------------------
# 3) Türkçe Excel'de çift tıklayınca düzgün açılan sürüm (";" ve ondalık virgül)
# ---------------------------------------------------------------------------
# Sadece bazı sütunları alalım (Excel'de sütun gizlemek / seçmek gibi).
sutunlar = ["sikayet_no", "tarih", "operator", "durum", "cozum_suresi_gun", "itiraz_tutari_tl"]
dosya2 = cikti / "ankara_internet_hizi_excel_tr.csv"
with open(dosya2, "w", encoding="utf-8-sig", newline="") as f:
    # extrasaction="ignore": sözlükte olup fieldnames'te olmayan sütunları sessizce atla
    yazici = csv.DictWriter(f, fieldnames=sutunlar, delimiter=";", extrasaction="ignore")
    yazici.writeheader()
    for kayit in secilenler:
        satir = dict(kayit)                       # orijinali bozmamak için kopya
        # 2404.26 -> 2404,26 (Türkçe Excel sayıyı ancak böyle sayı olarak tanır)
        satir["itiraz_tutari_tl"] = satir["itiraz_tutari_tl"].replace(".", ",")
        yazici.writerow(satir)
print("Yazıldı:", dosya2.relative_to(ROOT).as_posix())

# ---------------------------------------------------------------------------
# 4) Kontrol: yazdığımız dosyayı geri okuyalım. Satır sayısı tutuyor mu?
# ---------------------------------------------------------------------------
# utf-8-sig ile yazılan dosyayı utf-8-sig ile okumak, BOM'un ilk sütun adına
# yapışmasını ("﻿sikayet_no") engeller.
with open(dosya1, encoding="utf-8-sig", newline="") as f:
    geri = list(csv.DictReader(f))
print("Geri okunan satır:", len(geri), "(başlık hariç)")
print("İlk sütun adı:", list(geri[0].keys())[0])
# Excel uyarısı: Dosya Excel'de AÇIKKEN bu scripti tekrar çalıştırırsanız
# Windows "PermissionError: [Errno 13] Permission denied" verir. Excel'i kapatın.
