# -*- coding: utf-8 -*-
"""Veri tipleri ve tür dönüşümü: int, float, str, bool, None, type().

Ne öğretiyor:
    - Beş temel tip ve type() ile bir değerin tipini sorma.
    - Dosyadan/Excel'den gelen her şey önce METİNDİR; hesaptan önce dönüştürülür.
    - int(), float(), str(), bool() dönüşümleri ve tuzakları
      (Türkçe ondalık virgül, "3.7"i int'e çevirme, boş metin).
    - float'ın küçük yuvarlama farkı ve round().

Excel karşılığı:
    Excel'de "metin olarak saklanmış sayı" uyarısı (hücre köşesindeki yeşil
    üçgen) aynı sorundur: "12" metni ile 12 sayısı toplanınca beklenmedik
    sonuç çıkar. Python'da SAYIYADÖNÜŞTÜR / DEĞER() yerine int() / float().

Nasıl çalıştırılır:
    py gun01/08_tur_donusumu.py

Beklenen çıktı (son satır):
    Tür dönüşümü örnekleri bitti.
"""

# ---------------------------------------------------------------------------
# 1) BEŞ TEMEL TİP
# ---------------------------------------------------------------------------
sikayet_no = 10507              # int   : tam sayı (kimlik, adet)
indirme_mbps = 87.4             # float : ondalıklı sayı; ONDALIK AYRACI NOKTA
il = "İstanbul"                 # str   : metin; tek veya çift tırnak
cozuldu_mu = True               # bool  : True / False (büyük harfle başlar!)
memnuniyet = None               # None  : "değer yok / henüz bilinmiyor"
                                #         (Excel'de boş hücre gibi; 0 DEĞİL)

print("sikayet_no  ->", type(sikayet_no).__name__)
print("indirme_mbps->", type(indirme_mbps).__name__)
print("il          ->", type(il).__name__)
print("cozuldu_mu  ->", type(cozuldu_mu).__name__)
print("memnuniyet  ->", type(memnuniyet).__name__)
print()

# ---------------------------------------------------------------------------
# 2) METİN Mİ SAYI MI?
# ---------------------------------------------------------------------------
# CSV dosyasından okunan "12" bir METİNDİR. Metinde + birleştirme yapar:
print('"12" + "8"  =', "12" + "8")        # 128  (yan yana yapıştırdı)
print(' 12 +  8    =', 12 + 8)            # 20   (topladı)
print('int("12") + int("8") =', int("12") + int("8"))
print()

# ---------------------------------------------------------------------------
# 3) DÖNÜŞÜM FONKSİYONLARI
# ---------------------------------------------------------------------------
print('float("87.4")   =', float("87.4"))
print('int(87.9)       =', int(87.9), " <- yuvarlamaz, ondalığı KESER")
print('round(87.9)     =', round(87.9), " <- yuvarlar")
print('str(36) + " adet" =', str(36) + " adet")

# TUZAK 1: Türkçe ondalık virgül. float("12,5") HATA verir.
# Önce virgülü noktaya çeviririz (.replace metin işlemidir, 10. dosyada):
ham_deger = "12,5"
duzeltilmis = float(ham_deger.replace(",", "."))
print('"12,5" -> virgül noktaya çevrilince ->', duzeltilmis)

# TUZAK 2: int("3.7") HATA verir; önce float sonra int:
print('int(float("3.7")) =', int(float("3.7")))

# TUZAK 3: boş metin "" sayıya çevrilemez (İşlemde olan şikâyetin süresi boştur).
# Bu durumu Gün 2'de if ile, Gün 3'te try/except ile ele alacağız.
print()

# ---------------------------------------------------------------------------
# 4) bool(): Python neyi "boş/yanlış" sayar?
# ---------------------------------------------------------------------------
# 0, 0.0, "" (boş metin) ve None -> False. Diğer hemen her şey -> True.
print("bool(0) =", bool(0), "| bool(5) =", bool(5))
print('bool("") =', bool(""), '| bool("Ankara") =', bool("Ankara"))
print("bool(None) =", bool(None))
# DİKKAT: bool("False") True'dur! Çünkü boş olmayan bir metin.
print('bool("False") =', bool("False"), " <- metin dolu olduğu için True")
print()

# ---------------------------------------------------------------------------
# 5) FLOAT'IN KÜÇÜK SÜRPRİZİ
# ---------------------------------------------------------------------------
# Bilgisayar ondalıkları ikili sistemde tutar; bazı sayılar tam ifade edilemez.
# Excel de aynı şeyi yapar ama ekranda yuvarlayarak gizler.
print("0.1 + 0.2 =", 0.1 + 0.2)
print("round(0.1 + 0.2, 2) =", round(0.1 + 0.2, 2))
# Para hesabında sonucu gösterirken yuvarlayın (f-string ile: 10. dosya).
print("Tür dönüşümü örnekleri bitti.")
