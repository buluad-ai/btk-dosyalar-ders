# -*- coding: utf-8 -*-
"""SQLite oluşturma ve parametreli sorgu. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

import sqlite3
cikti = ROOT / "outputs" / "gun04"
cikti.mkdir(parents=True, exist_ok=True)
# Tekrar çalıştırınca satır çoğalmasını önlemek için eğitim tablosunu yenile.
with sqlite3.connect(cikti / "egitim.sqlite") as baglanti:
    baglanti.execute("CREATE TABLE IF NOT EXISTS basvurular (no INTEGER PRIMARY KEY, birim TEXT, sure INTEGER)")
    baglanti.execute("DELETE FROM basvurular")
    degerler = [(int(k["basvuru_no"]), k["birim_kodu"], int(k["islem_suresi"])) for k in kayitlar]
    baglanti.executemany("INSERT INTO basvurular VALUES (?, ?, ?)", degerler)
    # Veriyi SQL metnine birleştirmeyin; ? parametresi kullanın.
    adet = baglanti.execute("SELECT COUNT(*) FROM basvurular WHERE sure > ?", (5,)).fetchone()[0]
    print("5 günü aşan kayıt:", adet)
