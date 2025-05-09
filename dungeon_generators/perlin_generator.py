"""
Perlin Noise Dungeon Generator
-----------------------------

Tento modul implementuje generování dungeonů pomocí Perlinova šumu.
Perlinův šum je typ gradientního šumu, který vytváří přirozené, organické vzory
a je často používán pro generování terénu v počítačových hrách.

Základní princip:
1. Vygenerujeme Perlinův šum s různými oktávami pro různé úrovně detailů
2. Normalizujeme hodnoty šumu do rozsahu 0.0 až 1.0
3. Použijeme prahovou hodnotu pro určení, kde budou zdi a kde podlaha
4. Výsledkem je organicky vypadající jeskynní systém

Výhodou Perlinova šumu je vytváření přirozených, plynulých přechodů,
což vede k velmi přirozeně vypadajícím dungeonům.
"""

import random
import math
from typing import List, Tuple
from perlin_noise import PerlinNoise


def generate_perlin_dungeon(width: int, height: int, scale: float = 15.0, octaves: int = 4, threshold: float = 0.5) -> List[List[str]]:
    """
    Generuje dungeon pomocí Perlinova šumu.

    Args:
        width (int): Šířka dungeonu
        height (int): Výška dungeonu
        scale (float): Měřítko šumu (vyšší hodnota = více přiblížený)
        octaves (int): Počet oktáv šumu (více = více detailů)
        threshold (float): Hodnota, nad kterou jsou dlaždice podlahou (0.0 až 1.0)

    Returns:
        List[List[str]]: 2D mapa dungeonu, kde '#' představuje stěnu a '.' podlahu
    """
    # Inicializace dungeonu se zdmi
    dungeon = [['#' for _ in range(width)] for _ in range(height)]

    # Vytvoření vrstveného šumu (pro detaily)
    seed = random.randint(0, 1000)
    noises = [PerlinNoise(octaves=i+1, seed=seed) for i in range(octaves)]
    
    # Pro normalizaci najdeme minimální a maximální hodnoty
    min_val = 1.0
    max_val = -1.0
    
    # První průchod pro nalezení minimálních a maximálních hodnot pro lepší normalizaci
    sample_values = []
    for y in range(height):
        for x in range(width):
            nx = x / scale
            ny = y / scale
            value = sum(noise([nx, ny]) * (0.5**i) for i, noise in enumerate(noises))
            sample_values.append(value)
            min_val = min(min_val, value)
            max_val = max(max_val, value)
    
    # Výpočet rozsahu pro normalizaci
    value_range = max_val - min_val if max_val > min_val else 1.0
    
    # Druhý průchod pro generování dungeonu
    for y in range(height):
        for x in range(width):
            # Přeskočíme okraje
            if x == 0 or y == 0 or x == width-1 or y == height-1:
                dungeon[y][x] = '#'  # Zajistíme, že okraj je zeď
                continue
            
            nx = x / scale
            ny = y / scale
            value = sum(noise([nx, ny]) * (0.5**i) for i, noise in enumerate(noises))
            
            # Normalizace hodnoty do rozsahu 0.0-1.0
            normalized = (value - min_val) / value_range
            
            if normalized > threshold:
                dungeon[y][x] = '.'  # Podlaha
    
    return dungeon


if __name__ == "__main__":
    # Jednoduché testování
    try:
        dungeon = generate_perlin_dungeon(60, 30)
        for row in dungeon:
            print(''.join(row))
    except ImportError:
        print("Pro použití tohoto generátoru je nutné nainstalovat balíček 'perlin-noise'")
        print("Instalace: pip install perlin-noise")
