# -*- coding: utf-8 -*-
"""Gün 4 yardımcı modülü: veritabanını hazırlama, tablo yazdırma, Excel'i paketsiz okuma.

NE ÖĞRETİYOR?
    Gün 4 örneklerinin (05-16) ortak kullandığı fonksiyonlar burada durur.
    Örnek dosyalar "import db_yardimci" diyerek bunları kullanır (Gün 3'teki
    yardimcilar.py mantığının aynısı). Bu dosyayı satır satır anlamak zorunlu
    DEĞİLDİR; "hazır alet çantası" gibi kullanılabilir. Merak edenler için
    her fonksiyon ayrıntılı yorumlanmıştır.

    İçindekiler:
      csv_oku(dosya_adi)            -> data/ altındaki CSV'yi sözlük listesi olarak okur
      bos_ise_none(metin, tur)      -> "" -> None, "7" -> 7 (SQL'de boş = NULL)
      xlsx_sayfa_oku(yol, sayfa)    -> .xlsx dosyasının bir sayfasını PAKETSİZ okur
      veritabani_hazirla(yol)       -> CSV + Excel'den sıfırdan SQLite veritabanı kurar
      tablo_yazdir(imlec)           -> sorgu sonucunu terminalde düzgün tablo olarak basar
      sorgu_csv_yaz(imlec, yol)     -> sorgu sonucunu Excel'de açılabilen CSV'ye yazar

NASIL ÇALIŞTIRILIR?
    Normalde import edilir. Doğrudan çalıştırılırsa kısa bir kendi testi yapar:
        python gun04/db_yardimci.py

BEKLENEN ÇIKTI (doğrudan çalıştırınca):
    Hedefler sayfası: 6 satır
    db_yardimci modülü kendi testini geçti
"""
import csv
import sqlite3
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CIKTI = ROOT / "outputs" / "gun04"
VARSAYILAN_DB = CIKTI / "sikayet.sqlite"

# İl -> coğrafi bölge. Gerçek coğrafi bilgidir; JOIN örnekleri için ayrı tablo yapacağız.
IL_BOLGE = {
    "İstanbul": "Marmara", "Bursa": "Marmara",
    "Ankara": "İç Anadolu", "Konya": "İç Anadolu",
    "İzmir": "Ege", "Antalya": "Akdeniz",
    "Trabzon": "Karadeniz", "Erzurum": "Doğu Anadolu",
}


# ===========================================================================
# 1) CSV yardımcıları
# ===========================================================================
def csv_oku(dosya_adi):
    """data/ klasöründeki CSV dosyasını sözlük listesi olarak okur."""
    with (DATA / dosya_adi).open(encoding="utf-8", newline="") as dosya:
        return list(csv.DictReader(dosya))


def bos_ise_none(metin, tur=str):
    """CSV hücresini veritabanına uygun değere çevirir.

    Boş hücre ("") -> None. SQLite'a None verilirse hücre NULL olur.
    NULL, "bilinmiyor" demektir; AVG/SUM gibi fonksiyonlar NULL'ları atlar
    (Excel'in ORTALAMA fonksiyonunun boş hücreleri atlaması gibi).
    """
    metin = metin.strip()
    if metin == "":
        return None
    return tur(metin)


# ===========================================================================
# 2) Excel (.xlsx) dosyasını PAKETSİZ okumak
# ===========================================================================
# .xlsx aslında bir ZIP arşividir! Uzantısını .zip yapıp açarsanız içinde
# XML dosyaları görürsünüz:
#   xl/workbook.xml             -> sayfa adları listesi (Sikayetler, Hedefler ...)
#   xl/_rels/workbook.xml.rels  -> hangi sayfa adı hangi XML dosyasında
#   xl/worksheets/sheet3.xml    -> bir sayfanın hücreleri
#   xl/sharedStrings.xml        -> (varsa) metinlerin ortak sözlüğü
# Python'un standart kütüphanesindeki zipfile + xml.etree ile bunları okuyabiliriz.
# openpyxl kurulamazsa B planı budur.

# XML "ad alanları" (namespace): etiket adlarının uzun tam adları. Arama yaparken lazım.
_NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def _sutun_harfinden_sira(hucre_adresi):
    """'C12' -> 2 (A=0, B=1, C=2, ..., Z=25, AA=26). Satır numarasını yok sayar."""
    sira = 0
    for harf in hucre_adresi:
        if harf.isalpha():
            sira = sira * 26 + (ord(harf.upper()) - ord("A") + 1)   # 26'lık sayı sistemi
        else:
            break
    return sira - 1


def _metin_birlestir(eleman):
    """Bir XML elemanının içindeki tüm <t> metinlerini birleştirir.

    Excel bir hücre içinde farklı biçimli parçalar (kalın + normal) tutarsa
    metni birkaç <t> parçasına böler; hepsini birleştirmek gerekir.
    """
    return "".join(t.text or "" for t in eleman.iter(f"{{{_NS['m']}}}t"))


def xlsx_sayfa_oku(xlsx_yolu, sayfa_adi):
    """Bir .xlsx dosyasındaki sayfayı sözlük listesi olarak okur (ilk satır = başlık).

    Sadece standart kütüphane kullanır (openpyxl GEREKMEZ).
    Örnek: xlsx_sayfa_oku(DATA / "btk_ornek_veri.xlsx", "Hedefler")
           -> [{"kategori": "Fatura", "hedef_gun": 7}, ...]

    Sınırlar (eğitim için yeterli, her Excel dosyası için değil):
      - Formül hücrelerinde Excel'in SON KAYDEDİLEN sonucunu okur, formülü değil.
      - Tarih biçimli hücreler Excel'in içinde SAYI olarak durur (ör. 46023);
        bu fonksiyon onları sayı olarak verir. Metin olarak saklanmış tarihler sorunsuzdur.
      - Birleştirilmiş hücre, biçim, renk okunmaz (CSV gibi sadece değerler).
    """
    with zipfile.ZipFile(xlsx_yolu) as arsiv:
        dosyalar = set(arsiv.namelist())

        # --- Adım 1: Ortak metin sözlüğü (sharedStrings) ---------------------
        # Excel aynı metni ("İstanbul") binlerce kez tekrar yazmamak için metinleri
        # bir listede bir kez tutar; hücreye sadece SIRA NUMARASINI yazar.
        # Hücrede t="s" ve <v>3</v> görürseniz anlamı: "ortak listedeki 3 numaralı metin".
        # Bazı programlar (ör. openpyxl'in bazı sürümleri) metni doğrudan hücreye
        # yazar (t="inlineStr"); o durumda bu dosya hiç olmayabilir.
        ortak_metinler = []
        if "xl/sharedStrings.xml" in dosyalar:
            kok = ET.fromstring(arsiv.read("xl/sharedStrings.xml"))
            for si in kok.findall("m:si", _NS):          # her <si> bir metin
                ortak_metinler.append(_metin_birlestir(si))

        # --- Adım 2: Sayfa adından XML dosyasını bul -------------------------
        # workbook.xml: <sheet name="Hedefler" r:id="rId3"/>
        kitap = ET.fromstring(arsiv.read("xl/workbook.xml"))
        rid = None
        sayfa_adlari = []
        for sayfa in kitap.findall("m:sheets/m:sheet", _NS):
            sayfa_adlari.append(sayfa.get("name"))
            if sayfa.get("name") == sayfa_adi:
                rid = sayfa.get(f"{{{_NS['r']}}}id")
        if rid is None:
            raise ValueError(f"'{sayfa_adi}' sayfası yok. Mevcut sayfalar: {sayfa_adlari}")

        # workbook.xml.rels: <Relationship Id="rId3" Target="worksheets/sheet3.xml"/>
        iliskiler = ET.fromstring(arsiv.read("xl/_rels/workbook.xml.rels"))
        hedef = None
        for iliski in iliskiler.findall("rel:Relationship", _NS):
            if iliski.get("Id") == rid:
                hedef = iliski.get("Target")
        # Target bazen "/xl/worksheets/sheet3.xml" (mutlak), bazen
        # "worksheets/sheet3.xml" (xl/ klasörüne göre) yazılır. İkisini de karşıla.
        if hedef.startswith("/"):
            sayfa_yolu = hedef.lstrip("/")
        else:
            sayfa_yolu = "xl/" + hedef

        # --- Adım 3: Hücreleri oku ------------------------------------------
        kok = ET.fromstring(arsiv.read(sayfa_yolu))
        satirlar = []
        for satir in kok.iter(f"{{{_NS['m']}}}row"):
            degerler = {}      # {sütun sırası: değer} - boş hücreler XML'de hiç yazılmaz!
            for hucre in satir.findall("m:c", _NS):
                sira = _sutun_harfinden_sira(hucre.get("r"))   # "B5" -> 1
                tur = hucre.get("t")          # hücre türü: s, inlineStr, str, b, n, e
                v = hucre.find("m:v", _NS)    # <v> = değer
                if tur == "s":                # ortak metin listesindeki sıra numarası
                    deger = ortak_metinler[int(v.text)]
                elif tur == "inlineStr":      # metin doğrudan hücrede: <is><t>...</t></is>
                    deger = _metin_birlestir(hucre)
                elif v is None or v.text is None:
                    deger = None              # değeri olmayan (boş/biçimli) hücre
                elif tur == "str":            # formülün metin sonucu
                    deger = v.text
                elif tur == "b":              # mantıksal: 1/0
                    deger = v.text == "1"
                elif tur == "e":              # #YOK, #BÖL/0! gibi Excel hataları
                    deger = None
                else:                         # sayı (t="n" ya da t yazılmamış)
                    sayi = float(v.text)
                    deger = int(sayi) if sayi.is_integer() else sayi
                degerler[sira] = deger
            if degerler:
                # Atlanmış (boş) sütunları None ile doldurarak düz listeye çevir
                en_son = max(degerler)
                satirlar.append([degerler.get(i) for i in range(en_son + 1)])

    if not satirlar:
        return []
    # Başlık hücresi boşsa o sütuna "sutun_3" gibi bir ad ver (None anahtar olmasın)
    basliklar = [b if b is not None else f"sutun_{i + 1}" for i, b in enumerate(satirlar[0])]
    kayitlar = []
    for satir in satirlar[1:]:
        satir = satir + [None] * (len(basliklar) - len(satir))   # kısa satırları tamamla
        kayitlar.append(dict(zip(basliklar, satir)))             # başlık -> değer eşleştir
    return kayitlar


# ===========================================================================
# 3) Veritabanını sıfırdan kurmak (tekrar çalıştırılabilir)
# ===========================================================================
SEMA = """
CREATE TABLE iller (
    il      TEXT PRIMARY KEY,     -- birincil anahtar: her il bir kez
    bolge   TEXT NOT NULL
);
CREATE TABLE hedefler (
    kategori  TEXT PRIMARY KEY,
    hedef_gun INTEGER NOT NULL
);
CREATE TABLE sikayetler (
    sikayet_no        INTEGER PRIMARY KEY,
    tarih             TEXT NOT NULL,             -- SQLite'ta tarih türü yok: 'YYYY-AA-GG' metni
    il                TEXT NOT NULL REFERENCES iller(il),
    operator          TEXT NOT NULL,
    hizmet            TEXT,
    kategori          TEXT REFERENCES hedefler(kategori),
    kanal             TEXT,
    durum             TEXT NOT NULL,
    cozum_suresi_gun  INTEGER,                   -- boş olabilir (NULL): işlemdeki kayıt
    memnuniyet        INTEGER,
    itiraz_tutari_tl  REAL
);
CREATE TABLE hiz_olcumleri (
    olcum_no         INTEGER PRIMARY KEY,
    tarih            TEXT NOT NULL,
    il               TEXT NOT NULL REFERENCES iller(il),
    operator         TEXT NOT NULL,
    teknoloji        TEXT,
    paket_hizi_mbps  INTEGER,
    indirme_mbps     REAL,
    yukleme_mbps     REAL,
    ping_ms          REAL
);
"""


def veritabani_hazirla(db_yolu=VARSAYILAN_DB, sessiz=False):
    """CSV ve Excel'den SIFIRDAN bir SQLite veritabanı oluşturur; yolunu döndürür.

    Her çalıştırmada eski dosya silinir ve yeniden kurulur. Böylece script
    kaç kez çalışırsa çalışsın sonuç aynıdır (satırlar ikiye katlanmaz).
    """
    db_yolu = Path(db_yolu)
    db_yolu.parent.mkdir(parents=True, exist_ok=True)
    try:
        db_yolu.unlink(missing_ok=True)       # eski veritabanını sil (yoksa sorun etme)
    except PermissionError:
        # Windows: dosya DB Browser for SQLite veya başka bir programda açıksa silinemez.
        raise SystemExit(f"'{db_yolu.name}' başka bir programda açık. "
                         "DB Browser'ı kapatıp tekrar çalıştırın.") from None

    baglanti = sqlite3.connect(db_yolu)
    try:
        baglanti.executescript(SEMA)          # birden çok SQL komutunu tek seferde çalıştır

        baglanti.executemany("INSERT INTO iller VALUES (?, ?)", IL_BOLGE.items())

        # Hedefler Excel'den okunuyor (paketsiz okuyucu ile)
        hedefler = xlsx_sayfa_oku(DATA / "btk_ornek_veri.xlsx", "Hedefler")
        baglanti.executemany("INSERT INTO hedefler VALUES (?, ?)",
                             [(h["kategori"], h["hedef_gun"]) for h in hedefler])

        # Şikâyetler: her CSV satırını SQL'e uygun türlere çevirip demet (tuple) yapıyoruz
        sikayet_satirlari = []
        for k in csv_oku("sikayetler.csv"):
            sikayet_satirlari.append((
                int(k["sikayet_no"]), k["tarih"], k["il"], k["operator"], k["hizmet"],
                k["kategori"], k["kanal"], k["durum"],
                bos_ise_none(k["cozum_suresi_gun"], int),
                bos_ise_none(k["memnuniyet"], int),
                bos_ise_none(k["itiraz_tutari_tl"], float),
            ))
        # executemany: aynı INSERT'i listedeki her satır için çalıştırır (toplu ekleme)
        baglanti.executemany("INSERT INTO sikayetler VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                             sikayet_satirlari)

        olcum_satirlari = [
            (int(o["olcum_no"]), o["tarih"], o["il"], o["operator"], o["teknoloji"],
             int(o["paket_hizi_mbps"]), float(o["indirme_mbps"]),
             float(o["yukleme_mbps"]), float(o["ping_ms"]))
            for o in csv_oku("hiz_olcumleri.csv")
        ]
        baglanti.executemany("INSERT INTO hiz_olcumleri VALUES (?,?,?,?,?,?,?,?,?)",
                             olcum_satirlari)
        baglanti.commit()                     # değişiklikleri kalıcı olarak kaydet
    finally:
        baglanti.close()                      # Windows'ta dosya kilidini bırakmak için şart

    if not sessiz:
        print(f"Veritabanı hazır: {db_yolu.relative_to(ROOT).as_posix()} "
              f"({len(sikayet_satirlari)} şikâyet, {len(olcum_satirlari)} ölçüm)")
    return db_yolu


# ===========================================================================
# 4) Sonucu terminalde tablo olarak göstermek
# ===========================================================================
def _hucre_metni(deger):
    if deger is None:
        return "NULL"
    if isinstance(deger, float):
        # En fazla 2 ondalık; SQL'deki ROUND(...,1) sonucu 18.5 ise "18.5" görünür (18.50 değil)
        return str(round(deger, 2))
    return str(deger)


def tablo_yazdir(imlec_veya_satirlar, basliklar=None, en_fazla=20):
    """Sorgu sonucunu hizalı tablo olarak yazdırır (DB Browser kurulamazsa yeterli).

    Kullanım:
        tablo_yazdir(baglanti.execute("SELECT il, COUNT(*) FROM sikayetler GROUP BY il"))
    Başlıklar imlecin (cursor) description bilgisinden otomatik alınır.
    Satır listesi verilirse basliklar=[...] ile başlık verilebilir.
    en_fazla: ekranı doldurmamak için en fazla bu kadar satır gösterilir.
    """
    if basliklar is None and hasattr(imlec_veya_satirlar, "description"):
        basliklar = [sutun[0] for sutun in imlec_veya_satirlar.description]
    satirlar = [[_hucre_metni(d) for d in satir] for satir in imlec_veya_satirlar]
    if basliklar is None:
        basliklar = [f"s{i + 1}" for i in range(len(satirlar[0]) if satirlar else 0)]

    gosterilen = satirlar[:en_fazla]
    # Her sütunun genişliği: başlık ve hücrelerin en uzunu
    genislikler = [len(b) for b in basliklar]
    for satir in gosterilen:
        for i, hucre in enumerate(satir):
            genislikler[i] = max(genislikler[i], len(hucre))

    def bicimle(hucreler):
        parcalar = []
        for i, hucre in enumerate(hucreler):
            # Sayılar sağa, metinler sola yaslanır (Excel'deki gibi)
            sayi_mi = hucre.replace(".", "", 1).replace("-", "", 1).isdigit()
            parcalar.append(hucre.rjust(genislikler[i]) if sayi_mi else hucre.ljust(genislikler[i]))
        return " | ".join(parcalar).rstrip()     # satır sonundaki boşlukları at

    print(bicimle(basliklar))
    print("-+-".join("-" * g for g in genislikler))
    for satir in gosterilen:
        print(bicimle(satir))
    if len(satirlar) > en_fazla:
        print(f"... ({len(satirlar) - en_fazla} satır daha, toplam {len(satirlar)})")
    else:
        print(f"({len(satirlar)} satır)")


# ===========================================================================
# 5) Sorgu sonucunu CSV'ye yazmak
# ===========================================================================
def sorgu_csv_yaz(imlec, csv_yolu):
    """Sorgu sonucunu başlıklarıyla CSV'ye yazar (Excel için utf-8-sig). Satır sayısını döndürür."""
    basliklar = [sutun[0] for sutun in imlec.description]
    satirlar = imlec.fetchall()
    Path(csv_yolu).parent.mkdir(parents=True, exist_ok=True)
    with open(csv_yolu, "w", encoding="utf-8-sig", newline="") as f:
        yazici = csv.writer(f)
        yazici.writerow(basliklar)
        yazici.writerows(satirlar)
    return len(satirlar)


if __name__ == "__main__":
    hedefler = xlsx_sayfa_oku(DATA / "btk_ornek_veri.xlsx", "Hedefler")
    print("Hedefler sayfası:", len(hedefler), "satır")
    assert hedefler[0] == {"kategori": "Fatura", "hedef_gun": 7}
    assert _sutun_harfinden_sira("A1") == 0 and _sutun_harfinden_sira("AA10") == 26
    yol = veritabani_hazirla(CIKTI / "db_yardimci_test.sqlite", sessiz=True)
    db = sqlite3.connect(yol)
    assert db.execute("SELECT COUNT(*) FROM sikayetler").fetchone()[0] == 600
    assert db.execute("SELECT COUNT(*) FROM hiz_olcumleri").fetchone()[0] == 400
    db.close()
    yol.unlink()            # test veritabanını temizle
    print("db_yardimci modülü kendi testini geçti")
