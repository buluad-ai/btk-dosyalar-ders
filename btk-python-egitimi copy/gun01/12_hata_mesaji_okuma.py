# -*- coding: utf-8 -*-
"""Hata mesajı (Traceback) nasıl okunur? Kasıtlı hatalar, güvenli gösterim.

Ne öğretiyor:
    - Kırmızı hata metni "bilgisayar bozuldu" demek değildir; Python size
      NEREDE ve NE olduğunu söyler.
    - Traceback'i AŞAĞIDAN YUKARIYA okumak:
        1. EN ALT satır: hatanın TÜRÜ ve açıklaması (ör. NameError: ...)
        2. Hemen üstü : hatalı KOD satırı (ve ^^^^ işaretleri)
        3. Onun üstü  : File "...", line 12  -> hangi dosya, kaçıncı satır
    - En sık 6 hata: SyntaxError, IndentationError, NameError, TypeError,
      ValueError, ZeroDivisionError.

Bu dosya NEDEN çökmüyor?
    Her hatalı kod parçası önce YORUM olarak gösterilir, sonra try/except
    içinde çalıştırılıp hata "yakalanır" ve açıklanır. try/except bugün
    ezberlenmez; ayrıntısı Gün 3. Dosya baştan sona çalışır (çıkış kodu 0).

Nasıl çalıştırılır:
    py gun01/12_hata_mesaji_okuma.py

Beklenen çıktı (son satır):
    Hata okuma turu bitti: 6 hata türü görüldü.
"""
import traceback  # hata metnini (traceback) yazdırmak için hazır modül

# ---------------------------------------------------------------------------
# 0) GERÇEK BİR TRACEBACK NASIL GÖRÜNÜR?
# ---------------------------------------------------------------------------
# Aşağıdaki iki satırı YENİ bir dosyaya (ör. deneme.py) yazıp çalıştırırsanız:
#
#     il = "Ankara"
#     print(Il)
#
# terminalde şuna benzer bir metin görürsünüz:
#
#     Traceback (most recent call last):            <- "hata izi başlıyor"
#       File "C:\Users\ali\btk\deneme.py", line 2, in <module>   <- DOSYA + SATIR
#         print(Il)                                 <- HATALI SATIR
#               ^^                                  <- tam yer
#     NameError: name 'Il' is not defined. Did you mean: 'il'?   <- TÜR + AÇIKLAMA
#
# Okuma sırası: EN ALTTAN başlayın. "NameError: 'Il' tanımlı değil, 'il' mi
# demek istediniz?" -> Python büyük/küçük harf ayırır. Sonra "line 2"ye gidin.
#
# Aynı hatayı burada güvenli biçimde üretip, Python'un ürettiği gerçek
# traceback metnini ekrana basıyoruz:
il = "Ankara"
print("=== 0) Gerçek bir traceback örneği ===")
try:
    print(Il)  # noqa: F821  -> kasıtlı hata: 'Il' diye bir değişken yok
except NameError:
    print(traceback.format_exc())
# Not: Dosya yolu ve satır numarası sizin bilgisayarınızda farklı görünür.

hata_sayisi = 0  # gördüğümüz hata türlerini sayacağız


def acikla(hata, ne_oldu, cozum):
    """Yakalanan hatanın türünü, mesajını ve çözüm önerisini yazar.

    (def = fonksiyon tanımı; Gün 3'te öğreneceğiz. Şimdilik "tekrar eden
    print'leri tek isimle çağırma kısayolu" diye düşünün.)
    """
    print(f"  Python dedi : {type(hata).__name__}: {hata}")
    print(f"  Ne oldu     : {ne_oldu}")
    print(f"  Çözüm       : {cozum}")
    print()


# ---------------------------------------------------------------------------
# 1) SyntaxError — yazım (dilbilgisi) hatası; program HİÇ başlamaz
# ---------------------------------------------------------------------------
#     print("Merhaba"        <- kapanmayan parantez
# SyntaxError dosya ÇALIŞMADAN önce yakalanır; o yüzden onu doğrudan bu
# dosyaya yazamayız (bütün dosya çalışmaz). compile() ile bir METNİ
# derletip hatayı güvenle görüyoruz:
print("=== 1) SyntaxError ===")
try:
    compile('print("Merhaba"', "<ornek>", "exec")
except SyntaxError as hata:
    acikla(hata, "Açılan parantez kapanmamış.",
           "Parantez, tırnak ve iki noktayı (:) çiftler hâlinde kontrol edin.")
    hata_sayisi += 1

# ---------------------------------------------------------------------------
# 2) IndentationError — girinti hatası (SyntaxError'un özel bir türü)
# ---------------------------------------------------------------------------
#     if sure > 5:
#     print("Gecikmeli")     <- if bloğu girintisiz
print("=== 2) IndentationError ===")
try:
    compile('sure = 8\nif sure > 5:\nprint("Gecikmeli")\n', "<ornek>", "exec")
except IndentationError as hata:
    acikla(hata, "if satırından sonra gelen satır içeri itilmemiş.",
           "Bloktaki satırların başına 4 boşluk koyun (Tab tuşu VS Code'da 4 boşluk yapar).")
    hata_sayisi += 1

# ---------------------------------------------------------------------------
# 3) NameError — tanımlanmamış ad (yazım hatası ya da sıra hatası)
# ---------------------------------------------------------------------------
#     toplam = adet * birim_fiyat     <- birim_fiyat daha önce tanımlanmamış
print("=== 3) NameError ===")
adet = 3
try:
    toplam = adet * birim_fiyat  # noqa: F821
except NameError as hata:
    acikla(hata, "birim_fiyat bu satırdan ÖNCE tanımlanmamış.",
           "Adın yazımını kontrol edin; değişkeni kullanmadan önce tanımlayın.")
    hata_sayisi += 1

# ---------------------------------------------------------------------------
# 4) TypeError — tür uyuşmazlığı
# ---------------------------------------------------------------------------
#     sonuc = "5" + 3          <- metin + sayı
print("=== 4) TypeError ===")
try:
    sonuc = "5" + 3
except TypeError as hata:
    acikla(hata, "Metin ile sayı toplanamaz.",
           'Sayı istiyorsanız int("5") + 3; metin istiyorsanız "5" + str(3).')
    hata_sayisi += 1

# ---------------------------------------------------------------------------
# 5) ValueError — tür doğru ama DEĞER uygun değil
# ---------------------------------------------------------------------------
#     hiz = float("87,4")      <- Türkçe ondalık virgül
print("=== 5) ValueError ===")
try:
    hiz = float("87,4")
except ValueError as hata:
    acikla(hata, "Python ondalık ayracı olarak nokta bekler.",
           'float("87,4".replace(",", ".")) kullanın.')
    hata_sayisi += 1

# ---------------------------------------------------------------------------
# 6) ZeroDivisionError — sıfıra bölme
# ---------------------------------------------------------------------------
#     ortalama = toplam_sure / kayit_sayisi    <- kayit_sayisi = 0
print("=== 6) ZeroDivisionError ===")
toplam_sure = 0
kayit_sayisi = 0
try:
    ortalama = toplam_sure / kayit_sayisi
except ZeroDivisionError as hata:
    acikla(hata, "Hiç kayıt yokken ortalama alınmaya çalışıldı.",
           "Bölmeden önce kayıt sayısının 0 olup olmadığını kontrol edin (Gün 2: if).")
    hata_sayisi += 1

# ---------------------------------------------------------------------------
# HATA AYIKLAMA KONTROL LİSTESİ (sınıf duvarına asılabilir)
# ---------------------------------------------------------------------------
# 1. Dosyayı KAYDETTİM mi? (VS Code sekmesinde beyaz nokta = kaydedilmemiş)
# 2. Traceback'in EN ALT satırını okudum mu?
# 3. "line X"teki satıra gittim mi? (Hata bazen bir ÜST satırdadır:
#    kapanmamış parantez bir sonraki satırda fark edilir.)
# 4. Adı doğru mu yazdım? (büyük/küçük harf, ı/i)
# 5. Hâlâ çözülmediyse: hata metnini kopyalayıp eğitmene yazılı iletin.
print(f"Hata okuma turu bitti: {hata_sayisi} hata türü görüldü.")
