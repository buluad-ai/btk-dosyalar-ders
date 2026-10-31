# -*- coding: utf-8 -*-
"""NumPy tanışma — dizi (array), vektörel işlem, maske, yüzdelik, np.where.

Ne öğretiyor?
    08_hiz_standart.py'de listelerle yaptığımız işlerin aynısını NumPy ile:
    - np.array ile dizi oluşturma,
    - TÜM diziyi tek satırda 8'e bölme (döngü yok = "vektörel işlem"),
    - toplu istatistik (mean, median, std, min/max) ve np.percentile,
    - boolean maske: paket hızının %80'inin altında kalanlar,
    - np.where ile koşula göre etiket, np.round ile yuvarlama,
    - 07'deki statistics sonuçlarıyla AYNI çıktığının kontrolü,
    - basit hız karşılaştırması: Python döngüsü vs NumPy.

Nasıl çalıştırılır?
    python gun05/09_numpy_opsiyonel.py

Beklenen çıktı (özet):
    Dizi boyutu: (400,)
    Ortalama indirme: 77.91 Mbps = 9.74 MB/s
    Paketin %80'inin altında: 278 ölçüm (%69.5)
    Kontrol: statistics ile NumPy aynı sonucu verdi.
    NumPy yoksa: ATLANDI: numpy kurulu değil — B planı: 08_hiz_standart.py
"""
import csv
import statistics
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    import numpy as np  # "np" kısaltması dünya çapında gelenektir.
except ImportError:
    print("ATLANDI: numpy kurulu değil — B planı: 08_hiz_standart.py")
else:
    # NumPy CSV okuyabilir ama başlık/metin sütunlarında zorlanır; okumayı
    # bildiğimiz csv modülüyle yapıp sayı sütunlarını diziye çeviriyoruz.
    with (ROOT / "data" / "hiz_olcumleri.csv").open(encoding="utf-8", newline="") as dosya:
        olcumler = list(csv.DictReader(dosya))

    # --- 1) Dizi oluşturma --------------------------------------------------
    # np.array: listeyi, içindeki her elemanı AYNI tipte olan bir diziye çevirir.
    # Excel karşılığı: tek bir sütun (ör. C2:C401) gibi düşünün.
    paket = np.array([float(o["paket_hizi_mbps"]) for o in olcumler])
    indirme = np.array([float(o["indirme_mbps"]) for o in olcumler])
    ping = np.array([float(o["ping_ms"]) for o in olcumler])
    print("Dizi boyutu:", indirme.shape, "| tip:", indirme.dtype)

    # --- 2) Vektörel işlem: döngü yazmadan tüm diziyi 8'e böl ---------------
    # Listede [x / 8 for x in liste] gerekirdi; dizide "indirme / 8" yeter.
    indirme_mb = np.round(indirme / 8, 2)
    print("İlk 5 indirme (MB/s):", indirme_mb[:5].tolist())

    # --- 3) Toplu istatistik --------------------------------------------------
    print(f"Ortalama indirme: {indirme.mean():.2f} Mbps = {indirme_mb.mean():.2f} MB/s")
    print(f"Medyan indirme: {np.median(indirme):.2f} Mbps")
    # DİKKAT: np.std varsayılan olarak n'e böler (ddof=0, "popülasyon").
    # Excel STDSAPMA.S ve statistics.stdev n-1'e böler -> ddof=1 yazmalıyız.
    print(f"Std (ddof=0): {indirme.std():.2f}  |  Std (ddof=1, örneklem): {indirme.std(ddof=1):.2f}")
    print("Min / Max:", indirme.min(), "/", indirme.max())
    q1, q2, q3 = np.percentile(indirme, [25, 50, 75])
    print(f"Çeyrekler: {q1:.2f} {q2:.2f} {q3:.2f}")
    print(f"Ping 90. yüzdelik: {np.percentile(ping, 90):.2f} ms")

    # --- 4) Boolean maske --------------------------------------------------------
    # Karşılaştırma tüm diziye uygulanır, sonuç True/False dizisidir.
    maske = indirme < 0.8 * paket
    print("Maskenin ilk 5 elemanı:", maske[:5].tolist())
    # Maskeyi köşeli parantez içinde kullanınca yalnızca True olan satırlar kalır.
    # Excel karşılığı: Filtre ile koşulu sağlayan satırları göstermek.
    dusukler = indirme[maske]
    print(f"Paketin %80'inin altında: {maske.sum()} ölçüm (%{maske.mean() * 100:.1f})")
    print(f"Düşük ölçümlerin ortalama indirmesi: {dusukler.mean():.2f} Mbps")

    # --- 5) np.where: koşula göre değer seç (Excel'deki EĞER) -----------------
    etiket = np.where(maske, "DÜŞÜK", "UYGUN")
    degerler, adetler = np.unique(etiket, return_counts=True)
    print("Etiket dağılımı:", dict(zip(degerler.tolist(), adetler.tolist())))
    # Gerçekleşme oranı (%), 1 ondalık: np.round
    oran = np.round(indirme / paket * 100, 1)
    print("İlk 5 gerçekleşme oranı (%):", oran[:5].tolist())

    # --- 6) Kontrol: statistics (B planı) ile aynı mı? ------------------------
    # Ondalıklı sayılarda "==" yerine "çok yakın mı?" diye bakarız (np.isclose).
    liste = indirme.tolist()
    ayni = (np.isclose(indirme.mean(), statistics.mean(liste))
            and np.isclose(np.median(indirme), statistics.median(liste))
            and np.isclose(indirme.std(ddof=1), statistics.stdev(liste))
            and np.allclose([q1, q2, q3], statistics.quantiles(liste, n=4, method="inclusive")))
    print("Kontrol: statistics ile NumPy aynı sonucu verdi." if ayni else "Kontrol: FARK VAR!")

    # --- 7) Hız karşılaştırması (basit) -----------------------------------------
    # 1 milyon sayıyı 8'e bölelim. Süreler bilgisayara göre değişir; önemli olan oran.
    buyuk_liste = list(range(1_000_000))
    buyuk_dizi = np.arange(1_000_000)
    t0 = time.perf_counter()
    _ = [x / 8 for x in buyuk_liste]          # Python döngüsü
    t1 = time.perf_counter()
    _ = buyuk_dizi / 8                         # NumPy vektörel işlem
    t2 = time.perf_counter()
    print(f"1 milyon bölme: liste {t1 - t0:.3f} sn, NumPy {t2 - t1:.4f} sn")
    print("Not: Kod da kısaldı: döngü yerine tek ifade. 400 satırda fark hissedilmez,")
    print("     milyonlarca satırda belirgindir.")
