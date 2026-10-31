# -*- coding: utf-8 -*-
"""Hazır bir scripti OKUMA ve UYARLAMA: yalnızca AYARLAR bölümünü değiştir.

NE ÖĞRETİYOR?
    İş hayatında çoğu zaman sıfırdan kod yazmazsınız; bir meslektaşın scriptini alıp
    kendi sorunuza uyarlarsınız. İyi yazılmış bir script, değiştirilecek her şeyi
    EN ÜSTTE, büyük harfli "AYARLAR" bölümünde toplar. Aşağısına dokunmanız gerekmez.

    Uyarlama adımları (sınıfta birlikte):
      1) Scripti olduğu gibi çalıştırın; çıktıyı not edin.
      2) AYARLAR'da tek bir değeri değiştirin (ör. IL = "İzmir"); kaydedin; çalıştırın.
      3) Çıktı beklediğiniz gibi değişti mi? Elle küçük bir kontrol yapın.
      4) Sonra bir sonrakini değiştirin. (Aynı anda üç şeyi değiştirmeyin: hata
         çıkarsa hangisinden olduğunu bilemezsiniz.)

    Excel karşılığı: bir makronun başındaki "Const ESIK = 10" satırını değiştirmek.

NASIL ÇALIŞTIRILIR?
    python gun07/05_hazir_script_uyarlama.py

BEKLENEN ÇIKTI (varsayılan ayarlarla):
    Ankara / İnternet Hızı: 24 şikâyet, 17 çözülen
    10 günü aşan çözüm: 12
    Liste: outputs/gun07/05_esik_asanlar.csv
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# =========================== AYARLAR (yalnızca burayı değiştirin) ===========================
VERI_DOSYASI = ROOT / "data" / "sikayetler.csv"
IL = "Ankara"                   # Geçerli iller: İstanbul, Ankara, İzmir, Antalya, Konya, Bursa, Trabzon, Erzurum
KATEGORI = "İnternet Hızı"      # Fatura, İnternet Hızı, Taahhüt/İptal, Kesinti, Kapsama, Numara Taşıma
ESIK_GUN = 10                   # Bu günü AŞAN (>) çözüm süreleri listelenir
CIKTI_ADI = "05_esik_asanlar.csv"
# ============================================================================================
# Bu çizginin altını değiştirmeniz gerekmez.

with VERI_DOSYASI.open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

# Excel Otomatik Filtre: il = IL VE kategori = KATEGORI
secilen = [k for k in kayitlar if k["il"] == IL and k["kategori"] == KATEGORI]
cozulen = [k for k in secilen if k["durum"] == "Çözüldü"]
# Eşiği aşanlar: süre metin geldiği için int() ile sayıya çeviriyoruz
asanlar = [k for k in cozulen if int(k["cozum_suresi_gun"]) > ESIK_GUN]

print(f"{IL} / {KATEGORI}: {len(secilen)} şikâyet, {len(cozulen)} çözülen")
print(f"{ESIK_GUN} günü aşan çözüm: {len(asanlar)}")
if not secilen:
    print("UYARI: hiç kayıt yok. IL ve KATEGORI yazımını (büyük/küçük harf, Türkçe karakter) kontrol edin.")

cikti = ROOT / "outputs" / "gun07"
cikti.mkdir(parents=True, exist_ok=True)
# utf-8-sig: Excel'in Türkçe karakterleri doğru göstermesi için dosya başına işaret (BOM) koyar.
# delimiter=";" : Türkçe Excel'de liste ayırıcı noktalı virgüldür; çift tıklayınca sütunlar ayrı açılır.
with (cikti / CIKTI_ADI).open("w", encoding="utf-8-sig", newline="") as dosya:
    yazici = csv.writer(dosya, delimiter=";")
    yazici.writerow(["sikayet_no", "tarih", "operator", "kanal", "cozum_suresi_gun"])
    for k in asanlar:
        yazici.writerow([k["sikayet_no"], k["tarih"], k["operator"], k["kanal"], k["cozum_suresi_gun"]])
print(f"Liste: outputs/gun07/{CIKTI_ADI}")
