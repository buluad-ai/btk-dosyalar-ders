# Gün 6 alıştırmaları

## Temel — herkes
Duruma göre metin grafiği oluşturun.

Önce beklenen sonucu kağıda yazın. Sonra `calisma.py` adıyla kendi dosyanızı oluşturun.

## Ek — erken bitirenler
Adetlerin yanına yüzde ekleyin; toplamın %100 olduğunu kontrol edin.

## Kendi kontrolünüz
Sonucu elle hesaplayın; kodu yeniden çalıştırın. Aynı girdi aynı sonucu veriyor mu?

Çözüm: `cozumler.py`. Önce kendiniz deneyin; kopyalamadan bir satırın ne yaptığını anlatın.

## Kademeli mikro görevler (60–90 dakika)

Her görevde önce bireysel tahmin (3 dk), sonra eşli uygulama (7–10 dk), ardından açıklama (3–5 dk). Erken bitirenler örneği farklı bir sınır değeriyle tekrarlar.

### 1. Tahmin et

Kategori grafiğindeki Bilgi, Teknik ve Itiraz sayıları nedir?

### 2. Değiştir

Metin grafiğini kategori yerine durum alanına göre çizin.

### 3. Hatayı düzelt

Sütun grafiğini 8’den başlatırsanız 9 ve18 arasındaki fark nasıl algılanır?

### 4. Açıkla

Sütun, çizgi ve histogram için birer soru seçin. gunluk.svg dosyasını açıp ilk8 güne bakın.

---

## Ek alıştırmalar (büyük veri)

Paket yoksa her görevin B planı (SVG/metin) karşılığını yapın. Çözümler: `cozumler_ek.py` (paketsiz) ve `cozumler_ek_opsiyonel.py` (matplotlib). Her grafikte kontrol listesi: başlık, eksen adı, birim, 0'dan başlangıç, tek renk.

### Temel — herkes

- **T1.** `07_ilk_grafik_opsiyonel.py` dosyasını kopyalayın (`calisma_t1.py`); kategori yerine **operatöre** göre şikâyet sayısını sıralı yatay çubukla çizin. B planı: `svg_cizim.yatay_bar_svg`. *Beklenen: Operatör A 233, B 170, C 133, D 64.*
- **T2.** Hizmet türüne (Mobil / Sabit İnternet / Sabit Telefon) göre şikâyet **yüzdesini** metin grafiğiyle yazın; yüzdelerin toplamı %100 mü? *Beklenen: %56.5 / %36.0 / %7.5.*
- **T3. (kod yok, eleştiri)** Bir sunumda şu grafik var: 3 boyutlu pasta, 6 dilim, gökkuşağı renkleri, başlık "Veriler", y ekseni 140'tan başlayan bir çubuk grafik yanında. En az 3 hata yazın ve her biri için düzeltme önerin.

### Orta

- **O1.** Yalnızca **Çözüldü** şikâyetlerin aylık sayısını çizgi grafikle gösterin. Toplam kaç? En yüksek ay hangisi? *Beklenen: 415; Haziran.*
- **O2.** Ping sürelerinin dağılımını gösterin (matplotlib: `hist`, B planı: 10 ms'lik aralıklara sayım). Ölçümlerin çoğu hangi aralıkta?
- **O3.** Teknolojiye göre **medyan yükleme** hızını sütun grafikle çizin. Neden ortalama değil medyan?

### İleri — iki yazılımcı için

- **İ1.** Her operatör için aylık trendi `plt.subplots(2, 2, sharey=True)` ile ayrı küçük grafiklerde çizin. `sharey=True` neden önemli?
- **İ2.** `svg_cizim.py`'ye eklenebilecek `histogram_svg(degerler, aralik, baslik, x_birim)` fonksiyonunu yazın; çözüm süresi dağılımına uygulayın (aralık 5 gün).
- **İ3.** Paket olmadan ısı haritası: il × kategori sayılarını, hücre arka plan rengi değere göre koyulaşan bir HTML tablosu olarak üretin.

### T3 için eğitmen yanıtı (öğrenciye sonra gösterin)

3B ve 6 dilimli pasta okunmaz (açı/alan karşılaştırması zor) → sıralı çubuk; gökkuşağı renk anlam taşımaz → tek renk + vurgu; "Veriler" başlığı bilgi vermez → "Kategoriye göre şikâyet sayısı, Ocak–Eylül 2026"; 140'tan başlayan çubuk farkı abartır → 0'dan başlat; birim yok → "(adet)".
