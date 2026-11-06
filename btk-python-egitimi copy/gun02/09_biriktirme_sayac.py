# -*- coding: utf-8 -*-
"""Biriktirme (toplam) ve sayaç kalıpları: TOPLA, EĞERSAY, ETOPLA, MAK'ı elle yazmak.

Ne öğretiyor:
    Neredeyse her analiz şu üç adımlı kalıptır:
        1. Döngüden ÖNCE başlangıç değeri ver    (toplam = 0, sayac = 0)
        2. Döngü İÇİNDE her elemanla güncelle    (toplam += sure)
        3. Döngüden SONRA sonucu kullan          (print, ortalama)
    sum/len/max hazır olsa da kalıbı bilmek; KOŞULLU toplam/sayım için şart.

Excel karşılığı:
    toplam    -> TOPLA(C:C)
    sayac     -> EĞERSAY(C:C;">10")
    kosullu   -> ETOPLA(B:B;"Fatura";C:C)   (SUMIF)
    en_buyuk  -> MAK(C:C)

Nasıl çalıştırılır:
    py gun02/09_biriktirme_sayac.py

Beklenen çıktı (seçme satırlar):
    Toplam süre: 79 gün
    10 günü aşan: 3 şikâyet
    Fatura şikâyetlerinin toplam süresi: 15 gün
    En uzun: 15 gün (sıra 6)
"""

sureler = [7, 10, 3, 8, 11, 15, 2, 2, 8, 13]
kategoriler = ["Kesinti", "Fatura", "Fatura", "İnternet Hızı", "Taahhüt/İptal",
               "Kapsama", "Numara Taşıma", "Fatura", "Numara Taşıma", "Taahhüt/İptal"]

# ---------------------------------------------------------------------------
# 1) TOPLAM (biriktirici)
# ---------------------------------------------------------------------------
toplam = 0                       # 1. adım: başlangıç
for sure in sureler:
    toplam += sure               # 2. adım: her turda ekle
    # print("ara toplam:", toplam)   # <- açıp her turu izleyin (Excel'de "kümülatif toplam" sütunu)
print("Toplam süre:", toplam, "gün")         # 3. adım: sonuç
print("Kontrol (hazır sum):", sum(sureler))   # aynı olmalı
print()

# ---------------------------------------------------------------------------
# 2) KOŞULLU SAYAÇ  (EĞERSAY / COUNTIF)
# ---------------------------------------------------------------------------
sayac = 0
for sure in sureler:
    if sure > 10:
        sayac += 1
print("10 günü aşan:", sayac, "şikâyet")
print(f"Oranı: {sayac / len(sureler):.0%}")
print()

# ---------------------------------------------------------------------------
# 3) KOŞULLU TOPLAM  (ETOPLA / SUMIF) — iki listeyi zip ile birlikte yürüt
# ---------------------------------------------------------------------------
fatura_toplam = 0
fatura_adet = 0
for kategori, sure in zip(kategoriler, sureler):
    if kategori == "Fatura":
        fatura_toplam += sure
        fatura_adet += 1
print("Fatura şikâyetlerinin toplam süresi:", fatura_toplam, "gün")
print(f"Fatura ortalaması (EĞERORTALAMA): {fatura_toplam / fatura_adet:.2f} gün")
print()

# ---------------------------------------------------------------------------
# 4) EN BÜYÜĞÜ ve YERİNİ bulmak  (MAK + KAÇINCI)
# ---------------------------------------------------------------------------
en_uzun = sureler[0]             # başlangıç: İLK eleman (0 değil! hepsi eksi olsaydı?)
en_uzun_sira = 1
for sira, sure in enumerate(sureler, start=1):
    if sure > en_uzun:
        en_uzun = sure
        en_uzun_sira = sira
print(f"En uzun: {en_uzun} gün (sıra {en_uzun_sira})")
print()

# ---------------------------------------------------------------------------
# 5) LİSTE BİRİKTİRME — filtrelenmiş yeni liste
# ---------------------------------------------------------------------------
kisa_sureler = []
for sure in sureler:
    if sure <= 3:
        kisa_sureler.append(sure)
print("3 gün ve altı:", kisa_sureler)

# SIK HATA: başlangıç değerini döngünün İÇİNE yazmak
#   for sure in sureler:
#       toplam = 0          <- her turda sıfırlanır!
#       toplam += sure
#   -> sonuç sadece son eleman (13) olur.
