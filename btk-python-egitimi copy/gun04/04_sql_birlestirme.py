# -*- coding: utf-8 -*-
"""JOIN ve GROUP BY. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

import json
import sqlite3
birimler = json.loads((ROOT / "data" / "birimler.json").read_text(encoding="utf-8"))
# Bu bağımsız örnek geçici bellek veritabanı kullanır.
with sqlite3.connect(":memory:") as db:
    db.execute("CREATE TABLE birimler (kod TEXT PRIMARY KEY, ad TEXT)")
    db.execute("CREATE TABLE kayitlar (no INTEGER PRIMARY KEY, birim TEXT, sure INTEGER)")
    db.executemany("INSERT INTO birimler VALUES (?, ?)", birimler.items())
    db.executemany("INSERT INTO kayitlar VALUES (?, ?, ?)", [(int(k["basvuru_no"]), k["birim_kodu"], int(k["islem_suresi"])) for k in kayitlar])
    sorgu = """SELECT b.ad, COUNT(*), ROUND(AVG(k.sure), 2)
               FROM kayitlar AS k JOIN birimler AS b ON k.birim = b.kod
               GROUP BY b.kod, b.ad ORDER BY b.kod"""
    for ad, adet, ortalama in db.execute(sorgu):
        print(f"{ad}: {adet} kayıt, {ortalama} gün")
