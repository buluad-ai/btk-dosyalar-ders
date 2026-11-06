# Gün 3 alıştırmaları

## Temel — herkes
CSV'de açık başvuruları sayın.

Önce beklenen sonucu kağıda yazın. Sonra `calisma.py` adıyla kendi dosyanızı oluşturun.

## Ek — erken bitirenler
Açık kayıtları ayrı CSV'ye yazın; başlığı koruyun.

## Kendi kontrolünüz
Sonucu elle hesaplayın; kodu yeniden çalıştırın. Aynı girdi aynı sonucu veriyor mu?

Çözüm: `cozumler.py`. Önce kendiniz deneyin; kopyalamadan bir satırın ne yaptığını anlatın.

## Kademeli mikro görevler (60–90 dakika)

Her görevde önce bireysel tahmin (3 dk), sonra eşli uygulama (7–10 dk), ardından açıklama (3–5 dk). Erken bitirenler örneği farklı bir sınır değeriyle tekrarlar.

### 1. Tahmin et

ortalama_hesapla([]) neden 0 yerine None döndürüyor? [0,0] sonucu nedir?

### 2. Değiştir

CSV içinde yalnız Acik kayıtları sayın ve islem_suresi değerlerini toplayın.

### 3. Hatayı düzelt

CSV metin alanlarını toplamak için toplam += kayit["islem_suresi"] yazıldığında hatayı düzeltin.

### 4. Açıkla

Çıktı CSV dosyasını yeniden okuyun; başlık satırı kayda dahil mi?

---

# Ek alıştırmalar — 600 satırlık şikâyet verisi

Çözümler: [`cozumler_ek.py`](cozumler_ek.py). Her alıştırmada önce sonucu tahmin edin, sonra yazın. Kendi dosyanızı `gun03/` içine kaydedin (ör. `gun03/calisma_t1.py`) ki `import yardimcilar` çalışsın.

## Temel (herkes)

**T1 — Fonksiyonu tekrar kullan.** `yardimcilar.kdv_ekle` ile `[2404.26, 1952.36, 826.66]` tutarlarının KDV dahil toplamını bulun.
Kontrol: `6219.93 TL`. İpucu: döngü + toplama; `:.2f` biçimi.

**T2 — Sayma (EĞERSAY).** `sikayetler.csv` içinde kanalı `e-Devlet` olan şikâyet sayısı.
Kontrol: `195`.

**T3 — Filtrele ve yaz.** İzmir şikâyetlerini `outputs/gun03/izmir.csv` dosyasına `utf-8-sig` ile yazın; sonra dosyayı geri okuyup satır sayısını yazdırın.
Kontrol: `68`. Excel'de açıp Türkçe karakterleri kontrol edin.

## Orta

**O1 — Birden çok değer döndür.** `il_ozeti(kayitlar, il)` fonksiyonu `(toplam, çözülen, çözülenlerin ortalama süresi)` döndürsün. `toplam, cozulen, ort = il_ozeti(kayitlar, "Bursa")` ile çağırın.
Kontrol: Ankara `(107, 80, 8.7)`, Bursa `53 / 29 / 9.3`.

**O2 — Tarih.** Haziran 2026'da gelen şikâyetlerin haftanın günlerine dağılımını çıkarın; en yoğun gün hangisi?
Kontrol: `87 şikâyet, en yoğun gün Cuma (20)`. İpucu: `yardimcilar.gun_adi`, `collections.Counter`.

**O3 — Dosyaya log.** `hiz_olcumleri.csv` içinde indirme hızı paket hızının %50'sinin altında kalan ölçümleri sayın; her birini `outputs/gun03/dusuk_hiz_log.txt` dosyasına bir satır olarak yazın.
Kontrol: `167`. İpucu: `yardimcilar.hiz_yuzdesi`.

## İleri (yazılımcılar için)

**İ1 — Kural tablosu.** `sikayetler_kirli.csv` için kuralları `{ad: fonksiyon}` sözlüğünde tutun; her kuralın kaç satırda ihlal edildiğini sayıp `outputs/gun03/kural_sayimlari.json` dosyasına yazın. Tekrar kontrolünü ayrı tutun.
Kontrol: beş kuralın her biri 1 kez ihlal ediliyor.

**İ2 — Parametre listesi.** `14_parametreli_script.py` mantığını, birden çok il alan bir fonksiyona çevirin (`il_raporu(("Ankara", "İzmir"))`); her il için çözüm oranını yazsın.
Kontrol: Ankara `%74.8`, İzmir `%64.7`. Ek: `sys.argv[1:]` ile komut satırından birden çok il alın.

**İ3 — TAMİŞGÜNÜ.** Excel'in `TAMİŞGÜNÜ` fonksiyonu gibi iki tarih arasındaki iş günü sayısını (iki uç dahil, hafta sonu hariç) bulan fonksiyon yazın.
Kontrol: 02.03.2026–16.03.2026 → `11`. Tartışın: resmî tatiller nasıl eklenir?

## Çıkış bileti (3 soru, 5 dakika)

1. `print` ile `return` arasındaki fark nedir? Bir örnekle anlatın.
2. CSV'deki boş hücreyi neden `0` yapmıyoruz?
3. `except ValueError:` yerine yalnızca `except:` yazmanın tehlikesi nedir?
