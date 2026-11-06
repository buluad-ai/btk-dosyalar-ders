# -*- coding: utf-8 -*-
"""Liste, for ve biriktirme. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
sureler = [2, 5, 8, 3, 10, 4]
toplam = 0
uzun_sureler = []
for sure in sureler:
    toplam = toplam + sure
    if sure > 5:
        uzun_sureler.append(sure)
print("Toplam:", toplam)
print("Uzun süreler:", uzun_sureler)
# range bitiş sayısını içermez.
for sira in range(1, 4):
    print("Kontrol adımı", sira)
