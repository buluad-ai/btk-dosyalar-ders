# -*- coding: utf-8 -*-
"""İki yol aynı sonucu veriyor mu? (stdlib pipeline vs pandas pipeline)

NE ÖĞRETİYOR?
    Bir analizin GÜVENİLİR olduğunu göstermenin en iyi yolu: aynı soruyu iki farklı
    yöntemle çözüp sonuçları karşılaştırmak. (Excel'de PivotTable sonucunu
    ETOPLA/EĞERSAY ile çapraz kontrol etmek gibi.)
    Bu script:
      1) 07_pipeline_stdlib.py'yi çalıştırır  -> outputs/gun07/ozet_stdlib.json
      2) 08_pipeline_pandas_opsiyonel.py'yi çalıştırır -> outputs/gun07/ozet_pandas.json
      3) İki JSON'daki "ana_sayilar" sözlüğünü tek tek karşılaştırır.
    Verdiğiniz parametreler (--il, --operator, --baslangic, --bitis, --girdi) iki
    scripte de aynen aktarılır.

NASIL ÇALIŞTIRILIR?
    python gun07/09_iki_yol_karsilastir_opsiyonel.py
    python gun07/09_iki_yol_karsilastir_opsiyonel.py --il Ankara --baslangic 2026-04-01 --bitis 2026-06-30
    python gun07/09_iki_yol_karsilastir_opsiyonel.py --girdi data/sikayetler_kirli.csv

BEKLENEN ÇIKTI:
    Sonuç: iki yol AYNI ana sayıları üretti.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CIKTI = ROOT / "outputs" / "gun07"

try:
    import pandas  # noqa: F401  (yalnızca kurulu mu diye bakıyoruz)
    import matplotlib  # noqa: F401
except ImportError as hata:
    print(f"ATLANDI: {hata.name} kurulu değil — B planı: 07_pipeline_stdlib.py (tek başına çalıştırın)")
    sys.exit(0)

parametreler = sys.argv[1:]     # bu scripte verilen her şeyi olduğu gibi aktar
sonuclar = {}
for surum, dosya in [("stdlib", "07_pipeline_stdlib.py"), ("pandas", "08_pipeline_pandas_opsiyonel.py")]:
    # sys.executable = şu an bu scripti çalıştıran Python; aynı ortamı kullanmayı garanti eder
    calisma = subprocess.run([sys.executable, str(ROOT / "gun07" / dosya), *parametreler],
                             capture_output=True, text=True, encoding="utf-8")
    if calisma.returncode != 0:
        print(f"{dosya} HATA verdi:\n{calisma.stderr}")
        sys.exit(1)
    if "Filtreye uyan kayıt yok" in calisma.stdout:
        print("Filtreye uyan kayıt yok; karşılaştırılacak sonuç yok.")
        sys.exit(0)
    sonuclar[surum] = json.loads((CIKTI / f"ozet_{surum}.json").read_text(encoding="utf-8"))["ana_sayilar"]

print(f"{'Gösterge':<28} {'stdlib':>16} {'pandas':>16}  durum")
farkli = 0
for anahtar, deger in sonuclar["stdlib"].items():
    diger = sonuclar["pandas"].get(anahtar)
    ayni = deger == diger
    farkli += not ayni           # True 1, False 0 sayılır
    print(f"{anahtar:<28} {str(deger):>16} {str(diger):>16}  {'AYNI' if ayni else 'FARKLI!'}")

if farkli:
    print(f"Sonuç: {farkli} göstergede fark var — kuralları karşılaştırın.")
    sys.exit(1)
print("Sonuç: iki yol AYNI ana sayıları üretti.")
