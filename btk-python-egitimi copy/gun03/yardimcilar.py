# -*- coding: utf-8 -*-
"""Kendi modülümüz: tekrar tekrar kullandığımız iş fonksiyonları.

NE ÖĞRETİYOR?
    Bir .py dosyası aynı zamanda bir MODÜLDÜR. İçine fonksiyonlar yazıp başka
    bir scriptten `import yardimcilar` diyerek kullanabiliriz.
    Excel benzetmesi: Kişisel Makro Çalışma Kitabı (PERSONAL.XLSB) gibi düşünün;
    sık kullandığınız makroları bir yerde tutar, her dosyada çağırırsınız.

NASIL ÇALIŞTIRILIR?
    1) Normalde bu dosya başka bir dosyadan import edilir:
           python gun03/07_kendi_modulum.py
    2) Doğrudan çalıştırırsanız alttaki küçük kendi kendine testi çalışır:
           python gun03/yardimcilar.py

BEKLENEN ÇIKTI (doğrudan çalıştırınca):
    yardimcilar modülü kendi testini geçti
"""
import csv
from pathlib import Path

# Proje kökü: bu dosyanın bulunduğu klasörün (gun03) bir üstü.
# Böylece script hangi klasörden çalıştırılırsa çalıştırılsın data/ bulunur.
ROOT = Path(__file__).resolve().parents[1]

# Türkçe ay ve gün adları. Bilgisayarın dil ayarına (locale) güvenmiyoruz:
# Windows'ta locale ayarı makineden makineye değişir; kendi listemiz her yerde aynı çalışır.
AY_ADLARI = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
GUN_ADLARI = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]


def kdv_ekle(tutar, oran=0.20):
    """KDV hariç tutara KDV ekler, kuruşa yuvarlar.

    oran varsayılan olarak 0.20'dir (yüzde 20). Farklı oran gerekiyorsa
    kdv_ekle(100, oran=0.10) gibi çağrılır.
    Excel karşılığı: =YUVARLA(A2*(1+0,2); 2)
    """
    return round(tutar * (1 + oran), 2)


def kdv_ayir(kdv_dahil_tutar, oran=0.20):
    """KDV dahil tutarı (net, kdv) olarak İKİ değer döndürür.

    Kullanım:  net, kdv = kdv_ayir(1200)
    """
    net = round(kdv_dahil_tutar / (1 + oran), 2)
    kdv = round(kdv_dahil_tutar - net, 2)
    return net, kdv          # virgülle ayrılan değerler bir "tuple" olarak döner


def sla_asildi_mi(sure_gun, hedef_gun=10):
    """Çözüm süresi hedefi (SLA) aştı mı? True / False / None döndürür.

    Süre bilinmiyorsa (işlemdeki kayıt, boş hücre) None döndürür:
    "bilinmiyor" ile "aşmadı" aynı şey değildir.
    Excel karşılığı: =EĞER(A2="";"";A2>B2)
    """
    if sure_gun is None:
        return None
    return sure_gun > hedef_gun


def hiz_yuzdesi(olculen_mbps, paket_mbps):
    """Ölçülen hızın, paket hızının yüzde kaçı olduğunu bulur (1 ondalık)."""
    if paket_mbps <= 0:
        # Sıfıra bölmeyi sessizce geçmek yerine anlamlı bir hata veriyoruz.
        raise ValueError("Paket hızı sıfırdan büyük olmalı")
    return round(100 * olculen_mbps / paket_mbps, 1)


def sayiya_cevir(metin, tur=float):
    """CSV hücresini sayıya çevirir; boş hücre için None döndürür.

    CSV'den gelen her değer METİNDİR ("7", "", "2404.26").
    int("") hata verir; bu yüzden önce boş mu diye bakıyoruz.
    tur=int verilirse tam sayıya, verilmezse ondalıklı sayıya çevirir.
    """
    metin = metin.strip()
    if metin == "":
        return None
    return tur(metin)


def ortalama(sayilar):
    """Boş listede None döndüren güvenli ortalama (Gün 3 / 01 örneğindeki gibi)."""
    if not sayilar:
        return None
    return sum(sayilar) / len(sayilar)


def ay_adi(tarih):
    """date nesnesinden Türkçe ay adını verir: date(2026, 2, 5) -> 'Şubat'."""
    return AY_ADLARI[tarih.month - 1]     # month 1..12, liste sırası 0..11


def gun_adi(tarih):
    """date nesnesinden Türkçe gün adını verir. weekday(): Pazartesi=0 ... Pazar=6."""
    return GUN_ADLARI[tarih.weekday()]


def csv_oku(dosya_adi):
    """data/ klasöründeki bir CSV dosyasını sözlük listesi olarak okur.

    Örnek: kayitlar = csv_oku("sikayetler.csv")
    Her eleman bir satırdır: {"sikayet_no": "10507", "il": "İstanbul", ...}
    """
    with (ROOT / "data" / dosya_adi).open(encoding="utf-8", newline="") as dosya:
        return list(csv.DictReader(dosya))


# ---------------------------------------------------------------------------
# Aşağıdaki blok YALNIZCA bu dosya doğrudan çalıştırılınca çalışır.
# Başka bir dosya "import yardimcilar" dediğinde __name__ == "yardimcilar" olur
# ve bu test çalışmaz. Böylece import eden scriptin çıktısı kirlenmez.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from datetime import date

    # assert: "bu doğru olmalı, değilse dur" demektir. Küçük otomatik kontrol.
    assert kdv_ekle(1000) == 1200.0
    assert kdv_ekle(100, oran=0.10) == 110.0
    assert kdv_ayir(1200) == (1000.0, 200.0)
    assert sla_asildi_mi(12, 10) is True
    assert sla_asildi_mi(None) is None
    assert hiz_yuzdesi(50, 100) == 50.0
    assert sayiya_cevir("") is None
    assert sayiya_cevir(" 7 ", int) == 7
    assert ortalama([]) is None
    assert ay_adi(date(2026, 2, 5)) == "Şubat"
    assert gun_adi(date(2026, 10, 14)) == "Çarşamba"
    assert len(csv_oku("sikayetler.csv")) == 600
    print("yardimcilar modülü kendi testini geçti")
