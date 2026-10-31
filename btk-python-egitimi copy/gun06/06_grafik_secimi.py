# -*- coding: utf-8 -*-
"""Hangi soru, hangi grafik? (paket gerektirmez)

NE ÖĞRETİYOR?
    Grafik türünü "güzel görünüyor" diye değil, SORUYA göre seçeriz:
        karşılaştırma  -> çubuk (bar)          "Hangi kategoride daha çok şikâyet var?"
        zaman          -> çizgi (line)         "Şikâyetler aydan aya nasıl değişti?"
        dağılım        -> histogram / kutu     "İndirme hızları nasıl dağılıyor?"
        ilişki         -> serpme (scatter)     "Paket hızı arttıkça ölçülen hız artıyor mu?"
        oran (parça/bütün) -> dikkatli pasta veya yığılmış çubuk  "Şikâyetlerin yüzde kaçı çözüldü?"
    Sonra büyük veriden (data/sikayetler.csv, 600 satır) her soru için grafiğe
    girecek SAYILARI hesaplar ve metin grafiğiyle gösterir.
    Son bölüm: çubuk ekseni 0'dan başlamazsa göz nasıl aldanır?

NASIL ÇALIŞTIRILIR?
    python gun06/06_grafik_secimi.py

BEKLENEN ÇIKTI (özet):
    Soru -> grafik eşleştirme tablosu, kategori/ay/durum sayıları ve
    "Sonuç: grafik türünü soru belirler." satırı.
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# --- 1) Soru -> grafik tablosu -------------------------------------------------
# Liste içinde demetler (tuple): (iş sorusu, sorunun türü, önerilen grafik)
eslesmeler = [
    ("Hangi kategoride daha çok şikâyet var?", "karşılaştırma", "çubuk (bar / barh)"),
    ("Şikâyetler aydan aya nasıl değişti?", "zaman", "çizgi (line)"),
    ("İndirme hızları nasıl dağılıyor?", "dağılım", "histogram"),
    ("Teknolojiler arasında hız farkı var mı?", "dağılım + karşılaştırma", "kutu (boxplot)"),
    ("Paket hızı arttıkça ölçülen hız artıyor mu?", "ilişki", "serpme (scatter)"),
    ("Şikâyetlerin yüzde kaçı çözüldü?", "oran", "yığılmış çubuk / (dikkatli) pasta"),
]
print("SORU -> GRAFİK")
print("-" * 78)
for soru, tur, grafik in eslesmeler:
    # :<44 = 44 karakterlik alana sola yasla (Excel'de sütun genişliği gibi)
    print(f"{soru:<44} {tur:<24} {grafik}")
print()

# --- 2) Veriyi oku (600 şikâyet) ----------------------------------------------
with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))   # her satır bir sözlük: {"il": "Ankara", ...}
print(f"Okunan şikâyet: {len(kayitlar)}")


def metin_grafigi(sayilar, olcek=1):
    """Sözlükteki her değer için '#' çubuğu basar. olcek=10 ise her # 10 kayıt."""
    for ad, adet in sayilar:
        print(f"  {ad:<15} {'#' * round(adet / olcek):<20} {adet}")


# Karşılaştırma: kategori bazında adet. Excel: PivotTable'da Satırlar=kategori, Değer=Say.
print("\n[Karşılaştırma -> çubuk] Kategoriye göre şikâyet (her # = 10 kayıt)")
kategori_sayilari = Counter(k["kategori"] for k in kayitlar)
metin_grafigi(kategori_sayilari.most_common(), olcek=10)   # most_common = büyükten küçüğe

# Zaman: ay bazında adet. "2026-03-14"[:7] -> "2026-03" (Excel'deki SOLDAN(metin;7))
print("\n[Zaman -> çizgi] Aylık şikâyet sayısı (her # = 5 kayıt)")
aylik = Counter(k["tarih"][:7] for k in kayitlar)
metin_grafigi(sorted(aylik.items()), olcek=5)   # zaman verisi TARİH sırasıyla gösterilir!

# Oran: durumların toplam içindeki payı. Parçalar toplamı %100 olmalı.
print("\n[Oran -> yığılmış çubuk] Duruma göre pay")
durumlar = Counter(k["durum"] for k in kayitlar)
toplam_yuzde = 0
for durum, adet in durumlar.most_common():
    yuzde = adet / len(kayitlar) * 100
    toplam_yuzde += yuzde
    print(f"  {durum:<12} {adet:>4}  %{yuzde:.1f}")
print(f"  Toplam yüzde: %{toplam_yuzde:.0f}  (pasta yalnızca parçalar %100 ediyorsa anlamlıdır)")

# --- 3) Neden çubuk ekseni 0'dan başlamalı? -------------------------------------
# Çubuğun BOYU değeri temsil eder. Eksen 140'tan başlarsa 143 ile 160 arasındaki
# küçük fark devasa görünür. Aşağıda aynı iki sayıyı iki şekilde çiziyoruz.
print("\n[Hile mi?] Aynı iki sayı, iki farklı eksen başlangıcı")
fatura, hiz = kategori_sayilari["Fatura"], kategori_sayilari["İnternet Hızı"]
# (baslangic, her # kaç kayıt) çiftleri: iki çizimde de en uzun çubuk ~20 karakter olsun
for baslangic, olcek in ((0, 8), (140, 1)):
    print(f"  Eksen {baslangic} değerinden başlarsa (her # = {olcek} kayıt):")
    for ad, adet in (("Fatura", fatura), ("İnternet Hızı", hiz)):
        print(f"    {ad:<14} {'#' * ((adet - baslangic) // olcek)} {adet}")
gorunen = (fatura - 140) / (hiz - 140)
print(f"  Gerçek oran: {fatura}/{hiz} = {fatura / hiz:.2f} kat; "
      f"140'tan başlayan eksende çubuklar {gorunen:.1f} kat farklı görünür.")

print("\nSonuç: grafik türünü soru belirler.")
