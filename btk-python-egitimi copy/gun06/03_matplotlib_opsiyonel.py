# -*- coding: utf-8 -*-
"""Matplotlib ile sütun grafiği. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

try:
    import matplotlib
except ImportError:
    print("ATLANDI: matplotlib yok. 02_svg_grafik.py kullanın.")
else:
    matplotlib.use("Agg")  # Ekran gerektirmeden dosya üret; sınıfta dosyayı açın.
    import matplotlib.pyplot as plt
    import csv
    from collections import Counter
    with (ROOT / "data" / "basvurular.csv").open(encoding="utf-8", newline="") as dosya:
        sayilar = Counter(k["kategori"] for k in csv.DictReader(dosya))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(list(sayilar), list(sayilar.values()), color="#167d9a")
    ax.set(title="Kategoriye göre başvurular", ylabel="Başvuru sayısı", xlabel="Kategori")
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    cikti = ROOT / "outputs" / "gun06"
    cikti.mkdir(parents=True, exist_ok=True)
    fig.savefig(cikti / "kategori.png", dpi=150)
    plt.close(fig)
    print("PNG kaydedildi.")
