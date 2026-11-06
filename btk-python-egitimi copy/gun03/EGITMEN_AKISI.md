# Gün 3 — Eğitmen akışı (6 × 60 dakika)

Bu dosya yalnızca eğitmen içindir. Günün hedefi: katılımcı bir fonksiyonu çağırıp sonucunu kullanabilsin, hazır bir modülü import edebilsin, CSV okuyup filtreleyip yeni CSV yazabilsin, hatalı satırı programı durdurmadan ayırabilsin ve parametreli bir scripti komut satırından çalıştırabilsin.

**Derse girmeden önce (15 dk):**
- Eğitmen bilgisayarında `python -m unittest discover -s tests` çalıştırın; yeşil olmalı.
- `outputs/gun03/` klasörünü boşaltın; scriptler dosyaları yeniden üretir.
- Projektörde VS Code yazı boyutunu büyütün (Ctrl + `+`) ve terminal panelini açık tutun.
- Bir katılımcı bilgisayarında `python gun03/07_kendi_modulum.py` komutunu deneyin (modül import yolu sorun çıkarıyor mu?).
- `sikayetler.csv` dosyasını Excel'de açık tutun: sayıları Excel filtresiyle de gösterebilmek güven verir.

**Günün sabit cümlesi:** "Excel'de formül yazıyordunuz; bugün kendi formülünüzü (fonksiyon) yazıp kendi formül kütüphanenizi (modül) kuruyoruz."

---

## Blok 1 (0:00–1:00) — Isınma ve fonksiyonlar

| Dakika | Ne yapılır | Dosya |
|---|---|---|
| 0–10 | Gün 2 tekrarı: bir listenin içinden eşiği aşanları sayan döngüyü tahta/ekranda **tahmin ettirin**, sonra çalıştırın. | `gun02/02_listeler_donguler.py` |
| 10–20 | `def`, parametre, `return`. Boş listede neden `None`? | `01_fonksiyonlar.py` |
| 20–40 | Varsayılan parametre (`oran=0.20`), isimli argüman, **return vs print**, çoklu dönüş. | `05_fonksiyon_parametreleri.py` |
| 40–55 | Uygulama: `kdv_ekle(500)` ve `kdv_ekle(500, oran=0.10)` sonuçlarını önce kâğıda, sonra koda. `sla_asildi_mi(10)` ne döner? (eşit = aşmadı → `False`) | aynı dosya |
| 55–60 | Soru/telafi | |

**Konuşma notu:** "Fonksiyon bir makine: içine değer koyarsınız (parametre), dışarı sonuç çıkar (return). `print` sadece ekrana bakmaktır; sonucu başka hesapta kullanamazsınız."

**Sık hatalar:**
- `def` satırının sonunda `:` unutulur → `SyntaxError: expected ':'`.
- Fonksiyon tanımlanır ama çağrılmaz → "Hiçbir şey olmadı hocam." Parantezle çağırmayı gösterin.
- `return` yerine `print` → sonra `deger + 5` satırında `TypeError: ... 'NoneType'`. Bu hatayı bilerek gösterin (dosyada yorumlu satır var).
- Parametre sırası karışır: `hiz_yuzdesi(50, 29.8)` → 167.8. İsimli çağrının neden okunaklı olduğunu gösterin.

**Geride kalınırsa:** Çoklu dönüş (`sure_ozeti`) ve docstring bölümünü sadece gösterin. **Hızlı gidilirse:** "KDV dahil tutardan KDV hariç tutarı bulan fonksiyon" yazdırın, sonra `kdv_ayir` ile karşılaştırın.

---

## Blok 2 (1:00–2:00) — Hazır modüller, kendi modülümüz, tarih

| Dakika | Ne yapılır | Dosya |
|---|---|---|
| 0–15 | `import` çeşitleri; math, statistics (istatistikçiler burada canlanır: medyan, stdev, çeyrekler), random **seed**, pathlib. | `06_hazir_moduller.py` |
| 15–30 | Kendi modülümüz: `yardimcilar.py` dosyasını açın, fonksiyonları gösterin. Önce **doğrudan çalıştırın** (kendi testi), sonra import eden dosyayı çalıştırın. `if __name__ == "__main__":` için tek cümle: "Bu kısım yalnızca dosya doğrudan çalışınca çalışır." | `yardimcilar.py`, `07_kendi_modulum.py` |
| 30–45 | Tarih: metin → tarih, gün farkı, `timedelta`, Türkçe ay/gün adı, aylık dağılım. | `08_tarihler.py` |
| 45–55 | Uygulama: `08_tarihler.py` içinde `rapor_tarihi` değerini `date(2026, 12, 31)` yapın; ortalama bekleme nasıl değişir? `hedef_gun = 10` → `5` yapın. | aynı dosya |
| 55–60 | Soru/telafi | |

**Konuşma notu:** "Bu modüller Python ile birlikte gelir. İnternet, kurulum, IT izni gerekmez. Excel'in hazır fonksiyonları gibi; `import` ile 'bu kategoriyi açıyorum' diyoruz."

**Sık hatalar:**
- `ModuleNotFoundError: No module named 'yardimcilar'` → Dosya yanlış klasörde ya da katılımcı kendi dosyasını masaüstüne kaydetti. Kendi dosyası `gun03/` içinde olmalı.
- Katılımcı dosyasına `random.py` veya `statistics.py` adı verirse standart modül yerine kendi dosyası import edilir; garip `AttributeError` çıkar. Dosyayı yeniden adlandırın, varsa `__pycache__` klasörünü silin.
- `statistics.mean` sonucu `8` (8.0 değil) yazar; şaşırırlarsa: "tam sayıların ortalaması tam çıkarsa öyle görünür."
- `round(2.5)` → 2. Excel'in YUVARLA fonksiyonundan farklı; dosyada açıklaması var. İstatistikçiler sorarsa "bankacı yuvarlaması" deyin.
- `date.fromisoformat("2026-2-5")` → hata; biçim tam `2026-02-05` olmalı.

**Geride kalınırsa:** `06` dosyasında yalnızca statistics + pathlib anlatın; `08` dosyasının 3. ve 4. bölümünü ödev yapın. **Hızlı gidilirse:** `yardimcilar.py` içine `ay_adi` benzeri `ceyrek(tarih)` ("Ç1".."Ç4") fonksiyonu ekletin.

---

## Blok 3 (2:00–3:00) — Dosyalar ve CSV (küçükten büyüğe)

| Dakika | Ne yapılır | Dosya |
|---|---|---|
| 0–10 | Yol + UTF-8: `ROOT / "outputs"` neden? | `02_dosya_okuma_yazma.py` |
| 10–25 | `open` + `with`, `w` / `a` / `r` kipleri, satır satır okuma. Çalıştırdıktan sonra `outputs/gun03/islem_log.txt` dosyasını VS Code'da açın. | `09_log_dosyasi.py` |
| 25–35 | Küçük CSV: 36 satır, 192 toplamı (elle doğrulanabilir). | `03_csv_okuma.py` |
| 35–50 | Büyük CSV: aynı yöntem 600 satırda. Boş hücre neden 0 değil? EĞERSAY / ORTALAMAEĞER / ETOPLA karşılıkları. **Excel'de aynı sayıyı filtreyle gösterin** (Çözüldü = 415). | `10_sikayet_csv_okuma.py` |
| 50–60 | Uygulama: Temel T2 (e-Devlet sayısı = 195). | `ALISTIRMALAR.md` |

**Konuşma notu:** "CSV'den gelen her şey metindir. `'7'` ile `7` farklıdır. Excel bunu sizin yerinize tahmin ediyordu; Python tahmin etmez, siz söylersiniz."

**Sık hatalar:**
- `encoding="utf-8"` unutulur → Windows'ta `UnicodeDecodeError` veya `Ã¼` gibi bozuk karakterler. Kural: her `open` çağrısında encoding.
- `FileNotFoundError` → katılımcı yolu elle `"data/sikayetler.csv"` yazmış ve terminal başka klasörde. `ROOT / "data" / ...` kalıbını gösterin.
- Windows yolu kopyalanıp yapıştırılırsa: `"C:\Users\..."` içindeki `\U` hata verir (`SyntaxError: (unicode error)`). Çözüm: `r"C:\Users\..."` veya düz `/` kullanmak; en iyisi `Path`.
- `"w"` kipi dosyayı **siler**; log'a eklemek isteyen `"a"` kullanmalı.
- `int("")` → `ValueError`. Bunu bilerek gösterin.

**Geride kalınırsa:** `09` dosyasını hızlı gösterin; asıl hedef `10`. **Hızlı gidilirse:** "Operatör bazında ortalama memnuniyet" sözlükle hesaplatın.

---

## Blok 4 (3:00–4:00) — Filtreleyip yazma ve JSON

| Dakika | Ne yapılır | Dosya |
|---|---|---|
| 0–20 | Filtre = Excel Otomatik Filtre. `DictWriter`, `newline=""`, **utf-8-sig** ve Türkçe Excel'in `;` beklemesi. İki çıktıyı **Excel'de çift tıklayıp** açın ve farkı gösterin. | `11_csv_filtrele_yaz.py` |
| 20–30 | Kısa JSON tanışması (sabahki dosya). | `04_json_ve_dogrulama.py` |
| 30–40 | JSON'a özet yazma, `ensure_ascii=False`. `il_ozeti.json` dosyasını VS Code'da açın. | `12_json_okuma_yazma.py` |
| 40–60 | Bireysel/eşli uygulama: T1, T3. Erken bitenler O1. Eğitmen dolaşır. | `ALISTIRMALAR.md` |

**Konuşma notu:** "Excel'e gidecek dosya: `utf-8-sig`. Python'a, Power BI'a gidecek dosya: düz `utf-8` de olur. Kararsızsanız `utf-8-sig` her ikisinde de çalışır."

**Sık hatalar (Windows'a özgü):**
- `PermissionError: [Errno 13] Permission denied: '...ankara_internet_hizi.csv'` → dosya **Excel'de açık**. Excel'i kapatıp tekrar çalıştırın. Bu hatayı gün içinde kesin göreceksiniz; önceden söyleyin.
- `newline=""` unutulursa Windows'ta satır aralarında boş satırlar oluşur.
- Excel'de tek sütun → Türkçe bölge ayarı `;` bekliyor. `_excel_tr.csv` dosyasını açın.
- Excel `2404.26` sayısını tarih veya metin sanabilir → `_excel_tr` sürümünde ondalık virgül kullanıldı.

**Geride kalınırsa:** `12` dosyasını atlayın (JSON Gün 7'de yeniden geçecek). **Hızlı gidilirse:** O3 (düşük hız log'u).

---

## Blok 5 (4:00–5:00) — Hatalı satırlar ve parametreli script

| Dakika | Ne yapılır | Dosya |
|---|---|---|
| 0–5 | `sikayetler_kirli.csv` dosyasını Excel'de/VS Code'da açın; sınıfa "bu dosyada kaç hata görüyorsunuz?" diye sorun (2 dk). | `data/sikayetler_kirli.csv` |
| 5–25 | `try / except / else / finally` sırası. Çalıştırın; her hatalı satırı Excel'deki satır numarasıyla eşleştirin (scriptte `start=2` bu yüzden var). `hata_raporu.txt` dosyasını açın. | `13_hatali_satirlar.py` |
| 25–40 | `sys.argv`: Terminalde **sırayla** parametresiz, `İzmir`, `İstanbul İşlemde`, `Sabit` (hatalı) çalıştırın. Çıkış kodunu gösterin (PowerShell: `$LASTEXITCODE`, cmd: `echo %ERRORLEVEL%`). | `14_parametreli_script.py` |
| 40–55 | Uygulama: Herkes kendi seçtiği ille çalıştırsın ve sonucu söylesin. Erken bitenler İ2. | |
| 55–60 | Soru/telafi | |

**Konuşma notu:** "Gerçek veride hata olur. Amaç programın çökmesi değil; hatalı satırı gerekçesiyle ayırıp veri sahibine geri göndermek."

**Sık hatalar:**
- `except:` yalnız yazılırsa yazım hataları bile sessizce yutulur. Hep hata adını yazın (`except ValueError:`).
- VS Code'daki ▶ Run düğmesi parametre vermez → komutu terminale elle yazdırın.
- PowerShell'de `python` yerine Microsoft Store açılıyorsa: `py gun03\14_parametreli_script.py İzmir`.
- Türkçe karakterli parametre (`İzmir`) eski cmd pencerelerinde bozulabilir. VS Code terminali (PowerShell) genelde sorunsuzdur; sorun olursa `Ankara`, `Konya` gibi ASCII adlarla gösterin.
- Büyük/küçük harf: `izmir` yazılırsa geçersiz il mesajı çıkar. Bu bilinçli: mesaj geçerli değerleri listeliyor.
- `title()` Türkçe `i/İ` harfini bilmez (`"istanbul".title()` → `Istanbul`). Dosyada yorumu var; bu yüzden geçerli iller listesiyle karşılaştırıyoruz.

**Geride kalınırsa:** `finally` bölümünü yalnızca anlatın; `14` dosyasını sadece parametresiz + bir il ile gösterin. **Hızlı gidilirse:** İ1 (kural tablosu) yazılımcılara.

---

## Blok 6 (5:00–6:00) — Canlı kodlama mini proje, tekrar, çıkış bileti

| Dakika | Ne yapılır | Dosya |
|---|---|---|
| 0–5 | İskeleti çalıştırın: hata vermeden çalıştığını, sayaçların 0 olduğunu gösterin. | `15_mini_sla_raporu_bos.py` |
| 5–35 | TODO 1–6'yı **sınıfla birlikte** doldurun: her TODO'dan sonra çalıştırın, çıktının değişmesini izleyin. Katılımcılar kendi kopyalarında takip eder. | aynı dosya |
| 35–40 | Tamamlanmış sürümle karşılaştırın; `sla_raporu.csv` dosyasını Excel'de açın. Yorum sorusu: "İnternet Hızı'nda %61 aşım: hedef mi gerçekçi değil, süreç mi yavaş?" | `15_mini_sla_raporu.py` |
| 40–50 | Telafi: Geride kalanlar T1–T3; diğerleri Orta/İleri. | `ALISTIRMALAR.md` |
| 50–60 | Çıkış bileti (3 soru, ALISTIRMALAR.md sonunda) + Gün 4 önizleme: "Yarın bu CSV'yi veritabanına koyup aynı soruları SQL ile soracağız." | |

**Sık hatalar:** TODO 1'de `continue` yerine `break` yazılır → döngü ilk kayıtta biter, tüm sayaçlar 0 kalır. TODO 3'te `HEDEFLER[kayit]` yazılır → `TypeError: unhashable type: 'dict'`; doğrusu `HEDEFLER[kayit["kategori"]]`.

**Geride kalınırsa:** TODO 5–6'yı eğitmen yazar; katılımcı yalnızca 1–4'ü yapar. Tamamlanmış dosya her zaman yedektir.

---

## Gün sonu kontrol listesi

- [ ] Herkes en az bir kez `import yardimcilar` ile çalışan bir dosya çalıştırdı.
- [ ] Herkes Excel'de açılan bir CSV üretti.
- [ ] Herkes `14_parametreli_script.py` dosyasını kendi seçtiği parametreyle çalıştırdı.
- [ ] Çıkış biletinde "boş hücre neden 0 değil?" sorusuna doğru cevap oranı not edildi (Gün 4 başında tekrar için).

## Windows hızlı başvuru

| Durum | Çözüm |
|---|---|
| `python` komutu Microsoft Store açıyor | `py` kullanın veya VS Code'da yorumlayıcıyı seçin (Ctrl+Shift+P → Python: Select Interpreter) |
| PowerShell'de script çalıştırma engeli (`.ps1` ile ilgili kırmızı hata) | Bu bizi etkilemez; `python dosya.py` bir `.ps1` çalıştırmaz. venv `Activate.ps1` hatası ise IT'ye bildirin, `.venv\Scripts\python.exe gun03\...` ile tam yol kullanın |
| Yol ayırıcı | Komutta `gun03\dosya.py` de `gun03/dosya.py` de çalışır; kod içinde her zaman `Path` |
| Kod içine Windows yolu yapıştırma | `r"C:\..."` ham metin veya `/` |
| `PermissionError` | Dosya Excel'de açık; kapatın |
| Türkçe karakter bozuk | Kaydederken UTF-8; Excel için `utf-8-sig` |
| Çıkış kodu görme | PowerShell `$LASTEXITCODE`, cmd `echo %ERRORLEVEL%` |
