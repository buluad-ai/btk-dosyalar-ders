# -*- coding: utf-8 -*-
"""Koşul ve girinti. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
sure = 8
esik = 5
# Girinti aynı bloktaki satırları belirler; 4 boşluk kullanın.
if sure > esik:
    print("İnceleme gerekli")
elif sure == esik:
    print("Tam eşikte")
else:
    print("Eşiğin altında")
print("Açık ve uzun:", "Acik" == "Acik" and sure > esik)
