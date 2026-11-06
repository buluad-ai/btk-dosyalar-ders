# -*- coding: utf-8 -*-
"""Hazır parametreli script: komut satırından il (ve isteğe bağlı durum) vermek.

NE ÖĞRETİYOR?
    Kodu her seferinde değiştirmek yerine, değeri çalıştırırken veririz:
        python gun03/14_parametreli_script.py              -> varsayılan: Ankara
        python gun03/14_parametreli_script.py İzmir
        python gun03/14_parametreli_script.py İstanbul İşlemde
    Excel benzetmesi: Formüldeki sabit değeri bir "parametre hücresine" taşımak.
    Kullanıcı sadece o hücreyi değiştirir, formüle dokunmaz.

    sys.argv: komut satırında yazılan kelimelerin listesi.
        sys.argv[0] -> scriptin adı
        sys.argv[1] -> ilk parametre (varsa)
        sys.argv[2] -> ikinci parametre (varsa)
    (Gün 7'de daha kapsamlı argparse modülünü göreceğiz.)

    WINDOWS / POWERSHELL NOTU:
        python gun03\\14_parametreli_script.py "Sabit İnternet"
        Boşluk içeren değerleri tırnak içine alın. Windows'ta "python" çalışmazsa "py" deneyin.
    VS Code'da "Run" düğmesi parametre veremez: Terminal'e komutu yazın.

NASIL ÇALIŞTIRILIR?
    python gun03/14_parametreli_script.py [il] [durum]

BEKLENEN ÇIKTI (parametresiz):
    Parametre verilmedi, varsayılan kullanılıyor: Ankara
    Ankara: 107 şikâyet
    ...
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARSAYILAN_IL = "Ankara"

# ---------------------------------------------------------------------------
# 1) Parametreleri oku (yoksa varsayılan)
# ---------------------------------------------------------------------------
# len(sys.argv) > 1 : "script adından başka bir şey yazılmış mı?"
if len(sys.argv) > 1:
    il = sys.argv[1].strip()
else:
    il = VARSAYILAN_IL
    print("Parametre verilmedi, varsayılan kullanılıyor:", il)

durum_filtresi = sys.argv[2].strip() if len(sys.argv) > 2 else None   # kısa if yazımı

# ---------------------------------------------------------------------------
# 2) Veriyi oku ve parametreyi doğrula
# ---------------------------------------------------------------------------
with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

gecerli_iller = sorted({k["il"] for k in kayitlar})      # küme -> tekil iller
# Not: sorted() harfleri bilgisayar kod sırasına göre dizer; "İ" ve "Ç" gibi Türkçe
# harfler Z'den sonra gelir ("İstanbul" listenin sonunda çıkar). Bu bir hata değildir.
if il not in gecerli_iller:
    # Kullanıcıya NEYİ yanlış yaptığını ve NE yazabileceğini söyle.
    print(f"Hata: '{il}' verisi bulunamadı. Geçerli iller: {', '.join(gecerli_iller)}")
    # sys.exit(1): programı "başarısız" koduyla bitirir. Otomatik çalışan
    # zamanlanmış görevler (Görev Zamanlayıcı) bu kodla hatayı anlar.
    sys.exit(1)

# ---------------------------------------------------------------------------
# 3) Filtrele ve raporla
# ---------------------------------------------------------------------------
secilen = [k for k in kayitlar if k["il"] == il]
if durum_filtresi:
    secilen = [k for k in secilen if k["durum"] == durum_filtresi]
    print(f"{il} / {durum_filtresi}: {len(secilen)} şikâyet")
else:
    print(f"{il}: {len(secilen)} şikâyet")

# Kategori dağılımı (en çoktan aza)
# sorted(..., key=lambda cift: cift[1], reverse=True):
#   items() bize (kategori, adet) çiftleri verir; lambda "sıralarken çiftin 2. elemanına
#   (adede) bak" demektir; reverse=True büyükten küçüğe (Excel: Z'den A'ya sırala).
kategoriler = {}
for k in secilen:
    kategoriler[k["kategori"]] = kategoriler.get(k["kategori"], 0) + 1
for kategori, adet in sorted(kategoriler.items(), key=lambda cift: cift[1], reverse=True):
    print(f"  {kategori:<15} {adet:>3}")

# Ortalama çözüm süresi yalnızca "Çözüldü" kayıtlarından hesaplanır
# (işlemdekilerin süresi boş, reddedilenler ise "çözüm" değildir).
sureler = [int(k["cozum_suresi_gun"]) for k in secilen
           if k["durum"] == "Çözüldü" and k["cozum_suresi_gun"] != ""]
if sureler:
    print(f"Ortalama çözüm süresi: {sum(sureler) / len(sureler):.1f} gün ({len(sureler)} çözülen kayıt)")
else:
    print("Ortalama çözüm süresi: hesaplanamadı (çözülen kayıt yok)")
