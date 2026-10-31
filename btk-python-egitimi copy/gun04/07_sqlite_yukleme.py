# -*- coding: utf-8 -*-
"""SQLite'a CSV yüklemek: bağlan, CREATE TABLE, executemany ile toplu INSERT, commit, close.

NE ÖĞRETİYOR?
    SQLite, sunucu GEREKTİRMEYEN, tek dosyalık bir veritabanıdır. Python ile birlikte
    gelir (import sqlite3); kurulum, kullanıcı adı, şifre yoktur.
    Excel benzetmesi: .sqlite dosyası bir çalışma kitabı; her tablo bir sayfa.
    Farkı: her sütunun türü bellidir, kimlik tekrarına izin vermez, milyonlarca
    satırı rahat taşır ve SQL ile sorgulanır.

    Adımlar:
      1) sqlite3.connect(dosya)   -> dosyayı aç (yoksa oluştur)
      2) CREATE TABLE             -> tablo ve sütun türlerini tanımla
      3) executemany(INSERT ...)  -> satırları toplu ekle
      4) commit()                 -> kaydet (Excel'de Ctrl+S)
      5) close()                  -> kapat

    TEKRAR ÇALIŞTIRILABİLİRLİK: Her çalıştırmada aynı satırları tekrar eklersek
    tablo büyür (600, 1200, 1800...) veya PRIMARY KEY hatası alırız. Çözüm:
    önce DROP TABLE IF EXISTS (tabloyu sil) ve yeniden kur.

NASIL ÇALIŞTIRILIR?
    python gun04/07_sqlite_yukleme.py

BEKLENEN ÇIKTI (kısaltılmış):
    Veritabanı: outputs/gun04/adim_adim.sqlite
    sikayetler: 600 satır
    hiz_olcumleri: 400 satır
    NULL çözüm süresi: 96
    Beklenen hata yakalandı: UNIQUE constraint failed: sikayetler.sikayet_no
"""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cikti = ROOT / "outputs" / "gun04"
cikti.mkdir(parents=True, exist_ok=True)
db_yolu = cikti / "adim_adim.sqlite"


def bos_ise_none(metin, tur):
    """'' -> None (veritabanında NULL), dolu ise istenen türe çevir."""
    return tur(metin) if metin.strip() != "" else None


# 1) Bağlan --------------------------------------------------------------------
baglanti = sqlite3.connect(db_yolu)
print("Veritabanı:", db_yolu.relative_to(ROOT).as_posix())

# 2) Tabloyu sıfırdan kur ---------------------------------------------------------
# DROP TABLE IF EXISTS: "tablo varsa sil". Sadece EĞİTİM verisinde böyle yapılır;
# gerçek bir veritabanında bu komut tüm veriyi geri dönüşsüz siler!
baglanti.execute("DROP TABLE IF EXISTS sikayetler")
baglanti.execute("""
    CREATE TABLE sikayetler (
        sikayet_no        INTEGER PRIMARY KEY,  -- tekil kimlik, tekrar edemez
        tarih             TEXT NOT NULL,        -- NOT NULL: boş bırakılamaz
        il                TEXT NOT NULL,
        operator          TEXT NOT NULL,
        hizmet            TEXT,
        kategori          TEXT,
        kanal             TEXT,
        durum             TEXT NOT NULL,
        cozum_suresi_gun  INTEGER,              -- tam sayı (boş olabilir)
        memnuniyet        INTEGER,
        itiraz_tutari_tl  REAL                  -- REAL: ondalıklı sayı
    )
""")
# SQL'de "--" ile başlayan kısım yorumdur (Python'daki # gibi).

# 3) CSV'yi oku ve satırları demet (tuple) listesine çevir ---------------------
with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as f:
    satirlar = []
    for k in csv.DictReader(f):
        satirlar.append((
            int(k["sikayet_no"]), k["tarih"], k["il"], k["operator"], k["hizmet"],
            k["kategori"], k["kanal"], k["durum"],
            bos_ise_none(k["cozum_suresi_gun"], int),     # "" -> None -> NULL
            bos_ise_none(k["memnuniyet"], int),
            bos_ise_none(k["itiraz_tutari_tl"], float),
        ))

# 11 sütun -> 11 tane "?" yer tutucu. Değerler sırayla yerleştirilir.
baglanti.executemany("INSERT INTO sikayetler VALUES (?,?,?,?,?,?,?,?,?,?,?)", satirlar)

# Aynısı hız ölçümleri için (sütun adlarını açıkça yazmak daha güvenli bir yoldur)
baglanti.execute("DROP TABLE IF EXISTS hiz_olcumleri")
baglanti.execute("""
    CREATE TABLE hiz_olcumleri (
        olcum_no INTEGER PRIMARY KEY, tarih TEXT, il TEXT, operator TEXT, teknoloji TEXT,
        paket_hizi_mbps INTEGER, indirme_mbps REAL, yukleme_mbps REAL, ping_ms REAL
    )
""")
with (ROOT / "data" / "hiz_olcumleri.csv").open(encoding="utf-8", newline="") as f:
    olcumler = [(int(o["olcum_no"]), o["tarih"], o["il"], o["operator"], o["teknoloji"],
                 int(o["paket_hizi_mbps"]), float(o["indirme_mbps"]),
                 float(o["yukleme_mbps"]), float(o["ping_ms"]))
                for o in csv.DictReader(f)]
baglanti.executemany(
    """INSERT INTO hiz_olcumleri (olcum_no, tarih, il, operator, teknoloji,
                                  paket_hizi_mbps, indirme_mbps, yukleme_mbps, ping_ms)
       VALUES (?,?,?,?,?,?,?,?,?)""", olcumler)

# 4) Kaydet -------------------------------------------------------------------
baglanti.commit()      # commit yapılmazsa eklenenler dosyaya YAZILMAZ!

# Kontrol sayımları: CSV'deki satır sayısıyla aynı mı?
for tablo in ["sikayetler", "hiz_olcumleri"]:
    # Tablo adı kod içinde sabit (kullanıcıdan gelmiyor), f-string burada güvenli.
    adet = baglanti.execute(f"SELECT COUNT(*) FROM {tablo}").fetchone()[0]
    print(f"{tablo}: {adet} satır")

# fetchone() -> tek satır (demet); [0] -> o satırın ilk sütunu
bos = baglanti.execute("SELECT COUNT(*) FROM sikayetler WHERE cozum_suresi_gun IS NULL").fetchone()[0]
print("NULL çözüm süresi:", bos)
# DİKKAT: "= NULL" çalışmaz! NULL kontrolü her zaman "IS NULL" / "IS NOT NULL" ile yapılır.

# 5) Birincil anahtar bizi korur: aynı kimliği ikinci kez eklemeyi deneyelim
try:
    baglanti.execute("INSERT INTO sikayetler (sikayet_no, tarih, il, operator, durum) "
                     "VALUES (?, ?, ?, ?, ?)", (10527, "2026-01-02", "Ankara", "Operatör A", "Çözüldü"))
except sqlite3.IntegrityError as hata:
    print("Beklenen hata yakalandı:", hata)

# 6) Kapat ---------------------------------------------------------------------
baglanti.close()
# Windows'ta kapatılmayan bağlantı dosyayı kilitli tutabilir; bir sonraki
# çalıştırmada "database is locked" hatası görebilirsiniz.

# Bu adımların hepsini db_yardimci.veritabani_hazirla() fonksiyonuna koyduk;
# sonraki örnekler tek satırla hazır veritabanı alır.
