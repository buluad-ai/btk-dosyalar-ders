# -*- coding: utf-8 -*-
"""UÇTAN UCA PIPELINE — B PLANI (yalnızca standart kütüphane).

NE ÖĞRETİYOR?
    Bir analistin her ay elle yaptığı işi tek komuta bağlamak:
        ADIM 1  OKU        CSV (veya .xlsx) dosyasını oku
        ADIM 2  TEMİZLE    boşlukları sil, il/operatör yazımını düzelt, hatalı satırı ayır
        ADIM 3  FİLTRELE   komut satırından gelen il / operatör / tarih aralığı
        ADIM 4  SQLITE     temiz veriyi veritabanı dosyasına yaz
        ADIM 5  SORGULA    SQL ile özet tablolar (GROUP BY, JOIN)
        ADIM 6  GRAFİK     SVG grafikleri üret (gun06/svg_cizim.py yeniden kullanılır)
        ADIM 7  RAPORLA    tek HTML rapor (grafikler gömülü) + Excel özet + JSON
    Aynı işi pandas+matplotlib ile yapan sürüm: 08_pipeline_pandas_opsiyonel.py
    İkisinin aynı ANA SAYILARI ürettiğini kontrol eden: 09_iki_yol_karsilastir_opsiyonel.py

    Excel karşılığı: Power Query (oku+temizle) + PivotTable (özet) + grafik + "Farklı kaydet".
    Farkı: bir kez yazılır, her ay yeni dosyayla tek komutla tekrar çalışır.

NASIL ÇALIŞTIRILIR?
    python gun07/07_pipeline_stdlib.py                                  (tüm veri)
    python gun07/07_pipeline_stdlib.py --il Ankara --baslangic 2026-04-01 --bitis 2026-06-30
    python gun07/07_pipeline_stdlib.py --operator "Operatör B"
    python gun07/07_pipeline_stdlib.py --girdi data/sikayetler_kirli.csv     (temizlik kurallarını gör)
    python gun07/07_pipeline_stdlib.py --help                            (tüm seçenekler)

BEKLENEN ÇIKTI (argümansız):
    ANA SAYILAR
      Kayıt sayısı          : 600
      Çözülen               : 415
      ...
    Rapor: outputs/gun07/rapor_stdlib.html
"""
import argparse
import csv
import json
import sqlite3
import statistics
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CIKTI = ROOT / "outputs" / "gun07"

# Kendi klasörümüzdeki basit_xlsx.py ve geçen haftanın çizim aleti gun06/svg_cizim.py:
sys.path.insert(0, str(ROOT / "gun06"))   # "gun06 klasörüne de bak" demek
from basit_xlsx import xlsx_oku, xlsx_yaz          # noqa: E402  (import'un yeri bilinçli)
from svg_cizim import cizgi_svg, yatay_bar_svg     # noqa: E402

# Referans listeler (Excel'deki "Veri Doğrulama > Liste" gibi): geçerli yazımlar bunlar.
GECERLI_ILLER = ["İstanbul", "Ankara", "İzmir", "Antalya", "Konya", "Bursa", "Trabzon", "Erzurum"]
GECERLI_OPERATORLER = ["Operatör A", "Operatör B", "Operatör C", "Operatör D"]
GECERLI_DURUMLAR = ["Çözüldü", "Reddedildi", "İşlemde"]
AY_ADLARI = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]


def tr_kucuk(metin):
    """Türkçe doğru küçük harf: "İSTANBUL" -> "istanbul", "IĞDIR" -> "ığdır".

    Python'un .lower() fonksiyonu "I" harfini "i" yapar (İngilizce kuralı);
    Türkçede "I" -> "ı", "İ" -> "i" olmalı. Önce bu iki harfi elle çeviriyoruz.
    """
    return metin.strip().replace("İ", "i").replace("I", "ı").lower()


# "ankara" -> "Ankara" eşleme sözlükleri (DÜŞEYARA tablosu gibi)
IL_ESLEME = {tr_kucuk(il): il for il in GECERLI_ILLER}
OPERATOR_ESLEME = {tr_kucuk(op): op for op in GECERLI_OPERATORLER}


# ============================================================================
# ADIM 0: Komut satırı parametreleri
# ============================================================================
def parametreleri_al():
    parser = argparse.ArgumentParser(description="Şikâyet verisinden HTML + Excel rapor üretir (paketsiz).")
    parser.add_argument("--girdi", default="data/sikayetler.csv",
                        help="Okunacak dosya (.csv veya .xlsx), proje köküne göre. Varsayılan: data/sikayetler.csv")
    parser.add_argument("--il", help='Yalnızca bu il, ör. --il Ankara')
    parser.add_argument("--operator", help='Yalnızca bu operatör, ör. --operator "Operatör A"')
    parser.add_argument("--baslangic", type=date.fromisoformat, help="İlk tarih (dahil), YYYY-AA-GG")
    parser.add_argument("--bitis", type=date.fromisoformat, help="Son tarih (dahil), YYYY-AA-GG")
    args = parser.parse_args()
    if args.baslangic and args.bitis and args.baslangic > args.bitis:
        parser.error("--baslangic tarihi --bitis tarihinden sonra olamaz")   # mesaj yazar, çıkar
    return args


# ============================================================================
# ADIM 1: OKU
# ============================================================================
def oku(dosya):
    """CSV veya XLSX okur; her satırı METİN değerli sözlük olarak döndürür."""
    if dosya.suffix.lower() == ".xlsx":
        satirlar = xlsx_oku(dosya, "Sikayetler")
        # Excel'den sayı/None gelebilir; CSV ile aynı olsun diye hepsini metne çeviriyoruz.
        return [{k: "" if v is None else str(v) for k, v in s.items()} for s in satirlar]
    with dosya.open(encoding="utf-8-sig", newline="") as f:   # -sig: Excel'in BOM işaretini de tolere eder
        return list(csv.DictReader(f))


# ============================================================================
# ADIM 2: TEMİZLE
# ============================================================================
def tam_sayi_mi(metin):
    """ "12" -> True, "-3" -> True, "on iki" -> False, "7.5" -> False """
    return metin.lstrip("-").isdigit()


def temizle(ham_satirlar):
    """Kuralları sırayla uygular. Geçen satır 'temiz', kalan satır 'sorunlu' listesine gider.

    KURALLAR (sıra önemli; ilk bozulan kural "neden" olarak yazılır):
      1. il/operatör yazımı düzeltilir (" ankara " -> "Ankara"); listede yoksa sorunlu
      2. tarih YYYY-AA-GG biçiminde gerçek bir tarih olmalı (31.02.2026 olmaz)
      3. kategori boş olamaz; durum bilinen üç değerden biri olmalı
      4. çözüm süresi doluysa 0 veya pozitif TAM sayı olmalı ("on iki", -3 olmaz)
      5. memnuniyet doluysa 1-5 arası tam sayı olmalı
      6. aynı sikayet_no ikinci kez gelirse tekrar sayılır, ilki tutulur
    """
    temiz, sorunlu, gorulen_no = [], [], set()
    for ham in ham_satirlar:
        s = {k: (v or "").strip() for k, v in ham.items()}    # tüm hücrelerde baş/son boşluğu sil (KIRP)
        s["il"] = IL_ESLEME.get(tr_kucuk(s["il"]), s["il"])
        s["operator"] = OPERATOR_ESLEME.get(tr_kucuk(s["operator"]), s["operator"])
        neden = None
        try:
            date.fromisoformat(s["tarih"])
            tarih_gecerli = True
        except ValueError:
            tarih_gecerli = False

        if s["il"] not in GECERLI_ILLER:
            neden = "bilinmeyen il"
        elif s["operator"] not in GECERLI_OPERATORLER:
            neden = "bilinmeyen operatör"
        elif not tarih_gecerli:
            neden = "geçersiz tarih"
        elif s["kategori"] == "":
            neden = "kategori boş"
        elif s["durum"] not in GECERLI_DURUMLAR:
            neden = "bilinmeyen durum"
        elif s["cozum_suresi_gun"] and not (tam_sayi_mi(s["cozum_suresi_gun"]) and int(s["cozum_suresi_gun"]) >= 0):
            neden = "geçersiz çözüm süresi"
        elif s["memnuniyet"] and not (tam_sayi_mi(s["memnuniyet"]) and 1 <= int(s["memnuniyet"]) <= 5):
            neden = "memnuniyet 1-5 dışında"
        elif s["sikayet_no"] in gorulen_no:
            neden = "tekrar eden kayıt"

        if neden:
            sorunlu.append({"sikayet_no": s["sikayet_no"], "neden": neden})
            continue
        gorulen_no.add(s["sikayet_no"])
        # Türleri dönüştür: metin -> sayı; boş -> None (SQL'de NULL)
        s["sikayet_no"] = int(s["sikayet_no"])
        s["cozum_suresi_gun"] = int(s["cozum_suresi_gun"]) if s["cozum_suresi_gun"] else None
        s["memnuniyet"] = int(s["memnuniyet"]) if s["memnuniyet"] else None
        s["itiraz_tutari_tl"] = float(s["itiraz_tutari_tl"]) if s["itiraz_tutari_tl"] else None
        temiz.append(s)
    return temiz, sorunlu


# ============================================================================
# ADIM 3: FİLTRELE
# ============================================================================
def filtrele(satirlar, args):
    sonuc = []
    for s in satirlar:
        tarih = date.fromisoformat(s["tarih"])
        if args.il and s["il"] != args.il:
            continue                    # bu satırı atla, sonrakine geç
        if args.operator and s["operator"] != args.operator:
            continue
        if args.baslangic and tarih < args.baslangic:
            continue
        if args.bitis and tarih > args.bitis:
            continue
        sonuc.append(s)
    return sonuc


# ============================================================================
# ADIM 4: SQLITE'A YAZ
# ============================================================================
def sqlite_yaz(satirlar, hedefler, db_yolu):
    baglanti = sqlite3.connect(db_yolu)
    baglanti.execute("DROP TABLE IF EXISTS sikayetler")    # her çalıştırmada sıfırdan: tekrar çalıştırılabilir
    baglanti.execute("DROP TABLE IF EXISTS hedefler")
    baglanti.execute("""CREATE TABLE sikayetler (
        sikayet_no INTEGER PRIMARY KEY, tarih TEXT, il TEXT, operator TEXT, hizmet TEXT,
        kategori TEXT, kanal TEXT, durum TEXT, cozum_suresi_gun INTEGER,
        memnuniyet INTEGER, itiraz_tutari_tl REAL)""")
    baglanti.execute("CREATE TABLE hedefler (kategori TEXT PRIMARY KEY, hedef_gun INTEGER)")
    sutunlar = ["sikayet_no", "tarih", "il", "operator", "hizmet", "kategori", "kanal", "durum",
                "cozum_suresi_gun", "memnuniyet", "itiraz_tutari_tl"]
    # ? işaretleri: değerler SQL metnine yapıştırılmaz, güvenle ayrı gönderilir
    baglanti.executemany(f"INSERT INTO sikayetler VALUES ({','.join('?' * len(sutunlar))})",
                         [[s[k] for k in sutunlar] for s in satirlar])
    baglanti.executemany("INSERT INTO hedefler VALUES (?, ?)",
                         [(h["kategori"], h["hedef_gun"]) for h in hedefler])
    baglanti.commit()
    return baglanti


# ============================================================================
# ADIM 5: SQL İLE SORGULA
# ============================================================================
def sorgula(baglanti):
    genel = baglanti.execute("""
        SELECT COUNT(*),
               SUM(durum = 'Çözüldü'), SUM(durum = 'Reddedildi'), SUM(durum = 'İşlemde'),
               AVG(CASE WHEN durum = 'Çözüldü' THEN cozum_suresi_gun END)
        FROM sikayetler""").fetchone()
    # JOIN: her şikâyetin kategorisine ait hedef günü hedefler tablosundan getir (DÜŞEYARA)
    kategori = baglanti.execute("""
        SELECT s.kategori, COUNT(*) AS adet,
               SUM(s.durum = 'Çözüldü') AS cozulen,
               AVG(CASE WHEN s.durum = 'Çözüldü' THEN s.cozum_suresi_gun END) AS ort_gun,
               h.hedef_gun,
               SUM(s.durum = 'Çözüldü' AND s.cozum_suresi_gun > h.hedef_gun) AS hedef_asan
        FROM sikayetler s LEFT JOIN hedefler h ON s.kategori = h.kategori
        GROUP BY s.kategori ORDER BY adet DESC, s.kategori""").fetchall()
    aylik = baglanti.execute("""
        SELECT substr(tarih, 1, 7) AS ay, COUNT(*) FROM sikayetler GROUP BY ay ORDER BY ay""").fetchall()
    kanal = baglanti.execute("""
        SELECT kanal, COUNT(*), AVG(cozum_suresi_gun) FROM sikayetler
        WHERE durum = 'Çözüldü' GROUP BY kanal ORDER BY AVG(cozum_suresi_gun), kanal""").fetchall()
    il = baglanti.execute("""
        SELECT il, COUNT(*) AS adet FROM sikayetler GROUP BY il ORDER BY adet DESC, il""").fetchall()
    return genel, kategori, aylik, kanal, il


def yuvarla(sayi, basamak=2):
    return None if sayi is None else round(sayi, basamak)


# ============================================================================
# ANA AKIŞ
# ============================================================================
def main():
    args = parametreleri_al()
    girdi = Path(args.girdi)
    if not girdi.is_absolute():
        girdi = ROOT / girdi                 # göreli yol proje köküne göre çözülür
    CIKTI.mkdir(parents=True, exist_ok=True)

    ham = oku(girdi)                                                     # ADIM 1
    temiz, sorunlu = temizle(ham)                                        # ADIM 2
    secilen = filtrele(temiz, args)                                      # ADIM 3
    print(f"Okunan: {len(ham)} | Temiz: {len(temiz)} | Sorunlu: {len(sorunlu)} | Filtre sonrası: {len(secilen)}")
    if not secilen:
        print("Filtreye uyan kayıt yok; rapor üretilmedi. İl/operatör yazımını ve tarihleri kontrol edin.")
        return

    hedefler = xlsx_oku(ROOT / "data" / "btk_ornek_veri.xlsx", "Hedefler")
    baglanti = sqlite_yaz(secilen, hedefler, CIKTI / "pipeline_stdlib.sqlite")    # ADIM 4
    genel, kategori, aylik, kanal, il = sorgula(baglanti)                         # ADIM 5
    baglanti.close()

    kayit, cozulen, reddedilen, islemde, ort_gun = genel
    hedef_asan = sum(k[5] or 0 for k in kategori)
    ana = {   # İki sürümün karşılaştıracağı ANA SAYILAR (anahtar adları iki dosyada aynı)
        "kayit_sayisi": kayit,
        "cozulen": cozulen,
        "reddedilen": reddedilen,
        "islemde": islemde,
        "cozulme_orani_yuzde": round(cozulen / kayit * 100, 1),
        "ort_cozum_suresi_gun": yuvarla(ort_gun),
        "medyan_cozum_suresi_gun": float(statistics.median(
            s["cozum_suresi_gun"] for s in secilen if s["durum"] == "Çözüldü")) if cozulen else None,
        "hedef_asim_orani_yuzde": round(hedef_asan / cozulen * 100, 1) if cozulen else None,
        "en_cok_sikayet_kategori": kategori[0][0],
        "en_yogun_il": il[0][0],
        "en_hizli_kanal": kanal[0][0] if kanal else None,
        "sorunlu_kayit": len(sorunlu),
    }

    # ---- ADIM 6: GRAFİKLER (SVG metni) ----
    svg_kategori = yatay_bar_svg([k[0] for k in kategori], [k[1] for k in kategori],
                                 baslik="Kategoriye göre şikâyet", birim="adet")
    svg_aylik = cizgi_svg([AY_ADLARI[int(a[0][5:7]) - 1] for a in aylik], [a[1] for a in aylik],
                          baslik="Aylık şikâyet sayısı", y_etiketi="Şikâyet (adet)")
    svg_kanal = yatay_bar_svg([k[0] for k in kanal], [round(k[2], 1) for k in kanal],
                              baslik="Kanala göre ortalama çözüm süresi", birim="gün",
                              alt_not="Yalnızca 'Çözüldü' kayıtlar. Kısa = hızlı.")

    # ---- ADIM 7: RAPORLAR ----
    filtre_metni = ", ".join(f"{ad}={deger}" for ad, deger in
                             [("il", args.il), ("operatör", args.operator),
                              ("başlangıç", args.baslangic), ("bitiş", args.bitis)] if deger) or "yok (tüm veri)"
    etiketler = {"kayit_sayisi": "Kayıt sayısı", "cozulen": "Çözülen", "reddedilen": "Reddedilen",
                 "islemde": "İşlemde", "cozulme_orani_yuzde": "Çözülme oranı (%)",
                 "ort_cozum_suresi_gun": "Ort. çözüm süresi (gün)", "medyan_cozum_suresi_gun": "Medyan çözüm süresi (gün)",
                 "hedef_asim_orani_yuzde": "Hedef süreyi aşan çözüm (%)", "en_cok_sikayet_kategori": "En çok şikâyet kategorisi",
                 "en_yogun_il": "En yoğun il", "en_hizli_kanal": "En hızlı kanal", "sorunlu_kayit": "Sorunlu (ayrılan) kayıt"}
    kategori_satirlari = "".join(
        f"<tr><td>{escape(k[0])}</td><td>{k[1]}</td><td>{k[2]}</td><td>{yuvarla(k[3], 1)}</td>"
        f"<td>{k[4]}</td><td>{k[5]}</td></tr>" for k in kategori)
    ana_satirlari = "".join(f"<tr><td>{escape(etiketler[a])}</td><td>{escape(str(d))}</td></tr>" for a, d in ana.items())
    html = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Şikâyet Raporu</title>
<style>body{{font-family:"Segoe UI",Arial,sans-serif;max-width:1000px;margin:30px auto;padding:0 16px;color:#222}}
table{{border-collapse:collapse;margin:10px 0 24px}}td,th{{padding:6px 12px;border-bottom:1px solid #ddd;text-align:left}}
svg{{width:100%;height:auto;max-width:720px;display:block;margin:10px 0}}.not{{color:#666}}</style></head><body>
<h1>Şikâyet analiz raporu</h1>
<p class="not">Kaynak: {escape(girdi.name)} · Filtre: {escape(filtre_metni)} · Sürüm: standart kütüphane (B planı) · Sentetik veri</p>
<h2>Ana sayılar</h2><table>{ana_satirlari}</table>
<h2>Grafikler</h2>{svg_kategori}{svg_aylik}{svg_kanal}
<h2>Kategori tablosu</h2>
<table><tr><th>Kategori</th><th>Şikâyet</th><th>Çözülen</th><th>Ort. çözüm (gün)</th><th>Hedef (gün)</th><th>Hedefi aşan</th></tr>
{kategori_satirlari}</table>
<p class="not">Sınırlılık: ortalama çözüm süresi yalnızca "Çözüldü" kayıtlardan hesaplanır; kategori karışımı
farklı olan gruplar doğrudan karşılaştırılırken dikkatli olunmalıdır.</p></body></html>"""
    (CIKTI / "rapor_stdlib.html").write_text(html, encoding="utf-8")
    (CIKTI / "ozet_stdlib.json").write_text(
        json.dumps({"filtre": filtre_metni, "ana_sayilar": ana}, ensure_ascii=False, indent=2), encoding="utf-8")

    excel_yolu = CIKTI / "ozet_stdlib.xlsx"
    try:
        xlsx_yaz(excel_yolu, {
            "Ana_Sayilar": [["Gösterge", "Değer"]] + [[etiketler[a], d] for a, d in ana.items()],
            "Kategori": [["Kategori", "Şikâyet", "Çözülen", "Ort. çözüm (gün)", "Hedef (gün)", "Hedefi aşan"]]
                        + [[k[0], k[1], k[2], yuvarla(k[3]), k[4], k[5]] for k in kategori],
            "Aylik": [["Ay", "Şikâyet"]] + [list(a) for a in aylik],
            "Kanal": [["Kanal", "Çözülen", "Ort. çözüm (gün)"]] + [[k[0], k[1], yuvarla(k[2])] for k in kanal],
            "Sorunlu_Kayitlar": [["Şikâyet no", "Neden"]] + [[s["sikayet_no"], s["neden"]] for s in sorunlu],
        })
        print("Excel özet: outputs/gun07/ozet_stdlib.xlsx")
    except PermissionError:
        # Windows'ta dosya Excel'de AÇIKKEN üzerine yazılamaz.
        print("UYARI: ozet_stdlib.xlsx yazılamadı. Dosya Excel'de açık olabilir; kapatıp tekrar çalıştırın.")

    print("ANA SAYILAR")
    for anahtar, deger in ana.items():
        print(f"  {etiketler[anahtar]:<30}: {deger}")
    if sorunlu:
        print("Sorunlu kayıtlar:", ", ".join(f"{s['sikayet_no']} ({s['neden']})" for s in sorunlu))
    print("Rapor: outputs/gun07/rapor_stdlib.html")


if __name__ == "__main__":
    main()
