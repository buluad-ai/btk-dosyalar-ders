# -*- coding: utf-8 -*-
"""JSON ve hatalı veriyi ayırma. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

import json
birimler = json.loads((ROOT / "data" / "birimler.json").read_text(encoding="utf-8"))
print("A birimi:", birimler["A"])
gecerli = []
hatalar = []
for ham in ["2", " 5 ", "bilinmiyor", "-1"]:
    try:
        sure = int(ham)
        if sure < 0:
            raise ValueError("Süre negatif olamaz")
        gecerli.append(sure)
    except ValueError:
        hatalar.append(ham)
print("Geçerli:", gecerli)
print("Hatalı kayıt sayısı:", len(hatalar))
