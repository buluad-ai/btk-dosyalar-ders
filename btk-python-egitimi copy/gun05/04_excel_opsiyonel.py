# -*- coding: utf-8 -*-
"""Excel yazma ve yeniden okuma. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

try:
    import pandas as pd
    import openpyxl
except ImportError:
    print("ATLANDI: pandas/openpyxl yok. 02_gruplama_rapor.py ile CSV kullanın.")
else:
    cikti = ROOT / "outputs" / "gun05"
    cikti.mkdir(parents=True, exist_ok=True)
    veri = pd.read_csv(ROOT / "data" / "basvurular.csv")
    dosya = cikti / "basvurular.xlsx"
    veri.to_excel(dosya, index=False, engine="openpyxl")
    geri = pd.read_excel(dosya, engine="openpyxl")
    print("Excel'den okunan kayıt:", len(geri))
