# -*- coding: utf-8 -*-
"""Komut satırından rapor parametresi. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

import argparse
parser = argparse.ArgumentParser(description="Bir birimin kayıt sayısını gösterir.")
parser.add_argument("--birim", choices=["A", "B", "C"], default="A")
args = parser.parse_args()
secilen = [k for k in kayitlar if k["birim_kodu"] == args.birim]
print(f"Birim {args.birim}: {len(secilen)} kayıt")
# Örnek: python gun07/03_parametreli_script.py --birim B
