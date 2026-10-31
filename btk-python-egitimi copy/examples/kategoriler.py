sikayetler = [
    "İnternetim akşamları çok yavaş, hız testinde 5 Mbps görüyorum.",
    "Faturama haberim olmadan ek paket eklenmiş, faturamı itiraz ediyorum.",
    "Bağlantı sürekli kopuyor, modem ışıkları yanıp sönüyor.",
    "Aboneliğimi iptal etmek istiyorum ama cayma bedeli çıkarıyorlar.",
    "Evde çekmiyor, şebeke yok, aramalar kopuyor.",
    "İnternet hızı taahhüt edilenin yarısı bile değil, fatura da yüksek.",
    "İptal başvurumu üç kez yaptım, hâlâ fatura geliyor.",
    "Müşteri hizmetlerine ulaşamıyorum, saatlerce bekletiyorlar.",
]

anahtar = {
    "Hız":     ["yavaş", "hız", "mbps", "taahhüt"],
    "Fatura":  ["fatura", "ücret", "paket", "itiraz"],
    "Kesinti": ["kopuyor", "bağlantı", "modem", "çekmiyor", "şebeke"],
    "İptal":   ["iptal", "cayma", "abonelik"],
}

NOKTALAMA = '.,!?;:()"'

sonuc = []

for sikayet in sikayetler:
    # 1) Türkçe küçük harfe çevir.
    #    lower() Türkçeyi bilmez: "İ" -> "i̇" (noktalı), "I" -> "i" olur.
    #    Bu yüzden bu iki harfi önce kendimiz çeviriyoruz.
    metin = sikayet.replace("İ", "i").replace("I", "ı").lower()

    # 2) Noktalama işaretlerini boşluğa çevir: "yavaş," -> "yavaş "
    for isaret in NOKTALAMA:
        metin = metin.replace(isaret, " ")

    # 3) Her kategori 0 puanla başlar. Kategoriler sözlükten okunur,
    #    böylece sözlüğe yeni kategori eklenince kod değişmez.
    puan = {kategori: 0 for kategori in anahtar}

    # 4) Her kelime, kendisiyle başlayan her kök için 1 puan kazandırır.
    #    split() boşluklara göre böler; tekrar eden kelime yeniden sayılır.
    for kelime in metin.split():
        for kategori, kokler in anahtar.items():
            for kok in kokler:
                if kelime.startswith(kok):
                    puan[kategori] += 1

    # 5) En yüksek puanı bul; hiç puan yoksa "Diğer".
    en_yuksek = max(puan.values(), default=0)
    if en_yuksek == 0:
        sonuc.append("Diğer")
    else:
        # Beraberlikte en yüksek puanı alan tüm kategoriler yazılır.
        kazananlar = [kategori for kategori, p in puan.items() if p == en_yuksek]
        sonuc.append(", ".join(kazananlar))

for sikayet, kategori in zip(sikayetler, sonuc):
    print(f"{kategori:<15} | {sikayet}")




NOKTALAMA = str.maketrans({isaret: " " for isaret in '.,!?;:()"'})

# Ters sözlük: kök -> kategori. Bir kelimenin her ön ekine sözlükte bakmak,
# tüm kökleri tek tek denemekten çok daha hızlıdır.
kok_kategori = {kok: kategori for kategori, kokler in anahtar.items() for kok in kokler}

sonuc = []
for sikayet in sikayetler:
    metin = sikayet.replace("İ", "i").replace("I", "ı").lower().translate(NOKTALAMA)
    puan = dict.fromkeys(anahtar, 0)
    for kelime in metin.split():
        for uzunluk in range(1, len(kelime) + 1):
            kategori = kok_kategori.get(kelime[:uzunluk])
            if kategori:
                puan[kategori] += 1
    en_yuksek = max(puan.values(), default=0)
    sonuc.append(", ".join(k for k, p in puan.items() if p == en_yuksek) if en_yuksek else "Diğer")