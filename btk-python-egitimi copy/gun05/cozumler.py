# -*- coding: utf-8 -*-
"""Temel ve ek alıştırmanın bağımsız örnek çözümü."""
# Değişken adları, koşullar ve dosya yollarını örneklerle karşılaştırın.
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))
from statistics import mean
gruplar = {}
for k in kayitlar:
    if k["durum"] == "Kapali":
        gruplar.setdefault(k["birim_kodu"], []).append(int(k["islem_suresi"]))
for birim, sureler in sorted(gruplar.items()):
    print(f"{birim}: {len(sureler)} kapalı, {mean(sureler):.2f} gün")
