# Gün 4 alıştırmaları

## Temel — herkes
Bellekte SQLite tablosuna [2, 7, 3, 9] sürelerini ekleyin ve sayın.

Önce beklenen sonucu kağıda yazın. Sonra `calisma.py` adıyla kendi dosyanızı oluşturun.

## Ek — erken bitirenler
Parametreli sorguyla 5 günü aşanların ortalamasını bulun.

## Kendi kontrolünüz
Sonucu elle hesaplayın; kodu yeniden çalıştırın. Aynı girdi aynı sonucu veriyor mu?

Çözüm: `cozumler.py`. Önce kendiniz deneyin; kopyalamadan bir satırın ne yaptığını anlatın.

## Kademeli mikro görevler (60–90 dakika)

Her görevde önce bireysel tahmin (3 dk), sonra eşli uygulama (7–10 dk), ardından açıklama (3–5 dk). Erken bitirenler örneği farklı bir sınır değeriyle tekrarlar.

### 1. Tahmin et

36 satırlık tabloya aynı INSERT işlemi tekrar yapılırsa benzersiz kimlik ne sağlar?

### 2. Değiştir

SQL sorgusunda `sure > ?` parametresini 8 yapın; kayıt sayısını bulun.

### 3. Hatayı düzelt

JOIN koşulu kaldırılırsa 36 başvuru ve 3 birimden kaç satır gelir? Doğru koşulu yazın.

### 4. Açıkla

Basvuru(101,8).gecikti_mi(8) sonucu nedir? Eşitlik de gecikme sayılacaksa değişiklik?

---

# Ek alıştırmalar — şikâyet veritabanı

Çözümler: [`cozumler_ek.py`](cozumler_ek.py). Kendi dosyanızı `gun04/` içine kaydedin ve şu iki satırla başlayın:

```python
import sqlite3
import db_yardimci as dy
baglanti = sqlite3.connect(dy.veritabani_hazirla())
```

Sonuçları görmek için `dy.tablo_yazdir(baglanti.execute("SELECT ..."))` kullanın.

## Temel (herkes)

**T1 — Parametreli sayım.** `?` kullanarak Konya'daki şikâyet sayısını bulun. Kontrol: `54`.

**T2 — GROUP BY.** Kanal bazında şikâyet sayısını büyükten küçüğe sıralayın. Kontrol: ilk satır `Web | 208`.

**T3 — Koşullu ortalama.** Erzurum'da **çözülen** şikâyetlerin ortalama çözüm süresi (1 ondalık). Kontrol: `10.7`.

## Orta

**O1 — HAVING.** Ortalama memnuniyeti 3'ün altında kalan operatörler. Kontrol: `Operatör C` (2.75) ve `Operatör A` (2.98).
Tartışın: Bu farkı WHERE ile yapabilir miydik? Neden olmaz?

**O2 — JOIN + CSV.** `iller` tablosuyla birleştirip bölge bazında **işlemdeki** şikâyet sayısını bulun; sonucu `dy.sorgu_csv_yaz` ile `outputs/gun04/bolge_islemde.csv` dosyasına yazın. Kontrol: 6 satır.

**O3 — Class.** `tarih` niteliği olan ve `gecen_gun(rapor_tarihi)` metodu bulunan bir `Sikayet` sınıfı yazın (kalıtım kullanmadan). Kontrol: `Sikayet(10550, "2026-01-03", "İşlemde").gecen_gun(date(2026, 10, 1))` → `271`.

## İleri (yazılımcılar için)

**İ1 — CASE ile etiketleme.** Her şikâyete `sla_durumu` sütunu ekleyin: süre NULL ise `Bilinmiyor`, hedefi aşıyorsa `Aştı`, değilse `Hedefte`. Sonucu `sla_etiketli.csv` dosyasına yazın ve etiket bazında sayın. Kontrol: `Aştı 195, Bilinmiyor 96, Hedefte 309`. Tartışın: reddedilenler bu hesaba dahil edilmeli mi?

**İ2 — Çapraz tablo (PivotTable).** Satırda il, sütunlarda durum (`cozuldu`, `reddedildi`, `islemde`) ve `toplam` olan tabloyu tek SQL sorgusuyla üretin. İpucu: `SUM(durum = 'Çözüldü') AS cozuldu`.

**İ3 — Excel = CSV mi?** `dy.xlsx_sayfa_oku` ile `Hiz_Olcumleri` sayfasını okuyup `hiz_olcumleri.csv` ile **hücre hücre** karşılaştırın. Kontrol: `True`.
Tuzak: Excel `36.0` değerini `36` olarak saklar; metin karşılaştırması 137 satırda "farklı" der. Sayıları sayı olarak karşılaştırın.

## Çıkış bileti (3 soru, 5 dakika)

1. Birincil anahtar nedir? `sikayetler` tablosunda neden `il` birincil anahtar olamaz?
2. WHERE ile HAVING arasındaki fark nedir?
3. `f"... WHERE il = '{il}'"` yazmak neden tehlikelidir? Doğrusu nedir?
