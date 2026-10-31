# Gün 5 — Dosyadan sayısal analiz ve rapor (statistics, NumPy, pandas, Excel)

Komutları eğitim klasörünün kökünden VS Code terminalinde çalıştırın. Windows: `py` veya `python` (hangisi çalışıyorsa); macOS: etkin eğitim ortamında `python` veya `python3`. Scriptler çalışma klasöründen bağımsızdır. Windows'ta yol ayıracı ters eğik çizgidir: `py gun05\07_analiz_dusuncesi.py` (VS Code'daki "Run" düğmesi bu farkı sizin yerinize halleder).

**Günün fikri:** iş sorusu → veri → doğrulama → özet → yorum. Her paketli (`_opsiyonel`) dosyanın bir standart kütüphane karşılığı vardır; IT paketleri kurmadıysa gün yine işlenir. Paket yoksa opsiyonel dosya `ATLANDI: ... — B planı: <dosya>` yazar ve hatasız biter.

## Anlatım sırası

| Sıra | Konu | A yolu (paketler kurulu) | B yolu (yalnız standart kütüphane) |
|---|---|---|---|
| 1 | Küçük veriyle ısınma (36 başvuru) | `01`, `02`, `03` | `01`, `02` |
| 2 | Analiz düşüncesi + tanımlayıcı istatistik | `07` | `07` |
| 3 | Toplu işlem, maske, yüzdelik (hız verisi) | `08` (kısa) → `09` | `08` |
| 4 | DataFrame'e ilk bakış, filtre, sıralama | `10` | `12` (1–4. bölüm) |
| 5 | Gruplama, pivot, DÜŞEYARA, tarih | `11` | `12` (5–8. bölüm) |
| 6 | Eksik veri ve tekrar | `13` | `14` (1. bölüm) |
| 7 | Kirli veri temizleme | `05` (küçük) → `15` | `05` → `14` (2. bölüm) |
| 8 | Excel okuma/yazma | `04`, `16` | `17` (+ `xlsx_mini.py`) |
| 9 | Gün sonu mini proje: operatör karnesi | `18` → `19` → `20` | `18` → `19` |

`06_pandas_temizleme_opsiyonel.py` küçük kirli dosyada `05`in pandas eşidir; zaman kalırsa `15`ten önce gösterilir.

## Veri dosyaları

- `data/basvurular.csv` (36 satır), `data/kirli_basvurular.csv`: küçük ısınma verisi (01–06).
- `data/sikayetler.csv` (600 şikâyet), `data/hiz_olcumleri.csv` (400 ölçüm), `data/sikayetler_kirli.csv` (26 satır, kasıtlı hatalı), `data/btk_ornek_veri.xlsx` (sayfalar: `Sikayetler`, `Hiz_Olcumleri`, `Hedefler`). Operatör adları kurgusaldır.

## Dosyalar ve beklenen çıktılar

| Dosya | Ne öğretir | Beklenen kontrol (stdout) | Paket |
|---|---|---|---|
| `01_standart_analiz.py` | Ortalama/medyan (küçük veri) | `Kapalı kayıt: 27` | — |
| `02_gruplama_rapor.py` | Counter + CSV raporu | `Rapor toplamı: 36` | — |
| `03_pandas_numpy_opsiyonel.py` | Aynı analiz pandas/NumPy | `Kapalı kayıt: 27` | pandas, numpy |
| `04_excel_opsiyonel.py` | Excel yazma ve geri okuma | `Excel'den okunan kayıt: 36` | pandas, openpyxl |
| `05_veri_temizleme.py` | Eksik/tekrar/tarih denetimi | `Temiz kayıt: 3` | — |
| `06_pandas_temizleme_opsiyonel.py` | Aynısı pandas ile | `Temiz kayıt: 3` | pandas |
| `07_analiz_dusuncesi.py` | Soru→veri→doğrulama→özet→yorum; mean, median, mode, stdev, quantiles | `Çözülen şikâyet: 415`, `Ortalama: 9.60 gün` | — |
| `08_hiz_standart.py` | Mbps→MB/s listeyle, %80 maskesi, yüzdelik, EĞER | `Paketin %80'inin altında: 278 ölçüm` | — |
| `09_numpy_opsiyonel.py` | np.array, vektörel işlem, maske, np.percentile, np.where, np.round, ddof, hız | `Kontrol: statistics ile NumPy aynı sonucu verdi.` | numpy |
| `10_pandas_ilk_bakis_opsiyonel.py` | read_csv, head/info/describe/shape/dtypes, filtre, sort_values, yeni sütun, value_counts | `Satır, sütun: (600, 11)`, `İstanbul + Kesinti: 16 şikâyet` | pandas |
| `11_pandas_gruplama_opsiyonel.py` | groupby+agg, pivot_table, merge (DÜŞEYARA), to_datetime, dt.month, to_period | `Hedef aşım oranı (genel): %39.8` | pandas (+openpyxl) |
| `12_standart_filtre_grup.py` | 10 ve 11'in paketsiz hali | `Hedef aşım oranı (genel): %39.8` | — |
| `13_eksik_veri_opsiyonel.py` | isna, dropna, fillna (ne zaman doğru/yanlış), duplicated | `Yanlış (boş=0): 8.01` | pandas |
| `14_kirli_veri_standart.py` | Eksik veri + kirli veri temizliği (strip, title, sayı dönüşümü, aralık) | `Temiz kayıt: 20`, `İncelenecek kayıt: 5` | — |
| `15_kirli_veri_opsiyonel.py` | Aynısı pandas ile (to_numeric errors="coerce") | `İncelenecek şikâyet no: [10033, 10042, 10253, 10331, 10586]` | pandas |
| `16_excel_oku_yaz_opsiyonel.py` | read_excel (sheet_name, tüm sayfalar), ExcelWriter çok sayfa, PermissionError | `Yazılan sayfalar: ['Özet', 'Pivot', 'Detay']` | pandas, openpyxl |
| `17_xlsx_standart.py` | Paketsiz xlsx okuma + Türkçe Excel uyumlu CSV (`utf-8-sig`, `;`, ondalık virgül) | `Kontrol: Excel ve CSV aynı 600 kaydı içeriyor.` | — |
| `xlsx_mini.py` | Yardımcı modül: zipfile+XML ile .xlsx okuyucu (17, 19, 12 kullanır) | `Sayfalar: [...]` | — |
| `18_karne_bos.py` | Mini proje iskeleti (TODO'lu, canlı kodlama) | `İSKELET: TODO'ları doldurun.` | — |
| `19_karne_standart.py` | Operatör performans karnesi → CSV | `Karne yazıldı: outputs/gun05/operator_karnesi.csv` | — |
| `20_karne_opsiyonel.py` | Aynı karne pandas → çok sayfalı Excel + iki yol kontrolü | `KONTROL: pandas ve standart kütüphane AYNI sonucu verdi` | pandas, openpyxl |
| `cozumler.py` | Temel alıştırma çözümü | `A: 9 kapalı, 2.33 gün` | — |
| `cozumler_ek.py` | Ek alıştırmaların çözümleri (stdlib + varsa pandas kontrolü) | `Ek çözümler tamamlandı.` | — |

Örnek komutlar:

```console
python gun05/07_analiz_dusuncesi.py
python gun05/11_pandas_gruplama_opsiyonel.py
python gun05/19_karne_standart.py
python gun05/20_karne_opsiyonel.py
```

### Mini proje karnesi (beklenen sonuç)

| Operatör | Şikâyet | Çözüm % | Ort. gün | Medyan | Hedef aşım % | Memnuniyet |
|---|---|---|---|---|---|---|
| Operatör A | 233 | 69.5 | 10.06 | 10.0 | 39.5 | 2.98 |
| Operatör B | 170 | 66.5 | 7.96 | 8.0 | 21.2 | 3.38 |
| Operatör C | 133 | 66.9 | 11.24 | 11.0 | 64.0 | 2.75 |
| Operatör D | 64 | 79.7 | 8.92 | 8.0 | 39.2 | 3.26 |

Tanımlar: çözüm oranı = Çözüldü / tüm şikâyetler; süreler ve hedef aşımı yalnızca Çözüldü kayıtlarında; memnuniyet puan verilmiş tüm kayıtlarda.

## Üretilen dosyalar (`outputs/gun05/`)

`birim_ozeti.csv`, `basvurular.xlsx`, `temiz.json`, `sorunlu.json`, `pandas_temiz.csv`, `pandas_incele.csv` (01–06); `sikayet_temiz.csv`, `sikayet_incele.csv` (14); `sikayet_temiz_pandas.csv`, `sikayet_incele_pandas.csv` (15); `sikayet_raporu.xlsx` (16); `ozet_operator.csv` (17); `operator_karnesi.csv` (19); `operator_karnesi.xlsx` (20).

## Excel benzetmeleri (sınıf ileri Excel'den geliyor)

| Excel | Standart kütüphane | pandas / NumPy |
|---|---|---|
| ORTALAMA / ORTANCA / ENÇOK_OLAN | `statistics.mean / median / mode` | `.mean() / .median() / .mode()` |
| STDSAPMA.S | `statistics.stdev` | `.std()` (pandas), `np.std(x, ddof=1)` |
| DÖRTTEBİRLİK.DHL / YÜZDEBİRLİK | `statistics.quantiles(..., method="inclusive")` | `.quantile()`, `np.percentile` |
| Filtre | liste içi `if` | `df[koşul]`, `query` |
| Sırala | `sorted(..., key=...)` | `sort_values` |
| EĞERSAY | `Counter` | `value_counts` |
| PivotTable | `defaultdict(list)` + döngü | `groupby().agg()`, `pivot_table` |
| DÜŞEYARA | sözlük `hedef[kategori]` | `merge` |
| EĞER | `"A" if koşul else "B"` | `np.where` |
| KIRP / YAZIM.DÜZENİ | `str.strip()` / `str.title()` | `.str.strip()` / `.str.title()` |
| Yinelenenleri Kaldır | `set` ile görülenler | `drop_duplicates` |

## Sık sorunlar

- `python` bulunamadı: Windows'ta `py` deneyin; VS Code'da sağ alttan Python yorumlayıcısını seçin; IT kurulum kılavuzunu kullanın.
- `ModuleNotFoundError: No module named 'xlsx_mini'`: dosyayı `gun05` klasöründen başka yere kopyaladınız; `xlsx_mini.py`yi de yanına kopyalayın.
- `PermissionError`: çıktı dosyası (xlsx/csv) Excel'de açık. Excel'i kapatıp yeniden çalıştırın. Klasör yazılamıyorsa eğitim klasörünü Belgeler altına taşıyın.
- Paket bulunamadı: opsiyonel örneğin B planı dosyasına geçin; derste kurulum beklemeyin.
- Türkçe metin bozuk: dosyayı UTF-8 kaydedin. CSV'yi Excel'de Veri > Metinden/CSV'den ile açın (65001 UTF-8, ayıraç noktalı virgül).
- `"istanbul".title()` → `Istanbul` (noktasız I): Python'un harf dönüşümü Türkçe bilmez; geçerli değer listesiyle kontrol edin.
- `IndentationError` / `SyntaxError`: girinti 4 boşluk; parantez, tırnak ve iki noktayı kontrol edin.

## Resmî kaynaklar

- [statistics](https://docs.python.org/3/library/statistics.html) · [csv](https://docs.python.org/3/library/csv.html) · [collections](https://docs.python.org/3/library/collections.html) · [datetime](https://docs.python.org/3/library/datetime.html) · [zipfile](https://docs.python.org/3/library/zipfile.html) · [xml.etree](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [NumPy yeni başlayanlar](https://numpy.org/doc/stable/user/absolute_beginners.html) · [np.percentile](https://numpy.org/doc/stable/reference/generated/numpy.percentile.html) · [np.where](https://numpy.org/doc/stable/reference/generated/numpy.where.html)
- [pandas giriş eğitimleri](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html) · [Excel kullanıcıları için pandas](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_spreadsheets.html) · [groupby](https://pandas.pydata.org/docs/user_guide/groupby.html) · [pivot_table](https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html) · [merge](https://pandas.pydata.org/docs/user_guide/merging.html) · [eksik veri](https://pandas.pydata.org/docs/user_guide/missing_data.html) · [read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html) · [ExcelWriter](https://pandas.pydata.org/docs/reference/api/pandas.ExcelWriter.html)
- [Microsoft: CSV olarak kaydetme](https://support.microsoft.com/en-us/excel/save-a-workbook-to-text-format-txt-or-csv)

[Alıştırmalar](ALISTIRMALAR.md) · [Çözümler](cozumler.py) · [Ek çözümler](cozumler_ek.py) · [Eğitmen akışı](EGITMEN_AKISI.md)
