# Gün 7 alıştırmaları

## Temel — herkes
Bir birimi filtreleyen tekrar kullanılabilir fonksiyon yazın.

Önce beklenen sonucu kağıda yazın. Sonra `calisma.py` adıyla kendi dosyanızı oluşturun.

## Ek — erken bitirenler
Boş sonuç ve bilinmeyen birim durumlarını kontrol edin.

## Kendi kontrolünüz
Sonucu elle hesaplayın; kodu yeniden çalıştırın. Aynı girdi aynı sonucu veriyor mu?

Çözüm: `cozumler.py`. Önce kendiniz deneyin; kopyalamadan bir satırın ne yaptığını anlatın.

## Kademeli mikro görevler (60–90 dakika)

Her görevde önce bireysel tahmin (3 dk), sonra eşli uygulama (7–10 dk), ardından açıklama (3–5 dk). Erken bitirenler örneği farklı bir sınır değeriyle tekrarlar.

### 1. Tahmin et

01_analiz_pipeline.py çıktısında toplam,kapalı sayısı ve kapalı ortalama ne olmalı?

### 2. Değiştir

03_parametreli_script.py dosyasını --birim B ve --birim X ile çalıştırın.

### 3. Hatayı düzelt

Dosya başka klasörden çalışınca neden sabit data/basvurular.csv yolu bulunamayabilir?

### 4. Açıkla

HTML raporundan iki bulgu ve bir sınırlama yazın. Çıktıyı aynı veriyle yeniden üretin.

---

## Ek alıştırmalar (büyük veri, bitirme)

Çözümler: `cozumler_ek.py`. Ekip projesi için: `projeler/README.md`.

### Temel — herkes

- **T1.** `05_hazir_script_uyarlama.py` dosyasını `calisma_t1.py` olarak kopyalayın. Yalnızca AYARLAR bölümünü değiştirerek **İstanbul / Kapsama / 20 gün** için çalıştırın. *Beklenen: 20 şikâyet, 16 çözülen, 20 günü aşan 6.*
- **T2.** `06_filtre_parametreleri.py` ile **Operatör C**, **Temmuz–Eylül 2026** kaç şikâyet? Durum dağılımı nedir? (Komutu kendiniz yazın.) *Beklenen: 36 kayıt; 25 Çözüldü, 6 Reddedildi, 5 İşlemde.*
- **T3.** `07_pipeline_stdlib.py --il İzmir` çalıştırın. `outputs/gun07/rapor_stdlib.html` raporunu açın; 2 bulgu ve 1 sınırlılık yazın. `ozet_stdlib.xlsx` dosyasını Excel'de açıp sayfaları gezin.

### Orta

- **O1.** Pipeline'a kategoriye göre filtre eklemek istiyoruz. Önce `cozumler_ek.py` içindeki `filtrele(kayitlar, **kosullar)` fonksiyonunu okuyun; **Fatura + Ankara** için ana sayıları hesaplayın. *Beklenen: 25 kayıt, 19 çözülen, %76.0, 6.47 gün.*
- **O2.** `07_pipeline_stdlib.py --girdi data/sikayetler_kirli.csv` çalıştırın. 6 sorunlu kaydın her birinin nedenini dosyada satırı bularak doğrulayın. Tartışın: "memnuniyet 7" satırını atmak mı, yalnızca memnuniyeti boş bırakmak mı daha doğru?
- **O3.** Excel özetine il bazında şikâyet sayılarını gösteren **Il** sayfası ekleyin (`basit_xlsx.xlsx_yaz` veya `pd.ExcelWriter`).

### İleri — iki yazılımcı için

- **İ1.** Her iki pipeline'a `--hizmet` parametresi ekleyin; `09_iki_yol_karsilastir_opsiyonel.py --hizmet Mobil` ile iki sürümün hâlâ AYNI sonucu verdiğini gösterin.
- **İ2.** `temizle()` fonksiyonu için `unittest` ile en az 3 test yazın (il yazımı düzelir, metin süre reddedilir, tekrar ayıklanır). İpucu: adı rakamla başlayan dosyayı `importlib` ile yükleyin.
- **İ3.** İki dönemi (Q2: Nisan–Haziran, Q3: Temmuz–Eylül) ana sayılar açısından karşılaştıran bir tablo üretin (kayıt, çözülen, çözülme oranı, ortalama gün ve farklar). *Beklenen: 224 → 188 kayıt; ort. 9.61 → 9.01 gün.*
