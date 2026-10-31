# -*- coding: utf-8 -*-
"""Pandas ile hataları görünür kılma."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
try:
    import pandas as pd
except ImportError:
    print("ATLANDI: pandas yok. 05_veri_temizleme.py kullanın.")
else:
    veri = pd.read_csv(ROOT / "data/kirli_basvurular.csv", dtype=str, keep_default_na=False)
    veri["birim_kodu"] = veri["birim_kodu"].str.strip()
    sure = pd.to_numeric(veri["islem_suresi"], errors="coerce")
    tarih = pd.to_datetime(veri["tarih"], format="%Y-%m-%d", errors="coerce")
    # Eksik/geçersiz değerler NaN/NaT olur; maskeyle inceleme için ayırırız.
    gecerli = (sure.notna() & (sure >= 0) & (sure % 1 == 0) & tarih.notna()
               & veri["birim_kodu"].isin(["A", "B", "C"])
               & ~veri["basvuru_no"].duplicated())
    temiz = veri.loc[gecerli].copy()
    temiz["islem_suresi"] = sure.loc[gecerli].astype(int)
    cikti = ROOT / "outputs/gun05"
    cikti.mkdir(parents=True, exist_ok=True)
    temiz.to_csv(cikti / "pandas_temiz.csv", index=False)
    veri.loc[~gecerli].to_csv(cikti / "pandas_incele.csv", index=False)
    print("Temiz kayıt:", len(temiz))
    print("İncelenecek kayıt:", int((~gecerli).sum()))
