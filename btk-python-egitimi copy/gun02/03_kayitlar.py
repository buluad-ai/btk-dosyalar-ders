# -*- coding: utf-8 -*-
"""Sözlük, tuple ve küme. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
kayitlar = [
    {"no": 1, "birim": "A", "durum": "Acik"},
    {"no": 2, "birim": "B", "durum": "Kapali"},
    {"no": 3, "birim": "A", "durum": "Kapali"},
]
# dict alanlara isimle, list kayıtlara sıra ile erişim sağlar.
print("İlk birim:", kayitlar[0]["birim"])
birimler = set()
for kayit in kayitlar:
    birimler.add(kayit["birim"])
print("Tekil birimler:", sorted(birimler))
sabit_aralik = (0, 30)  # tuple: değiştirilemeyen sıralı değerler
print("Aralık:", sabit_aralik)
