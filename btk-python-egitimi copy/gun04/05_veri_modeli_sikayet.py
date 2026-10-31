# -*- coding: utf-8 -*-
"""Veri modelleme: tablo, kayıt, alan, birincil anahtar ve 1-N ilişki (şikâyet verisi).

NE ÖĞRETİYOR?
    Veritabanına geçmeden önce "verimiz neyi temsil ediyor?" sorusu:
      TABLO   = bir konu (şikâyetler, iller, hedefler)        -> Excel'de bir SAYFA
      KAYIT   = tablodaki bir satır (bir şikâyet)              -> Excel'de bir SATIR
      ALAN    = bir sütun (il, durum, süre)                    -> Excel'de bir SÜTUN
      BİRİNCİL ANAHTAR = her kaydı tek başına tanımlayan alan (sikayet_no)
                         -> Excel'de "bu sütunda tekrar olmamalı" dediğiniz kimlik sütunu
      İLİŞKİ 1-N = bir ilin ÇOK şikâyeti olur, bir şikâyetin TEK ili vardır
                   -> Excel'de DÜŞEYARA ile başka sayfadan bilgi getirmek

MODEL (metin diyagram):

    +-----------------+        +-------------------------+        +------------------+
    | iller           |        | sikayetler              |        | hedefler         |
    |-----------------|  1   N |-------------------------| N    1 |------------------|
    | il (PK)         |<-------| sikayet_no (PK)         |------->| kategori (PK)    |
    | bolge           |        | tarih, il (FK)          |        | hedef_gun        |
    +-----------------+        | operator, hizmet        |        +------------------+
            ^ 1                | kategori (FK), kanal    |
            |                  | durum, cozum_suresi_gun |
            | N                | memnuniyet, itiraz_tl   |
    +-----------------+        +-------------------------+
    | hiz_olcumleri   |
    |-----------------|        PK = birincil anahtar (Primary Key)
    | olcum_no (PK)   |        FK = yabancı anahtar (Foreign Key): başka tablonun
    | il (FK), ...    |             birincil anahtarını gösteren alan
    +-----------------+

NASIL ÇALIŞTIRILIR?
    python gun04/05_veri_modeli_sikayet.py

BEKLENEN ÇIKTI (kısaltılmış):
    Birincil anahtar tekil: 600/600
    Tekil il: 8 -> iller tablosu 8 satır olur
    İstanbul: 185 şikâyet (1 il -> N şikâyet)
    Kirli dosyada tekrar eden kimlik: ['10527']
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def oku(dosya_adi):
    with (ROOT / "data" / dosya_adi).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


sikayetler = oku("sikayetler.csv")

# ---------------------------------------------------------------------------
# 1) Kayıt ve alanlar
# ---------------------------------------------------------------------------
print("Tablo: sikayetler")
print("  Kayıt (satır) sayısı:", len(sikayetler))
print("  Alan (sütun) sayısı :", len(sikayetler[0]))
print("  Alanlar:", ", ".join(sikayetler[0].keys()))

# ---------------------------------------------------------------------------
# 2) Birincil anahtar adayı: sikayet_no tekil mi?
# ---------------------------------------------------------------------------
# Küme (set) tekrarları atar. Küme boyutu = liste boyutu ise tekrar YOK demektir.
# Excel: =SATIRSAY(BENZERSİZ(A2:A601)) sonucunu toplam satır sayısıyla karşılaştırmak gibi
# (veya Veri > Yinelenenleri Kaldır deyip "0 yinelenen" mesajını görmek).
numaralar = [k["sikayet_no"] for k in sikayetler]
print(f"Birincil anahtar tekil: {len(set(numaralar))}/{len(numaralar)}")

# "il" birincil anahtar OLAMAZ: aynı il yüzlerce kez geçiyor.
print(f"'il' alanı tekil mi? {len(set(k['il'] for k in sikayetler)) == len(sikayetler)}")

# ---------------------------------------------------------------------------
# 3) 1-N ilişki: iller tablosu ayrı tutulursa
# ---------------------------------------------------------------------------
# Bölge bilgisini 600 satırın her birine yazmak yerine 8 satırlık ayrı bir
# tabloya yazarız. Bölge adı değişirse tek yerde düzeltilir (tekrar yok).
il_sayilari = Counter(k["il"] for k in sikayetler)      # Counter: hazır sayaç sözlüğü
print("Tekil il:", len(il_sayilari), "-> iller tablosu", len(il_sayilari), "satır olur")
print(f"İstanbul: {il_sayilari['İstanbul']} şikâyet (1 il -> N şikâyet)")

# ---------------------------------------------------------------------------
# 4) Yabancı anahtar kontrolü: her şikâyetin kategorisinin bir hedefi var mı?
# ---------------------------------------------------------------------------
# Hedefler Excel'in "Hedefler" sayfasında; burada küçük bir sözlükle temsil ediyoruz.
hedef_kategoriler = {"Fatura", "İnternet Hızı", "Kesinti", "Taahhüt/İptal", "Numara Taşıma", "Kapsama"}
eslesmeyen = [k for k in sikayetler if k["kategori"] not in hedef_kategoriler]
print("Hedef tablosunda karşılığı olmayan şikâyet:", len(eslesmeyen))
# DÜŞEYARA'da #YOK hatası alacağınız satırları önceden bulmak gibi.

# ---------------------------------------------------------------------------
# 5) Aynı kontrol kirli dosyada: anahtar bozulmuşsa ne olur?
# ---------------------------------------------------------------------------
kirli = oku("sikayetler_kirli.csv")
sayac = Counter(k["sikayet_no"] for k in kirli)
tekrar_edenler = [no for no, adet in sayac.items() if adet > 1]
print("Kirli dosyada tekrar eden kimlik:", tekrar_edenler)
# Veritabanında sikayet_no PRIMARY KEY olduğu için bu satırı eklemeye çalışmak
# "UNIQUE constraint failed" hatası verir: veritabanı bizi korur.

# ---------------------------------------------------------------------------
# 6) Operatör: ayrı tablo olmalı mı? (tartışma sorusu)
# ---------------------------------------------------------------------------
operatorler = sorted(set(k["operator"] for k in sikayetler))
print("Operatörler:", operatorler)
# Operatör adı değişirse (şirket birleşmesi) 600 satırı mı güncellersiniz,
# yoksa operatorler tablosundaki 1 satırı mı? Tablo ayırmanın asıl faydası budur.
