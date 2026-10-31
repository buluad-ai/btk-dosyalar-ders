tablo = [
    {"hedef":14, "sure": 10, "sehir": "Ankara", "cozum": True, "kategori": "Fatura"}, 
    {"hedef":25, "sure": 30, "sehir": "Ankara", "cozum": True, "kategori": "Bağlantı"}, 
    {"hedef":18, "sure": 18, "sehir": "Ankara", "cozum": True, "kategori": "Kesinti"}, 
    {"hedef":21, "sure": 31, "sehir": "İstanbul", "cozum": True, "kategori":"Bağlantı"}, 
    {"hedef":14, "sure": 9, "sehir": "Konya", "cozum": True, "kategori": "Kesinti"},
    {"hedef":24, "sure": 15, "sehir": "Ankara", "cozum": True, "kategori": "Kesinti"}
]
sayim = {}
for satir in tablo:
    if satir["cozum"] and satir["sure"] <= satir["hedef"] and satir["kategori"] == "Kesinti":
        sehir = satir["sehir"]
        sure = satir["sure"]

        if sehir in sayim:
            if sure < sayim[sehir]:
                sayim[sehir] = sure
        else:
            sayim[sehir] = sure

en_kisa_sehir = None
en_kisa_sure = None

for sehir in sayim:
    if en_kisa_sure is None or sayim[sehir] < en_kisa_sure:
        en_kisa_sehir = sehir
        en_kisa_sure = sayim[sehir]

print((en_kisa_sehir, en_kisa_sure))





en_iyi = min((s for s in tablo if s["cozum"] and s["sure"] < s["hedef"] and s["kategori"] == "Kesinti"), key=lambda s: s["sure"])
print(en_iyi)
print((en_iyi["sehir"], en_iyi["sure"]))