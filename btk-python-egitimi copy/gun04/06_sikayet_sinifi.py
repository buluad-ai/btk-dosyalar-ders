# -*- coding: utf-8 -*-
"""Class tanışma: Sikayet sınıfı (__init__, nitelik, metot, __repr__) ve dataclass alternatifi.

NE ÖĞRETİYOR?
    Sınıf (class) = bir kayıt türünün KALIBI. Nesne = o kalıptan üretilmiş tek bir kayıt.
    Excel benzetmesi: Sınıf, bir "form şablonu"dur (alanları ve kuralları belli);
    her doldurulmuş form bir nesnedir.
      __init__   : nesne oluşturulurken çalışır; alanları doldurur
      self       : "bu nesnenin kendisi" (formun bu kopyası)
      nitelik    : nesnenin alanı (self.il, self.durum)
      metot      : nesneye ait fonksiyon (sikayet.sla_asildi_mi())
      __repr__   : nesne print edilince ne görüneceği
    Bu eğitimde class YAZMAK zorunlu değildir; amaç, hazır kodda gördüğünüzde OKUYABİLMEK.
    (Kalıtım vb. ileri konular kapsam dışıdır.)

NASIL ÇALIŞTIRILIR?
    python gun04/06_sikayet_sinifi.py

BEKLENEN ÇIKTI (kısaltılmış):
    Sikayet(no=10527, il='Ankara', kategori='Fatura', durum='Çözüldü', sure=10)
    Çözüldü mü? True
    SLA aşıldı mı (hedef 7)? True
    Nesneye dönüştürülen kayıt: 600
    ...
    Dataclass: SikayetDC(sikayet_no=10527, il='Ankara', kategori='Fatura', durum='Çözüldü', sure=10)
"""
import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Sikayet:
    """Bir şikâyet kaydı: veriler + o verilerle ilgili sorular (metotlar)."""

    def __init__(self, sikayet_no, il, kategori, durum, sure=None):
        # self.xxx = ... : nesnenin içine bir alan (nitelik) yerleştirir
        self.sikayet_no = sikayet_no
        self.il = il
        self.kategori = kategori
        self.durum = durum
        self.sure = sure                 # None = bilinmiyor (işlemdeki kayıt)

    def cozuldu_mu(self):
        """Metot: nesnenin kendi verisine bakarak cevap verir."""
        return self.durum == "Çözüldü"

    def sla_asildi_mi(self, hedef_gun):
        """Süre hedefi aştıysa True; süre bilinmiyorsa None."""
        if self.sure is None:
            return None
        return self.sure > hedef_gun

    def __repr__(self):
        # print(nesne) yazınca bu metin görünür. Olmasaydı:
        # <__main__.Sikayet object at 0x0000021F...> gibi anlamsız bir şey görürdük.
        return (f"Sikayet(no={self.sikayet_no}, il={self.il!r}, kategori={self.kategori!r}, "
                f"durum={self.durum!r}, sure={self.sure})")


# ---------------------------------------------------------------------------
# 1) Elle bir nesne oluşturmak
# ---------------------------------------------------------------------------
s = Sikayet(10527, "Ankara", "Fatura", "Çözüldü", 10)     # __init__ otomatik çalışır
print(s)                                                 # __repr__ çalışır
print("İl niteliği:", s.il)                              # nokta ile alana erişim
print("Çözüldü mü?", s.cozuldu_mu())                     # nokta ile metot çağrısı
print("SLA aşıldı mı (hedef 7)?", s.sla_asildi_mi(7))

# ---------------------------------------------------------------------------
# 2) CSV satırlarını nesnelere dönüştürmek
# ---------------------------------------------------------------------------
def satirdan_sikayet(satir):
    """CSV sözlüğünü Sikayet nesnesine çevirir (tür dönüşümü burada yapılır)."""
    sure = int(satir["cozum_suresi_gun"]) if satir["cozum_suresi_gun"] else None
    return Sikayet(int(satir["sikayet_no"]), satir["il"], satir["kategori"], satir["durum"], sure)


with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as f:
    nesneler = [satirdan_sikayet(satir) for satir in csv.DictReader(f)]
print("Nesneye dönüştürülen kayıt:", len(nesneler))
print("İlk üç:", nesneler[:3])

# Sözlükle: kayit["durum"] == "Çözüldü"   |   Nesneyle: kayit.cozuldu_mu()
# Kural tek yerde (sınıfın içinde) yazıldığı için değişirse tek yerde düzeltilir.
cozulen = [n for n in nesneler if n.cozuldu_mu()]
print("Çözülen:", len(cozulen))

HEDEFLER = {"Fatura": 7, "İnternet Hızı": 10, "Kesinti": 5,
            "Taahhüt/İptal": 15, "Numara Taşıma": 3, "Kapsama": 20}
asan = [n for n in cozulen if n.sla_asildi_mi(HEDEFLER[n.kategori])]
print("Hedefi aşan çözülmüş şikâyet:", len(asan))


# ---------------------------------------------------------------------------
# 3) Kısa yol: dataclass (aynı şeyi daha az kodla)
# ---------------------------------------------------------------------------
# @dataclass, __init__ ve __repr__ metotlarını bizim yerimize yazar.
# Sadece alan adlarını ve türlerini (ipucu olarak) yazmak yeterli.
@dataclass
class SikayetDC:
    sikayet_no: int
    il: str
    kategori: str
    durum: str
    sure: int | None = None          # varsayılan değer: None

    def cozuldu_mu(self):
        return self.durum == "Çözüldü"


d = SikayetDC(10527, "Ankara", "Fatura", "Çözüldü", 10)
print("Dataclass:", d)
print("Aynı mı? (alan alan karşılaştırma)", d == SikayetDC(10527, "Ankara", "Fatura", "Çözüldü", 10))
# Not: Türler (int, str) sadece ipucudur; Python bunları zorla kontrol ETMEZ.
