# -*- coding: utf-8 -*-
"""SQL temel sorgular: SELECT, WHERE, AND/OR, IN, LIKE, IS NULL, ORDER BY, LIMIT.

NE ÖĞRETİYOR?
    SQL cümlesinin okunuş sırası (Excel karşılıklarıyla):
      SELECT  sütunlar         -> hangi sütunları göreyim? (sütun gizle/göster)
      FROM    tablo            -> hangi sayfadan?
      WHERE   koşul            -> hangi satırlar? (Otomatik Filtre)
      ORDER BY sütun DESC      -> nasıl sıralansın? (Sırala: Z'den A'ya)
      LIMIT   10               -> ilk kaç satır? (İlk 10)
    Sonuçlar terminalde db_yardimci.tablo_yazdir ile tablo olarak gösterilir
    (DB Browser for SQLite kurulamayan bilgisayarlar için).

NASIL ÇALIŞTIRILIR?
    python gun04/08_select_where_order.py

BEKLENEN ÇIKTI (kısaltılmış):
    Veritabanı hazır: outputs/gun04/sikayet.sqlite (600 şikâyet, 400 ölçüm)
    ...
    Ankara'da çözülen fatura şikâyeti: ...
"""
import sqlite3

import db_yardimci as dy        # "as dy": uzun modül adına kısa takma ad

db_yolu = dy.veritabani_hazirla()          # her çalıştırmada sıfırdan kurulur
baglanti = sqlite3.connect(db_yolu)

# ---------------------------------------------------------------------------
print("\n1) İlk 5 kayıt, seçili sütunlar (SELECT ... LIMIT)")
dy.tablo_yazdir(baglanti.execute("""
    SELECT sikayet_no, tarih, il, kategori, durum
    FROM sikayetler
    LIMIT 5
"""))
# SELECT * : tüm sütunlar. Büyük tablolarda sadece gereken sütunları seçin.

# ---------------------------------------------------------------------------
print("\n2) WHERE ile filtre: Ankara + Fatura + Çözüldü (AND)")
imlec = baglanti.execute("""
    SELECT sikayet_no, tarih, operator, cozum_suresi_gun, itiraz_tutari_tl
    FROM sikayetler
    WHERE il = 'Ankara' AND kategori = 'Fatura' AND durum = 'Çözüldü'
    ORDER BY cozum_suresi_gun DESC
""")
dy.tablo_yazdir(imlec, en_fazla=5)
# SQL'de metin tek tırnakla yazılır: 'Ankara'. Eşitlik tek "=" (Python'daki == değil).
# Türkçe karakterler birebir eşleşmeli: 'Cozuldu' ile 'Çözüldü' FARKLIDIR.

adet = baglanti.execute("""SELECT COUNT(*) FROM sikayetler
                           WHERE il = 'Ankara' AND kategori = 'Fatura' AND durum = 'Çözüldü'""").fetchone()[0]
print("Ankara'da çözülen fatura şikâyeti:", adet)

# ---------------------------------------------------------------------------
print("\n3) IN ve ORDER BY: Ege ve Karadeniz illerinden en uzun süren 5 çözüm")
dy.tablo_yazdir(baglanti.execute("""
    SELECT sikayet_no, il, kategori, cozum_suresi_gun
    FROM sikayetler
    WHERE il IN ('İzmir', 'Trabzon') AND durum = 'Çözüldü'
    ORDER BY cozum_suresi_gun DESC, sikayet_no
    LIMIT 5
"""))
# IN (...) : listedeki değerlerden biri (Excel filtresinde birden çok kutuyu işaretlemek)
# ORDER BY a DESC, b : önce a'ya göre büyükten küçüğe, eşitlikte b'ye göre

# ---------------------------------------------------------------------------
print("\n4) LIKE ile metin arama: hizmet adı 'Sabit' ile başlayanlar")
dy.tablo_yazdir(baglanti.execute("""
    SELECT DISTINCT hizmet
    FROM sikayetler
    WHERE hizmet LIKE 'Sabit%'
"""))
# DISTINCT: tekrarları at, her farklı değeri bir kez göster (Excel: Yinelenenleri Kaldır)
# % = "herhangi bir metin" (Excel filtresindeki * joker karakteri gibi)
# Not: SQLite'ın LIKE'ı Türkçe büyük/küçük harfi (İ/i, Ş/ş) eşleştirmez; tam yazımı kullanın.

# ---------------------------------------------------------------------------
print("\n5) IS NULL: süresi boş olan (işlemdeki) en eski 5 kayıt")
dy.tablo_yazdir(baglanti.execute("""
    SELECT sikayet_no, tarih, il, durum, cozum_suresi_gun
    FROM sikayetler
    WHERE cozum_suresi_gun IS NULL
    ORDER BY tarih
    LIMIT 5
"""))
# Tarihler 'YYYY-AA-GG' biçiminde saklandığı için metin sıralaması = takvim sıralaması.
# '05.01.2026' gibi saklasaydık sıralama BOZUK olurdu. ISO biçimini tercih edin.

# ---------------------------------------------------------------------------
print("\n6) Tarih aralığı: Mart 2026'daki Kesinti şikâyetleri (BETWEEN)")
adet = baglanti.execute("""
    SELECT COUNT(*) FROM sikayetler
    WHERE kategori = 'Kesinti' AND tarih BETWEEN '2026-03-01' AND '2026-03-31'
""").fetchone()[0]
print("Mart 2026 kesinti şikâyeti:", adet)

baglanti.close()
