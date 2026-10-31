# -*- coding: utf-8 -*-
"""Gün 4 ek alıştırmalarının çözümleri (ALISTIRMALAR.md: Temel T1-T3, Orta O1-O3, İleri İ1-İ3).

NASIL ÇALIŞTIRILIR?
    python gun04/cozumler_ek.py

BEKLENEN ÇIKTI (kısaltılmış):
    T1 Konya şikâyeti: 54
    ...
    O1 Memnuniyeti 3'ün altında: ['Operatör C', 'Operatör A']
    ...
    İ3 Hiz_Olcumleri sayfası CSV ile aynı: True
Öğrenciye önce kendi çözümünü yazdırın; bu dosyayı karşılaştırma için açın.
"""
import csv
import sqlite3
from datetime import date

import db_yardimci as dy

baglanti = sqlite3.connect(dy.veritabani_hazirla(dy.CIKTI / "cozumler_ek.sqlite", sessiz=True))

# ===========================================================================
# TEMEL
# ===========================================================================
# T1: Parametreli sorguyla Konya'daki şikâyet sayısı
print("T1 Konya şikâyeti:",
      baglanti.execute("SELECT COUNT(*) FROM sikayetler WHERE il = ?", ("Konya",)).fetchone()[0])

# T2: Kanal bazında şikâyet sayısı, büyükten küçüğe
print("T2 Kanal dağılımı:")
dy.tablo_yazdir(baglanti.execute(
    "SELECT kanal, COUNT(*) AS adet FROM sikayetler GROUP BY kanal ORDER BY adet DESC"))

# T3: Erzurum'da çözülen şikâyetlerin ortalama süresi
ort = baglanti.execute("""SELECT ROUND(AVG(cozum_suresi_gun), 1) FROM sikayetler
                          WHERE il = ? AND durum = ?""", ("Erzurum", "Çözüldü")).fetchone()[0]
print("T3 Erzurum ortalama çözüm süresi:", ort, "gün")

# ===========================================================================
# ORTA
# ===========================================================================
# O1: HAVING - ortalama memnuniyeti 3'ün altında olan operatörler
satirlar = baglanti.execute("""
    SELECT operator, ROUND(AVG(memnuniyet), 2) AS ort
    FROM sikayetler
    GROUP BY operator
    HAVING AVG(memnuniyet) < 3
    ORDER BY ort
""").fetchall()
print("O1 Memnuniyeti 3'ün altında:", [s[0] for s in satirlar])

# O2: JOIN iller - bölge bazında işlemdeki şikâyetler, CSV'ye yaz
imlec = baglanti.execute("""
    SELECT i.bolge, COUNT(*) AS islemde
    FROM sikayetler s JOIN iller i ON s.il = i.il
    WHERE s.durum = 'İşlemde'
    GROUP BY i.bolge
    ORDER BY islemde DESC
""")
adet = dy.sorgu_csv_yaz(imlec, dy.CIKTI / "bolge_islemde.csv")
print("O2 Bölge CSV satırı:", adet)


# O3: Sikayet sınıfına tarih ve "kaç gündür açık" metodu (kalıtım YOK, yeni sınıf)
class Sikayet:
    def __init__(self, sikayet_no, tarih, durum):
        self.sikayet_no = sikayet_no
        self.tarih = date.fromisoformat(tarih)
        self.durum = durum

    def gecen_gun(self, rapor_tarihi):
        return (rapor_tarihi - self.tarih).days

    def __repr__(self):
        return f"Sikayet(no={self.sikayet_no}, tarih={self.tarih}, durum={self.durum!r})"


s = Sikayet(10550, "2026-01-03", "İşlemde")
print("O3", s, "->", s.gecen_gun(date(2026, 10, 1)), "gündür açık")

# ===========================================================================
# İLERİ
# ===========================================================================
# İ1: CASE ile her şikâyete SLA durumu etiketi, özet ve CSV
imlec = baglanti.execute("""
    SELECT s.sikayet_no, s.kategori, s.cozum_suresi_gun, h.hedef_gun,
           CASE
               WHEN s.cozum_suresi_gun IS NULL      THEN 'Bilinmiyor'
               WHEN s.cozum_suresi_gun > h.hedef_gun THEN 'Aştı'
               ELSE 'Hedefte'
           END AS sla_durumu
    FROM sikayetler s JOIN hedefler h ON s.kategori = h.kategori
    ORDER BY s.sikayet_no
""")
adet = dy.sorgu_csv_yaz(imlec, dy.CIKTI / "sla_etiketli.csv")
ozet = dict(baglanti.execute("""
    SELECT CASE WHEN s.cozum_suresi_gun IS NULL THEN 'Bilinmiyor'
                WHEN s.cozum_suresi_gun > h.hedef_gun THEN 'Aştı' ELSE 'Hedefte' END AS d,
           COUNT(*)
    FROM sikayetler s JOIN hedefler h ON s.kategori = h.kategori
    GROUP BY d ORDER BY d
""").fetchall())
print(f"İ1 SLA etiketli CSV: {adet} satır, özet: {ozet}")
# Not: Reddedilenler de süreye sahip olduğu için burada etiketlenir; iş kuralına göre
# WHERE s.durum = 'Çözüldü' eklenebilir. Hangisinin doğru olduğu bir İŞ KARARIDIR.

# İ2: Çapraz tablo (PivotTable: satırda il, sütunda durum)
print("İ2 İl x durum çapraz tablosu:")
dy.tablo_yazdir(baglanti.execute("""
    SELECT il,
           SUM(durum = 'Çözüldü')    AS cozuldu,
           SUM(durum = 'Reddedildi') AS reddedildi,
           SUM(durum = 'İşlemde')    AS islemde,
           COUNT(*)                  AS toplam
    FROM sikayetler
    GROUP BY il
    ORDER BY toplam DESC
"""))

# İ3: Excel'in Hiz_Olcumleri sayfası CSV ile birebir aynı mı? (tür farklarına dikkat)
sayfa = dy.xlsx_sayfa_oku(dy.DATA / "btk_ornek_veri.xlsx", "Hiz_Olcumleri")
with (dy.DATA / "hiz_olcumleri.csv").open(encoding="utf-8", newline="") as f:
    csv_satirlari = list(csv.DictReader(f))
# Excel sayıları int/float verir, CSV metin verir. Metne çevirip karşılaştırmak YETMEZ:
# CSV'de "36.0" yazan değer Excel'in içinde 36 olarak saklanır (Excel 36,0 ile 36'yı ayırmaz).
# Bu yüzden sayıya çevrilebilen değerleri SAYI olarak, diğerlerini metin olarak karşılaştırıyoruz.
def ayni_deger(excel_degeri, csv_metni):
    try:
        return float(excel_degeri) == float(csv_metni)
    except (TypeError, ValueError):
        return str(excel_degeri) == csv_metni


ayni = len(sayfa) == len(csv_satirlari) and all(
    ayni_deger(x[sutun], c[sutun]) for x, c in zip(sayfa, csv_satirlari) for sutun in c)
print("İ3 Hiz_Olcumleri sayfası CSV ile aynı:", ayni)

baglanti.close()
