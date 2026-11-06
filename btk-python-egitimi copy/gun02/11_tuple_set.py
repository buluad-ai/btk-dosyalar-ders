# -*- coding: utf-8 -*-
"""Tuple (değişmez sıralı değerler) ve set (küme: tekrarsız değerler).

Ne öğretiyor:
    tuple: (a, b, c) — oluşturulduktan sonra DEĞİŞTİRİLEMEZ.
           Sabit kayıtlar ve "birden çok değeri birlikte taşıma" için.
           Açma (unpacking): il, adet = ("Ankara", 3)
    set  : {a, b, c} — her değer BİR KEZ bulunur, SIRASI YOKTUR.
           Tekil iller, "var mı?" sorusu, iki listeyi karşılaştırma.

Excel karşılığı:
    set(iller)         -> Veri > Yinelenenleri Kaldır  /  BENZERSİZ()
    len(set(iller))    -> "kaç farklı il var?"
    a & b (kesişim)    -> iki listede de olanlar (iki sütunda DÜŞEYARA ile bulunanlar)
    a - b (fark)       -> A'da olup B'de olmayanlar (DÜŞEYARA'da #YOK çıkanlar)

Nasıl çalıştırılır:
    py gun02/11_tuple_set.py

Beklenen çıktı (seçme satırlar):
    Tekil iller: ['Ankara', 'Antalya', 'Erzurum', 'Konya', 'İstanbul', 'İzmir']
    Farklı il sayısı: 6
"""

# ---------------------------------------------------------------------------
# 1) TUPLE
# ---------------------------------------------------------------------------
hedef_araligi = (1, 30)               # geçerli çözüm süresi aralığı (gün)
ankara_koordinat = (39.93, 32.86)     # enlem, boylam: birlikte anlamlı, değişmez
print("Aralık:", hedef_araligi, "| alt sınır:", hedef_araligi[0])

# Açma (unpacking): tuple'ın elemanlarını ayrı değişkenlere dağıtmak
enlem, boylam = ankara_koordinat
print(f"Ankara: enlem {enlem}, boylam {boylam}")

# Değiştirmeye çalışırsak:
#   hedef_araligi[0] = 0   -> TypeError: 'tuple' object does not support item assignment
# Bu bir ÖZELLİKTİR: yanlışlıkla değişmemesi gereken değerleri korur.

# Zaten kullandık! zip ve .items() her turda tuple verir:
il_sayim = {"İstanbul": 5, "Ankara": 3}
for cift in il_sayim.items():
    print("items() bir tuple verir:", cift, type(cift).__name__)
print()

# ---------------------------------------------------------------------------
# 2) SET — tekil değerler
# ---------------------------------------------------------------------------
iller = ["İstanbul", "Ankara", "Antalya", "Konya", "İstanbul", "İstanbul",
         "İzmir", "Erzurum", "Ankara", "Antalya", "İzmir", "Erzurum",
         "İstanbul", "İstanbul", "Ankara"]
tekil_iller = set(iller)
# set'in sırası yoktur; yazdırırken her çalıştırmada farklı sıra görebilirsiniz.
# Rapor için sorted() ile sıralı listeye çeviriyoruz:
print("Tekil iller:", sorted(tekil_iller))
print("Farklı il sayısı:", len(tekil_iller))
print("Toplam kayıt   :", len(iller), "(set tekrarları sildi; ADET bilgisi kayboldu!)")
print("Konya var mı?  :", "Konya" in tekil_iller)

# Boş küme: set()   ({} boş SÖZLÜKTÜR, küme değil!)
gorulen = set()
gorulen.add("Ankara")
gorulen.add("Ankara")         # ikinci ekleme etkisiz
print("İki kez eklendi, bir kez var:", gorulen)
print()

# ---------------------------------------------------------------------------
# 3) KÜME İŞLEMLERİ — iki dönemi karşılaştırma
# ---------------------------------------------------------------------------
ocak_illeri = {"İstanbul", "Ankara", "Antalya", "Konya"}
subat_illeri = {"İstanbul", "Ankara", "İzmir", "Erzurum"}
print("İki ayda da şikâyet olan (&) :", sorted(ocak_illeri & subat_illeri))
print("Herhangi bir ayda olan (|)   :", sorted(ocak_illeri | subat_illeri))
print("Sadece Ocak'ta olan (-)      :", sorted(ocak_illeri - subat_illeri))
print("Şubat'ta yeni çıkan (-)      :", sorted(subat_illeri - ocak_illeri))

# Not: sorted() Türkçe harfleri (İ, Ç, Ş...) sona koyar; o yüzden
# "İstanbul" ve "İzmir" listenin sonunda görünür.
