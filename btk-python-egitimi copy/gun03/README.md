# Gün 3 — fonksiyon, modül, tarih, dosya ve hata yönetimi

Komutları eğitim klasörünün kökünden VS Code terminalinde çalıştırın. Windows: `python` (çalışmazsa `py`); macOS: etkin eğitim ortamında `python` veya `python3`. Scriptler çalışma klasöründen bağımsızdır; hepsi yalnızca standart kütüphane kullanır (paket gerekmez). Çıktılar `outputs/gun03/` altına yazılır.

Eğitmenin dakika dakika akışı: [EGITMEN_AKISI.md](EGITMEN_AKISI.md).

## Anlatım sırası

Sabah küçük veriyle (36 satırlık `basvurular.csv`) başlanır, öğleden sonra aynı teknikler 600 satırlık `sikayetler.csv` verisine uygulanır.

| Sıra | Dosya | Konu | Beklenen kontrol |
|---|---|---|---|
| 1 | `01_fonksiyonlar.py` | `def`, `return`, boş liste | `Boş liste: None` |
| 2 | `05_fonksiyon_parametreleri.py` | varsayılan/isimli parametre, return vs print, çoklu dönüş, docstring | `KDV dahil: 1200.00 TL` |
| 3 | `06_hazir_moduller.py` | `import`; math, statistics, random(seed), datetime, pathlib | `Gereken sayfa: 13` |
| 4 | `yardimcilar.py` + `07_kendi_modulum.py` | kendi modülünü yazıp import etmek | `yardimcilar modülü kendi testini geçti` / `Şikâyet sayısı: 600` |
| 5 | `08_tarihler.py` | gün farkı, `timedelta`, ay adı, hafta günü, `strptime/strftime` | `En yoğun ay: Haziran` |
| 6 | `02_dosya_okuma_yazma.py` | dosya yolu ve UTF-8 | `Dosya kaydedildi: not.txt` |
| 7 | `09_log_dosyasi.py` | `open`, `with`, `w/a/r` kipleri, satır satır okuma, log | `UYARI satırı: 2` |
| 8 | `03_csv_okuma.py` | küçük CSV, `int` dönüşümü | `Süre toplamı: 192` |
| 9 | `10_sikayet_csv_okuma.py` | büyük CSV, boş hücre, EĞERSAY/ORTALAMAEĞER/ETOPLA karşılığı | `Toplam şikâyet: 600` |
| 10 | `11_csv_filtrele_yaz.py` | filtre + `DictWriter`, `utf-8-sig`, Türkçe Excel için `;` | `Geri okunan satır: 24` |
| 11 | `04_json_ve_dogrulama.py` | JSON ve basit `try/except` | `Hatalı kayıt sayısı: 2` |
| 12 | `12_json_okuma_yazma.py` | `json.dump/load`, `ensure_ascii=False` | `JSON geri okundu: 8 il` |
| 13 | `13_hatali_satirlar.py` | `try/except/else/finally` ile kirli CSV ayıklama | `Temiz: 20, Hatalı: 6` |
| 14 | `14_parametreli_script.py` | `sys.argv` ile parametre, varsayılan değer, `sys.exit(1)` | `Ankara: 107 şikâyet` |
| 15 | `15_mini_sla_raporu_bos.py` → `15_mini_sla_raporu.py` | canlı kodlama: günün özeti | `İskelet çalıştı: 600 kayıt okundu` / `Toplam çözülen: 415` |

`yardimcilar.py` bir **modüldür**: `07`, `15_*` ve `cozumler_ek.py` onu import eder. Bu yüzden aynı klasörde kalmalı ve adı değiştirilmemelidir.

## Çalıştırma örnekleri

```console
python gun03/05_fonksiyon_parametreleri.py
python gun03/yardimcilar.py
python gun03/07_kendi_modulum.py
python gun03/13_hatali_satirlar.py
python gun03/14_parametreli_script.py
python gun03/14_parametreli_script.py İzmir
python gun03/14_parametreli_script.py İstanbul İşlemde
python gun03/14_parametreli_script.py "Sabit"      # geçersiz il -> açıklayıcı mesaj, çıkış kodu 1
```

PowerShell'de yol ayırıcı olarak `gun03\14_parametreli_script.py` da çalışır. Boşluk içeren değerleri tırnak içine alın.

## Üretilen dosyalar (`outputs/gun03/`)

| Dosya | Üreten | İçerik |
|---|---|---|
| `islem_log.txt` | 09 | 5 satırlık örnek log |
| `ankara_internet_hizi.csv` | 11 | 24 satır, virgül ayırıcı, utf-8-sig |
| `ankara_internet_hizi_excel_tr.csv` | 11 | aynı veri, `;` ayırıcı ve ondalık virgül (Türkçe Excel çift tık) |
| `il_ozeti.json` | 12 | il bazında sayım |
| `temiz_sikayetler.csv`, `hata_raporu.txt` | 13 | 20 temiz satır; 6 hatalı satır ve gerekçesi |
| `sla_raporu.csv` | 15 | kategori bazında SLA aşım oranı |
| `izmir.csv`, `dusuk_hiz_log.txt`, `kural_sayimlari.json` | cozumler_ek | alıştırma çıktıları |

## Kontrol edilmiş sayılar (eğitmen için)

- `sikayetler.csv`: 600 kayıt; Çözüldü 415, Reddedildi 89, İşlemde 96; boş çözüm süresi 96.
- Çözülenlerin ortalama süresi 9.60 gün. Ankara 107 şikâyet; Ankara + İnternet Hızı 24.
- En yoğun ay Haziran (87). Kirli dosya: 26 satır → 20 temiz, 6 hatalı, 2 düzeltilen.
- SLA aşımı en yüksek kategori: İnternet Hızı (%61.3).

## Resmî kaynaklar

- Fonksiyon ve varsayılan parametre: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Modüller: https://docs.python.org/3/tutorial/modules.html
- Standart kütüphane turu: https://docs.python.org/3/tutorial/stdlib.html
- math: https://docs.python.org/3/library/math.html · statistics: https://docs.python.org/3/library/statistics.html · random: https://docs.python.org/3/library/random.html
- datetime: https://docs.python.org/3/library/datetime.html (biçim kodları: https://docs.python.org/3/library/datetime.html#format-codes)
- pathlib: https://docs.python.org/3/library/pathlib.html
- Dosya okuma/yazma: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
- csv: https://docs.python.org/3/library/csv.html · json: https://docs.python.org/3/library/json.html
- Hatalar ve istisnalar: https://docs.python.org/3/tutorial/errors.html
- sys.argv: https://docs.python.org/3/library/sys.html#sys.argv

## Günün çalışma düzeni

1. 60 dk: hatırlama, elle çıktı tahmini ve fonksiyonlar.
2. 60 dk: hazır modüller, kendi modülümüz, tarih.
3. 60 dk: dosya ve CSV (küçük → büyük veri).
4. 60 dk: filtreleyip yazma, JSON; temel alıştırmalar.
5. 60 dk: hatalı satır ayıklama ve parametreli script.
6. 60 dk: canlı kodlama mini proje, tekrar ve telafi.

Her blok yaklaşık 15–20 dakika anlatım, 25–30 dakika uygulama ve 10–20 dakika soru/telafi içerir. Molalar ayrıca planlanır. Yeni konu yetiştirmek için uygulama atlanmaz.

## Sık sorunlar

- `python` bulunamadı: VS Code Python yorumlayıcısını seçin; Windows'ta `py` deneyin; IT kurulum kılavuzunu kullanın.
- `ModuleNotFoundError: No module named 'yardimcilar'`: dosya `gun03/` içinde değil ya da adı farklı (ör. `yardımcılar.py`). Kendi dosyanıza `csv.py`, `random.py`, `statistics.py` adını vermeyin.
- `IndentationError`: girintiyi 4 boşluk yapın; aynı bloktaki satırları hizalayın.
- `ValueError: invalid literal for int() with base 10: ''`: boş hücreyi `int`'e çevirmeye çalışıyorsunuz; önce `if metin == ""` kontrolü.
- `TypeError: ... 'NoneType'`: fonksiyon `return` yerine `print` kullanıyor.
- `PermissionError: [Errno 13]`: çıktı CSV'si Excel'de açık; Excel'i kapatıp tekrar çalıştırın.
- CSV Excel'de tek sütun: Türkçe Windows `;` bekler; `*_excel_tr.csv` dosyasını açın veya Veri > Metinden/CSV'den kullanın.
- Türkçe karakter bozuk (`Ä°stanbul`): yazarken `encoding="utf-8-sig"` kullanın.

[Alıştırmalar](ALISTIRMALAR.md) · [Temel çözüm](cozumler.py) · [Ek çözümler](cozumler_ek.py) · [Eğitmen akışı](EGITMEN_AKISI.md)
