# -*- coding: utf-8 -*-
"""Fonksiyonlar 2: parametre, varsayılan değer, return ve print farkı, çoklu dönüş, docstring.

NE ÖĞRETİYOR?
    - def ile kendi "formülümüzü" tanımlamak (Excel'deki LAMBDA / kendi formülünüz gibi)
    - Varsayılan parametre: oran=0.20 -> verilmezse 0.20 kullanılır
    - İsimli (keyword) argüman: kdv_ekle(100, oran=0.10)
    - return ile print arasındaki fark (en sık karışan konu!)
    - Birden çok değer döndürme ve "paket açma" (net, kdv = ...)
    - Docstring: fonksiyonun kullanım kılavuzu

NASIL ÇALIŞTIRILIR?
    python gun03/05_fonksiyon_parametreleri.py

BEKLENEN ÇIKTI (kısaltılmış):
    KDV dahil: 1200.00 TL
    %10 KDV ile: 110.00 TL
    ...
    Net: 1000.0 TL, KDV: 200.0 TL
    SLA aşıldı mı (12 gün, hedef 10): True
    Hız yüzdesi: 59.6
"""


# ---------------------------------------------------------------------------
# 1) En basit iş fonksiyonu: KDV ekleme
# ---------------------------------------------------------------------------
# def      -> "tanımla" (define)
# kdv_ekle -> fonksiyonun adı (küçük harf, kelimeler alt çizgiyle)
# tutar    -> zorunlu parametre (çağırırken mutlaka verilmeli)
# oran=0.20-> VARSAYILAN parametre: verilmezse 0.20 kabul edilir
def kdv_ekle(tutar, oran=0.20):
    """KDV hariç tutara KDV ekler ve kuruşa yuvarlar.

    Örnek: kdv_ekle(1000) -> 1200.0
           kdv_ekle(1000, oran=0.10) -> 1100.0
    """
    sonuc = tutar * (1 + oran)
    return round(sonuc, 2)   # return: sonucu ÇAĞIRAN YERE geri verir


# Çağırma: fonksiyon adı + parantez + değerler
kdv_dahil = kdv_ekle(1000)                       # oran verilmedi -> 0.20
print(f"KDV dahil: {kdv_dahil:.2f} TL")          # :.2f -> virgülden sonra 2 hane

# Varsayılanı değiştirmek için isimli (keyword) argüman kullanmak en okunaklısı:
print(f"%10 KDV ile: {kdv_ekle(100, oran=0.10):.2f} TL")

# Aynı fonksiyonu bir liste üzerinde tekrar kullanmak (fonksiyonun asıl faydası):
itiraz_tutarlari = [2404.26, 1952.36, 826.66]
for tutar in itiraz_tutarlari:
    print(f"  {tutar:>8.2f} TL -> KDV dahil {kdv_ekle(tutar):>8.2f} TL")


# ---------------------------------------------------------------------------
# 2) return ile print FARKI
# ---------------------------------------------------------------------------
# print sadece ekrana yazar; değeri "elinize" vermez.
# return değeri verir; onu bir değişkene koyabilir, hesaba katabilirsiniz.
def kdv_yazdir(tutar):
    """YANLIŞ ÖRNEK: hesaplar, ekrana yazar ama hiçbir şey döndürmez."""
    print("  (fonksiyon içinden print)", round(tutar * 1.2, 2))
    # return yok -> Python otomatik olarak None döndürür


deger = kdv_yazdir(100)                 # ekranda bir şey görürüz ...
print("kdv_yazdir'in döndürdüğü:", deger)   # ... ama elimizdeki değer None!
# deger + 5 yazsaydık: TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
# Excel benzetmesi: print, hücreye bakıp gözle okumak; return, sonucu başka
# bir formülde kullanılabilen hücre değeridir.


# ---------------------------------------------------------------------------
# 3) Birden çok değer döndürmek
# ---------------------------------------------------------------------------
def kdv_ayir(kdv_dahil_tutar, oran=0.20):
    """KDV dahil tutardan net tutar ve KDV'yi ayırır. İKİ değer döndürür."""
    net = round(kdv_dahil_tutar / (1 + oran), 2)
    kdv = round(kdv_dahil_tutar - net, 2)
    return net, kdv


net, kdv = kdv_ayir(1200)       # "paket açma": ilk değer net'e, ikinci kdv'ye
print(f"Net: {net} TL, KDV: {kdv} TL")


def sure_ozeti(sureler):
    """Süre listesinin en küçüğünü, en büyüğünü ve ortalamasını döndürür."""
    if not sureler:                       # boş liste -> hepsi bilinmiyor
        return None, None, None
    return min(sureler), max(sureler), round(sum(sureler) / len(sureler), 2)


en_az, en_cok, ort = sure_ozeti([7, 10, 3, 8, 11])
print(f"Süre özeti -> en az: {en_az}, en çok: {en_cok}, ortalama: {ort}")
print("Boş liste özeti:", sure_ozeti([]))


# ---------------------------------------------------------------------------
# 4) Telekom iş fonksiyonları: SLA kontrolü ve hız yüzdesi
# ---------------------------------------------------------------------------
def sla_asildi_mi(sure_gun, hedef_gun=10):
    """Çözüm süresi hedefi aştıysa True. Süre bilinmiyorsa None."""
    if sure_gun is None:
        return None
    return sure_gun > hedef_gun           # karşılaştırmanın sonucu zaten True/False


def hiz_yuzdesi(olculen_mbps, paket_mbps):
    """Ölçülen hız, paket hızının yüzde kaçı? (1 ondalık)"""
    return round(100 * olculen_mbps / paket_mbps, 1)


print("SLA aşıldı mı (12 gün, hedef 10):", sla_asildi_mi(12))
print("SLA aşıldı mı (4 gün, hedef 3):", sla_asildi_mi(4, hedef_gun=3))
print("SLA aşıldı mı (süre yok):", sla_asildi_mi(None))
print("Hız yüzdesi:", hiz_yuzdesi(29.8, 50))    # 50 Mbps pakette 29.8 ölçüldü

# Parametre SIRASI önemlidir: hiz_yuzdesi(50, 29.8) yazarsak 167.8 çıkar (yanlış!).
# İsimle çağırırsak sıra karışmaz:
print("İsimle çağrı:", hiz_yuzdesi(paket_mbps=50, olculen_mbps=29.8))


# ---------------------------------------------------------------------------
# 5) Docstring: fonksiyonun kullanım kılavuzu
# ---------------------------------------------------------------------------
# Üç tırnak içindeki ilk metin "docstring"dir. VS Code'da fonksiyon adının
# üzerine fareyi getirince bu metin görünür. Kod içinden de okunabilir:
print("kdv_ekle ne yapar? ->", kdv_ekle.__doc__.splitlines()[0])
# help(kdv_ekle)  # <- açarsanız tüm docstring'i biçimli gösterir
