# -*- coding: utf-8 -*-
"""Analiz düşüncesi: iş sorusu -> veri -> doğrulama -> özet -> yorum.

Ne öğretiyor?
    Kod yazmaya başlamadan önce SORUYU yazmayı; veriyi okuyup DOĞRULAMAYI;
    sonra tanımlayıcı istatistikleri (ortalama, medyan, mod, standart sapma,
    çeyrekler, min/max) yalnızca standart kütüphane `statistics` ile çıkarmayı.
    Paket gerekmez: bu dosya NumPy/pandas'ın B planıdır.

Nasıl çalıştırılır?
    python gun05/07_analiz_dusuncesi.py        (Windows'ta: py gun05\\07_analiz_dusuncesi.py)

Beklenen çıktı (özet):
    Toplam kayıt: 600
    Çözülen şikâyet: 415
    Ortalama: 9.60 gün, Medyan: 9.00 gün, Mod: 5 gün
    Çeyrekler (Q1, Q2, Q3): 5.0 9.0 14.0
"""
import csv
import statistics
from pathlib import Path

# Bu dosya nerede olursa olsun proje kökünü bulur (gun05 klasörünün bir üstü).
ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# 1) İŞ SORUSU — önce soruyu cümle olarak yazarız. Soru yoksa analiz de yoktur.
# ---------------------------------------------------------------------------
SORU = "Çözülen şikâyetler kaç günde çözülüyor ve süreler ne kadar dağınık?"
print("İş sorusu:", SORU)

# ---------------------------------------------------------------------------
# 2) VERİ — CSV dosyasını satır satır sözlük olarak okuruz.
#    Excel karşılığı: dosyayı açıp ilk satırı "başlık" kabul etmek.
# ---------------------------------------------------------------------------
with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))
print("Toplam kayıt:", len(kayitlar))

# ---------------------------------------------------------------------------
# 3) DOĞRULAMA — sayılara güvenmeden önce verinin beklediğimiz gibi olduğunu
#    kontrol ederiz. `assert` "bu doğru olmalı, değilse dur" demektir.
# ---------------------------------------------------------------------------
numaralar = [k["sikayet_no"] for k in kayitlar]
# set() tekrarları atar; uzunluk aynıysa her şikâyet numarası tektir.
assert len(set(numaralar)) == len(numaralar), "Tekrar eden şikâyet numarası var!"
durumlar = {k["durum"] for k in kayitlar}
print("Durum değerleri:", sorted(durumlar))

# Çözüm süresi yalnızca sonuçlanan kayıtlarda dolu olmalı; "İşlemde" olanlarda boş.
islemde_dolu = [k for k in kayitlar if k["durum"] == "İşlemde" and k["cozum_suresi_gun"] != ""]
print("İşlemde olup süresi dolu (beklenen 0):", len(islemde_dolu))

# ---------------------------------------------------------------------------
# 4) ÖZET — soruya uygun alt küme: yalnızca "Çözüldü" kayıtlarının süresi.
#    Excel karşılığı: Filtre ile durum = Çözüldü, sonra süre sütununu seçmek.
# ---------------------------------------------------------------------------
sureler = [int(k["cozum_suresi_gun"]) for k in kayitlar if k["durum"] == "Çözüldü"]
print("Çözülen şikâyet:", len(sureler))

ortalama = statistics.mean(sureler)        # Excel: ORTALAMA
medyan = statistics.median(sureler)        # Excel: ORTANCA
mod = statistics.mode(sureler)             # Excel: ENÇOK_OLAN (en sık görülen değer)
std = statistics.stdev(sureler)            # Excel: STDSAPMA.S (örneklem, n-1'e böler)
# quantiles(n=4) -> 3 kesim noktası: Q1, Q2 (=medyan), Q3.
# method="inclusive" Excel'in DÖRTTEBİRLİK.DHL ve NumPy/pandas varsayılanı ile aynı
# hesaplama yöntemidir. Varsayılan "exclusive" bazen biraz farklı sonuç verir.
q1, q2, q3 = statistics.quantiles(sureler, n=4, method="inclusive")

print(f"Ortalama: {ortalama:.2f} gün, Medyan: {medyan:.2f} gün, Mod: {mod} gün")
print(f"Standart sapma: {std:.2f} gün")
print("Çeyrekler (Q1, Q2, Q3):", q1, q2, q3)
print("En kısa / en uzun:", min(sureler), "/", max(sureler), "gün")

# ---------------------------------------------------------------------------
# 5) YORUM — sayıları iş diline çeviririz. Kod hesaplar, yorumu insan yapar.
# ---------------------------------------------------------------------------
print("Yorum:")
print(f"- Şikâyetlerin yarısı {medyan:.0f} gün veya daha kısa sürede çözülüyor (medyan).")
print(f"- Ortadaki %50'lik dilim {q1:.0f} ile {q3:.0f} gün arasında (çeyrekler arası).")
if ortalama > medyan:
    # Ortalama medyandan büyükse birkaç çok uzun kayıt ortalamayı yukarı çekiyordur.
    print("- Ortalama medyandan büyük: birkaç uzun süreli şikâyet ortalamayı yukarı çekiyor.")
else:
    print("- Ortalama medyana yakın/küçük: uç değerlerin etkisi sınırlı.")
print("- Dikkat: Bu, işlemdeki şikâyetleri kapsamaz; 'çözülme süresi' sorusunun sınırı budur.")
