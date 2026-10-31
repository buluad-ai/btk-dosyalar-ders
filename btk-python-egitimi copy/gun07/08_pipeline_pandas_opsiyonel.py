# -*- coding: utf-8 -*-
"""UÇTAN UCA PIPELINE — PAKETLİ SÜRÜM (pandas + matplotlib + openpyxl).

NE ÖĞRETİYOR?
    07_pipeline_stdlib.py ile AYNI 7 adımı, AYNI kurallarla, daha kısa kodla yapar:
        ADIM 1  OKU        pd.read_excel (varsayılan: data/btk_ornek_veri.xlsx, "Sikayetler" sayfası)
        ADIM 2  TEMİZLE    .str.strip(), .map(), pd.to_datetime(errors="coerce"), duplicated()
        ADIM 3  FİLTRELE   maske (True/False sütunu) ile satır seçme  (Excel: Otomatik Filtre)
        ADIM 4  SQLITE     DataFrame.to_sql(...)  tek satır
        ADIM 5  SORGULA    pd.read_sql(SQL) + groupby  (Excel: PivotTable)
        ADIM 6  GRAFİK     matplotlib PNG -> base64 metne çevirip HTML'e göm
        ADIM 7  RAPORLA    HTML + çok sayfalı Excel (ExcelWriter) + JSON
    İki sürüm aynı ANA SAYILARI vermeli: 09_iki_yol_karsilastir_opsiyonel.py kontrol eder.

NASIL ÇALIŞTIRILIR?
    python gun07/08_pipeline_pandas_opsiyonel.py
    python gun07/08_pipeline_pandas_opsiyonel.py --il Ankara --baslangic 2026-04-01 --bitis 2026-06-30
    python gun07/08_pipeline_pandas_opsiyonel.py --girdi data/sikayetler_kirli.csv

BEKLENEN ÇIKTI (argümansız):
    ANA SAYILAR
      Kayıt sayısı                  : 600
      ...
    Rapor: outputs/gun07/rapor_pandas.html
    (paket yoksa: ATLANDI: pandas kurulu değil — B planı: 07_pipeline_stdlib.py)
"""
import argparse
import base64
import io
import json
import sqlite3
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CIKTI = ROOT / "outputs" / "gun07"

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import openpyxl  # noqa: F401  (pandas Excel okurken/yazarken arka planda bunu kullanır)
except ImportError as hata:
    print(f"ATLANDI: {hata.name} kurulu değil — B planı: 07_pipeline_stdlib.py")
    sys.exit(0)

GECERLI_ILLER = ["İstanbul", "Ankara", "İzmir", "Antalya", "Konya", "Bursa", "Trabzon", "Erzurum"]
GECERLI_OPERATORLER = ["Operatör A", "Operatör B", "Operatör C", "Operatör D"]
GECERLI_DURUMLAR = ["Çözüldü", "Reddedildi", "İşlemde"]
AY_ADLARI = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]


def tr_kucuk(metin):
    """Türkçe doğru küçük harf (bkz. 07_pipeline_stdlib.py)."""
    return metin.strip().replace("İ", "i").replace("I", "ı").lower()


IL_ESLEME = {tr_kucuk(il): il for il in GECERLI_ILLER}
OPERATOR_ESLEME = {tr_kucuk(op): op for op in GECERLI_OPERATORLER}


def parametreleri_al():
    parser = argparse.ArgumentParser(description="Şikâyet verisinden HTML + Excel rapor üretir (pandas).")
    parser.add_argument("--girdi", default="data/btk_ornek_veri.xlsx",
                        help="Okunacak dosya (.xlsx veya .csv). Varsayılan: data/btk_ornek_veri.xlsx")
    parser.add_argument("--il")
    parser.add_argument("--operator")
    parser.add_argument("--baslangic", type=date.fromisoformat, help="YYYY-AA-GG (dahil)")
    parser.add_argument("--bitis", type=date.fromisoformat, help="YYYY-AA-GG (dahil)")
    args = parser.parse_args()
    if args.baslangic and args.bitis and args.baslangic > args.bitis:
        parser.error("--baslangic tarihi --bitis tarihinden sonra olamaz")
    return args


# ---------------------------------------------------------------- ADIM 1: OKU
def oku(dosya):
    # dtype=str: her hücreyi METİN olarak al; temizlik kurallarını biz uygulayacağız.
    # (Aksi halde pandas "on iki" gibi bir değeri görünce tüm sütunu metin yapar, kafa karışır.)
    if dosya.suffix.lower() == ".xlsx":
        tablo = pd.read_excel(dosya, sheet_name="Sikayetler", dtype=str)
    else:
        tablo = pd.read_csv(dosya, dtype=str, encoding="utf-8-sig")
    return tablo.fillna("")      # boş hücre -> "" (stdlib sürümüyle aynı başlangıç)


# ------------------------------------------------------------ ADIM 2: TEMİZLE
def temizle(ham):
    """07_pipeline_stdlib.py'deki kuralların AYNISI, sütun sütun (vektörel) uygulanır."""
    df = ham.apply(lambda sutun: sutun.str.strip())                  # her sütunda KIRP
    df["il"] = df["il"].map(lambda x: IL_ESLEME.get(tr_kucuk(x), x))   # " ankara " -> "Ankara"
    df["operator"] = df["operator"].map(lambda x: OPERATOR_ESLEME.get(tr_kucuk(x), x))

    tarih = pd.to_datetime(df["tarih"], format="%Y-%m-%d", errors="coerce")   # geçersiz -> NaT
    sure = pd.to_numeric(df["cozum_suresi_gun"], errors="coerce")           # "on iki" -> NaN
    memnuniyet = pd.to_numeric(df["memnuniyet"], errors="coerce")
    sure_tam = df["cozum_suresi_gun"].str.lstrip("-").str.isdigit()          # "7.5" tam sayı değil
    memn_tam = df["memnuniyet"].str.lstrip("-").str.isdigit()

    # (kural maskesi, neden) — sıra stdlib sürümüyle aynı; ilk bozulan kural yazılır
    kurallar = [
        (~df["il"].isin(GECERLI_ILLER), "bilinmeyen il"),
        (~df["operator"].isin(GECERLI_OPERATORLER), "bilinmeyen operatör"),
        (tarih.isna(), "geçersiz tarih"),
        (df["kategori"] == "", "kategori boş"),
        (~df["durum"].isin(GECERLI_DURUMLAR), "bilinmeyen durum"),
        ((df["cozum_suresi_gun"] != "") & ~(sure_tam & (sure >= 0)), "geçersiz çözüm süresi"),
        ((df["memnuniyet"] != "") & ~(memn_tam & memnuniyet.between(1, 5)), "memnuniyet 1-5 dışında"),
    ]
    neden = pd.Series("", index=df.index)
    for maske, metin in kurallar:
        neden = neden.mask((neden == "") & maske, metin)   # henüz nedeni olmayan ve kuralı bozan satıra yaz
    # Tekrar kontrolü yalnızca kurallardan geçen satırlar arasında yapılır (stdlib ile aynı)
    gecen = neden == ""
    tekrar = gecen & df["sikayet_no"].where(gecen).duplicated(keep="first")
    neden = neden.mask(tekrar, "tekrar eden kayıt")

    sorunlu = pd.DataFrame({"sikayet_no": df.loc[neden != "", "sikayet_no"], "neden": neden[neden != ""]})
    temiz = df[neden == ""].copy()
    # Tür dönüşümleri: metin -> sayı / tarih; boş -> NaN (SQL'de NULL)
    temiz["sikayet_no"] = temiz["sikayet_no"].astype(int)
    temiz["tarih"] = tarih[neden == ""].dt.date.astype(str)
    for sutun in ["cozum_suresi_gun", "memnuniyet"]:
        temiz[sutun] = pd.to_numeric(temiz[sutun], errors="coerce").astype("Int64")   # Int64: boş olabilen tam sayı
    temiz["itiraz_tutari_tl"] = pd.to_numeric(temiz["itiraz_tutari_tl"], errors="coerce")
    return temiz, sorunlu


# ----------------------------------------------------------- ADIM 3: FİLTRELE
def filtrele(df, args):
    maske = pd.Series(True, index=df.index)          # başta herkes seçili
    if args.il:
        maske &= df["il"] == args.il                  # &= : "VE bu koşul da sağlansın"
    if args.operator:
        maske &= df["operator"] == args.operator
    if args.baslangic:
        maske &= df["tarih"] >= args.baslangic.isoformat()   # YYYY-AA-GG metni sıralanabilir
    if args.bitis:
        maske &= df["tarih"] <= args.bitis.isoformat()
    return df[maske]


def png_base64(fig):
    """Grafiği diske yazmadan bellekte PNG'ye çevirip HTML'e gömülecek metne dönüştürür."""
    tampon = io.BytesIO()
    fig.savefig(tampon, format="png", dpi=120)
    plt.close(fig)
    return base64.b64encode(tampon.getvalue()).decode("ascii")


def main():
    args = parametreleri_al()
    girdi = Path(args.girdi)
    if not girdi.is_absolute():
        girdi = ROOT / girdi
    CIKTI.mkdir(parents=True, exist_ok=True)

    ham = oku(girdi)                                                       # ADIM 1
    temiz, sorunlu = temizle(ham)                                          # ADIM 2
    secilen = filtrele(temiz, args)                                        # ADIM 3
    print(f"Okunan: {len(ham)} | Temiz: {len(temiz)} | Sorunlu: {len(sorunlu)} | Filtre sonrası: {len(secilen)}")
    if secilen.empty:
        print("Filtreye uyan kayıt yok; rapor üretilmedi. İl/operatör yazımını ve tarihleri kontrol edin.")
        return

    hedefler = pd.read_excel(ROOT / "data" / "btk_ornek_veri.xlsx", sheet_name="Hedefler")

    # ADIM 4: SQLite'a yaz (if_exists="replace": tablo varsa sil, yeniden oluştur)
    with sqlite3.connect(CIKTI / "pipeline_pandas.sqlite") as baglanti:
        secilen.to_sql("sikayetler", baglanti, if_exists="replace", index=False)
        hedefler.to_sql("hedefler", baglanti, if_exists="replace", index=False)
        # ADIM 5a: SQL ile sorgu -> sonuç doğrudan DataFrame olarak gelir
        kategori = pd.read_sql("""
            SELECT s.kategori, COUNT(*) AS adet,
                   SUM(s.durum = 'Çözüldü') AS cozulen,
                   AVG(CASE WHEN s.durum = 'Çözüldü' THEN s.cozum_suresi_gun END) AS ort_gun,
                   h.hedef_gun,
                   SUM(s.durum = 'Çözüldü' AND s.cozum_suresi_gun > h.hedef_gun) AS hedef_asan
            FROM sikayetler s LEFT JOIN hedefler h ON s.kategori = h.kategori
            GROUP BY s.kategori ORDER BY adet DESC, s.kategori""", baglanti)
    baglanti.close()   # with bloğu commit eder ama bağlantıyı kapatmaz; Windows'ta dosya kilidi kalmasın

    # ADIM 5b: aynı türden özetleri pandas ile (groupby = PivotTable)
    cozulen_df = secilen[secilen["durum"] == "Çözüldü"]
    aylik = secilen.groupby(secilen["tarih"].str[:7]).size()
    kanal = (cozulen_df.groupby("kanal")["cozum_suresi_gun"].agg(["count", "mean"])
             .reset_index().sort_values(["mean", "kanal"]))
    il = secilen.groupby("il").size().reset_index(name="adet").sort_values(["adet", "il"], ascending=[False, True])

    kayit = len(secilen)
    cozulen = len(cozulen_df)
    ana = {
        "kayit_sayisi": kayit,
        "cozulen": cozulen,
        "reddedilen": int((secilen["durum"] == "Reddedildi").sum()),
        "islemde": int((secilen["durum"] == "İşlemde").sum()),
        "cozulme_orani_yuzde": round(cozulen / kayit * 100, 1),
        "ort_cozum_suresi_gun": round(float(cozulen_df["cozum_suresi_gun"].mean()), 2) if cozulen else None,
        "medyan_cozum_suresi_gun": float(cozulen_df["cozum_suresi_gun"].median()) if cozulen else None,
        "hedef_asim_orani_yuzde": round(int(kategori["hedef_asan"].fillna(0).sum()) / cozulen * 100, 1) if cozulen else None,
        "en_cok_sikayet_kategori": kategori.iloc[0]["kategori"],
        "en_yogun_il": il.iloc[0]["il"],
        "en_hizli_kanal": kanal.iloc[0]["kanal"] if len(kanal) else None,
        "sorunlu_kayit": len(sorunlu),
    }

    # ADIM 6: grafikler (PNG -> base64)
    fig, ax = plt.subplots(figsize=(8, 4))
    sirali = kategori.sort_values("adet")
    ax.bar_label(ax.barh(sirali["kategori"], sirali["adet"], color="#167d9a"), padding=3)
    ax.set(title="Kategoriye göre şikâyet", xlabel="Şikâyet sayısı (adet)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    png_kategori = png_base64(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot([AY_ADLARI[int(a[5:7]) - 1] for a in aylik.index], aylik.values, marker="o", color="#167d9a")
    ax.set(title="Aylık şikâyet sayısı", xlabel="Ay", ylabel="Şikâyet sayısı (adet)")
    ax.set_ylim(bottom=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    png_aylik = png_base64(fig)

    fig, ax = plt.subplots(figsize=(8, 3.5))
    kanal_sirali = kanal.sort_values("mean", ascending=False)
    ax.bar_label(ax.barh(kanal_sirali["kanal"], kanal_sirali["mean"], color="#167d9a"), fmt="%.1f", padding=3)
    ax.set(title="Kanala göre ortalama çözüm süresi (yalnızca Çözüldü)", xlabel="Ortalama çözüm süresi (gün)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    png_kanal = png_base64(fig)

    # ADIM 7: raporlar
    filtre_metni = ", ".join(f"{ad}={deger}" for ad, deger in
                             [("il", args.il), ("operatör", args.operator),
                              ("başlangıç", args.baslangic), ("bitiş", args.bitis)] if deger) or "yok (tüm veri)"
    etiketler = {"kayit_sayisi": "Kayıt sayısı", "cozulen": "Çözülen", "reddedilen": "Reddedilen",
                 "islemde": "İşlemde", "cozulme_orani_yuzde": "Çözülme oranı (%)",
                 "ort_cozum_suresi_gun": "Ort. çözüm süresi (gün)", "medyan_cozum_suresi_gun": "Medyan çözüm süresi (gün)",
                 "hedef_asim_orani_yuzde": "Hedef süreyi aşan çözüm (%)", "en_cok_sikayet_kategori": "En çok şikâyet kategorisi",
                 "en_yogun_il": "En yoğun il", "en_hizli_kanal": "En hızlı kanal", "sorunlu_kayit": "Sorunlu (ayrılan) kayıt"}
    ana_tablo = pd.DataFrame({"Gösterge": [etiketler[a] for a in ana], "Değer": [str(d) for d in ana.values()]})
    kategori_tablo = kategori.rename(columns={"kategori": "Kategori", "adet": "Şikâyet", "cozulen": "Çözülen",
                                              "ort_gun": "Ort. çözüm (gün)", "hedef_gun": "Hedef (gün)",
                                              "hedef_asan": "Hedefi aşan"}).round(1)
    html = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Şikâyet Raporu</title>
<style>body{{font-family:"Segoe UI",Arial,sans-serif;max-width:1000px;margin:30px auto;padding:0 16px;color:#222}}
table{{border-collapse:collapse;margin:10px 0 24px}}td,th{{padding:6px 12px;border-bottom:1px solid #ddd;text-align:left}}
img{{max-width:100%;display:block;margin:10px 0}}.not{{color:#666}}</style></head><body>
<h1>Şikâyet analiz raporu</h1>
<p class="not">Kaynak: {escape(girdi.name)} · Filtre: {escape(filtre_metni)} · Sürüm: pandas + matplotlib · Sentetik veri</p>
<h2>Ana sayılar</h2>{ana_tablo.to_html(index=False, border=0)}
<h2>Grafikler</h2>
<img alt="Kategoriye göre şikâyet" src="data:image/png;base64,{png_kategori}">
<img alt="Aylık şikâyet" src="data:image/png;base64,{png_aylik}">
<img alt="Kanala göre çözüm süresi" src="data:image/png;base64,{png_kanal}">
<h2>Kategori tablosu</h2>{kategori_tablo.to_html(index=False, border=0)}
<p class="not">Sınırlılık: ortalama çözüm süresi yalnızca "Çözüldü" kayıtlardan hesaplanır.</p></body></html>"""
    (CIKTI / "rapor_pandas.html").write_text(html, encoding="utf-8")
    (CIKTI / "ozet_pandas.json").write_text(
        json.dumps({"filtre": filtre_metni, "ana_sayilar": ana}, ensure_ascii=False, indent=2), encoding="utf-8")

    try:
        # ExcelWriter: tek dosyaya birden çok sayfa yazmak için
        with pd.ExcelWriter(CIKTI / "ozet_pandas.xlsx", engine="openpyxl") as yazici:
            ana_tablo.to_excel(yazici, sheet_name="Ana_Sayilar", index=False)
            kategori_tablo.to_excel(yazici, sheet_name="Kategori", index=False)
            aylik.rename_axis("Ay").reset_index(name="Şikâyet").to_excel(yazici, sheet_name="Aylik", index=False)
            kanal.rename(columns={"kanal": "Kanal", "count": "Çözülen", "mean": "Ort. çözüm (gün)"}).round(2) \
                .to_excel(yazici, sheet_name="Kanal", index=False)
            sorunlu.to_excel(yazici, sheet_name="Sorunlu_Kayitlar", index=False)
        print("Excel özet: outputs/gun07/ozet_pandas.xlsx")
    except PermissionError:
        print("UYARI: ozet_pandas.xlsx yazılamadı. Dosya Excel'de açık olabilir; kapatıp tekrar çalıştırın.")

    print("ANA SAYILAR")
    for anahtar, deger in ana.items():
        print(f"  {etiketler[anahtar]:<30}: {deger}")
    if len(sorunlu):
        print("Sorunlu kayıtlar:", ", ".join(f"{n} ({s})" for n, s in zip(sorunlu["sikayet_no"], sorunlu["neden"])))
    print("Rapor: outputs/gun07/rapor_pandas.html")


if __name__ == "__main__":
    main()
