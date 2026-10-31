# -*- coding: utf-8 -*-
"""Gün 6 ek alıştırma çözümleri — PAKETSİZ (B planı) kısım. Bkz. ALISTIRMALAR.md

Her görev ayrı bir fonksiyondur; sonunda hepsi sırayla çalışır.
Matplotlib ile yapılan çözümler: cozumler_ek_opsiyonel.py

NASIL ÇALIŞTIRILIR?
    python gun06/cozumler_ek.py

BEKLENEN ÇIKTI (son satır):
    Gün 6 ek çözümler tamamlandı.
"""
import csv
import statistics
from collections import Counter
from html import escape
from pathlib import Path

from svg_cizim import ANA_RENK, cizgi_svg, kaydet, sutun_svg, yatay_bar_svg

ROOT = Path(__file__).resolve().parents[1]
AY_ADLARI = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]


def csv_oku(ad):
    with (ROOT / "data" / ad).open(encoding="utf-8", newline="") as dosya:
        return list(csv.DictReader(dosya))


SIKAYET = csv_oku("sikayetler.csv")
HIZ = csv_oku("hiz_olcumleri.csv")


def temel_1_operator_svg():
    """T1 (B planı): operatöre göre şikâyet, sıralı yatay çubuk."""
    sayim = Counter(k["operator"] for k in SIKAYET).most_common()
    kaydet(yatay_bar_svg([o for o, a in sayim], [a for o, a in sayim],
                         baslik="Operatöre göre şikâyet", birim="adet"), "cozum_t1_operator.svg")
    print("T1:", ", ".join(f"{o} {a}" for o, a in sayim))


def temel_2_hizmet_yuzde():
    """T2: hizmet türüne göre yüzde, metin grafiği; toplam %100 kontrolü."""
    sayim = Counter(k["hizmet"] for k in SIKAYET)
    toplam = 0
    for hizmet, adet in sayim.most_common():
        yuzde = adet / len(SIKAYET) * 100
        toplam += yuzde
        print(f"T2: {hizmet:<15} {'#' * round(yuzde / 2):<30} %{yuzde:.1f}")   # her # = %2
    print(f"T2: toplam %{toplam:.0f}")


def orta_1_cozulen_trend():
    """O1 (B planı): yalnızca Çözüldü kayıtların aylık çizgisi."""
    aylik = Counter(k["tarih"][:7] for k in SIKAYET if k["durum"] == "Çözüldü")
    aylar = sorted(aylik)
    kaydet(cizgi_svg([AY_ADLARI[int(a[5:7]) - 1] for a in aylar], [aylik[a] for a in aylar],
                     baslik="Aylık çözülen şikâyet", y_etiketi="Çözülen (adet)"), "cozum_o1_cozulen.svg")
    print("O1: çözülen toplam", sum(aylik.values()), "| en yüksek ay", max(aylar, key=aylik.get))


def orta_2_ping_araliklari():
    """O2 (B planı): ping süresini 10 ms'lik aralıklara say (histogram mantığı)."""
    kutular = Counter(int(float(o["ping_ms"]) // 10) for o in HIZ)
    for i in sorted(kutular):
        print(f"O2: {i * 10:>2}-{i * 10 + 10:<3} ms {'#' * (kutular[i] // 4)} {kutular[i]}")


def orta_3_yukleme_medyan():
    """O3: teknolojiye göre MEDYAN yükleme hızı, sütun grafiği."""
    teknolojiler = ["ADSL", "VDSL", "4.5G", "Fiber"]
    medyanlar = [statistics.median(float(o["yukleme_mbps"]) for o in HIZ if o["teknoloji"] == t)
                 for t in teknolojiler]
    kaydet(sutun_svg(teknolojiler, medyanlar, baslik="Teknolojiye göre medyan yükleme hızı",
                     y_etiketi="Yükleme (Mbps)"), "cozum_o3_yukleme.svg")
    print("O3:", ", ".join(f"{t} {m:.1f}" for t, m in zip(teknolojiler, medyanlar)))


def histogram_svg(degerler, aralik, baslik, x_birim):
    """İ2: svg_cizim'e eklenebilecek yeni fonksiyon — sayısal değerlerden histogram."""
    kutular = Counter(int(d // aralik) for d in degerler)
    sira = range(0, max(kutular) + 1)
    etiketler = [f"{i * aralik:g}-{(i + 1) * aralik:g}" for i in sira]
    return sutun_svg(etiketler, [kutular[i] for i in sira], baslik=baslik,
                     y_etiketi="Adet", alt_not=f"Aralık genişliği: {aralik:g} {x_birim}")


def ileri_2_histogram():
    kaydet(histogram_svg([float(k["cozum_suresi_gun"]) for k in SIKAYET if k["durum"] == "Çözüldü"],
                         5, "Çözüm süresi dağılımı", "gün"), "cozum_i2_histogram.svg")
    print("İ2: histogram_svg -> outputs/gun06/cozum_i2_histogram.svg")


def ileri_3_html_isi_haritasi():
    """İ3: paketsiz ısı haritası = hücre rengi değere göre koyulaşan HTML tablo."""
    iller = [il for il, _ in Counter(k["il"] for k in SIKAYET).most_common()]
    kategoriler = sorted({k["kategori"] for k in SIKAYET})
    sayim = Counter((k["il"], k["kategori"]) for k in SIKAYET)
    en_buyuk = max(sayim.values())
    satirlar = []
    for il in iller:
        hucreler = []
        for kat in kategoriler:
            deger = sayim[(il, kat)]
            saydamlik = deger / en_buyuk        # 0 = beyaz, 1 = tam renk
            yazi = "white" if saydamlik > 0.55 else "#222"
            hucreler.append(f'<td style="background:rgba(22,125,154,{saydamlik:.2f});color:{yazi}">{deger}</td>')
        satirlar.append(f"<tr><th>{escape(il)}</th>{''.join(hucreler)}</tr>")
    html = (f'<!doctype html><html lang="tr"><meta charset="utf-8"><title>Isı Haritası</title>'
            f'<style>body{{font-family:Arial,sans-serif;margin:30px}}td,th{{padding:8px 12px;text-align:center}}</style>'
            f'<h2>İl x kategori şikâyet sayısı</h2><table><tr><th></th>'
            f'{"".join(f"<th>{escape(k)}</th>" for k in kategoriler)}</tr>{"".join(satirlar)}</table>'
            f'<p>Renk: {ANA_RENK}; koyu = çok.</p></html>')
    (ROOT / "outputs" / "gun06" / "cozum_i3_isi_haritasi.html").write_text(html, encoding="utf-8")
    print("İ3: outputs/gun06/cozum_i3_isi_haritasi.html")


if __name__ == "__main__":
    temel_1_operator_svg()
    temel_2_hizmet_yuzde()
    orta_1_cozulen_trend()
    orta_2_ping_araliklari()
    orta_3_yukleme_medyan()
    ileri_2_histogram()
    ileri_3_html_isi_haritasi()
    print("Gün 6 ek çözümler tamamlandı.")
