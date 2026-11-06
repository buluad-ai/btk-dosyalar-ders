# -*- coding: utf-8 -*-
"""İç içe yapı: LİSTE İÇİNDE SÖZLÜK = bir Excel tablosu.

Ne öğretiyor:
    - Her sözlük bir SATIR, anahtarlar SÜTUN başlıkları, liste TABLONUN kendisi.
    - Tek hücre okuma: tablo[0]["il"]  (0. satırın "il" sütunu)
    - Sütun çekme, satır filtreleme, yeni sütun ekleme, tabloyu yazdırma.
    - Gün 3'te csv.DictReader dosyayı TAM OLARAK bu yapıda okuyacak;
      Gün 5'te pandas DataFrame aynı fikrin hızlı/kısa hâli olacak.

Excel karşılığı:
    tablo[2]["sure"]                  -> C4 hücresi (başlık 1. satırda)
    [s["sure"] for s in tablo]        -> sadece "sure" sütununu seçmek
    if s["il"] == "Ankara"            -> Otomatik Filtre: il = Ankara
    s["asim"] = ...                   -> yeni sütun ekleyip formülü aşağı sürüklemek

Nasıl çalıştırılır:
    py gun02/14_tablo_liste_sozluk.py

Beklenen çıktı (seçme satırlar):
    Tabloda 6 satır var.
    İkinci satırın ili: Ankara
    Ankara satırları: 2
"""

# ---------------------------------------------------------------------------
# 1) TABLO
# ---------------------------------------------------------------------------
# sikayetler.csv'den 6 satır (birkaç sütunla). İşlemde olanın süresi None.
tablo = [
    {"no": 10507, "il": "İstanbul", "kategori": "Kesinti",       "durum": "Reddedildi", "sure": 7},
    {"no": 10527, "il": "Ankara",   "kategori": "Fatura",        "durum": "Çözüldü",    "sure": 10},
    {"no": 10550, "il": "Antalya",  "kategori": "İnternet Hızı", "durum": "İşlemde",    "sure": None},
    {"no": 10045, "il": "Konya",    "kategori": "Fatura",        "durum": "Çözüldü",    "sure": 3},
    {"no": 10076, "il": "İstanbul", "kategori": "İnternet Hızı", "durum": "Çözüldü",    "sure": 8},
    {"no": 10331, "il": "Ankara",   "kategori": "İnternet Hızı", "durum": "İşlemde",    "sure": None},
]
# Uzun tabloyu böyle hizalı yazmak zorunlu değil; okunaklı olsun diye.

print("Tabloda", len(tablo), "satır var.")
print("İlk satır (tamamı):", tablo[0])
print("İkinci satırın ili:", tablo[1]["il"])    # önce satır [1], sonra sütun ["il"]
print("Sütun adları:", list(tablo[0].keys()))
print()

# ---------------------------------------------------------------------------
# 2) TABLOYU EKRANA DÜZGÜN YAZDIRMA
# ---------------------------------------------------------------------------
# f-string genişlikleri: <14 sola yasla 14 karakter, >4 sağa yasla 4 karakter
print(f"{'No':<6} {'İl':<9} {'Kategori':<14} {'Durum':<11} {'Süre':>4}")
print("-" * 48)
for satir in tablo:
    # None ise "-" yazdır: koşullu ifade (12. dosya)
    sure_metni = "-" if satir["sure"] is None else satir["sure"]
    print(f"{satir['no']:<6} {satir['il']:<9} {satir['kategori']:<14} {satir['durum']:<11} {sure_metni:>4}")
print()

# ---------------------------------------------------------------------------
# 3) FİLTRE (Otomatik Filtre)
# ---------------------------------------------------------------------------
ankara_satirlari = [s for s in tablo if s["il"] == "Ankara"]
print("Ankara satırları:", len(ankara_satirlari))
for s in ankara_satirlari:
    print("  ", s["no"], s["kategori"], s["durum"])

cozulen_faturalar = [s["no"] for s in tablo if s["kategori"] == "Fatura" and s["durum"] == "Çözüldü"]
print("Çözülen fatura şikâyetleri:", cozulen_faturalar)
print()

# ---------------------------------------------------------------------------
# 4) SÜTUN ÜZERİNDE ÖZET (None'ları dışarıda bırakarak!)
# ---------------------------------------------------------------------------
sureler = [s["sure"] for s in tablo if s["sure"] is not None]
print("Süre sütunu (boşlar hariç):", sureler)
print(f"Ortalama süre: {sum(sureler) / len(sureler):.2f} gün")
# Excel'deki ORTALAMA da boş hücreleri atlar; Python'da bunu BİZ yaparız.
# sum([7, None]) -> TypeError. Boşları ayıklamayı unutmayın.
print()

# ---------------------------------------------------------------------------
# 5) YENİ SÜTUN EKLEME (formülü aşağı sürüklemek)
# ---------------------------------------------------------------------------
hedefler = {"Fatura": 7, "İnternet Hızı": 10, "Kesinti": 5}
for satir in tablo:
    hedef = hedefler[satir["kategori"]]          # DÜŞEYARA
    satir["hedef"] = hedef                       # yeni sütun: hedef
    if satir["sure"] is None:
        satir["asim"] = None                     # henüz bilinmiyor
    else:
        satir["asim"] = satir["sure"] > hedef    # yeni sütun: True/False
for satir in tablo:
    print(f"  {satir['no']}: hedef {satir['hedef']}, aşım {satir['asim']}")

# SIK HATA: tablo["il"] -> TypeError: list indices must be integers...
#   Tablo bir LİSTEdir; önce satır numarası verilir: tablo[0]["il"]
