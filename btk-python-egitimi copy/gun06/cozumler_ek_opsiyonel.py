# -*- coding: utf-8 -*-
"""Gün 6 ek alıştırma çözümleri — MATPLOTLIB kısmı. Bkz. ALISTIRMALAR.md

NASIL ÇALIŞTIRILIR?
    python gun06/cozumler_ek_opsiyonel.py

BEKLENEN ÇIKTI (son satır):
    Gün 6 matplotlib çözümleri tamamlandı.
    (paket yoksa: ATLANDI: matplotlib kurulu değil — B planı: cozumler_ek.py)
"""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("ATLANDI: matplotlib kurulu değil — B planı: cozumler_ek.py")
    sys.exit(0)

CIKTI = ROOT / "outputs" / "gun06"
CIKTI.mkdir(parents=True, exist_ok=True)
AY_ADLARI = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    SIKAYET = list(csv.DictReader(dosya))
with (ROOT / "data" / "hiz_olcumleri.csv").open(encoding="utf-8", newline="") as dosya:
    HIZ = list(csv.DictReader(dosya))

# T1: operatöre göre sıralı barh
sayim = sorted(Counter(k["operator"] for k in SIKAYET).items(), key=lambda x: x[1])
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.bar_label(ax.barh([o for o, a in sayim], [a for o, a in sayim], color="#167d9a"), padding=3)
ax.set(title="Operatöre göre şikâyet", xlabel="Şikâyet sayısı (adet)")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(CIKTI / "cozum_t1_operator.png", dpi=150)
plt.close(fig)
print("T1: cozum_t1_operator.png")

# O1: yalnızca çözülenlerin aylık trendi
aylik = Counter(k["tarih"][:7] for k in SIKAYET if k["durum"] == "Çözüldü")
aylar = sorted(aylik)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot([AY_ADLARI[int(a[5:7]) - 1] for a in aylar], [aylik[a] for a in aylar], marker="o", color="#167d9a")
ax.set(title="Aylık çözülen şikâyet", xlabel="Ay", ylabel="Çözülen (adet)")
ax.set_ylim(bottom=0)
fig.tight_layout()
fig.savefig(CIKTI / "cozum_o1_cozulen.png", dpi=150)
plt.close(fig)
print("O1: cozum_o1_cozulen.png")

# O2: ping histogramı
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist([float(o["ping_ms"]) for o in HIZ], bins=range(0, 61, 5), color="#167d9a", edgecolor="white")
ax.set(title="Ping süresi dağılımı", xlabel="Ping (ms)", ylabel="Ölçüm sayısı (adet)")
fig.tight_layout()
fig.savefig(CIKTI / "cozum_o2_ping.png", dpi=150)
plt.close(fig)
print("O2: cozum_o2_ping.png")

# İ1: küçük çoklu grafik (small multiples): her operatör ayrı alanda, ORTAK y ekseni
operatorler = sorted({k["operator"] for k in SIKAYET})
fig, axler = plt.subplots(2, 2, figsize=(11, 7), sharex=True, sharey=True)   # sharey: karşılaştırma adil olsun
for ax, op in zip(axler.flat, operatorler):
    aylik = Counter(k["tarih"][:7] for k in SIKAYET if k["operator"] == op)
    ax.plot([AY_ADLARI[int(a[5:7]) - 1] for a in aylar], [aylik[a] for a in aylar], marker="o", color="#167d9a")
    ax.set_title(f"{op} ({sum(aylik.values())} şikâyet)")
    ax.set_ylim(bottom=0)
fig.supylabel("Şikâyet sayısı (adet)")
fig.suptitle("Operatörlere göre aylık şikâyet (ortak y ekseni)")
fig.tight_layout()
fig.savefig(CIKTI / "cozum_i1_operator_trend.png", dpi=150)
plt.close(fig)
print("İ1: cozum_i1_operator_trend.png")
print("Gün 6 matplotlib çözümleri tamamlandı.")
