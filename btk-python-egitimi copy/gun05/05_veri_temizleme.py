# -*- coding: utf-8 -*-
"""Eksik tekrar tarih ve sayı denetimi."""
import csv
import json
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data/kirli_basvurular.csv").open(encoding="utf-8", newline="") as f:
    ham_kayitlar = list(csv.DictReader(f))

temiz, sorunlu = [], []
gorulen = set()
for satir_no, ham in enumerate(ham_kayitlar, start=2):
    kayit = {alan: deger.strip() for alan, deger in ham.items()}
    try:
        kimlik = int(kayit["basvuru_no"])
        if kimlik in gorulen:
            raise ValueError("Tekrarlayan kimlik")
        # Eğitim iş kuralı: tarih ISO, süre dolu ve sıfırdan büyük/eşit tam sayı.
        date.fromisoformat(kayit["tarih"])
        sure = int(kayit["islem_suresi"])
        if sure < 0:
            raise ValueError("Negatif süre")
        if kayit["birim_kodu"] not in {"A", "B", "C"}:
            raise ValueError("Bilinmeyen birim")
        kayit["basvuru_no"], kayit["islem_suresi"] = kimlik, sure
        gorulen.add(kimlik)
        temiz.append(kayit)
    except ValueError as hata:
        sorunlu.append({"satir": satir_no, "kayit": ham, "neden": str(hata)})
# Hatalı kayıtları sessizce yok etmeyiz; ayrı inceleme dosyasında saklarız.
cikti = ROOT / "outputs/gun05"
cikti.mkdir(parents=True, exist_ok=True)
for ad, veri in [("temiz.json", temiz), ("sorunlu.json", sorunlu)]:
    (cikti / ad).write_text(json.dumps(veri, ensure_ascii=False, indent=2), encoding="utf-8")
print("Temiz kayıt:", len(temiz))
print("İncelenecek kayıt:", len(sorunlu))
print("Kontrol toplamı:", len(temiz) + len(sorunlu))
