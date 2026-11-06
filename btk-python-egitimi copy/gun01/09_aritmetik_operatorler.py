# -*- coding: utf-8 -*-
"""Aritmetik operatörler ve işlem önceliği.

Ne öğretiyor:
    + - * /  (Excel ile aynı)
    //  tam bölüm (Excel: BÖLÜM)        %  kalan (Excel: MOD)
    **  üs alma (Excel: ^ veya KUVVET)
    İşlem önceliği: parantez > ** > * / // % > + -
    Kısaltılmış atama: +=, -=, *=

Nasıl çalıştırılır:
    py gun01/09_aritmetik_operatorler.py

Beklenen çıktı (seçme satırlar):
    17 / 5  = 3.4
    17 // 5 = 3
    17 % 5  = 2
    150 dakika = 2 saat 30 dakika
"""

a = 17
b = 5

# ---------------------------------------------------------------------------
# 1) TEMEL OPERATÖRLER
# ---------------------------------------------------------------------------
print("17 + 5  =", a + b)
print("17 - 5  =", a - b)
print("17 * 5  =", a * b)
print("17 / 5  =", a / b)     # / HER ZAMAN float verir: 10 / 2 = 5.0
print("17 // 5 =", a // b)    # tam bölüm: kaç TAM kere sığar?
print("17 % 5  =", a % b)     # kalan: geriye ne kalır?
print("2 ** 10 =", 2 ** 10)   # üs: 2 üzeri 10 = 1024
print("10 / 2  =", 10 / 2, " <- sonuç tam olsa bile float")
print()

# ---------------------------------------------------------------------------
# 2) // ve % NEREDE İŞE YARAR? — gerçek örnekler
# ---------------------------------------------------------------------------
# Çağrı merkezi görüşme süresi dakika olarak tutuluyor; saat:dakika gösterelim.
toplam_dakika = 150
saat = toplam_dakika // 60      # 150 içinde kaç tam saat var? -> 2
dakika = toplam_dakika % 60     # geriye kalan dakika        -> 30
print(toplam_dakika, "dakika =", saat, "saat", dakika, "dakika")

# 23 şikâyet, her personele 5'er dosya veriliyor. Kaç personele tam pay düşer,
# kaç dosya açıkta kalır?
dosya, kisi_basi = 23, 5
print("Tam paket:", dosya // kisi_basi, "| Artan dosya:", dosya % kisi_basi)

# % ile çift/tek kontrolü: sayı % 2 == 0 ise çifttir (Gün 2'de if ile).
print("10 % 2 =", 10 % 2, "-> çift;  7 % 2 =", 7 % 2, "-> tek")
print()

# ---------------------------------------------------------------------------
# 3) İŞLEM ÖNCELİĞİ — Excel ile aynı mantık
# ---------------------------------------------------------------------------
# Önce parantez, sonra üs, sonra çarpma/bölme, en son toplama/çıkarma.
# Aynı seviyedekiler soldan sağa yapılır.
print("2 + 3 * 4     =", 2 + 3 * 4)       # 14  (önce 3*4)
print("(2 + 3) * 4   =", (2 + 3) * 4)     # 20
print("2 * 3 ** 2    =", 2 * 3 ** 2)      # 18  (önce 3**2 = 9)
print("-2 ** 2       =", -2 ** 2)         # -4 ! (önce 2**2, sonra eksi)
print("(-2) ** 2     =", (-2) ** 2)       # 4
print("100 / 10 / 2  =", 100 / 10 / 2)    # 5.0 (soldan sağa)

# Sık hata: ortalama hesabında parantezi unutmak.
x, y, z = 4, 6, 8
yanlis = x + y + z / 3          # sadece z bölündü -> 12.666...
dogru = (x + y + z) / 3         # 6.0
print("Parantezsiz ortalama (YANLIŞ):", round(yanlis, 2))
print("Parantezli ortalama (DOĞRU)  :", dogru)
print()

# ---------------------------------------------------------------------------
# 4) KISALTILMIŞ ATAMA
# ---------------------------------------------------------------------------
sayac = 0
sayac += 1       # sayac = sayac + 1 ile aynı
sayac += 1
print("Sayaç iki kez arttı:", sayac)
bakiye = 500
bakiye -= 120    # bakiye = bakiye - 120
print("Bakiye:", bakiye)
