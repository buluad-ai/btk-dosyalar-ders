# -*- coding: utf-8 -*-
"""B PLANI yardımcısı: paketsiz basit .xlsx OKUMA ve YAZMA (yalnızca standart kütüphane).

NE ÖĞRETİYOR?
    Bu dosyayı satır satır anlamanız GEREKMEZ; "hazır alet" olarak kullanılır.
    Bilmeniz gereken tek gerçek: bir .xlsx dosyası aslında bir ZIP arşividir.
    İçinde her sayfa için bir XML (metin) dosyası vardır. Python'un zipfile ve
    xml modülleri bu dosyaları açıp okuyabilir/yazabilir. pandas+openpyxl yoksa
    bile Excel dosyası okuyup Excel'de açılan özet dosyası üretebiliriz.
    (Deneyin: bir .xlsx dosyasının kopyasının uzantısını .zip yapıp açın.)

    Kullanım:
        from basit_xlsx import xlsx_oku, xlsx_yaz
        satirlar = xlsx_oku(dosya_yolu, "Hedefler")   # [{"kategori": "Fatura", "hedef_gun": 7}, ...]
        xlsx_yaz(cikti_yolu, {"Özet": [["Başlık", "Değer"], ["Toplam", 600]]})

    SINIRLAR (dürüst olalım): biçim, formül, birleştirilmiş hücre, tarih biçimi
    desteklenmez. Excel'de tarih hücresi olarak kaydedilmiş bir değer sayı
    (ör. 46023) olarak gelir. Bu eğitimdeki dosyalarda tarihler metindir.

NASIL ÇALIŞTIRILIR? (kendi kendini dener)
    python gun07/basit_xlsx.py

BEKLENEN ÇIKTI:
    Hedefler sayfası: 6 satır
    basit_xlsx deneme: yaz-oku tutarlı
"""
import re
import zipfile
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
# Excel XML dosyalarındaki "ad alanı" (namespace). Etiket adlarının önüne eklenir.
ANA = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _sutun_no(hucre_adresi):
    """"C12" -> 2 (A=0, B=1, C=2 ... Z=25, AA=26)."""
    harfler = re.match(r"[A-Z]+", hucre_adresi).group()
    no = 0
    for harf in harfler:
        no = no * 26 + (ord(harf) - ord("A") + 1)
    return no - 1


def _sayiya_cevir(metin):
    """Excel sayıları metin olarak saklar: "7" -> 7, "2404.26" -> 2404.26."""
    sayi = float(metin)
    return int(sayi) if sayi.is_integer() and "." not in metin and "E" not in metin.upper() else sayi


def xlsx_oku(dosya_yolu, sayfa_adi):
    """Bir sayfayı okur; ilk satırı başlık kabul edip sözlük listesi döndürür.

    Boş hücreler None olur (CSV'deki boş metin "" yerine).
    """
    with zipfile.ZipFile(dosya_yolu) as arsiv:
        # 1) Sayfa adı -> sayfa dosyası eşleşmesini bul (workbook.xml + ilişkiler dosyası)
        kitap = ET.fromstring(arsiv.read("xl/workbook.xml"))
        iliskiler = ET.fromstring(arsiv.read("xl/_rels/workbook.xml.rels"))
        hedefler = {r.get("Id"): r.get("Target") for r in iliskiler.iter(PKG + "Relationship")}
        sayfa_dosyasi = None
        for sayfa in kitap.iter(ANA + "sheet"):
            if sayfa.get("name") == sayfa_adi:
                hedef = hedefler[sayfa.get(REL + "id")]
                # Hedef "/xl/worksheets/sheet1.xml" veya "worksheets/sheet1.xml" olabilir
                sayfa_dosyasi = hedef.lstrip("/") if hedef.startswith("/") else "xl/" + hedef
        if sayfa_dosyasi is None:
            raise KeyError(f"'{sayfa_adi}' adlı sayfa yok")

        # 2) Ortak metin tablosu: Excel tekrar eden metinleri bir kez saklar, hücrede sıra no tutar
        ortak_metinler = []
        if "xl/sharedStrings.xml" in arsiv.namelist():
            for si in ET.fromstring(arsiv.read("xl/sharedStrings.xml")).iter(ANA + "si"):
                ortak_metinler.append("".join(t.text or "" for t in si.iter(ANA + "t")))

        # 3) Hücreleri satır satır oku
        tablo = []
        for satir in ET.fromstring(arsiv.read(sayfa_dosyasi)).iter(ANA + "row"):
            degerler = {}
            for hucre in satir.iter(ANA + "c"):
                tur = hucre.get("t")
                v = hucre.find(ANA + "v")
                if tur == "inlineStr":
                    deger = "".join(t.text or "" for t in hucre.iter(ANA + "t"))
                elif v is None or v.text is None:
                    deger = None
                elif tur == "s":
                    deger = ortak_metinler[int(v.text)]
                elif tur in ("str", "e"):
                    deger = v.text
                elif tur == "b":
                    deger = v.text == "1"
                else:
                    deger = _sayiya_cevir(v.text)
                degerler[_sutun_no(hucre.get("r"))] = deger
            tablo.append(degerler)

    if not tablo:
        return []
    basliklar = tablo[0]
    return [{basliklar[i]: satir.get(i) for i in basliklar} for satir in tablo[1:]]


def _sutun_harfi(no):
    """0 -> "A", 26 -> "AA"."""
    harf = ""
    no += 1
    while no:
        no, kalan = divmod(no - 1, 26)
        harf = chr(ord("A") + kalan) + harf
    return harf


def _sayfa_xml(satirlar):
    parcalar = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                f'<worksheet xmlns="{ANA[1:-1]}"><sheetData>']
    for r, satir in enumerate(satirlar, start=1):
        parcalar.append(f'<row r="{r}">')
        for c, deger in enumerate(satir):
            adres = f"{_sutun_harfi(c)}{r}"
            stil = ' s="1"' if r == 1 else ""          # ilk satır kalın (stil 1)
            if deger is None or deger == "":
                continue
            if isinstance(deger, (int, float)) and not isinstance(deger, bool):
                parcalar.append(f'<c r="{adres}"{stil}><v>{deger}</v></c>')
            else:
                parcalar.append(f'<c r="{adres}" t="inlineStr"{stil}><is><t>{escape(str(deger))}</t></is></c>')
        parcalar.append("</row>")
    parcalar.append("</sheetData></worksheet>")
    return "".join(parcalar)


def xlsx_yaz(dosya_yolu, sayfalar):
    """sayfalar: {"Sayfa adı": [[başlık1, başlık2], [değer, değer], ...], ...}

    Excel'de açılabilen, çok sayfalı, ilk satırı kalın bir .xlsx dosyası yazar.
    Sayfa adları en fazla 31 karakter olmalı ve : \\ / ? * [ ] içermemeli (Excel kuralı).
    """
    adlar = list(sayfalar)
    icerik_turleri = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
        f'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(1, len(adlar) + 1))
    dosyalar = {
        "[Content_Types].xml":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            + icerik_turleri + "</Types>",
        "_rels/.rels":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>",
        "xl/workbook.xml":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<workbook xmlns="{ANA[1:-1]}" xmlns:r="{REL[1:-1]}"><sheets>'
            + "".join(f'<sheet name="{escape(ad)}" sheetId="{i}" r:id="rId{i}"/>' for i, ad in enumerate(adlar, 1))
            + "</sheets></workbook>",
        "xl/_rels/workbook.xml.rels":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                      f'Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(adlar) + 1))
            + f'<Relationship Id="rId{len(adlar) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            "</Relationships>",
        "xl/styles.xml":   # 2 yazı tipi: normal ve kalın; 2 hücre stili: 0=normal, 1=kalın
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<styleSheet xmlns="{ANA[1:-1]}">'
            '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
            '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
            '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
            '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
            "</styleSheet>",
    }
    for i, ad in enumerate(adlar, 1):
        dosyalar[f"xl/worksheets/sheet{i}.xml"] = _sayfa_xml(sayfalar[ad])
    with zipfile.ZipFile(dosya_yolu, "w", zipfile.ZIP_DEFLATED) as arsiv:
        for ad, metin in dosyalar.items():
            arsiv.writestr(ad, metin.encode("utf-8"))


if __name__ == "__main__":
    hedefler = xlsx_oku(ROOT / "data" / "btk_ornek_veri.xlsx", "Hedefler")
    print(f"Hedefler sayfası: {len(hedefler)} satır")
    for satir in hedefler:
        print(f"  {satir['kategori']:<14} hedef {satir['hedef_gun']} gün")
    # Yaz -> geri oku -> aynı mı?
    cikti = ROOT / "outputs" / "gun07"
    cikti.mkdir(parents=True, exist_ok=True)
    deneme = cikti / "basit_xlsx_deneme.xlsx"
    xlsx_yaz(deneme, {"Deneme": [["ad", "değer"], ["Çözüldü", 415], ["Oran", 69.2]]})
    geri = xlsx_oku(deneme, "Deneme")
    assert geri == [{"ad": "Çözüldü", "değer": 415}, {"ad": "Oran", "değer": 69.2}], geri
    print("basit_xlsx deneme: yaz-oku tutarlı")
