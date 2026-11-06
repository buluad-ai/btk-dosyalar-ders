# Gün 1 alıştırmaları

## Temel — herkes
Üç sürenin ortalamasını bulun: 3, 6, 12.

Önce beklenen sonucu kağıda yazın. Sonra `calisma.py` adıyla kendi dosyanızı oluşturun.

## Ek — erken bitirenler
Ortalamanın 5 güne göre yüzde farkını bulun.

## Kendi kontrolünüz
Sonucu elle hesaplayın; kodu yeniden çalıştırın. Aynı girdi aynı sonucu veriyor mu?

Çözüm: `cozumler.py`. Önce kendiniz deneyin; kopyalamadan bir satırın ne yaptığını anlatın.

## Kademeli mikro görevler (60–90 dakika)

Her görevde önce bireysel tahmin (3 dk), sonra eşli uygulama (7–10 dk), ardından açıklama (3–5 dk). Erken bitirenler örneği farklı bir sınır değeriyle tekrarlar.

### 1. Tahmin et

`print("12" + "8")` ve `print(12 + 8)` ne üretir? Çalıştırmadan yazın.

### 2. Değiştir

03_algoritma.py kopyasında süreleri 3, 6, 12 yapın; önce toplamı ve ortalamayı hesaplayın.

### 3. Hatayı düzelt

`ortalama = "15" / 3` satırı neden çalışmaz? Dönüşüm uygulayın.

### 4. Açıkla

`5 / 2`, `5 // 2`, `5 % 2` işlemlerini çalıştırın ve raporda hangisini kullanacağınızı açıklayın.

---

# Genişletilmiş alıştırmalar (seviyeli)

Her görevde önce sonucu **kağıda tahmin edin**, sonra kodu yazın, sonra karşılaştırın. Çözümler: `cozumler_ek.py` (görev kodlarıyla aynı başlıklar). Kendi dosyanızı `gun01/calisma_adim.py` gibi bir adla oluşturun (adda boşluk ve Türkçe harf kullanmayın).

## Temel — herkes

**T1. Ortalama.** Süreler 3, 6 ve 12 gün. Ortalamayı 2 ondalıkla yazdırın. (Beklenen: `Ortalama: 7.00`)

**T2. KDV.** KDV hariç 750 TL'lik bir paket için KDV dahil fiyatı (%20) hesaplayın. KDV oranını `KDV_ORANI` adlı bir sabite koyun. (Beklenen: `900.00 TL`)

**T3. Hız dönüşümü.** 50 Mbps paket kaç MB/s eder? (İpucu: 1 byte = 8 bit.) (Beklenen: `6.25 MB/s`)

**T4. Metin temizliği.** `"  operatör b "` metnini baştaki/sondaki boşluklardan arındırıp her kelimenin ilk harfini büyük yazın. Temizlikten önceki ve sonraki uzunluğu `len` ile yazdırın. (Beklenen: `Operatör B`, 13 → 10)

## Orta — erken bitirenler

**O1. Süre biçimi.** 200 dakikayı `3 saat 20 dakika` biçiminde yazdırın (`//` ve `%`).

**O2. Tarih biçimi.** `"2026-03-15"` metnini `15.03.2026` biçimine çevirin (`split` + f-string).

**O3. Fatura.** Paket 400 TL, 20 GB dahil, aşan her GB 25 TL, üstüne %20 KDV. 35 GB kullanan abonenin faturası? Önce akış şemasını metin olarak yazın. (Beklenen: `930.00 TL`)

**O4. Türk biçimli tutar.** `"1.234,56"` metnini `1234.56` sayısına çevirin ve iki katını alın. Hangi `replace` önce yapılmalı, neden?

## İleri — iki yazılımcı katılımcı için

**İ1. İndirme süresi tablosu.** 2048 MB'lık dosya için 25, 100 ve 1000 Mbps hızlarında indirme süresini `dk sn` biçiminde, hizalı yazdırın. (Döngüyü Gün 2'den önce kullanabilirsiniz.)

**İ2. CSV satırı.** `"10527,2026-01-02,Ankara,Operatör A,Sabit İnternet,Fatura,e-Devlet,Çözüldü,10,3,2404.26"` satırından il, kategori ve itiraz tutarını alın; tutar KDV dahil kabul edilirse KDV hariç tutarı bulun. (Beklenen: `2003.55 TL`)

**İ3. Sıfır kayıt.** Toplam süre 0 ve kayıt sayısı 0 iken ortalama hesabı ne yapmalı? Programı çökertmeden `kayıt yok` yazdıran bir çözüm tasarlayın; neden `0` yazdırmanın yanıltıcı olacağını bir cümleyle açıklayın.

## Çıkış bileti (gün sonu, 3 soru, 5 dakika)

1. `print("12" + "8")` ne yazar? Neden?
2. `17 // 5` ve `17 % 5` kaç eder?
3. Traceback'in hangi satırını ilk okursunuz?
