# -*- coding: utf-8 -*-
"""Küçük class örneği. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
class Basvuru:
    """Veri ve o veriye ait davranışı bir araya getirir."""
    def __init__(self, numara, sure):
        self.numara = numara
        self.sure = sure

    def gecikti_mi(self, esik=5):
        return self.sure > esik

kayit = Basvuru(101, 8)
print("Başvuru:", kayit.numara)
print("Eşiği aştı:", kayit.gecikti_mi())
# Veri analizi yapmak için class yazmak zorunlu değildir.
