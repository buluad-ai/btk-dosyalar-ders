# -*- coding: utf-8 -*-
"""Hazır SVG çizim fonksiyonları (B planı — paket gerektirmez).

NE ÖĞRETİYOR?
    Grafik çizmek için matplotlib şart değildir. SVG, tarayıcının açabildiği bir
    METİN dosyasıdır: "şu koordinata şu boyda dikdörtgen çiz" gibi komutlardan oluşur.
    Bu dosyadaki fonksiyonlar o komutları sizin yerinize yazar. Siz yalnızca
    VERİ + ETİKET + BAŞLIK verirsiniz. (SVG sözdizimini ezberlemek hedef DEĞİLDİR.)

    Excel benzetmesi: Excel'de "Ekle > Grafik" dediğinizde içini bilmediğiniz bir
    çizim motoru çalışır. Bu dosya bizim küçük çizim motorumuzdur.

NASIL KULLANILIR?
    Aynı klasördeki başka bir scriptten:
        from svg_cizim import yatay_bar_svg, cizgi_svg, sutun_svg, kaydet
    Doğrudan çalıştırırsanız küçük bir deneme grafiği üretir:
        python gun06/svg_cizim.py

BEKLENEN ÇIKTI:
    SVG yardımcı deneme: outputs/gun06/svg_deneme.svg
"""
from html import escape   # "<", "&" gibi özel karakterleri güvenli metne çevirir
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Tek renk kuralı: tek seri = tek renk. Vurgu gerekiyorsa ikinci bir renk yeter.
ANA_RENK = "#167d9a"      # kursun ana rengi (02_svg_grafik.py ile aynı)
VURGU_RENK = "#eb6834"    # yalnızca dikkat çekmek istediğimiz çubuk için
GRI = "#8a8a86"           # eksen, ızgara, yardımcı yazılar
YAZI = "#222222"
YAZI_TIPI = "Segoe UI, Arial, sans-serif"   # Windows'ta Segoe UI, diğerlerinde Arial


def guzel_adim(en_buyuk, hedef_cizgi_sayisi=5):
    """Eksen için "yuvarlak" bir adım bulur: 1, 2, 5, 10, 20, 50 ...

    Örnek: en büyük değer 187 ise adım 50 olur, eksen 0-50-100-150-200 gider.
    Excel de eksen sayılarını kendiliğinden böyle yuvarlar.
    """
    if en_buyuk <= 0:
        return 1
    kaba = en_buyuk / hedef_cizgi_sayisi
    us = 1
    while us * 10 <= kaba:      # 10'un uygun kuvvetini bul (1, 10, 100 ...)
        us *= 10
    for carpan in (1, 2, 5, 10):  # 1x, 2x, 5x, 10x adaylarından ilk yeterli olan
        if us * carpan >= kaba:
            return us * carpan
    return us * 10


def _sayi_yaz(deger):
    """12.0 yerine 12, 9.53 için 9.5 yazar (grafik üstünde sade görünüm)."""
    if float(deger).is_integer():
        return str(int(deger))
    return f"{deger:.1f}"


def _ust_bilgi(genislik, yukseklik, baslik, alt_not):
    """Her grafikte ortak olan beyaz zemin + başlık + alt not parçaları."""
    parcalar = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{genislik}" height="{yukseklik}" '
        f'viewBox="0 0 {genislik} {yukseklik}" font-family="{YAZI_TIPI}">',
        f'<rect width="{genislik}" height="{yukseklik}" fill="white"/>',
        f'<text x="20" y="32" font-size="20" font-weight="bold" fill="{YAZI}">{escape(baslik)}</text>',
    ]
    if alt_not:
        parcalar.append(f'<text x="20" y="{yukseklik - 12}" font-size="13" fill="{GRI}">{escape(alt_not)}</text>')
    return parcalar


def yatay_bar_svg(etiketler, degerler, baslik, birim="", vurgula=None, alt_not=""):
    """Yatay çubuk grafiği. Uzun kategori adları (il, kanal) için en okunaklı biçim.

    etiketler : ["İstanbul", "Ankara", ...]
    degerler  : [185, 107, ...]   (aynı sırada)
    vurgula   : renkli gösterilecek tek etiket (ör. "Erzurum"); None ise hepsi aynı renk
    Sıralamayı ÇAĞIRAN yapar: büyükten küçüğe sıralı vermek okuru yorar değil, rahatlatır.
    """
    satir_yuksekligi = 34
    sol = 170                       # etiketler için ayrılan boşluk
    cizim_genisligi = 420
    genislik = sol + cizim_genisligi + 90         # ~680 piksel
    yukseklik = 80 + satir_yuksekligi * len(etiketler) + 40
    en_buyuk = max(degerler) if degerler else 1
    olcek = cizim_genisligi / en_buyuk          # 1 birim kaç piksel?

    parcalar = _ust_bilgi(genislik, yukseklik, baslik, alt_not)
    # Çubukların başladığı dikey çizgi = SIFIR noktası. Çubuk grafik hep 0'dan başlar.
    parcalar.append(f'<line x1="{sol}" y1="60" x2="{sol}" y2="{yukseklik - 40}" stroke="{GRI}"/>')
    for sira, (etiket, deger) in enumerate(zip(etiketler, degerler)):
        y = 64 + sira * satir_yuksekligi
        boy = deger * olcek
        renk = VURGU_RENK if etiket == vurgula else ANA_RENK
        parcalar.append(f'<text x="{sol - 8}" y="{y + 18}" font-size="14" text-anchor="end" '
                        f'fill="{YAZI}">{escape(str(etiket))}</text>')
        parcalar.append(f'<rect x="{sol}" y="{y}" width="{boy:.1f}" height="{satir_yuksekligi - 10}" '
                        f'fill="{renk}"><title>{escape(str(etiket))}: {_sayi_yaz(deger)} {escape(birim)}</title></rect>')
        # Değeri çubuğun hemen sağına yazıyoruz: okur ekseni takip etmek zorunda kalmaz.
        parcalar.append(f'<text x="{sol + boy + 6:.1f}" y="{y + 18}" font-size="14" '
                        f'fill="{YAZI}">{_sayi_yaz(deger)}</text>')
    if birim:
        parcalar.append(f'<text x="{genislik - 20}" y="52" font-size="13" text-anchor="end" '
                        f'fill="{GRI}">Birim: {escape(birim)}</text>')
    parcalar.append("</svg>")
    return "\n".join(parcalar)


def sutun_svg(etiketler, degerler, baslik, y_etiketi="", alt_not=""):
    """Dikey sütun grafiği: az sayıda (2-7) kategori karşılaştırması için."""
    sol, ust, alt = 70, 60, 70
    cizim_genisligi, cizim_yuksekligi = 560, 240
    genislik = sol + cizim_genisligi + 50          # tüm grafikler ~680 piksel: panelde aynı boyda görünsün
    yuva = cizim_genisligi / len(etiketler)       # her sütuna düşen yatay alan
    sutun_genisligi = min(yuva * 0.6, 90)          # sütun, alanının %60'ı (aralarda boşluk kalsın)
    yukseklik = ust + cizim_yuksekligi + alt
    adim = guzel_adim(max(degerler) if degerler else 1)
    tavan = adim * (int(max(degerler) / adim) + 1) if degerler else 1
    taban_y = ust + cizim_yuksekligi                     # 0 değerinin y koordinatı

    def y_konumu(deger):
        # SVG'de y aşağı doğru büyür; bu yüzden "tabandan yukarı" hesaplıyoruz.
        return taban_y - deger / tavan * cizim_yuksekligi

    parcalar = _ust_bilgi(genislik, yukseklik, baslik, alt_not)
    deger = 0
    while deger <= tavan:                                 # yatay ızgara çizgileri
        y = y_konumu(deger)
        parcalar.append(f'<line x1="{sol}" y1="{y:.1f}" x2="{sol + cizim_genisligi}" y2="{y:.1f}" stroke="#e5e5e2"/>')
        parcalar.append(f'<text x="{sol - 8}" y="{y + 5:.1f}" font-size="12" text-anchor="end" fill="{GRI}">{_sayi_yaz(deger)}</text>')
        deger += adim
    for sira, (etiket, deger) in enumerate(zip(etiketler, degerler)):
        x = sol + sira * yuva + (yuva - sutun_genisligi) / 2
        y = y_konumu(deger)
        parcalar.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{sutun_genisligi:.1f}" height="{taban_y - y:.1f}" fill="{ANA_RENK}">'
                        f'<title>{escape(str(etiket))}: {_sayi_yaz(deger)}</title></rect>')
        parcalar.append(f'<text x="{x + sutun_genisligi / 2:.1f}" y="{y - 6:.1f}" font-size="13" text-anchor="middle" fill="{YAZI}">{_sayi_yaz(deger)}</text>')
        parcalar.append(f'<text x="{x + sutun_genisligi / 2:.1f}" y="{taban_y + 20}" font-size="13" text-anchor="middle" fill="{YAZI}">{escape(str(etiket))}</text>')
    parcalar.append(f'<line x1="{sol}" y1="{taban_y}" x2="{sol + cizim_genisligi}" y2="{taban_y}" stroke="{GRI}"/>')
    if y_etiketi:
        parcalar.append(f'<text x="18" y="{ust + cizim_yuksekligi / 2}" font-size="13" fill="{GRI}" '
                        f'transform="rotate(-90 18 {ust + cizim_yuksekligi / 2})" text-anchor="middle">{escape(y_etiketi)}</text>')
    parcalar.append("</svg>")
    return "\n".join(parcalar)


def cizgi_svg(etiketler, degerler, baslik, y_etiketi="", alt_not=""):
    """Çizgi grafiği: ZAMAN içindeki değişim (ay ay şikâyet sayısı gibi).

    etiketler: x ekseni (ör. ["Oca", "Şub", ...]) — sırası zaman sırası olmalı!
    """
    sol, ust, alt = 70, 60, 70
    cizim_genisligi, cizim_yuksekligi = 560, 240
    genislik, yukseklik = sol + cizim_genisligi + 50, ust + cizim_yuksekligi + alt
    adim = guzel_adim(max(degerler))
    tavan = adim * (int(max(degerler) / adim) + 1)
    taban_y = ust + cizim_yuksekligi
    aralik = cizim_genisligi / max(len(degerler) - 1, 1)   # iki nokta arası yatay mesafe

    parcalar = _ust_bilgi(genislik, yukseklik, baslik, alt_not)
    deger = 0
    while deger <= tavan:
        y = taban_y - deger / tavan * cizim_yuksekligi
        parcalar.append(f'<line x1="{sol}" y1="{y:.1f}" x2="{sol + cizim_genisligi}" y2="{y:.1f}" stroke="#e5e5e2"/>')
        parcalar.append(f'<text x="{sol - 8}" y="{y + 5:.1f}" font-size="12" text-anchor="end" fill="{GRI}">{_sayi_yaz(deger)}</text>')
        deger += adim
    noktalar = []
    for sira, (etiket, deger) in enumerate(zip(etiketler, degerler)):
        x = sol + sira * aralik
        y = taban_y - deger / tavan * cizim_yuksekligi
        noktalar.append(f"{x:.1f},{y:.1f}")
        parcalar.append(f'<text x="{x:.1f}" y="{taban_y + 20}" font-size="13" text-anchor="middle" fill="{YAZI}">{escape(str(etiket))}</text>')
    parcalar.append(f'<polyline points="{" ".join(noktalar)}" fill="none" stroke="{ANA_RENK}" stroke-width="2.5"/>')
    for nokta, (etiket, deger) in zip(noktalar, zip(etiketler, degerler)):
        x, y = nokta.split(",")
        parcalar.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{ANA_RENK}" stroke="white" stroke-width="1.5">'
                        f'<title>{escape(str(etiket))}: {_sayi_yaz(deger)}</title></circle>')
    parcalar.append(f'<line x1="{sol}" y1="{taban_y}" x2="{sol + cizim_genisligi}" y2="{taban_y}" stroke="{GRI}"/>')
    if y_etiketi:
        parcalar.append(f'<text x="18" y="{ust + cizim_yuksekligi / 2}" font-size="13" fill="{GRI}" '
                        f'transform="rotate(-90 18 {ust + cizim_yuksekligi / 2})" text-anchor="middle">{escape(y_etiketi)}</text>')
    parcalar.append("</svg>")
    return "\n".join(parcalar)


def kaydet(svg_metni, dosya_adi):
    """SVG metnini outputs/gun06/<dosya_adi> olarak UTF-8 kaydeder; yolu döndürür."""
    klasor = ROOT / "outputs" / "gun06"
    klasor.mkdir(parents=True, exist_ok=True)
    yol = klasor / dosya_adi
    yol.write_text(svg_metni, encoding="utf-8")
    return yol


if __name__ == "__main__":
    # Küçük deneme: modül tek başına çalışıyor mu?
    deneme = sutun_svg(["Çözüldü", "İşlemde", "Reddedildi"], [415, 96, 89],
                       "Deneme: duruma göre şikâyet", y_etiketi="Şikâyet sayısı")
    kaydet(deneme, "svg_deneme.svg")
    print("SVG yardımcı deneme: outputs/gun06/svg_deneme.svg")
