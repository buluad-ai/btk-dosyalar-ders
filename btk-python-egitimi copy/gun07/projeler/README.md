# Bitirme projesi kartları (Gün 7)

Ekipler (2–3 kişi) bir kart seçer. Her kartın **çalışan referans çözümü** bu klasördedir; ekiplere **sunumdan sonra** gösterilir. Referans çözümler yalnızca standart kütüphane kullanır (paket gerekmez). Paket varsa ekip aynı soruyu pandas/matplotlib ile de çözebilir; rubrikte ek puan yoktur, doğruluk ve yorum esastır.

Çalıştırma (proje kökünden):

```console
python gun07/projeler/kart1_kapsama_iller.py
```

Çıktılar `outputs/gun07/projeler/` altına yazılır (CSV, `;` ayraçlı ve Excel'de çift tıkla düzgün açılır; SVG tarayıcıda açılır).

**Önerilen başlangıç:** `gun07/05_hazir_script_uyarlama.py` dosyasını kopyalayın, AYARLAR bölümünü ve filtre satırını kendi sorunuza göre değiştirin. Grafik için `gun06/svg_cizim.py` fonksiyonlarını (veya matplotlib) kullanın.

---

## Kart 1 — "Kapsama şikâyetleri hangi illerde yoğun?"

| | |
|---|---|
| **İş sorusu** | Mobil kapsama iyileştirmesi için hangi illere öncelik verilmeli? |
| **Dosya** | `data/sikayetler.csv` (sütunlar: `il`, `kategori`) |
| **Beklenen çıktı** | İl bazında tablo: Kapsama adedi, ildeki toplam şikâyet, Kapsama payı (%) · sıralı yatay çubuk grafik · 2 bulgu + 1 sınırlılık |
| **İpucu** | "Yoğun" iki şey olabilir: ADET (büyük il hep önde) ve PAY (adil karşılaştırma). İkisini de gösterin. |
| **Referans çözüm** | `kart1_kapsama_iller.py` |
| **Doğru sonuç** | Adette İstanbul (20); payda Erzurum (%17.6). Çoğu ilde Kapsama kaydı 10'dan az → oranlar oynak. |

## Kart 2 — "Fiber paketler vaat edilen hızı veriyor mu?"

| | |
|---|---|
| **İş sorusu** | Fiber abonelere satılan hız ölçümlerde karşılanıyor mu? Hangi pakette sorun var? |
| **Dosya** | `data/hiz_olcumleri.csv` (sütunlar: `teknoloji`, `paket_hizi_mbps`, `indirme_mbps`) |
| **Beklenen çıktı** | "Vaadi karşılamak" tanımı (ör. paketin %80'i) yazılı olarak · paket hızına göre tablo: ölçüm sayısı, medyan indirme, eşiği geçen % · grafik · 2 bulgu + 1 sınırlılık |
| **İpucu** | Önce tanımı yazın, sonra kodlayın. Yeni sütun: `oran = indirme / paket`. Ortalama yerine medyan. |
| **Referans çözüm** | `kart2_fiber_vaat.py` (görsel destek: `gun06/12_scatter_opsiyonel.py`) |
| **Doğru sonuç** | Fiber 139 ölçüm, %80 eşiğini geçen %24. 100/200 Mbps paketlerde ~%54, 500/1000 Mbps paketlerde %0. |

## Kart 3 — "Hangi kanal daha hızlı çözüm alıyor?"

| | |
|---|---|
| **İş sorusu** | Vatandaşa "şikâyetinizi şu kanaldan iletirseniz daha hızlı sonuç alırsınız" denebilir mi? |
| **Dosya** | `data/sikayetler.csv` (sütunlar: `kanal`, `durum`, `cozum_suresi_gun`, `kategori`) |
| **Beklenen çıktı** | Yalnızca Çözüldü kayıtlar · kanal başına kayıt sayısı, ortalama ve medyan süre · grafik · kategori karışımı üzerine bir not · net bir "evet/hayır/kanıt yetersiz" cevabı |
| **İpucu** | "Fark yok" da bir bulgudur. Kapsama (~18 gün) hangi kanaldan çok gelirse o kanal yavaş görünür. |
| **Referans çözüm** | `kart3_kanal_cozum.py` |
| **Doğru sonuç** | Çağrı Merkezi 9.27 gün en hızlı; en yavaş Web 9.96 gün; fark 0.69 gün. Kategori içinde en hızlı kanal kategoriye göre değişiyor → kanal belirleyici görünmüyor. |

## Kart 4 — "Hangi operatör hedef çözüm süresini en çok aşıyor?"

| | |
|---|---|
| **İş sorusu** | Kategori hedeflerine göre en çok gecikme hangi operatörde ve hangi kategoride? |
| **Dosya** | `data/sikayetler.csv` + `data/btk_ornek_veri.xlsx` → **Hedefler** sayfası (`kategori`, `hedef_gun`) |
| **Beklenen çıktı** | Her çözülen şikâyete kategori hedefini getirme (DÜŞEYARA/merge/JOIN) · operatör başına hedef aşım % · operatör × kategori çapraz tablo · grafik · 2 bulgu + 1 sınırlılık |
| **İpucu** | Paket yoksa Excel'i `gun07/basit_xlsx.py` ile okuyun ya da Hedefler sayfasını Excel'den CSV UTF-8 olarak kaydedin. |
| **Referans çözüm** | `kart4_hedef_asimi.py` |
| **Doğru sonuç** | Operatör C %64.0 ile en yüksek; Operatör B %21.2 en düşük. C'de Kapsama, Taahhüt/İptal ve İnternet Hızı'nda aşım %80 üstü. |

---

## Değerlendirme rubriği (her kart için aynı, 20 puan)

| Ölçüt | 0 | 2 | 4 |
|---|---|---|---|
| **1. Soru ve tanım** | Soru yeniden yazılmamış | Soru var, ölçüt belirsiz | Soru + ölçüt/tanım açık (ör. "%80 eşiği", "yalnızca Çözüldü") |
| **2. Doğru veri ve filtre** | Yanlış alt küme / sütun | Doğru ama kontrol yok | Doğru alt küme + elle bir sayı kontrolü (ör. toplam 600 mü?) |
| **3. Sonuç doğruluğu** | Referansla çelişiyor | Küçük hata (yuvarlama, eksik grup) | Referansla tutarlı |
| **4. Grafik kalitesi** | Grafik yok | Grafik var, başlık/eksen/birim eksik | Doğru tür + başlık, eksen, birim, 0 başlangıç, sade renk |
| **5. Yorum ve sınırlılık** | Yalnızca sayı okunmuş | Bulgu var, sınırlılık yok | 2 bulgu + 1 sınırlılık, iş diliyle |

**Bonus (en fazla +2):** Script parametreli (`argparse`) veya tekrar çalıştırılabilir; çıktı dosya adları anlamlı; başka bir ekip dosyayı açıp hiç düzenlemeden çalıştırabiliyor.

**Sunum:** ekip başına 5 dakika — soru (30 sn), yöntem (1 dk), grafik + bulgular (2 dk), sınırlılık (30 sn), soru-cevap (1 dk).
