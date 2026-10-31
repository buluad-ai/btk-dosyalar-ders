# -*- coding: utf-8 -*-
"""Seaborn ile süre dağılımı. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

try:
    import matplotlib
    import seaborn as sns
    import pandas as pd
except ImportError:
    print("ATLANDI: seaborn/pandas/matplotlib yok. 01_metin_grafigi.py kullanın.")
else:
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    veri = pd.read_csv(ROOT / "data" / "basvurular.csv")
    kapali = veri.loc[veri["durum"] == "Kapali"]
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data=kapali, x="islem_suresi", discrete=True, ax=ax)
    ax.set(title="Kapalı başvuruların süre dağılımı", xlabel="Tamamlanma süresi (gün)", ylabel="Başvuru sayısı")
    fig.tight_layout()
    cikti = ROOT / "outputs" / "gun06"
    cikti.mkdir(parents=True, exist_ok=True)
    fig.savefig(cikti / "sure_dagilimi.png", dpi=150)
    plt.close(fig)
    print("Histogram kaydedildi.")
