# -*- coding: utf-8 -*-
"""Küçük .xlsx okuyucu — yalnızca standart kütüphane (zipfile + XML).

Bu bir YARDIMCI modüldür (numarasız): 17_xlsx_standart.py ve
19_karne_standart.py bunu `from xlsx_mini import sayfa_oku` ile kullanır.
Satır satır anlamanız gerekmez; "kara kutu" olarak kullanmak yeterlidir.
Merak eden için: .xlsx dosyası aslında bir ZIP arşividir; içinde her sayfa
için bir XML (metin) dosyası vardır. Arşivi açıp hücreleri okuyoruz.

Sınırlar (bilerek basit tutuldu):
    - Formüllerin yalnızca SON KAYDEDİLMİŞ değerini okur, formülü hesaplamaz.
    - Excel'in tarih olarak biçimlediği hücreler sayı (seri no) gelir;
      eğitim dosyamızda tarihler metin olduğu için sorun olmaz.
    - Biçim, renk, birleştirilmiş hücre bilgisi okunmaz.

Doğrudan çalıştırılırsa eğitim dosyasının sayfa adlarını yazar:
    python gun05/xlsx_mini.py
"""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Excel XML dosyalarındaki etiketlerin "ad alanları" (uzun ön ekler).
ANA = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
ILISKI = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PAKET = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _sutun_no(hucre_adresi):
    """'C12' -> 2 (A=0, B=1, C=2 ...). Boş hücreleri atlayan satırlar için gerekli."""
    no = 0
    for harf in hucre_adresi:
        if not harf.isalpha():
            break
        no = no * 26 + (ord(harf.upper()) - ord("A") + 1)
    return no - 1


def _sayiya_cevir(metin):
    """'7' -> 7, '2404.26' -> 2404.26 (Excel sayıları XML'de nokta ile yazar)."""
    sayi = float(metin)
    return int(sayi) if sayi.is_integer() else sayi


def _sayfa_yollari(arsiv):
    """{'Sikayetler': 'xl/worksheets/sheet1.xml', ...} sözlüğünü döndürür."""
    kitap = ET.fromstring(arsiv.read("xl/workbook.xml"))
    iliskiler = ET.fromstring(arsiv.read("xl/_rels/workbook.xml.rels"))
    hedefler = {r.get("Id"): r.get("Target") for r in iliskiler.iter(PAKET + "Relationship")}
    yollar = {}
    for sayfa in kitap.iter(ANA + "sheet"):
        hedef = hedefler[sayfa.get(ILISKI + "id")]
        # Hedef "/xl/worksheets/sheet1.xml" (mutlak) ya da "worksheets/sheet1.xml" olabilir.
        yollar[sayfa.get("name")] = hedef.lstrip("/") if hedef.startswith("/") else "xl/" + hedef
    return yollar


def sayfa_adlari(dosya_yolu):
    """Çalışma kitabındaki sayfa adlarını sırasıyla döndürür."""
    with zipfile.ZipFile(dosya_yolu) as arsiv:
        return list(_sayfa_yollari(arsiv))


def sayfa_oku(dosya_yolu, sayfa_adi):
    """Bir sayfayı csv.DictReader gibi sözlük listesi olarak döndürür.

    İlk satır başlıktır. Boş hücre -> None, sayı -> int/float, metin -> str.
    """
    with zipfile.ZipFile(dosya_yolu) as arsiv:
        yollar = _sayfa_yollari(arsiv)
        if sayfa_adi not in yollar:
            raise KeyError(f"'{sayfa_adi}' sayfası yok. Var olanlar: {list(yollar)}")
        # Excel'in kendi kaydettiği dosyalarda metinler ortak bir listede durur
        # (sharedStrings.xml). Bazı programlar metni hücreye gömer (inlineStr).
        ortak_metinler = []
        if "xl/sharedStrings.xml" in arsiv.namelist():
            kok = ET.fromstring(arsiv.read("xl/sharedStrings.xml"))
            for si in kok.iter(ANA + "si"):
                ortak_metinler.append("".join(t.text or "" for t in si.iter(ANA + "t")))
        sayfa = ET.fromstring(arsiv.read(yollar[sayfa_adi]))

    satirlar = []
    for satir in sayfa.iter(ANA + "row"):
        degerler = {}
        for hucre in satir.iter(ANA + "c"):
            tip = hucre.get("t")
            v = hucre.find(ANA + "v")
            if tip == "inlineStr":
                deger = "".join(t.text or "" for t in hucre.iter(ANA + "t"))
            elif v is None or v.text is None:
                deger = None
            elif tip == "s":
                deger = ortak_metinler[int(v.text)]
            elif tip in ("str", "e"):        # formül metni sonucu / hata (#YOK vb.)
                deger = v.text
            elif tip == "b":
                deger = v.text == "1"
            else:                            # sayı
                deger = _sayiya_cevir(v.text)
            degerler[_sutun_no(hucre.get("r"))] = deger
        if degerler:
            genislik = max(degerler) + 1
            satirlar.append([degerler.get(i) for i in range(genislik)])

    if not satirlar:
        return []
    basliklar = satirlar[0]
    return [{b: (s[i] if i < len(s) else None) for i, b in enumerate(basliklar)}
            for s in satirlar[1:]]


if __name__ == "__main__":
    ornek = Path(__file__).resolve().parents[1] / "data" / "btk_ornek_veri.xlsx"
    print("Sayfalar:", sayfa_adlari(ornek))
    print("Hedefler:", sayfa_oku(ornek, "Hedefler"))
