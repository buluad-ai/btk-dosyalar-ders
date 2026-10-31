# Gün 7

Komutları eğitim klasörünün kökünden VS Code terminalinde çalıştırın. Windows: `python`; macOS: etkin eğitim ortamında `python` veya `python3`. Scriptler çalışma klasöründen bağımsızdır.

## Bütünleşik analiz: oku doğrula özetle yaz

```console
python gun07/01_analiz_pipeline.py
```

Beklenen kontrol: `Analiz tamamlandı: 36 kayıt`.

[Resmî kaynak](https://docs.python.org/3/library/json.html)

## Paketsiz paylaşılabilir HTML raporu

```console
python gun07/02_html_rapor.py
```

Beklenen kontrol: `Rapor: outputs/gun07/rapor.html`.

[Resmî kaynak](https://docs.python.org/3/library/html.html)

## Komut satırından rapor parametresi

```console
python gun07/03_parametreli_script.py
```

Beklenen kontrol: `Birim A: 12 kayıt`.

[Resmî kaynak](https://docs.python.org/3/library/argparse.html)

## İsteğe bağlı Streamlit paneli

```console
python gun07/04_streamlit_opsiyonel.py --check
```

Beklenen kontrol: `Panel verisi: 36` veya paket yoksa `ATLANDI`. Eksik paket temel dersi engellemez.

[Resmî kaynak](https://docs.streamlit.io/get-started)

## Günün çalışma düzeni

1. 60 dk: hatırlama, elle çıktı tahmini ve ilk örnek.
2. 60 dk: anlatım + birlikte yazma + bir parametreyi değiştirme.
3. 60 dk: sonraki örnek + eşli uygulama + kısa kontrol.
4. 60 dk: temel alıştırmalar; eğitmen bireysel destek verir.
5. 60 dk: hata ayıklama ve ek uygulamalar; erken bitirenler derinleşir.
6. 60 dk: sonuç yorumlama, bağımsız tekrar ve telafi.

Her blok yaklaşık 15–20 dakika anlatım, 25–30 dakika uygulama ve 10–20 dakika soru/telafi içerir. Altı saat eğitim süresidir; molalar ayrıca planlanır. Yeni konu yetiştirmek için uygulama atlanmaz.

## Sık sorunlar

- `python` bulunamadı: VS Code Python yorumlayıcısını seçin; IT kurulum kılavuzunu kullanın.
- `IndentationError`: girintiyi 4 boşluk yapın; aynı bloktaki satırları hizalayın.
- `SyntaxError`: parantez, tırnak ve iki noktayı kontrol edin.
- `PermissionError`: eğitim klasörünü yazılabilir yere taşıyın; açık Excel çıktısını kapatın.
- Paket bulunamadı: opsiyonel örneğin paketsiz alternatifine dönün, derste kurulum beklemeyin.
- Türkçe metin bozuk: dosyayı UTF-8 kaydedin; Excel CSV açarken UTF-8 ve virgül ayıracı seçin.

[Alıştırmalar](ALISTIRMALAR.md) · [Çözümler](cozumler.py)

---

# Gün 7 — genişletilmiş içerik: uçtan uca bitirme

Günün hedefi: **hazır bir scripti okuyup uyarlamak** ve **tek komutla tekrar çalışan bir rapor akışı** kurmak:

```text
Excel/CSV oku → temizle → SQLite'a yaz → SQL ile sorgula → özetle → grafik → HTML rapor + Excel özet
```

Bu akışın iki sürümü var; ikisi **aynı ana sayıları** üretir:

| Sürüm | Dosya | Gerekenler | Rapor | Excel özet |
|---|---|---|---|---|
| B planı (paketsiz) | `07_pipeline_stdlib.py` | yalnızca Python | `rapor_stdlib.html` (SVG gömülü) | `ozet_stdlib.xlsx` (`basit_xlsx.py` ile) |
| Paketli | `08_pipeline_pandas_opsiyonel.py` | pandas, matplotlib, openpyxl | `rapor_pandas.html` (PNG base64 gömülü) | `ozet_pandas.xlsx` |

Kontrol: `python gun07/09_iki_yol_karsilastir_opsiyonel.py` → `Sonuç: iki yol AYNI ana sayıları üretti.`

## Anlatım sırası

1. `01_analiz_pipeline.py` (küçük veri; akış fikri) → `05_hazir_script_uyarlama.py` (AYARLAR bölümü)
2. `06_filtre_parametreleri_bos.py` (canlı kodlama) → `06_filtre_parametreleri.py` (argparse)
3. `07_pipeline_stdlib.py` (adım adım okuma) → farklı parametrelerle çalıştırma → `--girdi data/sikayetler_kirli.csv`
4. Paket varsa `08_pipeline_pandas_opsiyonel.py` ve `09_iki_yol_karsilastir_opsiyonel.py`
5. Ekip projesi: [projeler/README.md](projeler/README.md) (4 kart + rubrik) → sunum
6. `02_html_rapor.py`, `03_parametreli_script.py`, `04_streamlit_opsiyonel.py` (opsiyonel gösterim) mevcut haliyle durur.

## Parametreli çalıştırma örnekleri

```console
python gun07/07_pipeline_stdlib.py
python gun07/07_pipeline_stdlib.py --il Ankara --baslangic 2026-04-01 --bitis 2026-06-30
python gun07/07_pipeline_stdlib.py --operator "Operatör B"
python gun07/07_pipeline_stdlib.py --girdi data/sikayetler_kirli.csv
python gun07/07_pipeline_stdlib.py --help
```

Argüman verilmezse tüm veri kullanılır. Boşluklu değerler çift tırnakla yazılır (PowerShell ve cmd'de aynı). Tarih biçimi `YYYY-AA-GG`; hatalı tarih veya başlangıç > bitiş durumunda argparse açıklayıcı mesajla durur.

## Yeni dosyalar ve beklenen çıktılar

| Dosya | Ne öğretir | Beklenen (stdout'ta) |
|---|---|---|
| `05_hazir_script_uyarlama.py` | AYARLAR bölümünü değiştirerek uyarlama; Excel uyumlu `;` CSV | `Ankara / İnternet Hızı: 24 şikâyet, 17 çözülen` |
| `06_filtre_parametreleri_bos.py` | argparse canlı kodlama iskeleti | `Eşleşen kayıt: 600` |
| `06_filtre_parametreleri.py` | `--il`, `--operator`, `--baslangic`, `--bitis` | `Eşleşen kayıt: 600` |
| `basit_xlsx.py` | paketsiz .xlsx okuma/yazma (xlsx = zip + XML) | `basit_xlsx deneme: yaz-oku tutarlı` |
| `07_pipeline_stdlib.py` | uçtan uca akış, temizlik kuralları, SQL JOIN, SVG rapor | `Kayıt sayısı : 600` … `Rapor: outputs/gun07/rapor_stdlib.html` |
| `08_pipeline_pandas_opsiyonel.py` | aynı akış pandas ile; `to_sql`, `read_sql`, `ExcelWriter`, base64 PNG | `Rapor: outputs/gun07/rapor_pandas.html` |
| `09_iki_yol_karsilastir_opsiyonel.py` | iki yöntemle çapraz doğrulama | `Sonuç: iki yol AYNI ana sayıları üretti.` |
| `projeler/kart1..4_*.py` | proje kartlarının referans çözümleri | bkz. `projeler/README.md` |
| `cozumler_ek.py` | ek alıştırma çözümleri (unittest dahil) | `Gün 7 ek çözümler tamamlandı.` |

Ana sayılar (argümansız): 600 kayıt · 415 çözülen · 89 reddedilen · 96 işlemde · çözülme %69.2 · ortalama çözüm 9.6 gün (yalnızca Çözüldü) · medyan 9.0 · hedef aşımı %39.8 · en çok Fatura · en yoğun İstanbul · en hızlı kanal Çağrı Merkezi.
Kirli dosyayla: 26 okunur, 20 temiz, 6 sorunlu (geçersiz süre ×2, geçersiz tarih, memnuniyet 7, boş kategori, tekrar).

## Resmî kaynaklar

- argparse eğitimi: <https://docs.python.org/3/howto/argparse.html>
- sqlite3: <https://docs.python.org/3/library/sqlite3.html> · SQLite SELECT: <https://www.sqlite.org/lang_select.html>
- zipfile: <https://docs.python.org/3/library/zipfile.html> · xml.etree: <https://docs.python.org/3/library/xml.etree.elementtree.html>
- base64: <https://docs.python.org/3/library/base64.html> · subprocess: <https://docs.python.org/3/library/subprocess.html>
- pandas `read_excel`: <https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html> · `to_sql`: <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html> · `ExcelWriter`: <https://pandas.pydata.org/docs/reference/api/pandas.ExcelWriter.html>
- Matplotlib `savefig`: <https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html>
- unittest: <https://docs.python.org/3/library/unittest.html>

Eğitmen akışı: [EGITMEN_AKISI.md](EGITMEN_AKISI.md) · Proje kartları: [projeler/README.md](projeler/README.md)
