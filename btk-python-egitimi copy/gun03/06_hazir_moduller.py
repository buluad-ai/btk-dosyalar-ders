# -*- coding: utf-8 -*-
"""Hazır modüller (standart kütüphane): math, statistics, random, datetime, pathlib.

NE ÖĞRETİYOR?
    Python kurulumuyla birlikte gelen yüzlerce hazır modül vardır ("standart kütüphane").
    Bunlar için pip / internet / IT izni GEREKMEZ. import yazmak yeterlidir.
    Excel benzetmesi: Excel'in hazır fonksiyon kategorileri (Matematik, İstatistik,
    Tarih-Saat...). import = "bu kategoriyi bu dosyada kullanacağım" demek.

    Üç import yazım şekli:
        import math                       -> math.ceil(...) diye kullanılır
        from statistics import median     -> doğrudan median(...) diye kullanılır
        import datetime as dt             -> kısa takma adla: dt.date(...)

NASIL ÇALIŞTIRILIR?
    python gun03/06_hazir_moduller.py

BEKLENEN ÇIKTI (kısaltılmış):
    Gereken sayfa: 13
    Ortalama: 8
    Medyan: 9.0
    ...
    data klasöründeki CSV dosyaları: ['basvurular.csv', 'hiz_olcumleri.csv', ...]
"""
import math
import random
import statistics
from statistics import median          # sadece bir fonksiyonu almak
import datetime as dt                   # takma adla almak
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# math: matematik fonksiyonları
# ---------------------------------------------------------------------------
# 600 şikâyet var, bir rapor sayfasına 50 satır sığıyor: kaç sayfa gerekir?
# 600 / 50 = 12 ama 610 olsaydı 12.2 -> 13 sayfa gerekir: YUKARI yuvarlama.
print("Gereken sayfa:", math.ceil(610 / 50))   # Excel: =TAVANA.YUVARLA / YUKARIYUVARLA
print("Aşağı yuvarlama:", math.floor(12.9))     # Excel: =AŞAĞIYUVARLA(12,9;0)
print("Karekök 144:", math.sqrt(144))

# DİKKAT: Python'un round() fonksiyonu "bankacı yuvarlaması" yapar:
# round(2.5) -> 2, round(3.5) -> 4 (yarımları çift sayıya yuvarlar).
# Excel'in YUVARLA fonksiyonu 2,5'i 3 yapar. Raporda fark görürseniz sebebi budur.
print("round(2.5) =", round(2.5), "| round(3.5) =", round(3.5))

# ---------------------------------------------------------------------------
# statistics: istatistik fonksiyonları (istatistikçiler için tanıdık)
# ---------------------------------------------------------------------------
cozum_sureleri = [7, 10, 3, 8, 11, 2, 13, 10]        # gün
print("Ortalama:", statistics.mean(cozum_sureleri))      # Excel: =ORTALAMA
# Not: Tam sayıların ortalaması tam çıkarsa mean "8" yazar (8.0 değil); 7.8 gibi ise ondalık verir.
# Medyan: sıralı listenin ortası. 8 eleman var -> ortadaki iki değerin (8 ve 10) ortalaması = 9.0
print("Medyan:", median(cozum_sureleri))                 # Excel: =ORTANCA
print("En sık değer (mod):", statistics.mode(cozum_sureleri))   # Excel: =ENÇOK_OLAN
# stdev = ÖRNEKLEM standart sapması (Excel: =STDSAPMA.S); pstdev = ana kütle (STDSAPMA.P)
print("Std. sapma (örneklem):", round(statistics.stdev(cozum_sureleri), 2))
print("Çeyrekler (Q1, Q2, Q3):", statistics.quantiles(cozum_sureleri, n=4))
# statistics.mean([]) -> StatisticsError verir: boş liste kontrolünü unutmayın.

# ---------------------------------------------------------------------------
# random: rastgele seçim (denetim örneklemi). SEED ile tekrar üretilebilir.
# ---------------------------------------------------------------------------
# Denetçi 600 şikâyetten rastgele 5 tanesini kontrol etmek istiyor.
# random.seed(42) -> "zar"ı aynı yerden başlatır: herkes aynı 5 kaydı görür.
# seed olmasaydı her çalıştırmada farklı kayıtlar gelirdi (Excel: =RASTGELE()
# her F9'da değişir gibi). Raporların tekrar üretilebilir olması için seed şart.
random.seed(42)
sikayet_numaralari = list(range(10001, 10601))
orneklem = random.sample(sikayet_numaralari, 5)
print("Denetim örneklemi (seed=42):", sorted(orneklem))

# ---------------------------------------------------------------------------
# datetime: tarih (ayrıntısı 08_tarihler.py'de)
# ---------------------------------------------------------------------------
basvuru = dt.date(2026, 3, 2)
sonuc = dt.date(2026, 3, 16)
print("Geçen gün:", (sonuc - basvuru).days)      # Excel: =B2-A2

# ---------------------------------------------------------------------------
# pathlib: dosya ve klasör yolları
# ---------------------------------------------------------------------------
# Path ile "/" işareti yolları birleştirir; Windows'ta da doğru çalışır
# (Windows \ kullanır ama Path bunu bizim yerimize halleder).
veri_klasoru = ROOT / "data"
sikayet_dosyasi = veri_klasoru / "sikayetler.csv"
print("Dosya var mı?", sikayet_dosyasi.exists())
print("Dosya adı:", sikayet_dosyasi.name, "| uzantı:", sikayet_dosyasi.suffix,
      "| uzantısız ad:", sikayet_dosyasi.stem)
# glob("*.csv"): klasördeki .csv ile biten tüm dosyalar (Windows'taki *.csv araması gibi)
csv_dosyalari = sorted(p.name for p in veri_klasoru.glob("*.csv"))
print("data klasöründeki CSV dosyaları:", csv_dosyalari)
