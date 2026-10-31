# -*- coding: utf-8 -*-
"""SQL ile özet: COUNT, SUM, AVG, MIN, MAX, GROUP BY ve HAVING (PivotTable'ın SQL hâli).

NE ÖĞRETİYOR?
    Excel karşılıkları:
      COUNT(*)            -> BAĞ_DEĞ_DOLU_SAY / PivotTable "Say"
      SUM(sutun)          -> TOPLA / ETOPLA
      AVG(sutun)          -> ORTALAMA (NULL'ları atlar, boş hücreleri atlayan ORTALAMA gibi)
      GROUP BY il         -> PivotTable'da "il" alanını SATIRLAR'a sürüklemek
      HAVING COUNT(*)>50  -> PivotTable sonucuna değer filtresi uygulamak
    WHERE ile HAVING farkı:
      WHERE  gruplamadan ÖNCE satırları süzer  (ham veriye filtre)
      HAVING gruplamadan SONRA grupları süzer  (özet tabloya filtre)

NASIL ÇALIŞTIRILIR?
    python gun04/09_toplama_gruplama.py

BEKLENEN ÇIKTI (kısaltılmış):
    Toplam: 600 şikâyet, çözülen ortalama süre 9.6 gün
    ...
    100'den fazla şikâyeti olan il sayısı: 2
"""
import sqlite3

import db_yardimci as dy

baglanti = sqlite3.connect(dy.veritabani_hazirla())

# ---------------------------------------------------------------------------
# 1) Tüm tablo için tek satırlık özet
# ---------------------------------------------------------------------------
toplam, ort_sure, toplam_tutar = baglanti.execute("""
    SELECT COUNT(*),
           ROUND(AVG(CASE WHEN durum = 'Çözüldü' THEN cozum_suresi_gun END), 1),
           ROUND(SUM(itiraz_tutari_tl), 2)
    FROM sikayetler
""").fetchone()
print(f"Toplam: {toplam} şikâyet, çözülen ortalama süre {ort_sure} gün")
print(f"Toplam itiraz tutarı: {toplam_tutar} TL")
# CASE WHEN ... THEN ... END: Excel'deki EĞER. Koşul tutmazsa NULL döner,
# AVG de NULL'ları atlar -> "sadece çözülenlerin ortalaması" (ORTALAMAEĞER).

# COUNT(*) ile COUNT(sutun) farkı: COUNT(sutun) NULL olmayanları sayar.
print("COUNT(*) vs COUNT(cozum_suresi_gun):",
      baglanti.execute("SELECT COUNT(*), COUNT(cozum_suresi_gun) FROM sikayetler").fetchone())

# ---------------------------------------------------------------------------
print("\n1) Operatör bazında özet (GROUP BY) - PivotTable: satırda operatör")
dy.tablo_yazdir(baglanti.execute("""
    SELECT operator,
           COUNT(*)                                  AS sikayet,
           SUM(durum = 'Çözüldü')                    AS cozulen,
           ROUND(AVG(memnuniyet), 2)                 AS ort_memnuniyet
    FROM sikayetler
    GROUP BY operator
    ORDER BY sikayet DESC
"""))
# AS ad : sütuna takma ad (başlık) verir.
# SUM(durum = 'Çözüldü') : SQLite'ta koşul doğruysa 1, değilse 0 -> toplamı = sayı (EĞERSAY)

# ---------------------------------------------------------------------------
print("\n2) İki boyutlu gruplama: il + durum (ilk 8 satır)")
dy.tablo_yazdir(baglanti.execute("""
    SELECT il, durum, COUNT(*) AS adet
    FROM sikayetler
    GROUP BY il, durum
    ORDER BY il, adet DESC
"""), en_fazla=8)

# ---------------------------------------------------------------------------
print("\n3) HAVING: 100'den fazla şikâyeti olan iller")
imlec = baglanti.execute("""
    SELECT il, COUNT(*) AS sikayet
    FROM sikayetler
    GROUP BY il
    HAVING COUNT(*) > 100
    ORDER BY sikayet DESC
""")
satirlar = imlec.fetchall()
dy.tablo_yazdir(satirlar, basliklar=["il", "sikayet"])
print("100'den fazla şikâyeti olan il sayısı:", len(satirlar))

# ---------------------------------------------------------------------------
print("\n4) WHERE + GROUP BY + HAVING birlikte: Mobil hizmette kategori bazında")
print("   ortalama çözüm süresi 10 günü aşan kategoriler")
dy.tablo_yazdir(baglanti.execute("""
    SELECT kategori,
           COUNT(*)                         AS cozulen,
           ROUND(AVG(cozum_suresi_gun), 1)  AS ort_gun,
           MAX(cozum_suresi_gun)            AS en_uzun
    FROM sikayetler
    WHERE hizmet = 'Mobil' AND durum = 'Çözüldü'      -- önce satırları süz
    GROUP BY kategori                                 -- sonra grupla
    HAVING AVG(cozum_suresi_gun) > 10                 -- sonra grupları süz
    ORDER BY ort_gun DESC
"""))

# ---------------------------------------------------------------------------
print("\n5) Hız ölçümleri: teknolojiye göre paket hızının yüzde kaçı geliyor?")
dy.tablo_yazdir(baglanti.execute("""
    SELECT teknoloji,
           COUNT(*)                                             AS olcum,
           ROUND(AVG(indirme_mbps), 1)                          AS ort_indirme,
           ROUND(AVG(100.0 * indirme_mbps / paket_hizi_mbps), 1) AS ort_yuzde
    FROM hiz_olcumleri
    GROUP BY teknoloji
    ORDER BY ort_yuzde DESC
"""))
# 100.0 yazmak önemli: tam sayı / tam sayı SQLite'ta TAM SAYI bölmesi yapar (7/2 = 3).

baglanti.close()
