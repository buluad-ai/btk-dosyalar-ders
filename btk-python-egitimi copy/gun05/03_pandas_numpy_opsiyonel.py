# -*- coding: utf-8 -*-
"""Pandas ve NumPy ile aynı analiz. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ATLANDI: pandas/numpy yok. 01_standart_analiz.py kullanın.")
else:
    veri = pd.read_csv(ROOT / "data" / "basvurular.csv")
    kapali = veri.loc[veri["durum"] == "Kapali"]
    print("Kapalı kayıt:", len(kapali))
    print(f"Ortalama: {np.mean(kapali['islem_suresi'].to_numpy()):.2f}")
    print(veri.groupby("birim_kodu").size().to_string())
