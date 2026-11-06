# -*- coding: utf-8 -*-
"""Algoritma: girdi -> işlem -> çıktı. Dört küçük iş hayatı örneği.

Ne öğretiyor:
    - Algoritma, bir problemi çözmek için SIRALI ve NET adımlar listesidir
      (yemek tarifi gibi). Kod yazmadan önce adımları Türkçe yazarız.
    - Akış şeması (metin hâliyle) okumak.
    - Örnekler: KDV hesabı, fatura tutarı, Mbps -> MB/s ve indirme süresi,
      ortalama memnuniyet.

Nasıl çalıştırılır:
    py gun01/11_algoritma_ornekleri.py

Beklenen çıktı (seçme satırlar):
    KDV dahil fiyat: 600.00 TL
    Fatura toplamı: 570.00 TL
    100 Mbps = 12.50 MB/s
    Ortalama memnuniyet: 3.60
"""

# ===========================================================================
# ÖRNEK 1: KDV HESABI
# ===========================================================================
# AKIŞ ŞEMASI (metin):
#
#     [BAŞLA]
#        |
#     /KDV hariç fiyatı al/            <- GİRDİ  (paralelkenar)
#        |
#     [kdv = fiyat * 0.20]             <- İŞLEM  (dikdörtgen)
#     [toplam = fiyat + kdv]
#        |
#     /toplamı yaz/                    <- ÇIKTI
#        |
#     [BİTİR]
#
KDV_ORANI = 0.20                      # %20 (oran değişirse sadece burayı değiştirin)
kdv_haric_fiyat = 500                 # GİRDİ
kdv_tutari = kdv_haric_fiyat * KDV_ORANI          # İŞLEM
kdv_dahil_fiyat = kdv_haric_fiyat + kdv_tutari
print("--- Örnek 1: KDV ---")
print(f"KDV tutarı: {kdv_tutari:.2f} TL")          # ÇIKTI
print(f"KDV dahil fiyat: {kdv_dahil_fiyat:.2f} TL")

# Tersi: KDV DAHİL fiyattan KDV hariç fiyatı bulmak (sık yapılan hata:
# 600 * 0.80 = 480 YANLIŞ; doğrusu 600 / 1.20 = 500).
print(f"Geri hesap: {kdv_dahil_fiyat / (1 + KDV_ORANI):.2f} TL")
print()

# ===========================================================================
# ÖRNEK 2: MOBİL FATURA TUTARI
# ===========================================================================
# Kurgusal tarife: aylık paket 400 TL, pakete 20 GB dahil.
# Aşan her GB için 25 TL. Üstüne KDV %20 eklenir.
#
# ADIMLAR:
#   1. Kullanılan GB'ı al (girdi).
#   2. Aşım = kullanılan - paket (eksiyse 0 kabul et -> max(0, ...)).
#   3. Ara toplam = paket ücreti + aşım * GB ücreti.
#   4. Toplam = ara toplam * (1 + KDV).
#   5. Yaz.
PAKET_UCRETI_TL = 400
PAKET_GB = 20
ASIM_GB_UCRETI_TL = 25
kullanilan_gb = 23                                    # GİRDİ

asim_gb = max(0, kullanilan_gb - PAKET_GB)            # max: büyük olanı seç (Excel: MAK)
ara_toplam = PAKET_UCRETI_TL + asim_gb * ASIM_GB_UCRETI_TL
fatura_toplami = ara_toplam * (1 + KDV_ORANI)
print("--- Örnek 2: Fatura ---")
print(f"Aşım: {asim_gb:.2f} GB")
print(f"Ara toplam: {ara_toplam:.2f} TL")
print(f"Fatura toplamı: {fatura_toplami:.2f} TL")
# Elle kontrol: aşım 23 - 20 = 3 GB; 3 * 25 = 75 TL; 400 + 75 = 475 TL;
# 475 * 1.20 = 570.00 TL. Kodun çıktısı da bu olmalı.
# DENEYİN: kullanilan_gb = 15 yapın. Aşım eksi çıkmaz, max(0, -5) = 0 olur;
# fatura 400 * 1.20 = 480.00 TL. max() olmasaydı müşteriye para iade ederdik!
print()

# ===========================================================================
# ÖRNEK 3: Mbps -> MB/s DÖNÜŞÜMÜ ve İNDİRME SÜRESİ
# ===========================================================================
# Operatör "100 Mbps" der; indirme programı "12.5 MB/s" gösterir. Neden?
#   Mbps = megaBIT / saniye      MB/s = megaBYTE / saniye
#   1 byte = 8 bit  ->  MB/s = Mbps / 8
#
# ADIMLAR: hızı al -> 8'e böl -> dosya boyutunu (MB) bu hıza böl -> saniye
#          -> saniyeyi // ve % ile dakika:saniye yap.
paket_hizi_mbps = 100
dosya_boyutu_mb = 4500                     # yaklaşık 4.5 GB'lık bir dosya
hiz_mb_s = paket_hizi_mbps / 8
sure_sn = dosya_boyutu_mb / hiz_mb_s
print("--- Örnek 3: Hız ---")
print(f"{paket_hizi_mbps} Mbps = {hiz_mb_s:.2f} MB/s")
print(f"{dosya_boyutu_mb} MB dosya: {sure_sn:.0f} sn "
      f"= {int(sure_sn) // 60} dk {int(sure_sn) % 60} sn")
# Gerçekte ölçülen hız paket hızından düşüktür; Gün 3'te hiz_olcumleri.csv
# ile "taahhüdün yüzde kaçı verilmiş?" sorusunu soracağız.
olculen_mbps = 73.5
print(f"Ölçülen {olculen_mbps} Mbps, taahhüdün %{olculen_mbps / paket_hizi_mbps * 100:.1f}'i")
print()

# ===========================================================================
# ÖRNEK 4: ORTALAMA MEMNUNİYET (1-5 puan)
# ===========================================================================
# ADIMLAR: puanları al -> topla -> adede böl -> yaz.
# Elle önce tahmin edin: 4 + 2 + 5 + 3 + 4 = 18; 18 / 5 = 3.6
puan_1, puan_2, puan_3, puan_4, puan_5 = 4, 2, 5, 3, 4
toplam_puan = puan_1 + puan_2 + puan_3 + puan_4 + puan_5
adet = 5
print("--- Örnek 4: Ortalama ---")
print(f"Toplam puan: {toplam_puan}")
print(f"Ortalama memnuniyet: {toplam_puan / adet:.2f}")
# Gün 2'de 5 ayrı değişken yerine tek bir LİSTE kullanacağız:
#   puanlar = [4, 2, 5, 3, 4];  sum(puanlar) / len(puanlar)
