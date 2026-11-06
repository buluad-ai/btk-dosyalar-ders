# -*- coding: utf-8 -*-
"""Sözlük (dict): anahtar -> değer. Kayıt, sayım ve DÜŞEYARA.

Ne öğretiyor:
    - {"anahtar": değer, ...}  — değere SIRA ile değil İSİM ile ulaşırız.
    - Erişim: kayit["il"]  /  güvenli erişim: kayit.get("il", varsayılan)
    - Ekleme/değiştirme: kayit["durum"] = "Çözüldü"
    - Gezinme: .keys(), .values(), .items()
    - Üç kullanım: (1) bir kaydı tutmak, (2) sayım tablosu, (3) arama tablosu.

Excel karşılığı:
    (1) Kayıt  -> bir SATIR; anahtarlar SÜTUN BAŞLIKLARI.
    (2) Sayım  -> PivotTable: satırlarda il, değerlerde "Say".
    (3) Arama  -> DÜŞEYARA(kategori; Hedefler!A:B; 2; YANLIŞ)
                  hedefler[kategori] ile AYNI iş; bulamazsa #YOK yerine KeyError.
                  .get(kategori, 10) ise EĞERHATA(DÜŞEYARA(...); 10) gibidir.

Nasıl çalıştırılır:
    py gun02/10_sozlukler.py

Beklenen çıktı (seçme satırlar):
    İl: İstanbul | Kategori: Kesinti | Süre: 7
    Kesinti hedefi: 5 gün
    İl sayımı: {'İstanbul': 5, 'Ankara': 3, 'Antalya': 2, 'Konya': 1, 'İzmir': 2, 'Erzurum': 2}
"""

# ---------------------------------------------------------------------------
# 1) BİR KAYIT = BİR SATIR
# ---------------------------------------------------------------------------
kayit = {
    "sikayet_no": 10507,
    "il": "İstanbul",
    "kategori": "Kesinti",
    "durum": "Reddedildi",
    "sure": 7,
}
print(f"İl: {kayit['il']} | Kategori: {kayit['kategori']} | Süre: {kayit['sure']}")
# Not: f-string içinde sözlük anahtarı için TEK tırnak kullandık, çünkü
# dıştaki f"..." çift tırnaklı. (Python 3.12+ ikisini karıştırmaya izin verir
# ama bu alışkanlık her sürümde çalışır.)

# Değiştirme ve yeni alan ekleme: aynı yazım
kayit["durum"] = "Çözüldü"          # var olan anahtar -> değişir
kayit["memnuniyet"] = 2             # olmayan anahtar -> eklenir
print("Güncel kayıt:", kayit)
print("Alan sayısı:", len(kayit))
print("'operator' alanı var mı?", "operator" in kayit)   # in anahtarlara bakar
print()

# ---------------------------------------------------------------------------
# 2) ARAMA TABLOSU = DÜŞEYARA
# ---------------------------------------------------------------------------
# btk_ornek_veri.xlsx -> "Hedefler" sayfası (kategori -> hedef_gun)
hedefler = {
    "Fatura": 7,
    "İnternet Hızı": 10,
    "Kesinti": 5,
    "Taahhüt/İptal": 15,
    "Numara Taşıma": 3,
    "Kapsama": 20,
}
print("Kesinti hedefi:", hedefler["Kesinti"], "gün")
# 06_sikayet_onceliklendirme.py'deki 12 satırlık elif zinciri = TEK satır:
hedef = hedefler[kayit["kategori"]]
print(f"Bu kaydın hedefi {hedef} gün; aşıldı mı? {kayit['sure'] > hedef}")

# Olmayan anahtar:
#   hedefler["Roaming"]  -> KeyError: 'Roaming'   (Excel'deki #YOK)
# Güvenli yol .get(anahtar, varsayılan):
print("Roaming hedefi (.get):", hedefler.get("Roaming", 10), "(varsayılan)")
print("Roaming hedefi (.get, varsayılansız):", hedefler.get("Roaming"))  # None
print()

# ---------------------------------------------------------------------------
# 3) .keys() .values() .items() ile gezinme
# ---------------------------------------------------------------------------
print("Kategoriler :", list(hedefler.keys()))
print("Hedef günler:", list(hedefler.values()))
print("En sıkı hedef:", min(hedefler.values()), "gün")
for kategori, gun in hedefler.items():          # (anahtar, değer) çiftleri
    if gun >= 15:
        print(f"  Uzun hedefli kategori: {kategori} ({gun} gün)")
print()

# ---------------------------------------------------------------------------
# 4) SAYIM TABLOSU = PivotTable "Say"
# ---------------------------------------------------------------------------
# sikayetler.csv'nin ilk 15 satırının il sütunu:
iller = ["İstanbul", "Ankara", "Antalya", "Konya", "İstanbul", "İstanbul",
         "İzmir", "Erzurum", "Ankara", "Antalya", "İzmir", "Erzurum",
         "İstanbul", "İstanbul", "Ankara"]

# Yol A — if ile (mantığı en açık olan):
il_sayim = {}
for il in iller:
    if il in il_sayim:
        il_sayim[il] += 1        # daha önce gördük: bir artır
    else:
        il_sayim[il] = 1         # ilk kez görüyoruz: 1'den başlat
print("İl sayımı:", il_sayim)

# Yol B — .get ile (kısa yazım, aynı sonuç):
il_sayim_b = {}
for il in iller:
    il_sayim_b[il] = il_sayim_b.get(il, 0) + 1
print("Aynı mı?", il_sayim == il_sayim_b)

# Sayımı okunaklı yazdır:
for il, adet in il_sayim.items():
    print(f"  {il:<10} {adet}")
print("Toplam (kontrol):", sum(il_sayim.values()), "=", len(iller))

# SIK HATALAR:
#   kayit[il]       -> tırnak yok; "il" adlı DEĞİŞKENİN değerini anahtar sanır
#   kayit["İl"]     -> büyük harf; anahtar "il" olduğu için KeyError
#   il_sayim[il] += 1  (ilk görüşte) -> KeyError; önce 0/1 başlatılmalı
