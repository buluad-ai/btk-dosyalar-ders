# -*- coding: utf-8 -*-
"""Python'a özgü yapılar: list comprehension ve birkaç kısa yazım.

Ne öğretiyor:
    - List comprehension: "for + if + append" kalıbının TEK SATIRLIK hâli.
        [ifade for eleman in liste]                -> dönüştür
        [ifade for eleman in liste if koşul]       -> filtrele (+ dönüştür)
    - Dict comprehension (bir örnek), any / all, koşullu ifade (tek satır if).
    - Bunlar ZORUNLU DEĞİL: uzun yazım (for + append) her zaman çalışır.
      Amaç başkasının yazdığı hazır scriptte gördüğünüzde OKUYABİLMEK.

C ile fark:
    C'de bir diziyi filtrelemek için yeni dizi, sayaç ve for döngüsü yazılır.
    Python'da [s for s in sureler if s > 10] yeterlidir.

Excel karşılığı:
    [s * 24 for s in sureler]          -> yan sütuna =C2*24 yazıp aşağı sürüklemek
    [s for s in sureler if s > 10]     -> Otomatik Filtre ya da FİLTRE(C:C; C:C>10)

Nasıl çalıştırılır:
    py gun02/12_pythona_ozgu_yapilar.py

Beklenen çıktı (seçme satırlar):
    Uzun yol : [11, 15, 13]
    Kısa yol : [11, 15, 13]
    Saat cinsinden: [168, 240, 72, 192, 264, 360, 48, 48, 192, 312]
"""

sureler = [7, 10, 3, 8, 11, 15, 2, 2, 8, 13]

# ---------------------------------------------------------------------------
# 1) FİLTRELEME: uzun yol vs kısa yol
# ---------------------------------------------------------------------------
# Uzun yol (09_biriktirme_sayac.py'deki kalıp):
uzunlar = []
for s in sureler:
    if s > 10:
        uzunlar.append(s)
print("Uzun yol :", uzunlar)

# Kısa yol — list comprehension. Sağdan sola değil, şöyle okuyun:
#   "sureler'deki her s için, s > 10 ise, s'yi listeye koy"
uzunlar_kisa = [s for s in sureler if s > 10]
print("Kısa yol :", uzunlar_kisa)
print()

# ---------------------------------------------------------------------------
# 2) DÖNÜŞTÜRME: her elemana aynı işlem
# ---------------------------------------------------------------------------
saatler = [s * 24 for s in sureler]
print("Saat cinsinden:", saatler)

# Metin listesi temizleme (Gün 5'te kirli veride çok işe yarar):
ham_iller = ["  ankara", "İZMİR ", " Konya "]
temiz_iller = [il.strip() for il in ham_iller]
print("Temizlenmiş   :", temiz_iller)

# CSV'den gelen metin sayıları int'e çevirme:
ham_sureler = ["7", "10", "3"]
print("int listesi   :", [int(x) for x in ham_sureler])
print()

# ---------------------------------------------------------------------------
# 3) FİLTRE + DÖNÜŞTÜR + ÖZET birlikte
# ---------------------------------------------------------------------------
hedef = 10
asim_gunleri = [s - hedef for s in sureler if s > hedef]   # sadece aşanların gecikmesi
print("Gecikme günleri:", asim_gunleri, "| toplam gecikme:", sum(asim_gunleri))
print("Hedef aşan adet:", len([s for s in sureler if s > hedef]))
print()

# ---------------------------------------------------------------------------
# 4) KOŞULLU İFADE (tek satır if) — Excel'deki EĞER'in birebir karşılığı
# ---------------------------------------------------------------------------
# =EĞER(C2>10; "Gecikmeli"; "Zamanında")
sure = 13
etiket = "Gecikmeli" if sure > 10 else "Zamanında"
print("Tek satır if:", etiket)
etiketler = ["Gecikmeli" if s > 10 else "Zamanında" for s in sureler]
print("Etiket sütunu (3..5):", etiketler[3:6])
print()

# ---------------------------------------------------------------------------
# 5) any / all  — "hiç var mı?" / "hepsi mi?"
# ---------------------------------------------------------------------------
print("15 günü aşan HİÇ var mı?   :", any(s > 15 for s in sureler))   # False
print("HEPSİ 30 günden kısa mı?   :", all(s < 30 for s in sureler))   # True
print()

# ---------------------------------------------------------------------------
# 6) DICT COMPREHENSION (tanışma)
# ---------------------------------------------------------------------------
hedefler = {"Fatura": 7, "İnternet Hızı": 10, "Kesinti": 5}
saat_hedefleri = {kategori: gun * 24 for kategori, gun in hedefler.items()}
print("Hedefler (saat):", saat_hedefleri)

# NE ZAMAN KULLANMAYALIM?
#   Satır 80 karakteri geçiyorsa, iç içe iki for veya iki if varsa:
#   uzun yolu (for + append) yazın. Okunaklılık kısalıktan önemlidir.
