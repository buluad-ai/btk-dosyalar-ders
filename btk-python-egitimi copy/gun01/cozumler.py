# -*- coding: utf-8 -*-
"""Temel ve ek alıştırmanın bağımsız örnek çözümü."""
# Değişken adları, koşullar ve dosya yollarını örneklerle karşılaştırın.
sureler = [3, 6, 12]
ortalama = sum(sureler) / len(sureler)
print(f"Ortalama: {ortalama:.2f}")
print(f"5 güne göre fark: {(ortalama - 5) / 5 * 100:.0f}%")
