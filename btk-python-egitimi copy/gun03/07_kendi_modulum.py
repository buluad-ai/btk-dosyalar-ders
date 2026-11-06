# -*- coding: utf-8 -*-
"""Kendi modülünü kullanmak: gun03/yardimcilar.py içindeki fonksiyonları import etmek.

NE ÖĞRETİYOR?
    05 numaralı dosyada yazdığımız fonksiyonları her dosyaya kopyalamak yerine
    tek bir dosyada (yardimcilar.py) topladık. Bu script onları import ediyor.
    "Hazır script çalıştırma" mantığının temeli budur: biri fonksiyonları yazar,
    diğerleri sadece çağırır. Hata düzeltilince tek yerde düzeltilir.

    Python, import edilen modülü önce ÇALIŞTIRILAN scriptin bulunduğu klasörde arar.
    Bu yüzden yardimcilar.py, bu dosyayla AYNI klasörde (gun03/) durmalıdır.

NASIL ÇALIŞTIRILIR?
    python gun03/07_kendi_modulum.py

BEKLENEN ÇIKTI:
    Modül dosyası: yardimcilar.py
    KDV dahil: 1200.0
    Hız yüzdesi: 59.6
    Şikâyet sayısı: 600
    İlk kaydın ayı: Ocak
    Çözülen kayıtların ortalama süresi: 9.60 gün
"""
from datetime import date

# Yöntem 1: modülün tamamını al; fonksiyonları "modul_adi.fonksiyon" diye çağır.
import yardimcilar

# Yöntem 2: sadece istediğin fonksiyonları al; doğrudan adıyla çağır.
from yardimcilar import sayiya_cevir, ortalama

# Modülün hangi dosyadan geldiğini görmek (yanlış dosya import ediliyor mu kontrolü):
print("Modül dosyası:", yardimcilar.__file__.replace("\\", "/").split("/")[-1])

print("KDV dahil:", yardimcilar.kdv_ekle(1000))
print("Hız yüzdesi:", yardimcilar.hiz_yuzdesi(29.8, 50))

# Modüldeki CSV okuma fonksiyonu: 4 satırlık kod tek satıra indi.
kayitlar = yardimcilar.csv_oku("sikayetler.csv")
print("Şikâyet sayısı:", len(kayitlar))

ilk_tarih = date.fromisoformat(kayitlar[0]["tarih"])     # "2026-01-01" -> date
print("İlk kaydın ayı:", yardimcilar.ay_adi(ilk_tarih))

# Çözülen kayıtların süreleri (boş hücreler sayiya_cevir ile None olur, atlanır)
sureler = []
for kayit in kayitlar:
    if kayit["durum"] == "Çözüldü":
        sure = sayiya_cevir(kayit["cozum_suresi_gun"], int)
        if sure is not None:
            sureler.append(sure)
print(f"Çözülen kayıtların ortalama süresi: {ortalama(sureler):.2f} gün")

# SIK HATA: "ModuleNotFoundError: No module named 'yardimcilar'"
#   -> yardimcilar.py başka klasörde ya da adı farklı yazılmış (yardımcılar.py gibi).
#   -> Modül adlarında Türkçe karakter ve boşluk KULLANMAYIN.
# SIK HATA: Kendi dosyanıza "statistics.py", "csv.py", "random.py" adını vermek.
#   -> Python standart modül yerine SİZİN dosyanızı import eder, garip hatalar çıkar.
