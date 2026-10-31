# Sentetik eğitim verisi

Gerçek kişi veya kurum kaydı içermez. 36 başvuru, 3 birim. Her satır bir başvurudur. `basvuru_no` benzersiz kimliktir. `islem_suresi` gündür; açık kayıtlarda geçen, kapalı kayıtlarda tamamlanma süresidir. Bu nedenle tamamlanma süresi analizi yalnızca kapalı kayıtlarda yapılmalıdır. Tüm kayıtların süre toplamı 192, ortalaması 5.333333 gündür; kapalı kayıtların ortalaması farklıdır.

## Zengin eğitim verisi (Gün 3 ve sonrası)

Hepsi sentetiktir; `data/kaynak/veri_uret.py` sabit tohumla (seed=2026) yeniden üretir. Operatör adları kurgusaldır (Operatör A–D).

| Dosya | İçerik |
|---|---|
| `sikayetler.csv` | 600 abone şikâyeti (Ocak–Eylül 2026): il, operatör, hizmet, kategori, kanal, durum (Çözüldü/Reddedildi/İşlemde), çözüm süresi, memnuniyet (1–5), fatura itiraz tutarı |
| `hiz_olcumleri.csv` | 400 internet hız ölçümü: teknoloji (Fiber/VDSL/ADSL/4.5G), paket hızı, indirme/yükleme Mbps, ping |
| `sikayetler_kirli.csv` | 26 satır; kasıtlı hatalar (boşluklu il, küçük harf operatör, "on iki", 31.02.2026, aralık dışı memnuniyet, negatif süre, tekrar satır, boş kategori) |
| `btk_ornek_veri.xlsx` | Aynı verinin Excel hali; sayfalar: `Sikayetler`, `Hiz_Olcumleri`, `Hedefler` (kategori bazında hedef çözüm günü) |

İşlemde olan şikâyetlerde `cozum_suresi_gun` boştur — eksik veri tartışması için bilinçli bırakıldı.
