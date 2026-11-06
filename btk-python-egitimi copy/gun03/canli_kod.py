import yardimcilar

kayitlar = yardimcilar.csv_oku('basvurular.csv')
toplam_islem_suresi = 0

for kayit in kayitlar:
    toplam_islem_suresi += yardimcilar.sayiya_cevir(kayit['islem_suresi'])

print(toplam_islem_suresi)