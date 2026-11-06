# -*- coding: utf-8 -*-
"""Temel veri tipleri. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
basvuru_sayisi = 36        # int: tam sayı
ortalama = 5.33           # float: ondalık sayı; nokta kullanılır
kurum = "BTK"            # str: metin
tamamlandi = True        # bool: doğru / yanlış
bilinmeyen = None        # Henüz bir değer yok
for deger in [basvuru_sayisi, ortalama, kurum, tamamlandi, bilinmeyen]:
    print(repr(deger), type(deger).__name__)
# CSV'den okunan sayı metin olabilir: önce dönüştür.
print("Toplam:", int("12") + int("8"))
