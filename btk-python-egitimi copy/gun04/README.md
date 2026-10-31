# Gün 4 — veri modeli, class tanışma, SQLite ve Excel'den veritabanına

Komutları eğitim klasörünün kökünden VS Code terminalinde çalıştırın. Windows: `python` (çalışmazsa `py`); macOS: etkin eğitim ortamında `python` veya `python3`. Scriptler çalışma klasöründen bağımsızdır. `14_excel_openpyxl_opsiyonel.py` dışındaki her şey yalnızca standart kütüphane kullanır. Çıktılar `outputs/gun04/` altına yazılır.

Eğitmenin dakika dakika akışı: [EGITMEN_AKISI.md](EGITMEN_AKISI.md).

## Anlatım sırası

| Sıra | Dosya | Konu | Beklenen kontrol |
|---|---|---|---|
| 1 | `01_veri_modeli.py` | küçük veride benzersiz kimlik | `Benzersiz kimlik: 36` |
| 2 | `05_veri_modeli_sikayet.py` | tablo/kayıt/alan, birincil anahtar, 1-N ilişki, metin diyagram | `Birincil anahtar tekil: 600/600` |
| 3 | `02_class_tanisma.py` | en küçük class | `Eşiği aştı: True` |
| 4 | `06_sikayet_sinifi.py` | `Sikayet` sınıfı: `__init__`, nitelik, metot, `__repr__`; dataclass | `Hedefi aşan çözülmüş şikâyet: 165` |
| 5 | `03_sqlite_sorgu.py` | küçük veride SQLite ve `?` | `5 günü aşan kayıt: 12` |
| 6 | `07_sqlite_yukleme.py` | CREATE TABLE, executemany, commit, NULL, PRIMARY KEY koruması | `NULL çözüm süresi: 96` |
| 7 | `08_select_where_order.py` | SELECT, WHERE, IN, LIKE, IS NULL, ORDER BY, LIMIT, BETWEEN | `Ankara'da çözülen fatura şikâyeti: 19` |
| 8 | `09_toplama_gruplama.py` | COUNT/SUM/AVG, GROUP BY, HAVING (PivotTable) | `100'den fazla şikâyeti olan il sayısı: 2` |
| 9 | `04_sql_birlestirme.py` | küçük veride JOIN | `Tuketici: 12 kayıt, 2.5 gün` |
| 10 | `10_join_hedefler.py` | JOIN/LEFT JOIN (DÜŞEYARA), alt sorgu | `Hedefi en sık aşılan kategori: İnternet Hızı` |
| 11 | `11_update_delete_guvenli.py` | kopya üzerinde UPDATE/DELETE, rowcount, rollback | `Asıl veritabanı değişmedi: 600 şikâyet` |
| 12 | `12_sql_injection_parametre.py` | `?` parametresi ve SQL injection | `Kötü girdi -> Parametreli sorgu: 0 satır` |
| 13 | `13_excel_stdlib_okuma.py` | .xlsx = zip + xml; paketsiz okuma ve DB'ye yazma | `Hedefler: 6 kategori` |
| 14 | `14_excel_openpyxl_opsiyonel.py` | aynı iş openpyxl ile (paket yoksa ATLANDI) | `Hedefler: 6 kategori` |
| 15 | `15_sorgu_csv_rapor.py` | sorgu sonucunu CSV'ye yazma | `Geri okunan toplam şikâyet: 600` |
| 16 | `16_mini_proje_bos.py` → `16_mini_proje.py` | mini proje: CSV → SQLite → 3 iş sorusu → rapor CSV | `İskelet çalıştı: ...` / `Rapor: outputs/gun04/mini_proje_rapor.csv (3 soru)` |

### Yardımcı modül: `db_yardimci.py`

05–16 arasındaki örneklerin ortak aletleri; `import db_yardimci as dy` ile kullanılır. Aynı klasörde kalmalıdır.

| Fonksiyon | Ne yapar |
|---|---|
| `veritabani_hazirla()` | `outputs/gun04/sikayet.sqlite` dosyasını **her çalıştırmada sıfırdan** kurar (iller, hedefler, sikayetler, hiz_olcumleri). Tekrar çalıştırmada satırlar katlanmaz. |
| `tablo_yazdir(imlec)` | Sorgu sonucunu terminalde hizalı tablo olarak basar. **DB Browser for SQLite kurulamazsa bu yeterlidir.** |
| `xlsx_sayfa_oku(yol, sayfa)` | .xlsx sayfasını **paketsiz** okur (zipfile + xml.etree). Hem `sharedStrings` (Excel'in kendi kaydettiği dosyalar) hem satır içi metin (`inlineStr`) biçimini, boş hücreleri, mantıksal değerleri ve göreli/mutlak sayfa yollarını işler. Sınırlar: formül yerine son kaydedilen değeri okur; tarih biçimli hücreler sayı (seri no) olarak gelir. |
| `sorgu_csv_yaz(imlec, yol)` | Sorgu sonucunu başlıklarıyla `utf-8-sig` CSV'ye yazar. |

Doğrudan çalıştırınca kendi testini yapar: `python gun04/db_yardimci.py` → `db_yardimci modülü kendi testini geçti`.

### Veri modeli

```text
iller (il PK, bolge) 1 ──< N sikayetler (sikayet_no PK, il FK, kategori FK, ...) N >── 1 hedefler (kategori PK, hedef_gun)
iller 1 ──< N hiz_olcumleri (olcum_no PK, il FK, operator, teknoloji, ...)
```

`hedefler` tablosu `data/btk_ornek_veri.xlsx` dosyasının **Hedefler** sayfasından okunur. Bölge bilgisi gerçek coğrafi bölgedir; operatör adları kurgusaldır.

## Üretilen dosyalar (`outputs/gun04/`)

| Dosya | Üreten |
|---|---|
| `egitim.sqlite` | 03 (mevcut test bunu kontrol eder) |
| `sikayet.sqlite` | 08–12, 15 (`veritabani_hazirla`) |
| `adim_adim.sqlite` | 07 |
| `egitim_kopya.sqlite` | 11 (UPDATE/DELETE yalnızca bu kopyada) |
| `excelden.sqlite` | 13 |
| `operator_ozeti.csv`, `aylik_trend.csv` | 15 |
| `mini_proje.sqlite`, `mini_proje_rapor.csv` | 16 |
| `mini_proje_bos.sqlite`, `mini_proje_bos_rapor.csv` | 16_bos |
| `cozumler_ek.sqlite`, `bolge_islemde.csv`, `sla_etiketli.csv` | cozumler_ek |

Tüm `.sqlite` dosyaları silinip yeniden üretilebilir. DB Browser for SQLite ile açıkken script çalıştırılırsa Windows dosyayı silemez; script anlaşılır bir mesajla durur.

## Kontrol edilmiş sayılar (eğitmen için)

- 600 şikâyet, 400 ölçüm, 6 hedef, 8 il, 6 bölge. NULL çözüm süresi 96; `COUNT(cozum_suresi_gun)` = 504.
- Operatör A 233 / B 170 / C 133 / D 64 şikâyet. 100'den fazla şikâyeti olan iller: İstanbul 185, Ankara 107.
- SLA aşımı (çözülenler): İnternet Hızı %61.3 en yüksek; toplam aşan 165.
- Mini proje: S1 Bursa (%54.7 çözüm oranı), S2 İnternet Hızı (%61.3), S3 Operatör C (%58.2; fark çok küçük, yorumda dikkat).

## Resmî kaynaklar

- sqlite3 modülü: https://docs.python.org/3/library/sqlite3.html (yer tutucular: https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders)
- SQLite SELECT: https://www.sqlite.org/lang_select.html · CREATE TABLE: https://www.sqlite.org/lang_createtable.html
- Toplama fonksiyonları: https://www.sqlite.org/lang_aggfunc.html · UPDATE: https://www.sqlite.org/lang_update.html · DELETE: https://www.sqlite.org/lang_delete.html
- SQLite veri türleri ve NULL: https://www.sqlite.org/datatype3.html
- Class: https://docs.python.org/3/tutorial/classes.html · dataclasses: https://docs.python.org/3/library/dataclasses.html
- zipfile: https://docs.python.org/3/library/zipfile.html · xml.etree: https://docs.python.org/3/library/xml.etree.elementtree.html
- openpyxl (opsiyonel paket): https://openpyxl.readthedocs.io/en/stable/tutorial.html
- DB Browser for SQLite (kurulabiliyorsa): https://sqlitebrowser.org/

## Günün çalışma düzeni

1. 60 dk: tekrar + veri modeli + class tanışma.
2. 60 dk: SQLite'a yükleme, SELECT/WHERE.
3. 60 dk: GROUP BY / HAVING ve rehberli SQL alıştırması.
4. 60 dk: JOIN, UPDATE/DELETE güvenliği, parametreli sorgu.
5. 60 dk: Excel'den veritabanına (paketsiz ve paketli yol), sorgudan CSV.
6. 60 dk: mini proje, tekrar ve 5. gün paket kararı.

## Sık sorunlar

- `ModuleNotFoundError: No module named 'db_yardimci'`: kendi dosyanız `gun04/` içinde olmalı.
- `sqlite3.OperationalError: no such table`: önce `veritabani_hazirla()` çağrılmamış ya da tablo adı yanlış yazılmış.
- `sqlite3.OperationalError: database is locked` veya `PermissionError`: DB Browser'da veya başka bir pencerede açık; kapatın.
- `sqlite3.IntegrityError: UNIQUE constraint failed`: aynı birincil anahtar ikinci kez eklenmeye çalışılıyor (tekrar çalıştırmada DROP/DELETE yok).
- `Incorrect number of bindings supplied`: `?` sayısı ile verilen değer sayısı farklı; tek değerde `(il,)` virgülünü unutmayın.
- SQL'de metin tek tırnak: `'Ankara'`. `= NULL` çalışmaz, `IS NULL` kullanın.
- Türkçe büyük/küçük harf: SQLite `LOWER/UPPER/LIKE` yalnız İngilizce harfleri dönüştürür; değerleri tam yazımla arayın.

[Alıştırmalar](ALISTIRMALAR.md) · [Temel çözüm](cozumler.py) · [Ek çözümler](cozumler_ek.py) · [Eğitmen akışı](EGITMEN_AKISI.md)
