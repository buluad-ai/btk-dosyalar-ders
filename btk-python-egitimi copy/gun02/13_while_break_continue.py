# -*- coding: utf-8 -*-
"""while (sınırlı kullanım), break ve continue.

Ne öğretiyor:
    - while koşul:  -> koşul True olduğu SÜRECE tekrar et.
      Kaç tur döneceğini bilmediğimiz durumlar için; veri analizinde nadirdir
      (çoğu zaman for yeterlidir).
    - Sonsuz döngü riski: koşulu değiştiren satırı unutmak. Takılırsa
      terminalde Ctrl + C ile durdurulur.
    - break    -> döngüden HEMEN çık (aradığını bulduysan dur).
    - continue -> bu turu ATLA, sıradaki elemana geç (geçersiz kaydı atla).

Nasıl çalıştırılır:
    py gun02/13_while_break_continue.py

Beklenen çıktı (seçme satırlar):
    3. ayda birikimli şikâyet 100'ü geçti: 112
    İlk hedef aşımı: 10527 (10 gün > 7)
    Sonuçlanmış 4 kaydın ortalama süresi: 5.75 gün
"""

# ---------------------------------------------------------------------------
# 1) while: "eşiğe ulaşana kadar" — kaç tur olacağı baştan belli değil
# ---------------------------------------------------------------------------
aylik_sikayet = [30, 35, 47, 52, 41, 38]   # Ocak..Haziran
birikimli = 0
ay = 0                                      # indeks olarak kullanacağız
while birikimli <= 100 and ay < len(aylik_sikayet):   # ikinci koşul: GÜVENLİK SINIRI
    birikimli += aylik_sikayet[ay]
    ay += 1                                 # BU SATIR OLMAZSA SONSUZ DÖNGÜ!
print(f"{ay}. ayda birikimli şikâyet 100'ü geçti: {birikimli}")

# Tekrar deneme kalıbı (ör. bağlantı denemesi) — azami deneme sayısıyla:
deneme = 1
AZAMI_DENEME = 3
basarili = False
while deneme <= AZAMI_DENEME and not basarili:
    print(f"  Bağlantı denemesi {deneme}...")
    basarili = deneme == 2          # kurgusal: 2. denemede bağlanıyor
    deneme += 1
print("  Bağlandı mı?", basarili)
print()

# ---------------------------------------------------------------------------
# 2) break: aradığını bulunca dur
# ---------------------------------------------------------------------------
hedefler = {"Fatura": 7, "Kesinti": 5, "İnternet Hızı": 10}
kayitlar = [
    (10550, "İnternet Hızı", None),   # (no, kategori, süre)  None = işlemde, süre yok
    (10527, "Fatura", 10),
    (10045, "Fatura", 3),
    (10076, "İnternet Hızı", 8),
    (10331, "İnternet Hızı", None),
    (10477, "Fatura", 2),
]
for no, kategori, sure in kayitlar:            # tuple açma, her turda
    if sure is not None and sure > hedefler[kategori]:
        print(f"İlk hedef aşımı: {no} ({sure} gün > {hedefler[kategori]})")
        break                                  # gerisine bakmaya gerek yok
print()

# ---------------------------------------------------------------------------
# 3) continue: geçersiz/eksik kaydı atla
# ---------------------------------------------------------------------------
toplam = 0
adet = 0
for no, kategori, sure in kayitlar:
    if sure is None:
        print(f"  {no}: süre yok (işlemde), atlandı")
        continue                               # aşağıdaki satırlar bu turda çalışmaz
    toplam += sure
    adet += 1
print(f"Sonuçlanmış {adet} kaydın ortalama süresi: {toplam / adet:.2f} gün")

# Aynı işi continue OLMADAN if ile de yazabilirdik:
#   for ...:
#       if sure is not None:
#           toplam += sure; adet += 1
# continue, koşullar çoğaldığında girintiyi azaltır; zorunlu değildir.

# SONSUZ DÖNGÜ ÖRNEĞİ (ÇALIŞTIRMAYIN):
#   sayac = 0
#   while sayac < 5:
#       print(sayac)        # sayac hiç artmıyor -> sonsuza dek 0 yazar
# Takılırsa: terminale tıklayın, Ctrl + C.
