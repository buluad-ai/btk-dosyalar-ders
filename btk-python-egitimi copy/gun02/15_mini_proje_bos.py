# -*- coding: utf-8 -*-
"""GÜN 2 MİNİ PROJE — İSKELET (öğrenci doldurur).

Görev: TODO'ları sırayla doldurun. Dosya şu hâliyle de HATASIZ çalışır;
her TODO'yu tamamladıkça çıktıdaki 0 / boş değerler gerçek sonuçlara döner.
Takılırsanız: 15_mini_proje.py (tamamlanmış hâl). Önce kendiniz deneyin!

Doğru doldurulursa beklenen sonuçlar (elle kontrol için):
    Toplam şikâyet: 15
    İl sayımı: İstanbul 5, Ankara 3, Antalya 2, İzmir 2, Erzurum 2, Konya 1
    En uzun süren: 10520, 17 gün
    Hedef aşan: 5 / 12

Nasıl çalıştırılır:
    py gun02/15_mini_proje_bos.py

Beklenen çıktı (doldurmadan önce, son satır):
    İskelet çalıştı. TODO sayısı: 5
"""

sikayetler = [
    {"no": 10507, "il": "İstanbul", "kategori": "Kesinti",       "durum": "Reddedildi", "sure": 7},
    {"no": 10527, "il": "Ankara",   "kategori": "Fatura",        "durum": "Çözüldü",    "sure": 10},
    {"no": 10550, "il": "Antalya",  "kategori": "İnternet Hızı", "durum": "İşlemde",    "sure": None},
    {"no": 10045, "il": "Konya",    "kategori": "Fatura",        "durum": "Çözüldü",    "sure": 3},
    {"no": 10076, "il": "İstanbul", "kategori": "İnternet Hızı", "durum": "Çözüldü",    "sure": 8},
    {"no": 10416, "il": "İstanbul", "kategori": "Taahhüt/İptal", "durum": "Çözüldü",    "sure": 11},
    {"no": 10253, "il": "İzmir",    "kategori": "Kapsama",       "durum": "Çözüldü",    "sure": 15},
    {"no": 10290, "il": "Erzurum",  "kategori": "Numara Taşıma", "durum": "Çözüldü",    "sure": 2},
    {"no": 10331, "il": "Ankara",   "kategori": "İnternet Hızı", "durum": "İşlemde",    "sure": None},
    {"no": 10477, "il": "Antalya",  "kategori": "Fatura",        "durum": "Çözüldü",    "sure": 2},
    {"no": 10586, "il": "İzmir",    "kategori": "Numara Taşıma", "durum": "Çözüldü",    "sure": 8},
    {"no": 10530, "il": "Erzurum",  "kategori": "Taahhüt/İptal", "durum": "Çözüldü",    "sure": 13},
    {"no": 10042, "il": "İstanbul", "kategori": "Fatura",        "durum": "İşlemde",    "sure": None},
    {"no": 10520, "il": "İstanbul", "kategori": "Taahhüt/İptal", "durum": "Çözüldü",    "sure": 17},
    {"no": 10567, "il": "Ankara",   "kategori": "İnternet Hızı", "durum": "Çözüldü",    "sure": 11},
]
hedefler = {"Fatura": 7, "İnternet Hızı": 10, "Kesinti": 5,
            "Taahhüt/İptal": 15, "Numara Taşıma": 3, "Kapsama": 20}

# TODO 1: toplam şikâyet sayısını bulun  (ipucu: len)
toplam = 0
print("Toplam şikâyet:", toplam)

# TODO 2: il bazında sayın. Boş sözlükle başlayın; her satırda
#         il_sayim[il] = il_sayim.get(il, 0) + 1
il_sayim = {}
for s in sikayetler:
    pass            # pass = "şimdilik bir şey yapma". Bu satırı silip kodunuzu yazın.
print("İl sayımı:", il_sayim)

# TODO 3: en uzun süren şikâyeti bulun. sure None ise continue ile atlayın.
en_uzun_no = None
en_uzun_sure = 0
for s in sikayetler:
    pass
print("En uzun süren:", en_uzun_no, en_uzun_sure, "gün")

# TODO 4: hedefi aşanları sayın. hedef = hedefler[s["kategori"]]
#         Süresi olan (None olmayan) kayıtları da ayrıca sayın.
asan_sayisi = 0
sonuclanan = 0
for s in sikayetler:
    pass
print(f"Hedef aşan: {asan_sayisi} / {sonuclanan}")

# TODO 5: aşım oranını yüzde olarak yazdırın. DİKKAT: sonuclanan 0 iken
#         bölme ZeroDivisionError verir; if ile koruyun.
if sonuclanan > 0:
    print(f"Oran: %{asan_sayisi / sonuclanan * 100:.1f}")
else:
    print("Oran: hesaplanamadı (sonuçlanmış kayıt yok)")

print("İskelet çalıştı. TODO sayısı: 5")
