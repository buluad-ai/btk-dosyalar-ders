# -*- coding: utf-8 -*-
"""CANLI KODLAMA İSKELETİ: tek bir hız ölçümünden küçük rapor.

Görev: TODO yazan satırları birlikte dolduracağız. Dosya ŞU HÂLİYLE DE
çalışır (yer tutucu değerlerle); her TODO'yu doldurdukça çıktı düzelir.
Tamamlanmış hâli: 13_hiz_raporu.py (önce kendiniz deneyin!).

Nasıl çalıştırılır:
    py gun01/13_hiz_raporu_bos.py

Beklenen çıktı (doldurulmadan önce):
    === Hız ölçümü raporu (iskelet) ===
    ... değerler ? veya 0 görünür ...
    TODO sayısı: 7
Doldurduktan sonra çıktı 13_hiz_raporu.py ile aynı olmalı.
"""

satir = "3,2026-08-23,Ankara,Operatör B,Fiber,100,77.7,36.0,10.6"
#  indeks: 0=olcum_no 1=tarih 2=il 3=operator 4=teknoloji
#          5=paket_hizi_mbps 6=indirme_mbps 7=yukleme_mbps 8=ping_ms

alanlar = satir.split(",")   # hazır: metni virgülden böldük

# TODO 1: il adını alanlar listesinden al  (ipucu: alanlar[2])
il = "?"
# TODO 2: operatör adını al
operator_adi = "?"
# TODO 3: paket hızını al ve int'e çevir  (ipucu: int(alanlar[5]))
paket_hizi_mbps = 1          # yer tutucu (0 olursa aşağıda sıfıra bölme olur!)
# TODO 4: indirme hızını al ve float'a çevir
indirme_mbps = 0.0

# TODO 5: Mbps'yi MB/s'ye çevir (ipucu: 8'e böl)
indirme_mb_s = 0.0
# TODO 6: taahhüt oranı = indirme / paket
taahhut_orani = indirme_mbps / paket_hizi_mbps

# TODO 7: f-string ile MB/s değerini 2 ondalıklı yazdır  (ipucu: {deger:.2f})
print("=== Hız ölçümü raporu (iskelet) ===")
print(f"İl / Operatör : {il} / {operator_adi}")
print(f"Paket hızı    : {paket_hizi_mbps} Mbps")
print(f"İndirme       : {indirme_mbps} Mbps = {indirme_mb_s} MB/s")
print(f"Taahhüt oranı : %{taahhut_orani * 100:.1f}")
print("TODO sayısı: 7")
