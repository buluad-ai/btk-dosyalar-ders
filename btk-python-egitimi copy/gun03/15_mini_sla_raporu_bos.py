# -*- coding: utf-8 -*-
"""CANLI KODLAMA İSKELETİ: kategori bazında SLA raporu (öğrenci TODO'ları doldurur).

NE ÖĞRETİYOR?
    Günün tüm konularını birleştirir: modül import, fonksiyon, CSV okuma,
    boş hücre, sözlükle gruplama, CSV yazma.
    Tamamlanmış hâli: gun03/15_mini_sla_raporu.py (önce ona bakmayın!)

NASIL ÇALIŞTIRILIR?
    python gun03/15_mini_sla_raporu_bos.py
    Dosya bu hâliyle de HATASIZ çalışır; sadece eksik sonuç üretir.
    Her TODO'yu doldurdukça tekrar çalıştırın ve çıktının değişmesini izleyin.

BEKLENEN ÇIKTI (doldurulmadan önce):
    İskelet çalıştı: 600 kayıt okundu
    TODO: ...
"""
import csv
from pathlib import Path

import yardimcilar            # aynı klasördeki kendi modülümüz

ROOT = Path(__file__).resolve().parents[1]

# Kategori başına hedef çözüm süresi (gün). Gün 4'te bunu Excel'den okuyacağız.
HEDEFLER = {"Fatura": 7, "İnternet Hızı": 10, "Kesinti": 5,
            "Taahhüt/İptal": 15, "Numara Taşıma": 3, "Kapsama": 20}

kayitlar = yardimcilar.csv_oku("sikayetler.csv")
print("İskelet çalıştı:", len(kayitlar), "kayıt okundu")

# Her kategori için iki sayaç tutacağız: {"Fatura": {"cozulen": 0, "asan": 0}, ...}
ozet = {kategori: {"cozulen": 0, "asan": 0} for kategori in HEDEFLER}

for kayit in kayitlar:
    # TODO 1: Sadece "Çözüldü" durumundaki kayıtlarla ilgileniyoruz.
    #         Durum "Çözüldü" DEĞİLSE "continue" ile sonraki kayda geçin.

    # TODO 2: Süreyi sayıya çevirin. İpucu: yardimcilar.sayiya_cevir(..., int)
    sure = None

    # TODO 3: Kaydın kategorisinin hedefini HEDEFLER sözlüğünden alın.
    hedef = None

    # TODO 4: ozet[kategori]["cozulen"] sayacını 1 artırın.
    #         yardimcilar.sla_asildi_mi(sure, hedef) True ise "asan" sayacını da artırın.
    pass

# TODO 5: Her kategori için aşım oranını (%) hesaplayıp yazdırın.
#         Oran = 100 * asan / cozulen   (cozulen 0 ise bölmeyin!)
for kategori, sayac in ozet.items():
    print(f"  {kategori:<15} çözülen={sayac['cozulen']:>3}  aşan={sayac['asan']:>3}")

# TODO 6: Sonucu outputs/gun03/sla_raporu.csv dosyasına yazın
#         (sütunlar: kategori, hedef_gun, cozulen, asan, asim_orani).
#         İpucu: 11_csv_filtrele_yaz.py dosyasındaki DictWriter örneği.
print("TODO: 1-6 arası adımları doldurun; sonra 15_mini_sla_raporu.py ile karşılaştırın.")
