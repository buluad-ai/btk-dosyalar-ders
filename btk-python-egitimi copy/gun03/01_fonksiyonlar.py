# -*- coding: utf-8 -*-
def ortalama_hesapla(sureler):
    if not sureler:
        return None
    sonuc = sum(sureler) / len(sureler)
    return round(sonuc, 1)

# return hesaplanan sonucu çağıran yere verir; print yalnızca gösterir.
sonuc = ortalama_hesapla([2, 4, 9])
sonuc1 = ortalama_hesapla([160,170,180,190,200])
print(f"Ortalama: {sonuc:.2f}")
print("Boş liste:", ortalama_hesapla([]))
