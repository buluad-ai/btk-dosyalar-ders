# -*- coding: utf-8 -*-
"""GÜN 2 MİNİ PROJE (tamamlanmış hâl): 15 şikâyetlik tablodan özet rapor.

Ne öğretiyor (Gün 2'nin hepsi bir arada):
    liste içinde sözlük (tablo) + for + if + sayaç/biriktirici + dict sayım
    + DÜŞEYARA (hedefler sözlüğü) + None kontrolü + f-string ile rapor.

Veri: data/sikayetler.csv dosyasının İLK 15 satırı, elle koda gömüldü.
      Dosyadan okumayı Gün 3'te yapacağız; o zaman aynı kod 600 satırda çalışacak.
Hedefler: data/btk_ornek_veri.xlsx -> "Hedefler" sayfası.

Sorular:
    1. Kaç şikâyet var, durumlara göre dağılımı ne?
    2. İl bazında kaç şikâyet var? (PivotTable)
    3. En uzun süren şikâyet hangisi?
    4. Hangi şikâyetler kategori hedef süresini aştı? Kaç gün gecikti?

Öğrenci önce 15_mini_proje_bos.py dosyasını doldurur.

Nasıl çalıştırılır:
    py gun02/15_mini_proje.py

Beklenen çıktı (seçme satırlar):
    Toplam şikâyet: 15
    Durumlar: Çözüldü 11, Reddedildi 1, İşlemde 3
    İstanbul   ##### 5
    En uzun süren: 10520 (İstanbul, Taahhüt/İptal) 17 gün
    Hedef aşan: 5 / 12 sonuçlanmış şikâyet (%41.7)
    Rapor kaydedildi: outputs/gun02/mini_proje_raporu.txt
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# VERİ: her sözlük bir satır (sure: çözüm süresi gün; İşlemde ise None)
# ---------------------------------------------------------------------------
sikayetler = [
    {"no": 10507, "tarih": "2026-01-01", "il": "İstanbul", "operator": "Operatör A", "kategori": "Kesinti",       "durum": "Reddedildi", "sure": 7},
    {"no": 10527, "tarih": "2026-01-02", "il": "Ankara",   "operator": "Operatör A", "kategori": "Fatura",        "durum": "Çözüldü",    "sure": 10},
    {"no": 10550, "tarih": "2026-01-03", "il": "Antalya",  "operator": "Operatör A", "kategori": "İnternet Hızı", "durum": "İşlemde",    "sure": None},
    {"no": 10045, "tarih": "2026-01-05", "il": "Konya",    "operator": "Operatör C", "kategori": "Fatura",        "durum": "Çözüldü",    "sure": 3},
    {"no": 10076, "tarih": "2026-01-05", "il": "İstanbul", "operator": "Operatör A", "kategori": "İnternet Hızı", "durum": "Çözüldü",    "sure": 8},
    {"no": 10416, "tarih": "2026-01-05", "il": "İstanbul", "operator": "Operatör B", "kategori": "Taahhüt/İptal", "durum": "Çözüldü",    "sure": 11},
    {"no": 10253, "tarih": "2026-01-06", "il": "İzmir",    "operator": "Operatör B", "kategori": "Kapsama",       "durum": "Çözüldü",    "sure": 15},
    {"no": 10290, "tarih": "2026-01-06", "il": "Erzurum",  "operator": "Operatör A", "kategori": "Numara Taşıma", "durum": "Çözüldü",    "sure": 2},
    {"no": 10331, "tarih": "2026-01-06", "il": "Ankara",   "operator": "Operatör D", "kategori": "İnternet Hızı", "durum": "İşlemde",    "sure": None},
    {"no": 10477, "tarih": "2026-01-07", "il": "Antalya",  "operator": "Operatör A", "kategori": "Fatura",        "durum": "Çözüldü",    "sure": 2},
    {"no": 10586, "tarih": "2026-01-07", "il": "İzmir",    "operator": "Operatör C", "kategori": "Numara Taşıma", "durum": "Çözüldü",    "sure": 8},
    {"no": 10530, "tarih": "2026-01-08", "il": "Erzurum",  "operator": "Operatör B", "kategori": "Taahhüt/İptal", "durum": "Çözüldü",    "sure": 13},
    {"no": 10042, "tarih": "2026-01-10", "il": "İstanbul", "operator": "Operatör C", "kategori": "Fatura",        "durum": "İşlemde",    "sure": None},
    {"no": 10520, "tarih": "2026-01-10", "il": "İstanbul", "operator": "Operatör C", "kategori": "Taahhüt/İptal", "durum": "Çözüldü",    "sure": 17},
    {"no": 10567, "tarih": "2026-01-10", "il": "Ankara",   "operator": "Operatör A", "kategori": "İnternet Hızı", "durum": "Çözüldü",    "sure": 11},
]

# Arama tablosu (DÜŞEYARA'nın sağ tarafı)
hedefler = {"Fatura": 7, "İnternet Hızı": 10, "Kesinti": 5,
            "Taahhüt/İptal": 15, "Numara Taşıma": 3, "Kapsama": 20}

# Raporu hem ekrana yazıp hem dosyaya kaydetmek için satırları bir listede topluyoruz.
rapor = []


def yaz(metin=""):
    """Satırı ekrana basar ve rapor listesine ekler. (def ayrıntısı Gün 3.)"""
    print(metin)
    rapor.append(metin)


yaz("=== GÜN 2 MİNİ PROJE: ŞİKÂYET ÖZETİ ===")

# ---------------------------------------------------------------------------
# SORU 1: toplam ve durum dağılımı
# ---------------------------------------------------------------------------
durum_sayim = {}
for s in sikayetler:
    durum_sayim[s["durum"]] = durum_sayim.get(s["durum"], 0) + 1
yaz(f"Toplam şikâyet: {len(sikayetler)}")
yaz(f"Durumlar: Çözüldü {durum_sayim.get('Çözüldü', 0)}, "
    f"Reddedildi {durum_sayim.get('Reddedildi', 0)}, İşlemde {durum_sayim.get('İşlemde', 0)}")
yaz()

# ---------------------------------------------------------------------------
# SORU 2: il bazında sayım (PivotTable: satır=il, değer=say)
# ---------------------------------------------------------------------------
il_sayim = {}
for s in sikayetler:
    il_sayim[s["il"]] = il_sayim.get(s["il"], 0) + 1

# Çoktan aza sıralama. "key=lambda ..." HAZIR KALIPTIR; ezberlemeyin, okuyun:
#   "çiftleri (il, adet) 2. elemanına (adet) göre, büyükten küçüğe sırala"
sirali_iller = sorted(il_sayim.items(), key=lambda cift: cift[1], reverse=True)
yaz("İl bazında şikâyet sayısı:")
for il, adet in sirali_iller:
    yaz(f"  {il:<10} {'#' * adet} {adet}")       # '#' * 5 -> '#####' : metin grafiği
yaz()

# ---------------------------------------------------------------------------
# SORU 3: en uzun süren şikâyet (MAK + o satırın bilgileri)
# ---------------------------------------------------------------------------
en_uzun = None                       # henüz bir satır seçmedik
for s in sikayetler:
    if s["sure"] is None:
        continue                     # işlemdekileri atla
    if en_uzun is None or s["sure"] > en_uzun["sure"]:
        en_uzun = s                  # SATIRIN TAMAMINI saklıyoruz
yaz(f"En uzun süren: {en_uzun['no']} ({en_uzun['il']}, {en_uzun['kategori']}) {en_uzun['sure']} gün")
yaz()

# ---------------------------------------------------------------------------
# SORU 4: hedef aşımı raporu
# ---------------------------------------------------------------------------
asanlar = []                         # hedefi aşan satırlar
sonuclanan = 0                       # süresi belli olan kayıt sayısı
for s in sikayetler:
    if s["sure"] is None:
        continue
    sonuclanan += 1
    hedef = hedefler.get(s["kategori"], 10)      # DÜŞEYARA (bulamazsa 10)
    if s["sure"] > hedef:
        asanlar.append({"no": s["no"], "il": s["il"], "kategori": s["kategori"],
                        "sure": s["sure"], "hedef": hedef, "gecikme": s["sure"] - hedef})

yaz("Hedef süreyi aşan şikâyetler:")
yaz(f"  {'No':<6} {'İl':<9} {'Kategori':<14} {'Süre':>4} {'Hedef':>5} {'Gecikme':>7}")
for a in asanlar:
    yaz(f"  {a['no']:<6} {a['il']:<9} {a['kategori']:<14} {a['sure']:>4} {a['hedef']:>5} {a['gecikme']:>7}")
oran = len(asanlar) / sonuclanan
yaz(f"Hedef aşan: {len(asanlar)} / {sonuclanan} sonuçlanmış şikâyet (%{oran * 100:.1f})")
toplam_gecikme = sum(a["gecikme"] for a in asanlar)
yaz(f"Toplam gecikme: {toplam_gecikme} gün")

# İl bazında aşım sayısı (hangi ilde sorun yoğun?)
il_asim = {}
for a in asanlar:
    il_asim[a["il"]] = il_asim.get(a["il"], 0) + 1
yaz(f"İl bazında aşım: {il_asim}")
yaz()

# ---------------------------------------------------------------------------
# RAPORU DOSYAYA KAYDET (Gün 3 önizlemesi — şimdilik olduğu gibi kabul edin)
# ---------------------------------------------------------------------------
# ROOT: bu dosyanın iki üst klasörü = proje kökü. Böylece script hangi
# klasörden çalıştırılırsa çalıştırılsın çıktı doğru yere gider.
ROOT = Path(__file__).resolve().parents[1]
cikti_klasoru = ROOT / "outputs" / "gun02"
cikti_klasoru.mkdir(parents=True, exist_ok=True)
cikti_dosyasi = cikti_klasoru / "mini_proje_raporu.txt"
cikti_dosyasi.write_text("\n".join(rapor) + "\n", encoding="utf-8")
print("Rapor kaydedildi: outputs/gun02/mini_proje_raporu.txt")
# Windows'ta dosyayı Not Defteri ile açabilirsiniz. Excel'de AÇIK tutarken
# tekrar çalıştırırsanız PermissionError alabilirsiniz: önce kapatın.
