# -*- coding: utf-8 -*-
"""argparse ile parametreli çalıştırma: --il, --operator, --baslangic, --bitis (TAMAMLANMIŞ hali).

NE ÖĞRETİYOR?
    05'te ayarı değiştirmek için DOSYAYI düzenliyorduk. Şimdi dosyaya hiç dokunmadan,
    ayarı KOMUT SATIRINDAN veriyoruz:
        python gun07/06_filtre_parametreleri.py --il Ankara --baslangic 2026-04-01
    Hiç parametre verilmezse VARSAYILAN: filtre yok, tüm veri.
    argparse bizim için:
      - --help ile kullanım kılavuzu üretir,
      - tarihi doğrular (type=date.fromisoformat -> "2026-13-45" reddedilir),
      - hatalı kullanımda anlaşılır mesaj verip durur.
    Canlı kodlama iskeleti: 06_filtre_parametreleri_bos.py

    Windows notu: Boşluk içeren değeri tırnakla yazın: --operator "Operatör A"
    (PowerShell ve cmd'de çift tırnak çalışır.)

NASIL ÇALIŞTIRILIR?
    python gun07/06_filtre_parametreleri.py
    python gun07/06_filtre_parametreleri.py --il İzmir --operator "Operatör B"
    python gun07/06_filtre_parametreleri.py --baslangic 2026-07-01 --bitis 2026-09-30
    python gun07/06_filtre_parametreleri.py --help

BEKLENEN ÇIKTI (parametresiz):
    Filtre: yok (tüm veri)
    Eşleşen kayıt: 600
"""
import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

parser = argparse.ArgumentParser(description="Şikâyetleri il, operatör ve tarih aralığına göre süzer.")
# default=None: parametre verilmezse filtre uygulanmaz
parser.add_argument("--il", default=None, help="Örnek: --il Ankara")
parser.add_argument("--operator", default=None, help='Örnek: --operator "Operatör A"')
parser.add_argument("--baslangic", type=date.fromisoformat, default=None, help="İlk tarih (dahil), YYYY-AA-GG")
parser.add_argument("--bitis", type=date.fromisoformat, default=None, help="Son tarih (dahil), YYYY-AA-GG")
args = parser.parse_args()       # komut satırını oku; hatalıysa burada mesaj verip çıkar

if args.baslangic and args.bitis and args.baslangic > args.bitis:
    parser.error("--baslangic, --bitis tarihinden sonra olamaz")

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

secilen = []
for k in kayitlar:
    tarih = date.fromisoformat(k["tarih"])
    # Her koşul: "parametre verildiyse VE satır uymuyorsa -> atla"
    if args.il and k["il"] != args.il:
        continue
    if args.operator and k["operator"] != args.operator:
        continue
    if args.baslangic and tarih < args.baslangic:
        continue
    if args.bitis and tarih > args.bitis:
        continue
    secilen.append(k)

verilenler = {"il": args.il, "operatör": args.operator, "başlangıç": args.baslangic, "bitiş": args.bitis}
filtre = ", ".join(f"{ad}={deger}" for ad, deger in verilenler.items() if deger) or "yok (tüm veri)"
print(f"Filtre: {filtre}")
print(f"Eşleşen kayıt: {len(secilen)}")
for durum, adet in Counter(k["durum"] for k in secilen).most_common():
    print(f"  {durum}: {adet}")
if not secilen:
    gecerli = sorted({k["il"] for k in kayitlar})
    print("Hiç kayıt yok. Geçerli il yazımları:", ", ".join(gecerli))
