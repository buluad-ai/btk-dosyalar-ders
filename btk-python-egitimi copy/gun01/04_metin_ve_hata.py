# -*- coding: utf-8 -*-
"""Metin işlemleri ve kontrollü hata. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
birim = "  teknik destek  "
print("Birim:", birim.strip().title())
# EĞİTMEN DEMOSU: try/except bugün ezberlenmez; ayrıntı 3. gün.
# Bir hata bütün dersi durdurmasın: yalnızca beklenen hatayı yakala.
ham_sayi = "on iki"
try:
    sayi = int(ham_sayi)
except ValueError:
    print("Geçersiz sayı:", ham_sayi)
# Bu örnekte try/except'i tanıyoruz; ayrıntısı 3. gün.
print("Program tamamlandı.")
