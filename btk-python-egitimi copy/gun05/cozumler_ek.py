# -*- coding: utf-8 -*-
"""Gün 5 ek alıştırmalarının çözümleri (ALISTIRMALAR.md -> "Ek alıştırmalar").

Her çözüm önce STANDART KÜTÜPHANE ile yazılmıştır (herkes çalıştırabilir).
pandas/NumPy kuruluysa aynı sonucun paketli hali de hesaplanıp karşılaştırılır.

Nasıl çalıştırılır?
    python gun05/cozumler_ek.py

Beklenen çıktı (özet):
    T1 Reddedilen memnuniyet: ort 1.85, medyan 2.0
    T2 Fiber düşük: 105 / 139
    T3 Kanal: Web 208, e-Devlet 195, Çağrı Merkezi 151, Dilekçe 46
    Ek çözümler tamamlandı.
"""
import csv
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True   # içe aktarmada __pycache__ klasörü oluşmasın
from xlsx_mini import sayfa_oku  # noqa: E402  (aynı klasördeki paketsiz xlsx okuyucu)

ROOT = Path(__file__).resolve().parents[1]

try:
    import pandas as pd
    import numpy as np
    PAKET_VAR = True
except ImportError:
    PAKET_VAR = False


def csv_oku(ad):
    with (ROOT / "data" / ad).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


sikayet = csv_oku("sikayetler.csv")
hiz = csv_oku("hiz_olcumleri.csv")
HEDEF = {s["kategori"]: s["hedef_gun"] for s in sayfa_oku(ROOT / "data" / "btk_ornek_veri.xlsx", "Hedefler")}

# ============================== TEMEL ==========================================
# T1: Reddedilen şikâyetlerin memnuniyet ortalaması ve medyanı
puan = [int(k["memnuniyet"]) for k in sikayet if k["durum"] == "Reddedildi" and k["memnuniyet"]]
print(f"T1 Reddedilen memnuniyet: ort {statistics.mean(puan):.2f}, medyan {statistics.median(puan):.1f}")

# T2: Fiber ölçümlerinden kaçı paket hızının %80'inin altında?
fiber = [o for o in hiz if o["teknoloji"] == "Fiber"]
dusuk = [o for o in fiber if float(o["indirme_mbps"]) < 0.8 * float(o["paket_hizi_mbps"])]
print(f"T2 Fiber düşük: {len(dusuk)} / {len(fiber)}")

# T3: Kanal bazında şikâyet sayısı (çoktan aza)
kanal = Counter(k["kanal"] for k in sikayet).most_common()
print("T3 Kanal: " + ", ".join(f"{ad} {n}" for ad, n in kanal))
if PAKET_VAR:
    df = pd.read_csv(ROOT / "data" / "sikayetler.csv")
    assert df["kanal"].value_counts().to_dict() == dict(kanal)
    print("   (pandas value_counts ile aynı)")

# ============================== ORTA ===========================================
# O1: İl bazında çözüm oranı; en yüksek ve en düşük il
toplam, cozulen = Counter(), Counter()
for k in sikayet:
    toplam[k["il"]] += 1
    cozulen[k["il"]] += k["durum"] == "Çözüldü"     # True -> 1, False -> 0
oran = {il: cozulen[il] / toplam[il] * 100 for il in toplam}
en_iyi = max(oran, key=oran.get)
en_kotu = min(oran, key=oran.get)
print(f"O1 En yüksek çözüm oranı: {en_iyi} %{oran[en_iyi]:.1f} | en düşük: {en_kotu} %{oran[en_kotu]:.1f}")
if PAKET_VAR:
    pd_oran = df.assign(c=df["durum"] == "Çözüldü").groupby("il")["c"].mean() * 100
    assert pd_oran.idxmax() == en_iyi and abs(pd_oran.max() - oran[en_iyi]) < 1e-9
    print("   (pandas groupby ile aynı)")

# O2: Hedefi aşan çözülmüş şikâyetlerde kategori bazında ortalama GECİKME (süre - hedef)
gecikme = defaultdict(list)
for k in sikayet:
    if k["durum"] == "Çözüldü":
        fark = int(k["cozum_suresi_gun"]) - HEDEF[k["kategori"]]
        if fark > 0:
            gecikme[k["kategori"]].append(fark)
print("O2 Ortalama gecikme (gün):",
      ", ".join(f"{kat} {statistics.mean(v):.1f}" for kat, v in sorted(gecikme.items())))

# O3: Operatör bazında MEDYAN gerçekleşme oranı (indirme / paket * 100)
gercek = defaultdict(list)
for o in hiz:
    gercek[o["operator"]].append(float(o["indirme_mbps"]) / float(o["paket_hizi_mbps"]) * 100)
print("O3 Medyan gerçekleşme %:",
      ", ".join(f"{op} {statistics.median(v):.1f}" for op, v in sorted(gercek.items())))
if PAKET_VAR:
    h = pd.read_csv(ROOT / "data" / "hiz_olcumleri.csv")
    pd_med = (h["indirme_mbps"] / h["paket_hizi_mbps"] * 100).groupby(h["operator"]).median()
    assert all(abs(pd_med[op] - statistics.median(v)) < 1e-9 for op, v in gercek.items())
    print("   (pandas ile aynı)")

# ============================== İLERİ ==========================================
# İ1: Karneye itiraz sütunları: toplam itiraz tutarı ve itiraz eden oranı
itiraz_top, itiraz_say, op_say = defaultdict(float), Counter(), Counter()
for k in sikayet:
    op_say[k["operator"]] += 1
    if k["itiraz_tutari_tl"]:
        itiraz_top[k["operator"]] += float(k["itiraz_tutari_tl"])
        itiraz_say[k["operator"]] += 1
for op in sorted(op_say):
    print(f"İ1 {op}: itiraz {itiraz_top[op]:.2f} TL, itiraz eden %{itiraz_say[op] / op_say[op] * 100:.1f}")
if PAKET_VAR:
    g = df.groupby("operator")["itiraz_tutari_tl"]
    assert all(abs(g.sum()[op] - itiraz_top[op]) < 1e-6 for op in op_say)
    assert all(abs(g.count()[op] - itiraz_say[op]) == 0 for op in op_say)
    print("   (pandas sum/count ile aynı)")

# İ2: Aylık hedef aşım oranı (çözülenler içinde, %)
ay_cozulen, ay_asan = Counter(), Counter()
for k in sikayet:
    if k["durum"] == "Çözüldü":
        t = date.fromisoformat(k["tarih"])
        ay = f"{t.year}-{t.month:02d}"
        ay_cozulen[ay] += 1
        ay_asan[ay] += int(k["cozum_suresi_gun"]) > HEDEF[k["kategori"]]
print("İ2 Aylık hedef aşım %:", ", ".join(f"{ay} {ay_asan[ay] / ay_cozulen[ay] * 100:.0f}"
                                          for ay in sorted(ay_cozulen)))

# İ3: Hiz_Olcumleri SAYFASINDAN (xlsx) ping 90. yüzdelik; NumPy varsa karşılaştır
ping = [s["ping_ms"] for s in sayfa_oku(ROOT / "data" / "btk_ornek_veri.xlsx", "Hiz_Olcumleri")]
p90 = statistics.quantiles(ping, n=100, method="inclusive")[89]
print(f"İ3 Ping 90. yüzdelik (xlsx): {p90:.2f} ms")
if PAKET_VAR:
    assert abs(np.percentile(ping, 90) - p90) < 1e-9
    print("   (np.percentile ile aynı)")

print("Ek çözümler tamamlandı.")
