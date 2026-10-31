# -*- coding: utf-8 -*-
"""CANLI KODLAMA İSKELETİ: argparse ile parametreli filtre (öğrenci doldurur).

NE ÖĞRETİYOR?
    Bu dosya ÇALIŞIR; şu an yalnızca --il parametresini tanır. TODO'ları sırayla
    tamamlayın, her adımdan sonra farklı parametrelerle çalıştırıp deneyin.
    Tamamlanmış hali: 06_filtre_parametreleri.py

NASIL ÇALIŞTIRILIR?
    python gun07/06_filtre_parametreleri_bos.py
    python gun07/06_filtre_parametreleri_bos.py --il Ankara

BEKLENEN ÇIKTI (parametresiz):
    Eşleşen kayıt: 600
"""
import argparse
import csv
from datetime import date  # noqa: F401  (TODO 2'de kullanacaksınız)
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

parser = argparse.ArgumentParser(description="Şikâyetleri süzer.")
parser.add_argument("--il", default=None, help="Örnek: --il Ankara")
# TODO 1: --operator parametresini ekleyin (yukarıdaki satırı örnek alın).
# TODO 2: --baslangic ve --bitis ekleyin. İpucu: type=date.fromisoformat
args = parser.parse_args()

# TODO 3 (ileri): başlangıç bitişten sonraysa parser.error("...") ile durdurun.

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

secilen = []
for k in kayitlar:
    if args.il and k["il"] != args.il:
        continue
    # TODO 4: operatör filtresi
    # TODO 5: tarih filtresi. İpucu: tarih = date.fromisoformat(k["tarih"])
    secilen.append(k)

print(f"Eşleşen kayıt: {len(secilen)}")
