# -*- coding: utf-8 -*-
"""Karşılaştırma ve mantıksal operatörler: sonucu her zaman True / False.

Ne öğretiyor:
    ==  eşit mi?          !=  farklı mı?
    >  <  >=  <=          büyük / küçük
    and  (VE)  -> ikisi de doğruysa True
    or   (VEYA)-> en az biri doğruysa True
    not  (DEĞİL)-> tersine çevirir
    in   -> içinde var mı?   ve  zincirleme: 3 <= x <= 7

Excel karşılığı:
    =B2>10 hücresi DOĞRU/YANLIŞ döner; Python'da True/False.
    VE(...)  -> and      YADA(...) -> or      DEĞİL(...) -> not
    Excel'de eşitlik "=" ile, Python'da ÇİFT "==" ile sorulur.
    Tek "=" Python'da ATAMADIR (kutuya değer koy), soru değildir!

Nasıl çalıştırılır:
    py gun02/05_karsilastirma_mantiksal.py

Beklenen çıktı (son satır):
    Karşılaştırma örnekleri bitti.
"""

sure = 12            # şikâyetin çözüm süresi (gün)
hedef = 10           # kategori için hedef süre (gün)
kategori = "Fatura"
durum = "Çözüldü"

# ---------------------------------------------------------------------------
# 1) KARŞILAŞTIRMA: sonuç bool (True/False)
# ---------------------------------------------------------------------------
print("sure > hedef   :", sure > hedef)      # True
print("sure < hedef   :", sure < hedef)      # False
print("sure >= 12     :", sure >= 12)        # True  (eşit de sayılır)
print("sure == hedef  :", sure == hedef)     # False
print("sure != hedef  :", sure != hedef)     # True
# Sonucu bir değişkende saklayabiliriz (Excel'de yardımcı sütun gibi):
hedef_asildi = sure > hedef
print("hedef_asildi değişkeni:", hedef_asildi, type(hedef_asildi).__name__)
print()

# ---------------------------------------------------------------------------
# 2) METİN KARŞILAŞTIRMA: harfi harfine!
# ---------------------------------------------------------------------------
print('kategori == "Fatura" :', kategori == "Fatura")    # True
print('kategori == "fatura" :', kategori == "fatura")    # False (küçük f)
print('"Fatura " == "Fatura":', "Fatura " == "Fatura")   # False (sonda boşluk!)
# Çözüm: önce temizle -> .strip(). Gün 5'te kirli veride bunu çok yapacağız.
print('"Fatura ".strip() == "Fatura":', "Fatura ".strip() == "Fatura")
# Sayı ile metin: 10 == "10" -> False (farklı türler)
print('10 == "10" :', 10 == "10")
print()

# ---------------------------------------------------------------------------
# 3) and / or / not
# ---------------------------------------------------------------------------
# DOĞRULUK TABLOSU
#   A      B      A and B   A or B
#   True   True   True      True
#   True   False  False     True
#   False  True   False     True
#   False  False  False     False
cozuldu = durum == "Çözüldü"
print("Çözüldü VE hedef aşıldı  :", cozuldu and sure > hedef)          # True
print("Fatura VEYA Kesinti      :", kategori == "Fatura" or kategori == "Kesinti")
print("Çözülmedi mi? (not)      :", not cozuldu)                        # False
# Öncelik: not > and > or. Karışık ifadede PARANTEZ kullanın, okuyan rahat etsin:
print("Parantezli birleşik koşul:", (kategori == "Fatura" or kategori == "Kesinti") and sure > hedef)
print()

# ---------------------------------------------------------------------------
# 4) in: "listede/metinde var mı?"  (Excel: EĞERSAY(...)>0 ya da BUL)
# ---------------------------------------------------------------------------
oncelikli_kategoriler = ["Kesinti", "Kapsama"]
print('"Kesinti" in liste :', "Kesinti" in oncelikli_kategoriler)
print('kategori in liste  :', kategori in oncelikli_kategoriler)
print('"Fat" in "Fatura"  :', "Fat" in "Fatura")
print('not in örneği      :', kategori not in oncelikli_kategoriler)
print()

# ---------------------------------------------------------------------------
# 5) ZİNCİRLEME KARŞILAŞTIRMA (Python'a özgü, çok okunaklı)
# ---------------------------------------------------------------------------
memnuniyet = 3
# Excel: =VE(B2>=3; B2<=5)     Python: 3 <= memnuniyet <= 5
print("Memnuniyet 3-5 arası mı? :", 3 <= memnuniyet <= 5)
print("Memnuniyet 1-2 arası mı? :", 1 <= memnuniyet <= 2)
print("Karşılaştırma örnekleri bitti.")
