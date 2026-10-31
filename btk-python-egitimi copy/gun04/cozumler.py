# -*- coding: utf-8 -*-
"""Temel ve ek alıştırmanın bağımsız örnek çözümü."""
# Değişken adları, koşullar ve dosya yollarını örneklerle karşılaştırın.
import sqlite3
with sqlite3.connect(":memory:") as db:
    db.execute("CREATE TABLE sureler (gun INTEGER)")
    db.executemany("INSERT INTO sureler VALUES (?)", [(2,), (7,), (3,), (9,)])
    print("Adet:", db.execute("SELECT COUNT(*) FROM sureler").fetchone()[0])
    print("Ortalama:", db.execute("SELECT AVG(gun) FROM sureler WHERE gun > ?", (5,)).fetchone()[0])
