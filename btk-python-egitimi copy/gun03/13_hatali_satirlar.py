# -*- coding: utf-8 -*-
"""Hatalı satırları ayıklamak: try / except / else / finally ile kirli CSV temizliği.

NE ÖĞRETİYOR?
    data/sikayetler_kirli.csv içinde KASITLI hatalar var (gerçek hayattaki gibi):
      - yazıyla süre ("on iki"), negatif süre (-3)
      - olmayan tarih (31.02.2026 hem yanlış biçim hem olmayan gün)
      - 1-5 dışında memnuniyet puanı (7)
      - boş kategori
      - aynı şikâyet numarasının iki kez gelmesi (tekrar eden satır)
      - fazladan boşluk / küçük harf (" ankara ", "operatör a") -> DÜZELTİLEBİLİR
    Amaç: programı DURDURMADAN hatalı satırları ayırıp gerekçesiyle raporlamak.

    try     : "bunu dene"
    except  : "hata olursa bunu yap" (program durmaz)
    else    : "hata OLMAZSA bunu yap"
    finally : "her durumda (hata olsa da olmasa da) bunu yap"

NASIL ÇALIŞTIRILIR?
    python gun03/13_hatali_satirlar.py

BEKLENEN ÇIKTI (kısaltılmış):
    Satır 8 (10253): Süre sayı değil: 'on iki'
    ...
    İşlenen: 26
    Temiz: 20, Hatalı: 6
    Düzeltilen (boşluk/harf): 2
"""
import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cikti = ROOT / "outputs" / "gun03"
cikti.mkdir(parents=True, exist_ok=True)

GECERLI_ILLER = {"İstanbul", "Ankara", "İzmir", "Antalya", "Konya", "Bursa", "Trabzon", "Erzurum"}
GECERLI_DURUMLAR = {"Çözüldü", "Reddedildi", "İşlemde"}


def satiri_dogrula(kayit):
    """Bir satırı kontrol eder ve temizlenmiş kopyasını döndürür.

    Sorun bulursa ValueError fırlatır (raise). Mesaj, hatanın gerekçesidir.
    """
    temiz = dict(kayit)        # orijinal satırı değiştirmemek için kopya

    # 1) Düzeltilebilir sorunlar: baş/son boşluk ve büyük/küçük harf
    #    strip(): baştaki/sondaki boşlukları siler (Excel: =KIRP)
    #    title(): Kelimelerin ilk harfini büyütür (Excel: =YAZIM.DÜZENİ)
    #    UYARI: title() Türkçe "i" harfini bilmez: "istanbul".title() -> "Istanbul" (noktasız!)
    #    Bu yüzden sonucu geçerli iller listesiyle karşılaştırıyoruz.
    temiz["il"] = kayit["il"].strip().title()
    temiz["operator"] = kayit["operator"].strip().title()
    if temiz["il"] not in GECERLI_ILLER:
        raise ValueError(f"Tanınmayan il: {kayit['il']!r}")

    # 2) Tarih: date.fromisoformat yanlış biçimde/olmayan günde ValueError verir
    try:
        date.fromisoformat(kayit["tarih"])
    except ValueError:
        # Kendi anlaşılır mesajımızla yeniden fırlatıyoruz
        raise ValueError(f"Geçersiz tarih: {kayit['tarih']!r}") from None

    # 3) Zorunlu alan
    if kayit["kategori"].strip() == "":
        raise ValueError("Kategori boş")
    if kayit["durum"] not in GECERLI_DURUMLAR:
        raise ValueError(f"Bilinmeyen durum: {kayit['durum']!r}")

    # 4) Süre: boş olabilir (işlemde), ama doluysa 0 veya pozitif tam sayı olmalı
    if kayit["cozum_suresi_gun"] != "":
        try:
            sure = int(kayit["cozum_suresi_gun"])
        except ValueError:
            raise ValueError(f"Süre sayı değil: {kayit['cozum_suresi_gun']!r}") from None
        if sure < 0:
            raise ValueError(f"Süre negatif: {sure}")

    # 5) Memnuniyet: boş olabilir, doluysa 1-5 arası
    if kayit["memnuniyet"] != "":
        puan = int(kayit["memnuniyet"])
        if not 1 <= puan <= 5:              # 1 <= puan <= 5 : "1 ile 5 arasında mı?"
            raise ValueError(f"Memnuniyet 1-5 dışında: {puan}")

    return temiz


with (ROOT / "data" / "sikayetler_kirli.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

temizler = []
hatalar = []                 # (satır no, şikâyet no, gerekçe)
gorulen_numaralar = set()    # tekrar kontrolü için: küme, "daha önce gördüm mü?" sorusuna hızlı cevap
islenen = 0
duzeltilen = 0

# start=2: Excel'de 1. satır başlık olduğundan ilk veri satırı 2. satırdır.
# Böylece mesajdaki satır numarası Excel'de açınca gördüğünüz numarayla aynı olur.
for satir_no, kayit in enumerate(kayitlar, start=2):
    try:
        if kayit["sikayet_no"] in gorulen_numaralar:
            raise ValueError("Tekrar eden şikâyet no")
        temiz = satiri_dogrula(kayit)
    except ValueError as hata:
        # Hata oldu: satırı atla ama NEDENİNİ kaydet
        hatalar.append((satir_no, kayit["sikayet_no"], str(hata)))
        print(f"Satır {satir_no} ({kayit['sikayet_no']}): {hata}")
    else:
        # Hata olmadı: temiz listeye ekle
        temizler.append(temiz)
        gorulen_numaralar.add(kayit["sikayet_no"])
        if temiz["il"] != kayit["il"] or temiz["operator"] != kayit["operator"]:
            duzeltilen += 1
    finally:
        # Her satırda (hatalı veya değil) çalışır: sayaç tutmak için ideal yer
        islenen += 1

print("İşlenen:", islenen)
print(f"Temiz: {len(temizler)}, Hatalı: {len(hatalar)}")
print("Düzeltilen (boşluk/harf):", duzeltilen)

# Temiz satırlar: analize hazır CSV
with open(cikti / "temiz_sikayetler.csv", "w", encoding="utf-8-sig", newline="") as f:
    yazici = csv.DictWriter(f, fieldnames=list(kayitlar[0].keys()))
    yazici.writeheader()
    yazici.writerows(temizler)

# Hatalar: veri sahibine geri gönderilecek rapor (insan okuyacak -> .txt)
with open(cikti / "hata_raporu.txt", "w", encoding="utf-8") as f:
    f.write(f"Kaynak: data/sikayetler_kirli.csv - {len(hatalar)} hatalı satır\n")
    for satir_no, no, gerekce in hatalar:
        f.write(f"Satır {satir_no}\tşikâyet {no}\t{gerekce}\n")
print("Yazıldı: outputs/gun03/temiz_sikayetler.csv ve outputs/gun03/hata_raporu.txt")

# DİKKAT: "except:" veya "except Exception:" ile HER hatayı yutmayın.
# Yazım hatası (NameError) bile sessizce "hatalı satır" sayılır ve fark etmezsiniz.
# Beklediğiniz hatayı (burada ValueError) adıyla yakalayın.
