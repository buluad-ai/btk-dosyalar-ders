# -*- coding: utf-8 -*-
"""Bütünleşik analiz: oku doğrula özetle yaz. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

import json
from collections import Counter
from statistics import mean

def temizle(ham_kayitlar):
    sonuc = []
    gorulen = set()
    for ham in ham_kayitlar:
        kayit = dict(ham)  # Girdiyi değiştirmeden bir kopya al.
        kayit["basvuru_no"] = int(ham["basvuru_no"])
        kayit["islem_suresi"] = int(ham["islem_suresi"])
        if kayit["basvuru_no"] in gorulen or kayit["islem_suresi"] < 0:
            raise ValueError("Tekrarlayan kimlik veya negatif süre")
        gorulen.add(kayit["basvuru_no"])
        sonuc.append(kayit)
    return sonuc

veri = temizle(kayitlar)
kapali = [k["islem_suresi"] for k in veri if k["durum"] == "Kapali"]
ozet = {"kayit_sayisi": len(veri), "kapali_sayisi": len(kapali),
        "kapali_ortalama_gun": round(mean(kapali), 2) if kapali else None,
        "birim_sayilari": dict(Counter(k["birim_kodu"] for k in veri))}
cikti = ROOT / "outputs" / "gun07"
cikti.mkdir(parents=True, exist_ok=True)
(cikti / "ozet.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
print("Analiz tamamlandı:", ozet["kayit_sayisi"], "kayıt")
