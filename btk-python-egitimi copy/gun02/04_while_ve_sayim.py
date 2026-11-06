# -*- coding: utf-8 -*-
"""Sınırlı while ve kategorileri sayma. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
deneme = 1
while deneme <= 3:
    print("Deneme:", deneme)
    deneme += 1  # Bu adım olmazsa sonsuz döngü oluşur.
kategoriler = ["Bilgi", "Teknik", "Bilgi", "Itiraz"]
sayilar = {}
for kategori in kategoriler:
    sayilar[kategori] = sayilar.get(kategori, 0) + 1
print("Bilgi sayısı:", sayilar["Bilgi"])
