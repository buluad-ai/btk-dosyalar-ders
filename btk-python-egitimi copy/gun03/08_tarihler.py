# -*- coding: utf-8 -*-
"""Tarih işlemleri: datetime ile gün farkı, ay adı, hafta günü, tarih biçimi.

NE ÖĞRETİYOR?
    - Metin tarihi ("2026-03-02") gerçek tarihe çevirmek: date.fromisoformat
    - Türk biçimini ("02.03.2026") okumak/yazmak: strptime / strftime
    - İki tarih arasındaki gün farkı (Excel'de =B2-A2 veya =GÜNSAY)
    - Tarihe gün eklemek: timedelta (Excel'de =A2+10)
    - Ay adı ve hafta günü (Excel'de =METNEÇEVİR(A2;"aaaa") / =HAFTANINGÜNÜ)
    - sikayetler.csv üzerinde aylık ve haftanın gününe göre sayım

NASIL ÇALIŞTIRILIR?
    python gun03/08_tarihler.py

BEKLENEN ÇIKTI (kısaltılmış):
    Geçen gün: 14
    Hedef son gün: 12.03.2026 (Perşembe)
    ...
    En yoğun ay: ...
    İşlemdeki kayıtların ortalama bekleme süresi: ... gün
"""
import csv
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AY_ADLARI = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
GUN_ADLARI = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

# ---------------------------------------------------------------------------
# 1) Metinden tarihe
# ---------------------------------------------------------------------------
# CSV'deki tarih bir METİNDİR. "2026-03-16" - "2026-03-02" yapılamaz.
# Önce date nesnesine çevirmek gerekir. ISO biçimi (YYYY-AA-GG) için:
basvuru = date.fromisoformat("2026-03-02")
kapanis = date.fromisoformat("2026-03-16")
print("Geçen gün:", (kapanis - basvuru).days)    # iki tarih farkı -> timedelta; .days gün sayısı

# Türk biçimi "02.03.2026" ise strptime ve biçim kalıbı kullanılır:
#   %d gün, %m ay, %Y dört haneli yıl
tr_tarih = datetime.strptime("02.03.2026", "%d.%m.%Y").date()
print("Türk biçiminden okunan:", tr_tarih, "| aynı mı?", tr_tarih == basvuru)

# ---------------------------------------------------------------------------
# 2) Tarihe gün eklemek ve biçimli yazmak
# ---------------------------------------------------------------------------
hedef_gun = 10
son_gun = basvuru + timedelta(days=hedef_gun)            # Excel: =A2+10
# strftime: tarihi istediğimiz biçimde METNE çevirir.
# Ay/gün adlarını kendi listemizden alıyoruz (Windows dil ayarına güvenmiyoruz).
print(f"Hedef son gün: {son_gun.strftime('%d.%m.%Y')} ({GUN_ADLARI[son_gun.weekday()]})")
print(f"Başvuru: {basvuru.day} {AY_ADLARI[basvuru.month - 1]} {basvuru.year}")

# Yanlış tarih Python'u durdurur: date.fromisoformat("2026-02-31") -> ValueError
# (Şubat 31 yok). Bu hatayı 13_hatali_satirlar.py'de yakalayacağız.

# ---------------------------------------------------------------------------
# 3) Gerçek veri: sikayetler.csv'de aylara ve günlere göre dağılım
# ---------------------------------------------------------------------------
with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

aylik = {}          # {"Ocak": 61, "Şubat": 58, ...}  -> PivotTable: satırda ay, değerde say
gunluk = {}         # {"Pazartesi": 90, ...}
for kayit in kayitlar:
    tarih = date.fromisoformat(kayit["tarih"])
    ay = AY_ADLARI[tarih.month - 1]
    gun = GUN_ADLARI[tarih.weekday()]
    aylik[ay] = aylik.get(ay, 0) + 1          # get(ay, 0): yoksa 0'dan başla
    gunluk[gun] = gunluk.get(gun, 0) + 1

print("\nAylara göre şikâyet sayısı:")
for ay in AY_ADLARI:                          # takvim sırasıyla yaz (alfabetik değil)
    if ay in aylik:
        print(f"  {ay:<8} {aylik[ay]:>4}")

en_yogun = max(aylik, key=aylik.get)          # en büyük değere sahip anahtar
print("En yoğun ay:", en_yogun, f"({aylik[en_yogun]} şikâyet)")

print("\nHaftanın gününe göre:")
for gun in GUN_ADLARI:
    print(f"  {gun:<10} {gunluk.get(gun, 0):>4}")

# ---------------------------------------------------------------------------
# 4) İşlemdeki kayıtlar kaç gündür bekliyor?
# ---------------------------------------------------------------------------
# date.today() her gün değişir; rapor tekrar üretilebilsin diye SABİT bir
# rapor tarihi kullanıyoruz. Gerçek kullanımda: rapor_tarihi = date.today()
rapor_tarihi = date(2026, 10, 1)
bekleme = [(rapor_tarihi - date.fromisoformat(k["tarih"])).days
           for k in kayitlar if k["durum"] == "İşlemde"]
print(f"\nRapor tarihi: {rapor_tarihi.strftime('%d.%m.%Y')}")
print(f"İşlemdeki kayıt: {len(bekleme)}")
print(f"İşlemdeki kayıtların ortalama bekleme süresi: {sum(bekleme) / len(bekleme):.1f} gün")
print("En uzun bekleyen:", max(bekleme), "gün")
