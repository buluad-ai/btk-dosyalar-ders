# BTK — Python ile Uygulamalı Veri Analizi (7 gün + 1 AI günü)

Eğitmen: Bayram Uluad · Vektörel Bilişim · Hedef kitle: BTK teknik ekibi (çoğunluğu yazılımcı değil)

Ortam: **VS Code + Python eklentisi + CPython 3.15**, yalnızca yerel `.py` dosyaları (Jupyter/Colab yok). İlk 4 gün yalnızca standart kütüphane; 5–7. günler pandas/NumPy/Matplotlib/Seaborn ile, **her paketli örneğin paketsiz (B planı) karşılığı var**.

## Nereden başlamalı?

| Kim | Dosya |
|---|---|
| Eğitmen — sabah özeti, kalan işler | [`docs/SABAH_OZETI.md`](docs/SABAH_OZETI.md) |
| Eğitmen — gün planı (dakika dakika) | `gunXX/EGITMEN_AKISI.md` |
| Eğitmen — sunum (notlu, PAYLAŞMAYIN) | `slides/BTK_Python_Instructor_PRIVATE.pptx`, `slides/BTK_AI_Instructor_PRIVATE.pptx` |
| Öğrenci — sunum (notsuz) | `slides/BTK_Python_Student.pdf/.pptx`, `slides/BTK_AI_Student.pdf/.pptx` |
| Müfredat | [`docs/YEDI_GUN_MUFREDAT.md`](docs/YEDI_GUN_MUFREDAT.md) |
| Paket kurulamazsa | [`docs/B_PLANI_SIFIR_EK_PAKET.md`](docs/B_PLANI_SIFIR_EK_PAKET.md) |
| IT'ye gönderilecek | [`setup/IT_TEK_SEFERLIK_TALEP.md`](setup/IT_TEK_SEFERLIK_TALEP.md), [`setup/WINDOWS_KURULUM_KILAVUZU.md`](setup/WINDOWS_KURULUM_KILAVUZU.md), `setup/wheelhouse-win-cp315/` |
| Sınıf içi sorunlar | [`docs/SORUN_GIDERME.md`](docs/SORUN_GIDERME.md) |
| AI araçları günü | [`docs/AI_TOOLS_AYRI_GUN.md`](docs/AI_TOOLS_AYRI_GUN.md) |

## Klasörler

| Klasör | İçerik |
|---|---|
| `gun01` … `gun07` | Gün gün çalışan, yorumlu örnekler; `README.md` (anlatım sırası, beklenen çıktılar, resmî linkler), `ALISTIRMALAR.md` (Temel/Orta/İleri), `cozumler*.py`, `*_bos.py` canlı kodlama iskeletleri |
| `data` | Sentetik veri: küçük `basvurular.csv` (Gün 1–4 ısınma), zengin `sikayetler.csv` (600), `hiz_olcumleri.csv` (400), `sikayetler_kirli.csv`, `btk_ornek_veri.xlsx` |
| `outputs` | Scriptlerin ürettiği CSV/Excel/SQLite/PNG/SVG/HTML (her çalıştırmada yeniden oluşur) |
| `setup` | Ortam kontrolü, Windows kurulum betiği, çevrimdışı paketler, öğrenci ZIP üreticisi |
| `slides` | Sunumlar ve `build_slides.py` (sunumu yeniden üretir) |
| `tests` | Tüm örnekleri ayrı süreçte çalıştırıp çıktılarını doğrulayan testler |

## Sık komutlar (proje kökünde)

```console
py gun03/10_sikayet_csv_okuma.py           # Windows (Mac: python3 veya .venv/bin/python)
python -m unittest discover -s tests -v     # bütün örnekleri doğrula
python setup/check_environment.py           # öğrenci bilgisayarında ortam raporu
python setup/paket_olustur.py 3             # Gün 3 öğrenci ZIP'i (dist/); --cozumlu ile çözümler dahil
```

Mac'teki hazır ortamlar: `.venv` (3.15, paketli), `.venv-analytics` (3.14, paketli + Streamlit), **`.venv-bplan` (3.15, hiç paket yok — B planını sınıfta birebir simüle etmek için)**.
