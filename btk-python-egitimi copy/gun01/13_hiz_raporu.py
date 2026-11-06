# -*- coding: utf-8 -*-
"""Canlı kodlamanın TAMAMLANMIŞ hâli: tek bir hız ölçümünden küçük rapor.

Ne öğretiyor (Gün 1'in hepsi bir arada):
    split ile metni parçalama -> indeksle alan seçme -> float/int dönüşümü
    -> aritmetik (/, //, %) -> f-string ile biçimli rapor.

Veri: data/hiz_olcumleri.csv dosyasının 3 numaralı satırı (elle kopyalandı;
dosyadan okumayı Gün 3'te yapacağız).

Öğrenci önce 13_hiz_raporu_bos.py dosyasını doldurur; takılan bu dosyaya bakar.

Nasıl çalıştırılır:
    py gun01/13_hiz_raporu.py

Beklenen çıktı:
    === Hız ölçümü raporu ===
    Ölçüm no      : 3
    İl / Operatör : Ankara / Operatör B (Fiber)
    Paket hızı    : 100 Mbps
    İndirme       : 77.7 Mbps = 9.71 MB/s
    Taahhüt oranı : %77.7
    1000 MB indirme süresi: 1 dk 42 sn
"""

# GİRDİ: CSV dosyasındaki bir satır, tam olarak dosyada göründüğü gibi.
# Sütunlar: olcum_no,tarih,il,operator,teknoloji,paket_hizi_mbps,
#           indirme_mbps,yukleme_mbps,ping_ms
satir = "3,2026-08-23,Ankara,Operatör B,Fiber,100,77.7,36.0,10.6"

# İŞLEM 1: virgülden böl -> 9 parçalı liste. Parçaların HEPSİ metin!
alanlar = satir.split(",")

# İŞLEM 2: ihtiyacımız olan alanları indeksle seç ve doğru türe çevir.
#   indeks: 0=olcum_no 1=tarih 2=il 3=operator 4=teknoloji
#           5=paket_hizi_mbps 6=indirme_mbps 7=yukleme_mbps 8=ping_ms
olcum_no = int(alanlar[0])
il = alanlar[2]
operator_adi = alanlar[3]          # "operator" yerine operator_adi: daha açık bir ad
teknoloji = alanlar[4]
paket_hizi_mbps = int(alanlar[5])
indirme_mbps = float(alanlar[6])

# İŞLEM 3: hesaplar
indirme_mb_s = indirme_mbps / 8                    # bit -> byte
taahhut_orani = indirme_mbps / paket_hizi_mbps     # 0.777 gibi bir oran
dosya_mb = 1000
sure_sn = int(dosya_mb / indirme_mb_s)             # tam saniyeye kes
dakika = sure_sn // 60
saniye = sure_sn % 60

# ÇIKTI
print("=== Hız ölçümü raporu ===")
print(f"Ölçüm no      : {olcum_no}")
print(f"İl / Operatör : {il} / {operator_adi} ({teknoloji})")
print(f"Paket hızı    : {paket_hizi_mbps} Mbps")
print(f"İndirme       : {indirme_mbps} Mbps = {indirme_mb_s:.2f} MB/s")
print(f"Taahhüt oranı : %{taahhut_orani * 100:.1f}")
print(f"{dosya_mb} MB indirme süresi: {dakika} dk {saniye} sn")

# DENEYİN: satir değişkenini dosyadaki 1. satırla değiştirin:
#   "1,2026-07-11,İstanbul,Operatör B,Fiber,1000,53.6,26.6,14.7"
# 1000 Mbps paket alıp 53.6 Mbps almak: taahhüdün %5.4'ü! Şikâyet nedeni olur mu?
