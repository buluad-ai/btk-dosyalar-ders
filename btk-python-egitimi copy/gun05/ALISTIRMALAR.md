# Gün 5 alıştırmaları

## Temel — herkes
Birimlere göre kapalı başvuru sayısını hesaplayın.

Önce beklenen sonucu kağıda yazın. Sonra `calisma.py` adıyla kendi dosyanızı oluşturun.

## Ek — erken bitirenler
Her birimin kapalı başvurularının ortalamasını hesaplayın.

## Kendi kontrolünüz
Sonucu elle hesaplayın; kodu yeniden çalıştırın. Aynı girdi aynı sonucu veriyor mu?

Çözüm: `cozumler.py`. Önce kendiniz deneyin; kopyalamadan bir satırın ne yaptığını anlatın.

## Kademeli mikro görevler (60–90 dakika)

Her görevde önce bireysel tahmin (3 dk), sonra eşli uygulama (7–10 dk), ardından açıklama (3–5 dk). Erken bitirenler örneği farklı bir sınır değeriyle tekrarlar.

### 1. Tahmin et

kirli_basvurular.csv dosyasını metin olarak açın; hangi 6 satır inceleme gerektiriyor?

### 2. Değiştir

05_veri_temizleme.py kopyasında tam gün yerine ondalıklı gün kabul edin. Hangi kayıt değişir?

### 3. Hatayı düzelt

Eksik süreyi 0 ile doldurmak ortalamayı nasıl etkiler? [2,5,eksik,3] örneğini hesaplayın.

### 4. Açıkla

Birim başına sayı ve kapalı başvuruların ortalamasını karşılaştırın. Ortalama kaliteyi tek başına ölçer mi?

---

# Ek alıştırmalar — büyük veri (600 şikâyet, 400 hız ölçümü)

Kural: Her alıştırmada önce **iş sorusunu** bir cümleyle yazın, sonra beklenen sonucu tahmin edin. Önce standart kütüphane ile çözün (herkes çalıştırabilir); paketler kuruluysa aynı sonucu pandas/NumPy ile de bulun ve karşılaştırın. Çözümler: `cozumler_ek.py` (kontrol etiketleri T1, O1, İ1… ile eşleşir).

İpucu dosyaları: `07` (statistics), `08`/`09` (hız, maske), `12`/`11` (gruplama, DÜŞEYARA, tarih), `17` (xlsx okuma), `19`/`20` (karne).

## Temel — herkes

**T1.** Reddedilen şikâyetlerin memnuniyet ortalaması ve medyanı nedir? Çözülenlerinkiyle karşılaştırın; fark sizce ne anlatıyor?
Beklenen: `ort 1.85, medyan 2.0`.

**T2.** Fiber ölçümlerinin kaçı paket hızının %80'inin altında? (`08_hiz_standart.py`'deki maske satırını kopyalayıp bir `if` ekleyin.)
Beklenen: `105 / 139`.

**T3.** Kanal bazında şikâyet sayısını çoktan aza yazdırın. (Excel: EĞERSAY; Python: `Counter(...).most_common()`; pandas: `value_counts()`.)
Beklenen: `Web 208, e-Devlet 195, Çağrı Merkezi 151, Dilekçe 46`.

**T4 (değiştir).** `07_analiz_dusuncesi.py`'de filtreyi `"Reddedildi"` yapın. Ortalama/medyan nasıl değişti? Yorum satırlarını da yeni soruya göre güncelleyin.

## Orta

**O1.** İl bazında çözüm oranını (Çözüldü / tüm şikâyetler) hesaplayın; en yüksek ve en düşük ili yazın.
Beklenen: `Erzurum %76.5`, `Bursa %54.7`. Tartışın: Erzurum'da 34 şikâyet var — küçük grupta oran ne kadar güvenilir?

**O2.** Hedefi aşan çözülmüş şikâyetlerde kategori bazında ortalama **gecikmeyi** (süre − hedef gün) bulun. (DÜŞEYARA = sözlük / `merge`.)
Beklenen: `Fatura 2.9, Kapsama 3.1, Kesinti 1.6, Numara Taşıma 2.4, Taahhüt/İptal 2.8, İnternet Hızı 3.1`.

**O3.** Operatör bazında **medyan** gerçekleşme oranını (indirme / paket × 100) hesaplayın. Neden ortalama değil medyan?
Beklenen: `Operatör A 57.1, Operatör B 64.5, Operatör C 54.2, Operatör D 55.8`.

**O4 (eksik veri).** `memnuniyet` sütunundaki 96 boşu medyanla (3) doldurmak doğru olur mu? Ortalama ne olur? Bu boşların hangi durumdaki şikâyetler olduğuna bakarak karar verin. (İpucu: `13_eksik_veri_opsiyonel.py`.)

## İleri — yazılımcılar için

**İ1.** Karneye iki sütun ekleyin: toplam itiraz tutarı (TL) ve itiraz eden oranı (%). Boş itiraz = itiraz yok. Hem `19` hem `20`ye ekleyin ve `20`deki KONTROL bloğunu yeni sütunları da karşılaştıracak şekilde genişletin.
Beklenen (A): `itiraz 59935.15 TL, itiraz eden %23.2`.

**İ2.** Aylık hedef aşım oranını (çözülenler içinde) hesaplayın. pandas'ta `to_period("M")` ile, standart kütüphanede `date.fromisoformat` ile. Hangi aylar göze çarpıyor?
Beklenen başlangıç: `2026-01 60, 2026-02 55, 2026-03 35 …`.

**İ3.** `xlsx_mini.sayfa_oku` ile `Hiz_Olcumleri` sayfasını okuyun; ping'in 90. yüzdeliğini `statistics.quantiles(..., method="inclusive")` ile bulun; NumPy varsa `np.percentile` ile aynı çıktığını gösterin. `method="exclusive"` ile ne değişir?
Beklenen: `52.44 ms`.

**İ4 (tasarım).** `18_karne_bos.py`'yi tamamlayın, sonra karneye `sys.argv` ile il filtresi ekleyin (`python gun05/18_karne_bos.py Ankara`). Parametre verilmezse tüm iller kullanılsın. `input()` kullanmayın.

## Kendi kontrolünüz

- Toplamlar tutuyor mu? (Karne şikâyet sayılarının toplamı 600; temiz + incele + tekrar = 26.)
- Aynı soruyu iki yolla (stdlib ve pandas) çözdüyseniz sonuçlar aynı mı?
- Sonucu bir cümleyle iş diline çevirebiliyor musunuz? Sınırlılığı (hangi kayıtlar dahil değil) söylediniz mi?
