# -*- coding: utf-8 -*-
"""Metin dosyası: open, with, yazma kipleri (w/a/r), satır satır okuma, log dosyası.

NE ÖĞRETİYOR?
    - open(dosya, kip, encoding="utf-8") ve "with" bloğu (dosya otomatik kapanır)
    - "w" = sıfırdan yaz (eski içerik SİLİNİR), "a" = sona ekle, "r" = oku
    - Satır sonu "\\n" (yeni satır) karakterini kendimiz eklemek
    - Dosyayı satır satır okumak ve içinde arama yapmak
    Gerçek hayat: Her gece çalışan bir scriptin "ne yaptım" kaydı (log) tutması.

NASIL ÇALIŞTIRILIR?
    python gun03/09_log_dosyasi.py

BEKLENEN ÇIKTI (kısaltılmış):
    Log dosyası: outputs/gun03/islem_log.txt
    1: 2026-10-14 09:00 BILGI Rapor başladı
    ...
    Log satır sayısı: 5
    UYARI satırı: 2
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cikti = ROOT / "outputs" / "gun03"
cikti.mkdir(parents=True, exist_ok=True)       # klasör yoksa oluştur, varsa sorun etme
log_dosyasi = cikti / "islem_log.txt"

# ---------------------------------------------------------------------------
# 1) "w" kipi: dosyayı SIFIRDAN yazar. Varsa eski içerik silinir!
# ---------------------------------------------------------------------------
# with bloğu bittiğinde dosya otomatik kapanır (Excel'de "Kaydet ve Kapat").
# Kapatılmayan dosya Windows'ta kilitli kalabilir, içerik diske yazılmamış olabilir.
with open(log_dosyasi, "w", encoding="utf-8") as f:
    f.write("2026-10-14 09:00 BILGI Rapor başladı\n")       # \n -> satır sonu
    f.write("2026-10-14 09:01 BILGI sikayetler.csv okundu: 600 satır\n")

# ---------------------------------------------------------------------------
# 2) "a" kipi: dosyanın SONUNA ekler (append). Eski satırlar korunur.
# ---------------------------------------------------------------------------
yeni_satirlar = [
    "2026-10-14 09:02 UYARI 96 kayıtta çözüm süresi boş",
    "2026-10-14 09:02 UYARI 1 tekrar eden kayıt bulundu",
    "2026-10-14 09:03 BILGI Rapor bitti",
]
with open(log_dosyasi, "a", encoding="utf-8") as f:
    for satir in yeni_satirlar:
        f.write(satir + "\n")
# Alternatif: print fonksiyonu da dosyaya yazabilir ve \n'yi kendisi ekler:
#     print("mesaj", file=f)

# Bu script her çalıştığında 1. adımdaki "w" dosyayı sıfırladığı için
# log hep 5 satır kalır. Sadece "a" kullansaydık her çalıştırmada büyürdü.

print("Log dosyası:", log_dosyasi.relative_to(ROOT).as_posix())

# ---------------------------------------------------------------------------
# 3) "r" kipi: satır satır okuma
# ---------------------------------------------------------------------------
uyari_sayisi = 0
satir_sayisi = 0
with open(log_dosyasi, "r", encoding="utf-8") as f:
    # enumerate(f, start=1): her satırı sıra numarasıyla birlikte verir
    for numara, satir in enumerate(f, start=1):
        satir = satir.rstrip("\n")         # sondaki satır sonunu at, yoksa boş satır basılır
        print(f"{numara}: {satir}")
        satir_sayisi += 1
        if " UYARI " in satir:             # Excel: Bul / EĞERSAY(...;"*UYARI*")
            uyari_sayisi += 1

print("Log satır sayısı:", satir_sayisi)
print("UYARI satırı:", uyari_sayisi)

# Kısa yol: tüm dosyayı tek seferde metin olarak almak (küçük dosyalar için)
tum_metin = log_dosyasi.read_text(encoding="utf-8")
print("Toplam karakter:", len(tum_metin))

# SIK HATA: encoding="utf-8" yazmamak. Windows'ta eski sistemlerde Türkçe
# karakterler "Ã¼" gibi bozuk görünür. HER open() çağrısında encoding yazın.
# SIK HATA: Dosya Excel'de açıkken yazmaya çalışmak -> PermissionError (Windows'ta
# Excel dosyayı kilitler). Not Defteri kilitlemez ama eski içeriği göstermeye devam eder.
