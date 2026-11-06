# -*- coding: utf-8 -*-
"""if / elif / else: şikâyet önceliklendirme ve SLA (hedef süre) kontrolü.

Ne öğretiyor:
    - if koşul:      -> koşul True ise girintili blok çalışır
    - elif koşul:    -> (else if) önceki koşullar tutmadıysa bunu dene
    - else:          -> hiçbiri tutmadıysa
    - Python yukarıdan aşağı bakar; İLK doğru koşulun bloğunu çalıştırır,
      gerisine BAKMAZ. Bu yüzden sıra önemlidir.
    - Girinti: blok içindeki satırlar 4 boşluk içeride; iki nokta (:) şart.

Excel karşılığı:
    =EĞER(B2="Kesinti";"Yüksek";EĞER(B2="Kapsama";"Orta";"Normal"))
    iç içe EĞER'lerin okunaklı hâli -> if / elif / else
    (Excel 365'teki ÇOKEĞER / IFS fonksiyonuna da benzer.)

Nasıl çalıştırılır:
    py gun02/06_sikayet_onceliklendirme.py

Beklenen çıktı:
    Şikâyet 10507 (Kesinti): öncelik YÜKSEK
    SLA: hedef 5 gün, süre 7 gün -> HEDEF AŞILDI (2 gün gecikme)
    Memnuniyet 2 -> Olumsuz
    Bu şikâyet yöneticiye raporlanacak.
    İşlemde olan şikâyet: süre henüz yok, SLA hesaplanmadı.
"""

# Tek bir şikâyet kaydı (data/sikayetler.csv'nin ilk satırı)
sikayet_no = 10507
kategori = "Kesinti"
durum = "Reddedildi"
cozum_suresi_gun = 7
memnuniyet = 2

# ---------------------------------------------------------------------------
# 1) ÖNCELİK: kategoriye göre
# ---------------------------------------------------------------------------
# Kural (kurgusal): Kesinti -> YÜKSEK; Kapsama veya İnternet Hızı -> ORTA;
#                   diğerleri -> NORMAL
if kategori == "Kesinti":
    oncelik = "YÜKSEK"
elif kategori == "Kapsama" or kategori == "İnternet Hızı":
    oncelik = "ORTA"
else:
    oncelik = "NORMAL"
print(f"Şikâyet {sikayet_no} ({kategori}): öncelik {oncelik}")

# ---------------------------------------------------------------------------
# 2) SLA: kategorinin hedef süresi aşıldı mı?
# ---------------------------------------------------------------------------
# Hedefler data/btk_ornek_veri.xlsx -> "Hedefler" sayfasıyla aynıdır.
# (Bu uzun elif zincirini 10_sozlukler.py'de TEK SATIRLIK sözlük aramasıyla
#  değiştireceğiz — Excel'de DÜŞEYARA gibi.)
if kategori == "Fatura":
    hedef_gun = 7
elif kategori == "İnternet Hızı":
    hedef_gun = 10
elif kategori == "Kesinti":
    hedef_gun = 5
elif kategori == "Taahhüt/İptal":
    hedef_gun = 15
elif kategori == "Numara Taşıma":
    hedef_gun = 3
elif kategori == "Kapsama":
    hedef_gun = 20
else:
    hedef_gun = 10   # listede olmayan kategori için varsayılan

if cozum_suresi_gun > hedef_gun:
    gecikme = cozum_suresi_gun - hedef_gun
    print(f"SLA: hedef {hedef_gun} gün, süre {cozum_suresi_gun} gün -> HEDEF AŞILDI ({gecikme} gün gecikme)")
else:
    print(f"SLA: hedef {hedef_gun} gün, süre {cozum_suresi_gun} gün -> hedef içinde")

# ---------------------------------------------------------------------------
# 3) SIRA ÖNEMLİDİR: aralık sınıflandırma
# ---------------------------------------------------------------------------
# Büyükten küçüğe kontrol ediyoruz. Sırayı ters yazarsanız (önce >= 1)
# her puan "Olumsuz" çıkar, çünkü ilk doğru koşulda durulur.
if memnuniyet >= 4:
    memnuniyet_grubu = "Olumlu"
elif memnuniyet == 3:
    memnuniyet_grubu = "Nötr"
else:
    memnuniyet_grubu = "Olumsuz"
print(f"Memnuniyet {memnuniyet} -> {memnuniyet_grubu}")

# ---------------------------------------------------------------------------
# 4) BİRLEŞİK KOŞUL ve İÇ İÇE if
# ---------------------------------------------------------------------------
# Yöneticiye raporla: öncelik YÜKSEK ve (hedef aşıldı ya da reddedildi)
if oncelik == "YÜKSEK" and (cozum_suresi_gun > hedef_gun or durum == "Reddedildi"):
    print("Bu şikâyet yöneticiye raporlanacak.")
else:
    print("Rutin takip.")

# İç içe if: önce "süre var mı?" sonra "hedef aşıldı mı?"
# İşlemde olan şikâyetin süresi yoktur (None). None ile > karşılaştırması
# TypeError verir; bu yüzden ÖNCE None kontrolü yapılır.
islemdeki_sure = None
if islemdeki_sure is None:              # None kontrolü için "is None" kullanılır
    print("İşlemde olan şikâyet: süre henüz yok, SLA hesaplanmadı.")
else:
    if islemdeki_sure > hedef_gun:
        print("Hedef aşıldı")

# SIK HATALAR:
#   if kategori = "Kesinti":     -> SyntaxError (tek = atamadır, == olmalı)
#   if kategori == "Kesinti"     -> SyntaxError (sonda : unutulmuş)
#   bloğu girintisiz yazmak      -> IndentationError
#   else: koşul yazmak  (else kategori == ...) -> SyntaxError; else koşulsuzdur
