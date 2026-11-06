# -*- coding: utf-8 -*-
"""for döngüsü, range, enumerate, zip.

Ne öğretiyor:
    - for eleman in liste:  -> listedeki HER eleman için bloğu bir kez çalıştır.
    - range(başla, bitiş, adım) -> sayı dizisi üretir; bitiş HARİÇ.
    - enumerate(liste, start=1) -> sıra numarası + eleman birlikte.
    - zip(liste1, liste2)       -> iki listeyi yan yana yürüt (aynı satır).

Excel karşılığı:
    for -> formülü bir sütunda AŞAĞI DOĞRU SÜRÜKLEMEK; her satır için aynı işlem.
    enumerate -> yanına "Sıra No" sütunu eklemek.
    zip -> A ve B sütunlarını aynı satırda birlikte okumak (A2 ile B2, A3 ile B3).

Nasıl çalıştırılır:
    py gun02/08_for_range_enumerate_zip.py

Beklenen çıktı (seçme satırlar):
    1. İstanbul
    Ankara: 3 şikâyet
    Toplam 15 şikâyet, 6 il.
"""

iller = ["İstanbul", "Ankara", "Antalya", "Konya", "İzmir", "Erzurum"]
adetler = [5, 3, 2, 1, 2, 2]   # aynı sırayla: İstanbul 5, Ankara 3, ...

# ---------------------------------------------------------------------------
# 1) EN BASİT for
# ---------------------------------------------------------------------------
# "il" adı döngüde OTOMATİK olarak her turda bir sonraki elemanı alır.
# Adını siz seçersiniz; tekil isim seçmek okumayı kolaylaştırır (iller -> il).
print("--- for ---")
for il in iller:
    print("İl:", il)          # 4 boşluk içeride: döngünün PARÇASI
print("Döngü bitti.")         # içeride değil: döngüden SONRA bir kez çalışır
print()

# ---------------------------------------------------------------------------
# 2) range
# ---------------------------------------------------------------------------
print("--- range ---")
print("range(5)        :", list(range(5)))          # 0,1,2,3,4 (5 yok)
print("range(1, 6)     :", list(range(1, 6)))       # 1..5
print("range(0, 20, 5) :", list(range(0, 20, 5)))   # 5'er atlayarak
# Kaç tur dönmesi gerektiğini bildiğimiz işler için:
for ay in range(1, 4):
    print(f"2026-{ay:02d} ayı raporu hazırlanıyor")  # :02d -> 01, 02, 03
print()

# ---------------------------------------------------------------------------
# 3) enumerate: sıra numarası lazım olduğunda
# ---------------------------------------------------------------------------
print("--- enumerate ---")
for sira, il in enumerate(iller, start=1):          # start=1 olmazsa 0'dan başlar
    print(f"{sira}. {il}")
print()

# ---------------------------------------------------------------------------
# 4) zip: iki listeyi satır satır eşleştirme
# ---------------------------------------------------------------------------
print("--- zip ---")
for il, adet in zip(iller, adetler):
    print(f"{il}: {adet} şikâyet")
# Dikkat: listelerin uzunluğu farklıysa zip KISA olanda durur, hata vermez.
# Sıralar kayarsa (ör. bir il eksik yazıldıysa) sonuç sessizce yanlış olur.
# Bu yüzden Gün 2'nin sonunda "liste içinde sözlük" yapısına geçeceğiz.
print()

# ---------------------------------------------------------------------------
# 5) for + if birlikte: filtrelemek (Excel'de Otomatik Filtre)
# ---------------------------------------------------------------------------
print("--- for + if ---")
for il, adet in zip(iller, adetler):
    if adet >= 3:
        print(f"Yoğun il: {il} ({adet})")
print()

# Toplam ve il sayısı (sum/len hazır fonksiyonlarıyla):
print(f"Toplam {sum(adetler)} şikâyet, {len(iller)} il.")

# SIK HATALAR:
#   for il in iller        -> sonda : yok -> SyntaxError
#   for i in range(len(iller)): print(iller[i])
#       -> çalışır ama "C usulü"; Python'da doğrudan "for il in iller" yazılır.
#   Döngü içinde print'i girintisiz yazmak -> sadece BİR KEZ (sonda) çalışır.
