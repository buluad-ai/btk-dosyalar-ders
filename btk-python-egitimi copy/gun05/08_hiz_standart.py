# -*- coding: utf-8 -*-
"""Hız ölçümleri — liste ile toplu işlem (NumPy'ın B planı).

Ne öğretiyor?
    NumPy olmadan, listeler ve `statistics` ile:
    - tüm ölçümleri Mbps'tan MB/s'ye çevirme (her elemanı 8'e bölme),
    - toplu istatistik (ortalama, medyan, std, yüzdelikler),
    - "maske" mantığı: paket hızının %80'inin altında kalan ölçümleri bulma,
    - koşula göre etiket (NumPy'daki np.where karşılığı).
    Aynı işlerin NumPy hali: 09_numpy_opsiyonel.py

Nasıl çalıştırılır?
    python gun05/08_hiz_standart.py

Beklenen çıktı (özet):
    Ölçüm sayısı: 400
    Ortalama indirme: 77.91 Mbps = 9.74 MB/s
    Paketin %80'inin altında: 278 ölçüm (%69.5)
"""
import csv
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

with (ROOT / "data" / "hiz_olcumleri.csv").open(encoding="utf-8", newline="") as dosya:
    olcumler = list(csv.DictReader(dosya))
print("Ölçüm sayısı:", len(olcumler))

# CSV'den gelen her şey metindir; sayıya çevirmeden hesap yapılamaz.
paket = [float(o["paket_hizi_mbps"]) for o in olcumler]
indirme = [float(o["indirme_mbps"]) for o in olcumler]
ping = [float(o["ping_ms"]) for o in olcumler]

# --- 1) Toplu dönüşüm: Mbps -> MB/s (1 bayt = 8 bit, o yüzden 8'e böleriz) ----
# Excel karşılığı: yan sütuna =B2/8 yazıp aşağı doğru sürüklemek.
indirme_mb = [round(x / 8, 2) for x in indirme]
print("İlk 5 indirme (Mbps):", indirme[:5])
print("İlk 5 indirme (MB/s):", indirme_mb[:5])

# --- 2) Toplu istatistik ----------------------------------------------------
ort = statistics.mean(indirme)
print(f"Ortalama indirme: {ort:.2f} Mbps = {ort / 8:.2f} MB/s")
print(f"Medyan indirme: {statistics.median(indirme):.2f} Mbps")
print(f"Standart sapma (örneklem): {statistics.stdev(indirme):.2f} Mbps")
# 100'e bölünmüş kesim noktaları = yüzdelikler. [89] -> 90. yüzdelik.
# method="inclusive" NumPy'ın np.percentile varsayılanıyla aynı sonucu verir.
yuzdelikler = statistics.quantiles(ping, n=100, method="inclusive")
print(f"Ping 90. yüzdelik: {yuzdelikler[89]:.2f} ms (ölçümlerin %90'ı bunun altında)")

# --- 3) Maske: paket hızının %80'inin altında kalan ölçümler -----------------
# Her ölçüm için True/False listesi. Excel: =C2<0,8*B2 formülünü sürüklemek.
dusuk_mu = [i < 0.8 * p for i, p in zip(indirme, paket)]
dusuk_sayi = sum(dusuk_mu)  # True = 1, False = 0 sayılır; toplam = kaç True var.
print(f"Paketin %80'inin altında: {dusuk_sayi} ölçüm (%{dusuk_sayi / len(paket) * 100:.1f})")

# --- 4) Koşula göre etiket (np.where karşılığı) ------------------------------
# Excel: =EĞER(C2<0,8*B2; "DÜŞÜK"; "UYGUN")
etiket = ["DÜŞÜK" if d else "UYGUN" for d in dusuk_mu]
print("Etiket dağılımı:", dict(Counter(etiket)))

# --- 5) Teknolojiye göre düşük ölçüm oranı ----------------------------------
toplam_tek = Counter(o["teknoloji"] for o in olcumler)
dusuk_tek = Counter(o["teknoloji"] for o, d in zip(olcumler, dusuk_mu) if d)
for tek in sorted(toplam_tek):
    print(f"  {tek:6}: {dusuk_tek[tek]:3} / {toplam_tek[tek]:3} düşük (%{dusuk_tek[tek] / toplam_tek[tek] * 100:.0f})")

print("Yorum: Ölçümler anlıktır (Wi-Fi, saat, cihaz etkiler); tek ölçümle operatör suçlanmaz,")
print("       ama aynı teknolojide oranın yüksek olması incelenecek bir işarettir.")
