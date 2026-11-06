# -*- coding: utf-8 -*-
"""Liste (list): sıralı değerler. Ekleme, indeks, dilim, sıralama, özet.

Ne öğretiyor:
    - Liste köşeli parantezle yazılır: [3, 8, 2]
    - append / insert / remove / pop ile değiştirme
    - indeks [0], [-1]; dilim [1:4]  (metindekiyle AYNI kurallar)
    - sort / sorted / reverse
    - len, sum, min, max, in, count, index

Excel karşılığı:
    Liste = Excel'de TEK BİR SÜTUN (ör. C2:C11 aralığı).
    len  -> BAĞ_DEĞ_SAY      sum -> TOPLA      min/max -> MİN/MAK
    sum/len -> ORTALAMA      in  -> EĞERSAY(...)>0
    sort -> Veri > Sırala (ama sadece bu sütunu!)

Nasıl çalıştırılır:
    py gun02/07_listeler.py

Beklenen çıktı (seçme satırlar):
    Süreler: [7, 10, 3, 8, 11, 15, 2, 2, 8, 13]
    Adet: 10 | Toplam: 79 | Ortalama: 7.90
    En kısa: 2 | En uzun: 15
"""

# ---------------------------------------------------------------------------
# 1) LİSTE OLUŞTURMA
# ---------------------------------------------------------------------------
# sikayetler.csv'deki ilk 10 sonuçlanmış şikâyetin çözüm süreleri (gün)
sureler = [7, 10, 3, 8, 11, 15, 2, 2, 8, 13]
iller = ["İstanbul", "Ankara", "Konya"]
bos_liste = []                       # sonra doldurulacak
karisik = [10507, "Ankara", 7.5, True]   # farklı türler olabilir (tavsiye edilmez)
print("Süreler:", sureler)
print("Boş liste:", bos_liste, "uzunluğu", len(bos_liste))
print()

# ---------------------------------------------------------------------------
# 2) ÖZET FONKSİYONLARI
# ---------------------------------------------------------------------------
adet = len(sureler)
toplam = sum(sureler)
print(f"Adet: {adet} | Toplam: {toplam} | Ortalama: {toplam / adet:.2f}")
print(f"En kısa: {min(sureler)} | En uzun: {max(sureler)}")
print("8 gün kaç kez geçiyor?", sureler.count(8))
print("15 listede var mı?", 15 in sureler)
print("15 kaçıncı sırada (indeks)?", sureler.index(15))
print()

# ---------------------------------------------------------------------------
# 3) İNDEKS ve DİLİM — 0'dan başlar!
# ---------------------------------------------------------------------------
#   değer :  7  10  3  8  11  15  2  2  8  13
#   indeks:  0   1  2  3   4   5  6  7  8   9
print("İlk eleman [0]   :", sureler[0])
print("Son eleman [-1]  :", sureler[-1])
print("İlk 3 [:3]       :", sureler[:3])
print("Son 3 [-3:]      :", sureler[-3:])
print("2..4 [2:5]       :", sureler[2:5])      # 5 HARİÇ
# sureler[10] -> IndexError: list index out of range (10 elemanlı listede son indeks 9)
print()

# ---------------------------------------------------------------------------
# 4) DEĞİŞTİRME — liste değiştirilebilir (metin değiştirilemezdi)
# ---------------------------------------------------------------------------
iller.append("İzmir")           # sona ekle
print("append sonrası :", iller)
iller.insert(0, "Erzurum")      # 0. sıraya ekle
print("insert sonrası :", iller)
iller.remove("Konya")           # değere göre sil (ilk bulduğunu)
print("remove sonrası :", iller)
son = iller.pop()               # sondakini çıkar ve ver
print("pop ile çıkan  :", son, "| kalan:", iller)
iller[1] = "Antalya"            # indeksle değiştir
print("[1] değişti    :", iller)
print()

# ---------------------------------------------------------------------------
# 5) SIRALAMA
# ---------------------------------------------------------------------------
# sorted(liste) -> YENİ sıralı liste verir, orijinal bozulmaz.
# liste.sort()  -> listenin KENDİSİNİ sıralar, geriye None döner.
sirali = sorted(sureler)
print("sorted (yeni)       :", sirali)
print("orijinal (değişmedi):", sureler)
print("büyükten küçüğe     :", sorted(sureler, reverse=True))
kopya = sureler.copy()          # orijinali korumak için kopya
kopya.sort()
print("kopya.sort() sonrası:", kopya)
# SIK HATA:  sirali = sureler.sort()  -> sirali None olur!
print("Metin sıralama      :", sorted(["Konya", "Ankara", "İzmir", "Erzurum"]))
# Dikkat: Türkçe harfler (İ, Ş, Ç...) alfabenin SONUNA gider, çünkü Python
# karakter kodlarına göre sıralar. Raporda önemliyse Gün 5'te çözeceğiz.
print()

# ---------------------------------------------------------------------------
# 6) LİSTE + LİSTE, LİSTE * SAYI
# ---------------------------------------------------------------------------
ocak = [3, 5]
subat = [8]
print("Birleştirme:", ocak + subat)
print("Tekrar     :", [0] * 4)       # 4 elemanlı sıfır listesi
