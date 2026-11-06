# -*- coding: utf-8 -*-
"""Python nedir, nereden geldi, C'den farkı ne?

Ne öğretiyor:
    - Python'u kim, ne zaman yazdı; neden veri işlerinde bu kadar yaygın.
    - C ile dört temel fark: (1) derleme / yorumlama + bytecode,
      (2) statik / dinamik tip, (3) süslü parantez / girinti,
      (4) bellek yönetimi ve tam sayı sınırı.
    - C kodları YORUM olarak verilmiştir; çalıştırılmaz, sadece okunur.

Nasıl çalıştırılır:
    VS Code: dosyayı açın, sağ üstteki üçgen (Run Python File).
    Terminal (Windows):  py gun01/05_python_ve_c.py
    Terminal (macOS):    python3 gun01/05_python_ve_c.py

Beklenen çıktı (özet):
    Python 1991'de Guido van Rossum tarafından yayımlandı.
    ... dört farkın her biri için kısa satırlar ...
    Python ve C karşılaştırması bitti.
"""

# ---------------------------------------------------------------------------
# 1) KISA TARİHÇE
# ---------------------------------------------------------------------------
# Guido van Rossum, Hollanda'daki CWI araştırma merkezinde çalışırken
# Python'u geliştirdi; ilk kamuya açık sürüm Şubat 1991'de yayımlandı.
# Adı yılandan değil, İngiliz komedi grubu "Monty Python"dan gelir.
# Bugün Python Software Foundation (PSF) adlı vakıf tarafından yönetilir.
print("Python 1991'de Guido van Rossum tarafından yayımlandı.")

# Neden veri işlerinde popüler?
# - Okunması kolay: kod neredeyse İngilizce cümle gibi.
# - "Pil dahil" (batteries included): CSV, JSON, SQLite, istatistik
#   modülleri kurulum yapmadan gelir.
# - pandas, NumPy, Matplotlib gibi analiz kütüphaneleri çok olgun.
# - Excel'de elle yapılan tekrar eden işi bir kez yazıp her ay aynı
#   şekilde tekrar çalıştırabilirsiniz (makroya benzer ama daha güçlü).
print("Neden popüler: okunaklı, kütüphanesi zengin, tekrar çalıştırılabilir.")
print()

# ---------------------------------------------------------------------------
# 2) FARK 1 — DERLEME vs YORUMLAMA (+ bytecode)
# ---------------------------------------------------------------------------
# C'de önce derleyici (gcc gibi) tüm dosyayı makine koduna çevirir,
# bir .exe üretir; sonra o .exe çalıştırılır:
#
#     /* merhaba.c */
#     #include <stdio.h>
#     int main(void) {
#         printf("Merhaba BTK!\n");
#         return 0;
#     }
#     /* terminal:  gcc merhaba.c -o merhaba.exe   sonra   merhaba.exe */
#
# Python'da tek adım vardır:  py merhaba.py
# Ama "Python hiç derlenmez" demek YANLIŞ olur: CPython (resmî Python)
# kodunuzu önce "bytecode" denen ara bir dile çevirir, sonra bu
# bytecode'u satır satır yürütür. İçe aktarılan (import edilen)
# dosyaların bytecode'u __pycache__ klasöründe .pyc olarak saklanır.
# Aşağıdaki satır, bir metni Python'un kendisine "derletiyor":
kod_nesnesi = compile("toplam = 2 + 3", "<ornek>", "exec")
print("Fark 1: Python kodu önce bytecode'a çevrilir. Nesne türü:", type(kod_nesnesi).__name__)
print()

# ---------------------------------------------------------------------------
# 3) FARK 2 — STATİK vs DİNAMİK TİP
# ---------------------------------------------------------------------------
# C'de her değişkenin türünü baştan yazarsınız ve değiştiremezsiniz:
#
#     int sikayet_sayisi = 36;
#     sikayet_sayisi = "otuz alti";   /* DERLEME HATASI: tür uyuşmuyor */
#
# Python'da tür DEĞERDE durur, değişken adı sadece bir etikettir.
# Aynı ada başka türde bir değer bağlanabilir (iyi bir alışkanlık değildir!).
sikayet_sayisi = 36
print("Fark 2: önce türü", type(sikayet_sayisi).__name__)
sikayet_sayisi = "otuz altı"
print("Fark 2: sonra türü", type(sikayet_sayisi).__name__)
# Dikkat: Python da türleri DENETLER, ama çalışırken denetler.
# "5" + 3 gibi bir işlem çalıştığı anda TypeError verir (12_hata_mesaji_okuma.py).
print()

# ---------------------------------------------------------------------------
# 4) FARK 3 — SÜSLÜ PARANTEZ vs GİRİNTİ
# ---------------------------------------------------------------------------
# C'de blok { } ile belirlenir, girinti sadece görünüş içindir:
#
#     if (sure > 5) {
#         printf("Gecikmeli\n");
#     }
#
# Python'da blok GİRİNTİ ile belirlenir (standart: 4 boşluk).
# İki nokta (:) "bir blok başlıyor" demektir. Noktalı virgül gerekmez.
sure = 8
if sure > 5:
    print("Fark 3: girinti bloğu belirler -> Gecikmeli")
# Girintiyi bozarsanız Python IndentationError verir. Ayrıntı Gün 2.
print()

# ---------------------------------------------------------------------------
# 5) FARK 4 — BELLEK YÖNETİMİ ve TAM SAYI SINIRI
# ---------------------------------------------------------------------------
# C'de büyük bir dizi için belleği siz ayırır, işiniz bitince siz
# geri verirsiniz; unutursanız bellek sızıntısı olur:
#
#     int *sureler = malloc(1000 * sizeof(int));
#     /* ... kullan ... */
#     free(sureler);
#
# Python'da bellek otomatik yönetilir; kullanılmayan nesneler kendiliğinden
# temizlenir (referans sayma + çöp toplayıcı). Liste büyüdükçe kendisi yer açar.
sureler = []
sureler.append(3)
sureler.append(7)
print("Fark 4: listeye eleman ekledik, malloc/free yok. Eleman sayısı:", len(sureler))

# C'de int genelde 32 bittir; en büyük değer 2147483647'dir.
#     int x = 2147483647;
#     x = x + 1;   /* taşma! sonuç tanımsız / eksi bir sayı olabilir */
# Python'da tam sayının sınırı yoktur (bellek yettiği kadar büyür):
en_buyuk_c_int = 2147483647
print("Fark 4: C'de taşacak toplam Python'da sorunsuz:", en_buyuk_c_int + 1)
print()

# ---------------------------------------------------------------------------
# ÖZET (tahtaya yazılabilir)
# ---------------------------------------------------------------------------
#   Konu              C                         Python
#   Çalıştırma        derle -> .exe -> çalıştır  py dosya.py (arka planda bytecode)
#   Tür               int x; (sabit, baştan)     x = 5 (değerde, çalışırken)
#   Blok              { }                        girinti + :
#   Bellek            malloc / free              otomatik
#   Hız               çok hızlı                  daha yavaş; ama analiz
#                                                kütüphaneleri içte C kullanır
print("Python ve C karşılaştırması bitti.")
