# -*- coding: utf-8 -*-
"""Gün 1 genişletilmiş alıştırmalarının (ALISTIRMALAR.md) çözümleri.

Temel (T1-T4) herkes, Orta (O1-O4) erken bitirenler, İleri (İ1-İ3) iki
yazılımcı katılımcı için. Her çözüm kendi başlığı altında, birbirinden bağımsız.
T1'in çözümü ayrıca cozumler.py dosyasındadır (testler ona bakar).

Nasıl çalıştırılır:
    py gun01/cozumler_ek.py

Beklenen çıktı (son satır):
    Gün 1 ek çözümler tamamlandı.
"""

# ======================= TEMEL =======================
print("--- T1: üç sürenin ortalaması ---")
sure_1, sure_2, sure_3 = 3, 6, 12
print(f"Ortalama: {(sure_1 + sure_2 + sure_3) / 3:.2f}")      # 7.00

print("--- T2: KDV dahil fiyat ---")
KDV_ORANI = 0.20
kdv_haric = 750
print(f"KDV dahil: {kdv_haric * (1 + KDV_ORANI):.2f} TL")      # 900.00

print("--- T3: Mbps -> MB/s ---")
paket_mbps = 50
print(f"{paket_mbps} Mbps = {paket_mbps / 8:.2f} MB/s")        # 6.25

print("--- T4: metin temizleme ---")
ham = "  operatör b "
temiz = ham.strip().title()
print(f"Temiz: {temiz} | uzunluk önce {len(ham)}, sonra {len(temiz)}")   # 13 -> 10

# ======================= ORTA =======================
print("--- O1: dakikayı saat ve dakikaya çevir ---")
dakika_toplam = 200
print(f"{dakika_toplam // 60} saat {dakika_toplam % 60} dakika")  # 3 saat 20 dakika

print("--- O2: tarih biçimi değiştir ---")
tarih = "2026-03-15"
yil, ay, gun = tarih.split("-")            # 3 parçayı 3 değişkene aç
print(f"{gun}.{ay}.{yil}")                 # 15.03.2026

print("--- O3: fatura ---")
PAKET_UCRETI, PAKET_GB, ASIM_UCRETI = 400, 20, 25
kullanilan = 35
asim = max(0, kullanilan - PAKET_GB)
toplam = (PAKET_UCRETI + asim * ASIM_UCRETI) * (1 + KDV_ORANI)
print(f"Fatura: {toplam:.2f} TL")          # (400 + 15*25) * 1.2 = 930.00

print("--- O4: Türk biçimli tutarı sayıya çevir ---")
ham_tutar = "1.234,56"
# Önce binlik noktayı sil, sonra ondalık virgülü noktaya çevir. SIRA ÖNEMLİ!
tutar = float(ham_tutar.replace(".", "").replace(",", "."))
print("Tutar:", tutar, "| iki katı:", tutar * 2)   # 1234.56 | 2469.12

# ======================= İLERİ =======================
print("--- İ1: 2 GB dosyanın üç hızda indirme süresi ---")
dosya_mb = 2048
for hiz_mbps in (25, 100, 1000):          # döngü Gün 2 konusu; ileri grup için erken tanışma
    sure_sn = int(dosya_mb / (hiz_mbps / 8))
    print(f"{hiz_mbps:>5} Mbps: {sure_sn // 60} dk {sure_sn % 60} sn")
# 25 -> 10 dk 55 sn, 100 -> 2 dk 43 sn, 1000 -> 0 dk 16 sn

print("--- İ2: CSV satırından KDV hariç itiraz tutarı ---")
satir = "10527,2026-01-02,Ankara,Operatör A,Sabit İnternet,Fatura,e-Devlet,Çözüldü,10,3,2404.26"
alanlar = satir.split(",")
itiraz_kdv_dahil = float(alanlar[10])     # son sütun: itiraz_tutari_tl
print(f"{alanlar[2]} / {alanlar[5]}: KDV hariç {itiraz_kdv_dahil / (1 + KDV_ORANI):.2f} TL")  # 2003.55

print("--- İ3: sıfır kayıt için güvenli ortalama ---")
toplam_sure = 0
kayit_sayisi = 0
# if Gün 2'nin konusu; tek satırlık koşullu ifade ile sıfıra bölmeyi önlüyoruz:
sonuc = f"{toplam_sure / kayit_sayisi:.2f} gün" if kayit_sayisi > 0 else "kayıt yok"
print("Ortalama:", sonuc)                 # kayıt yok

print("Gün 1 ek çözümler tamamlandı.")
