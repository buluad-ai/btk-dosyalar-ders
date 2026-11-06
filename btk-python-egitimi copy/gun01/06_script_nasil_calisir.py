# -*- coding: utf-8 -*-
"""Script nasıl çalışır: yukarıdan aşağı, satır satır. print() ve yorum satırı.

Ne öğretiyor:
    - Python dosyayı EN ÜSTTEN başlar, her satırı sırayla bir kez çalıştırır.
    - Yorum satırı (#) ve docstring (üç tırnak) çalıştırılmaz; insan içindir.
    - print() ile birden çok değer, sep= ve end= kullanımı, boş satır.
    - Çalıştırmanın üç yolu (aşağıda).

Nasıl çalıştırılır:
    1) VS Code: dosyayı açın -> sağ üstteki üçgen -> "Run Python File".
       (Kısayol yoksa: sağ tık -> "Run Python File in Terminal".)
    2) Terminal, Windows:  py gun01/06_script_nasil_calisir.py
       (Kurum kurulumunda "py" yoksa "python" deneyin.)
    3) Terminal, macOS/Linux:  python3 gun01/06_script_nasil_calisir.py

Beklenen çıktı (ilk ve son satırlar):
    Adım 1: dosyanın en üstü
    ...
    Adım 5: dosyanın sonu
"""

# Bu satır bir YORUMDUR. Python # işaretinden sonrasını görmez.
# Yorumları "neden böyle yaptım?" sorusunu cevaplamak için yazarız.

print("Adım 1: dosyanın en üstü")

# Bir değişken tanımlıyoruz. Bu satır EKRANA BİR ŞEY YAZMAZ;
# sadece "il" adlı kutuya "Ankara" metnini koyar.
il = "Ankara"

print("Adım 2: il değişkeni şu an:", il)

# Değişkeni değiştiriyoruz. Bundan SONRAKİ satırlar yeni değeri görür.
# Yukarıda çalışmış olan print geri dönüp değişmez — sıra önemlidir.
il = "İzmir"
print("Adım 3: il değişkeni artık:", il)

# --- print() fonksiyonunun birkaç özelliği ---
# Virgülle ayrılmış değerleri araya bir boşluk koyarak yazar:
print("Şikâyet", "sayısı", 36)
# sep= ayırıcıyı değiştirir (Excel'de METİNBİRLEŞTİR'deki ayraç gibi):
print("2026", "10", "14", sep="-")
# end= satır sonunu değiştirir; varsayılan "\n" (yeni satır):
print("Yükleniyor", end="...")
print("tamam")
# Hiçbir şey vermezseniz boş bir satır basar:
print()

# Aşağıdaki satır yorum olduğu için ÇALIŞMAZ. Başındaki # işaretini
# silip kaydedin ve tekrar çalıştırın: çıktıda yeni bir satır belirecek.
# print("Gizli satır: yorumdan çıkarıldım!")

print("Adım 4: hesap yapalım:", 12 + 30)

# VS Code ipucu: bir satırı yorum yapmak/açmak için
#   Windows: Ctrl + /       macOS: Cmd + /

print("Adım 5: dosyanın sonu")
# Dosya bitince program da biter. Terminalde tekrar komut yazabilirsiniz.
