# -*- coding: utf-8 -*-
"""Değişken ve adlandırma kuralları (PEP 8'in kısa özeti).

Ne öğretiyor:
    - Değişken = bir değere verilen isim (Excel'de "Ad Tanımla" ile hücreye
      isim vermek gibi: =B2*KDV yerine =tutar*kdv_orani).
    - Zorunlu kurallar (uyulmazsa hata) ve önerilen stil (PEP 8).
    - Neden değişken adlarında Türkçe karakter kullanmıyoruz.
    - Çoklu atama ve değer değiş tokuşu.

Nasıl çalıştırılır:
    py gun01/07_degiskenler_ve_adlandirma.py      (Windows)
    python3 gun01/07_degiskenler_ve_adlandirma.py (macOS)

Beklenen çıktı (son satır):
    Toplam tutar: 1200.0 TL
"""
import keyword  # Python'un ayrılmış kelimelerinin listesini verir

# ---------------------------------------------------------------------------
# ZORUNLU KURALLAR — uyulmazsa SyntaxError
# ---------------------------------------------------------------------------
# 1) Harf veya alt çizgi (_) ile başlar; RAKAMLA BAŞLAYAMAZ.
#       2026_sikayet = 5     -> HATA
#       sikayet_2026 = 5     -> doğru
# 2) Boşluk içeremez:   sikayet sayisi = 5   -> HATA;  sikayet_sayisi -> doğru
# 3) Tire (-) kullanılamaz (çıkarma sanılır):  il-adi -> HATA
# 4) Büyük/küçük harf farklıdır: Il, il, IL üç ayrı değişkendir.
# 5) Python'un ayrılmış kelimeleri ad olamaz: if, for, class, None ...
print("Ayrılmış kelime sayısı:", len(keyword.kwlist))
print("Örnekler:", keyword.kwlist[:6])

# ---------------------------------------------------------------------------
# ÖNERİLEN STİL (PEP 8) — uyulmazsa çalışır ama okunması zorlaşır
# ---------------------------------------------------------------------------
# - Değişkenler küçük harf, kelimeler alt çizgiyle: cozum_suresi_gun
#   (buna "snake_case" denir)
# - Değişmeyecek sabitler BÜYÜK harf: KDV_ORANI = 0.20
# - Anlamlı ad: x, a1, deger2 yerine paket_hizi_mbps
# - Tek harfli adlar sadece çok kısa döngülerde (i, j) kabul edilir.
KDV_ORANI = 0.20
paket_ucreti_tl = 1000
print("Sabit KDV_ORANI:", KDV_ORANI)

# ---------------------------------------------------------------------------
# TÜRKÇE KARAKTER: teknik olarak ÇALIŞIR ama KULLANMIYORUZ
# ---------------------------------------------------------------------------
# Python 3 değişken adında ş, ğ, ı, ç, ö, ü kabul eder:
#     şikâyet_sayısı = 5    # çalışır
# Neden önermiyoruz?
#   - Farklı klavyeden "ı" ile "i" karışır; hatayı bulmak zorlaşır
#     (sikayet_sayısı ile sikayet_sayisi Python için İKİ AYRI addır).
#   - Bazı eski araçlar/editörler bozuk gösterebilir.
#   - Kurum dışındaki yazılımcılarla paylaşırken sorun olur.
# Kural: ADLAR Türkçe ama ASCII (sikayet_sayisi); METİNLER tam Türkçe ("Şikâyet").
sikayet_sayisi = 5
print("Değişken adı ASCII, metin Türkçe -> Şikâyet sayısı:", sikayet_sayisi)

# ---------------------------------------------------------------------------
# ÇOKLU ATAMA ve DEĞİŞ TOKUŞ
# ---------------------------------------------------------------------------
il, operator_adi, sure = "Ankara", "Operatör A", 4   # sırayla eşleşir
print("Çoklu atama:", il, operator_adi, sure)

eski, yeni = 10, 20
eski, yeni = yeni, eski        # C'de geçici değişken gerekirdi; Python'da tek satır
print("Değiş tokuş sonrası eski =", eski, "yeni =", yeni)

# ---------------------------------------------------------------------------
# DEĞİŞKEN BİR "FORMÜL" DEĞİLDİR
# ---------------------------------------------------------------------------
# Excel'de B3 = B1 + B2 yazarsanız B1 değişince B3 de değişir.
# Python'da atama O ANDAKİ değeri hesaplar ve saklar; sonra kendiliğinden güncellenmez.
kdv_tutari = paket_ucreti_tl * KDV_ORANI
paket_ucreti_tl = 2000                 # kdv_tutari HÂLÂ 200.0
print("Ücret değişti ama kdv_tutari güncellenmedi:", kdv_tutari)
paket_ucreti_tl = 1000                 # geri alalım

toplam_tutar = paket_ucreti_tl + paket_ucreti_tl * KDV_ORANI
print("Toplam tutar:", toplam_tutar, "TL")
