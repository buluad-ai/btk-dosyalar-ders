# -*- coding: utf-8 -*-
"""Gün 7 ek alıştırma çözümleri (paketsiz). Bkz. ALISTIRMALAR.md

İçerik:
    T1  05 scriptinin ayarlarını fonksiyon parametresine çevirip İstanbul/Kapsama/20 gün
    T2  Operatör C, Temmuz-Eylül: kayıt ve durum dağılımı
    O1  Pipeline'a --kategori benzeri yeni filtre: tekrar kullanılabilir fonksiyon
    O3  Excel özetine "Il" sayfası eklemek (basit_xlsx)
    İ2  temizle() fonksiyonu için küçük otomatik testler (unittest)
    İ3  İki dönemin ana sayılarını karşılaştırma (Q2 vs Q3)

NASIL ÇALIŞTIRILIR?
    python gun07/cozumler_ek.py

BEKLENEN ÇIKTI (son satır):
    Gün 7 ek çözümler tamamlandı.
"""
import csv
import importlib.util
import io
import statistics
import unittest
from collections import Counter
from datetime import date
from pathlib import Path

from basit_xlsx import xlsx_oku, xlsx_yaz

ROOT = Path(__file__).resolve().parents[1]

with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    KAYITLAR = list(csv.DictReader(dosya))

# Adı rakamla başlayan dosya ("07_...") normal "import" ile alınamaz; importlib ile yüklüyoruz.
_spec = importlib.util.spec_from_file_location("pipeline", ROOT / "gun07" / "07_pipeline_stdlib.py")
pipeline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pipeline)       # main() çalışmaz; yalnızca fonksiyonlar tanımlanır


def esik_raporu(il, kategori, esik_gun):
    """T1: AYARLAR bölümü artık fonksiyonun parametreleri."""
    secilen = [k for k in KAYITLAR if k["il"] == il and k["kategori"] == kategori]
    cozulen = [k for k in secilen if k["durum"] == "Çözüldü"]
    asan = [k for k in cozulen if int(k["cozum_suresi_gun"]) > esik_gun]
    return len(secilen), len(cozulen), len(asan)


def filtrele(kayitlar, **kosullar):
    """O1: herhangi bir sütuna eşitlik filtresi. filtrele(v, kategori="Fatura", il="Ankara")"""
    return [k for k in kayitlar if all(k[sutun] == deger for sutun, deger in kosullar.items())]


def ana_sayilar(kayitlar):
    cozulen = [int(k["cozum_suresi_gun"]) for k in kayitlar if k["durum"] == "Çözüldü"]
    return {"kayit": len(kayitlar), "cozulen": len(cozulen),
            "cozulme_orani": round(len(cozulen) / len(kayitlar) * 100, 1),
            "ort_gun": round(statistics.mean(cozulen), 2)}


def donem(kayitlar, bas, bit):
    return [k for k in kayitlar if bas <= date.fromisoformat(k["tarih"]) <= bit]


class TemizleTestleri(unittest.TestCase):
    """İ2: kural başına bir test. Ham satır sözlüğünü elle kurup temizle()'ye veriyoruz."""
    ORNEK = {"sikayet_no": "1", "tarih": "2026-01-05", "il": "Ankara", "operator": "Operatör A",
             "hizmet": "Mobil", "kategori": "Fatura", "kanal": "Web", "durum": "Çözüldü",
             "cozum_suresi_gun": "4", "memnuniyet": "3", "itiraz_tutari_tl": ""}

    def test_il_yazimi_duzelir(self):
        temiz, sorunlu = pipeline.temizle([dict(self.ORNEK, il=" ankara ")])
        self.assertEqual(temiz[0]["il"], "Ankara")

    def test_metin_sure_reddedilir(self):
        temiz, sorunlu = pipeline.temizle([dict(self.ORNEK, cozum_suresi_gun="on iki")])
        self.assertEqual(sorunlu[0]["neden"], "geçersiz çözüm süresi")

    def test_tekrar_ayiklanir(self):
        temiz, sorunlu = pipeline.temizle([self.ORNEK, dict(self.ORNEK)])
        self.assertEqual((len(temiz), sorunlu[0]["neden"]), (1, "tekrar eden kayıt"))


if __name__ == "__main__":
    toplam, cozulen, asan = esik_raporu("İstanbul", "Kapsama", 20)
    print(f"T1: İstanbul / Kapsama: {toplam} şikâyet, {cozulen} çözülen, 20 günü aşan {asan}")

    c = [k for k in donem(KAYITLAR, date(2026, 7, 1), date(2026, 9, 30)) if k["operator"] == "Operatör C"]
    print(f"T2: Operatör C, Tem-Eyl: {len(c)} kayıt |", dict(Counter(k["durum"] for k in c)))

    fatura_ankara = filtrele(KAYITLAR, kategori="Fatura", il="Ankara")
    print("O1: Fatura + Ankara:", ana_sayilar(fatura_ankara))

    il_sayfasi = [["İl", "Şikâyet"]] + [list(x) for x in Counter(k["il"] for k in KAYITLAR).most_common()]
    hedef = ROOT / "outputs" / "gun07" / "cozum_o3_il.xlsx"
    xlsx_yaz(hedef, {"Il": il_sayfasi})
    print("O3: Il sayfası satır sayısı:", len(xlsx_oku(hedef, "Il")))

    sonuc = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(TemizleTestleri))
    print(f"İ2: {sonuc.testsRun} test, hata: {len(sonuc.failures) + len(sonuc.errors)}")

    q2 = ana_sayilar(donem(KAYITLAR, date(2026, 4, 1), date(2026, 6, 30)))
    q3 = ana_sayilar(donem(KAYITLAR, date(2026, 7, 1), date(2026, 9, 30)))
    print(f"{'İ3: gösterge':<18} {'Q2':>8} {'Q3':>8} {'fark':>8}")
    for anahtar in q2:
        print(f"    {anahtar:<14} {q2[anahtar]:>8} {q3[anahtar]:>8} {round(q3[anahtar] - q2[anahtar], 2):>8}")
    print("Gün 7 ek çözümler tamamlandı.")
