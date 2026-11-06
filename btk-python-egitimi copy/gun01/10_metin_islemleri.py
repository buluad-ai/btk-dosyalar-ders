# -*- coding: utf-8 -*-
"""String (metin) işlemleri: f-string, temizlik metotları, len, indeks, dilim.

Ne öğretiyor:
    - f-string ile değişkeni metnin içine yerleştirme ve sayı biçimlendirme.
    - upper / lower / strip / replace / split / startswith / count.
    - len(), indeks [0], [-1] ve dilimleme [başlangıç:bitiş].
    - Türkçe büyük/küçük harf tuzağı (İ / ı).

Excel karşılığı:
    upper -> BÜYÜKHARF     lower -> KÜÇÜKHARF     strip -> KIRP
    replace -> YERİNEKOY   len -> UZUNLUK         s[:3] -> SOLDAN(s;3)
    s[-4:] -> SAĞDAN(s;4)  s[2:5] -> PARÇAAL(s;3;3)
    split -> "Metni Sütunlara Dönüştür"           f-string -> & ile birleştirme

Nasıl çalıştırılır:
    py gun01/10_metin_islemleri.py

Beklenen çıktı (seçme satırlar):
    Ankara ilinde 42 şikâyet var.
    Operatör: OPERATÖR A
    Yıl: 2026 | Ay: 10 | Gün: 14
"""

# ---------------------------------------------------------------------------
# 1) f-string: metnin içine değişken koymak
# ---------------------------------------------------------------------------
# Tırnağın önüne f koyun, değişkeni {süslü parantez} içine yazın.
il = "Ankara"
adet = 42
print(f"{il} ilinde {adet} şikâyet var.")

# Biçimlendirme: iki nokta (:) sonrası "nasıl gösterilsin"
ortalama = 5.333333
oran = 0.4567
tutar = 1234567.891
print(f"Ortalama: {ortalama:.2f} gün")       # 2 ondalık  -> 5.33
print(f"Oran: {oran:.1%}")                    # yüzde      -> 45.7%
print(f"Tutar: {tutar:,.2f} TL")              # binlik ayraç -> 1,234,567.89
# Not: Python binlik ayracı olarak virgül, ondalık için nokta kullanır
# (İngilizce biçim). Türk biçimi için Gün 3'te küçük bir yardımcı göreceğiz.
print(f"Hizalı: [{il:>10}] [{adet:5}]")      # sağa yasla / genişlik
print()

# ---------------------------------------------------------------------------
# 2) TEMİZLİK METOTLARI — veri girişinden gelen "kirli" metin
# ---------------------------------------------------------------------------
ham_operator = "  operatör a  "
print(f"Ham değer: [{ham_operator}]")                 # köşeli parantez boşlukları gösterir
temiz = ham_operator.strip()                          # baş/son boşlukları sil
print(f"strip   : [{temiz}]")
print("Operatör:", temiz.upper())                     # OPERATÖR A
print("title   :", temiz.title())                     # Operatör A
print("lower   :", "KAPSAMA SORUNU".lower())     # İ harfi yok; İ tuzağı için 5. bölüm
print("replace :", "Sabit-Internet".replace("-", " "))
# Metot ORİJİNALİ DEĞİŞTİRMEZ, yeni metin döndürür. Saklamak için atayın:
ham_operator.strip()                                  # sonuç hiçbir yere kaydedilmedi
print(f"Atamadan sonra değişmedi: [{ham_operator}]")
print()

# split: metni parçalara ayırıp LİSTE yapar (liste Gün 2'nin konusu)
tarih = "2026-10-14"
parcalar = tarih.split("-")
print("split sonucu:", parcalar)
print(f"Yıl: {parcalar[0]} | Ay: {parcalar[1]} | Gün: {parcalar[2]}")
csv_satiri = "10507,2026-01-01,İstanbul,Operatör A"
print("CSV satırının 3. alanı:", csv_satiri.split(",")[2])
print()

# ---------------------------------------------------------------------------
# 3) len, İNDEKS ve DİLİMLEME
# ---------------------------------------------------------------------------
# İndeks 0'dan başlar! Eksi indeks sondan sayar.
#   metin:   T  R  -  0  6  -  A  N  K
#   indeks:  0  1  2  3  4  5  6  7  8
#   eksi  : -9 -8 -7 -6 -5 -4 -3 -2 -1
kod = "TR-06-ANK"
print("Uzunluk:", len(kod))
print("İlk karakter [0]:", kod[0])
print("Son karakter [-1]:", kod[-1])
print("Ülke kodu [0:2]:", kod[0:2])     # 0 dahil, 2 HARİÇ -> "TR"
print("Plaka [3:5]   :", kod[3:5])      # "06"
print("Son 3 [-3:]   :", kod[-3:])      # "ANK"
print("Başı boş [:2] :", kod[:2])       # baştan itibaren
print()

# ---------------------------------------------------------------------------
# 4) ARAMA
# ---------------------------------------------------------------------------
aciklama = "İnternet kesintisi; internet hızı düşük; kesinti tekrarlıyor"
print("'kesinti' geçiyor mu?", "kesinti" in aciklama)
print("'kesinti' kaç kez?", aciklama.count("kesinti"))
print("Abone no 'TR' ile mi başlıyor?", kod.startswith("TR"))
print()

# ---------------------------------------------------------------------------
# 5) TÜRKÇE KARAKTER TUZAĞI
# ---------------------------------------------------------------------------
# Python büyük/küçük harfi uluslararası kurala göre çevirir, Türkçeye göre değil:
#   "i".upper() -> "I"  (Türkçede "İ" olmalıydı)
#   "İ".lower() -> "i" + görünmez bir nokta işareti (2 karakter!)
print('"istanbul".upper() =', "istanbul".upper())                 # ISTANBUL (noktasız!)
print('"İstanbul".lower() == "istanbul" ?', "İstanbul".lower() == "istanbul")
print('len("İstanbul".lower()) =', len("İstanbul".lower()), "(8 değil!)")
# Ders: il adlarını karşılaştırırken büyük/küçük çevirmeye güvenmeyin;
# veriyi tek bir yazımda (ör. "İstanbul") tutun ve olduğu gibi karşılaştırın.
