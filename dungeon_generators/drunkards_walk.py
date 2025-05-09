"""
Drunkard's Walk Dungeon Generator
--------------------------------

Tento modul implementuje generování dungeonů metodou Drunkard's Walk (Náhodná procházka).
Algoritmus simuluje náhodný pohyb "opilce", který vytváří podlahu tam, kde se pohybuje.

Základní princip:
1. Začneme s dungeon mapou plnou zdí
2. Umístíme "opilce" na náhodnou pozici
3. Opilec se náhodně pohybuje a proměňuje zdi na podlahu
4. Pokračujeme, dokud nevygenerujeme požadovaný poměr podlahy k celkové ploše

Výhodou Drunkard's Walk je vytváření organických, nepravidelných chodeb a prostor,
které mohou sloužit jako jeskyně nebo bludiště.
"""

import random
from typing import List, Tuple


def generate_drunkards_dungeon(width: int, height: int, floor_ratio: float = 0.35) -> List[List[str]]:
    """
    Generuje dungeon pomocí algoritmu Drunkard's Walk (Náhodná procházka).
    
    Args:
        width (int): Šířka dungeonu
        height (int): Výška dungeonu
        floor_ratio (float): Poměr podlahy k celkové ploše dungeonu (0.0 až 1.0)
        
    Returns:
        List[List[str]]: 2D mapa dungeonu, kde '#' představuje stěnu a '.' podlahu
    """
    # Inicializace dungeonu se zdmi
    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    
    # Počáteční pozice (vyhýbáme se okrajům)
    x = random.randint(1, width - 2) 
    y = random.randint(1, height - 2)
    
    # Nastavení počáteční pozice jako podlahy
    dungeon[y][x] = '.'
    floor_tiles = 1
    
    # Výpočet cílového počtu podlahových dlaždic
    target_floor = int(width * height * floor_ratio)
    
    # Hlavní smyčka - pokračujeme, dokud nemáme dostatek podlahových dlaždic
    while floor_tiles < target_floor:
        # Výběr náhodného směru: nahoru, dolů, doprava, doleva
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        
        # Výpočet nové pozice (udržujeme v rámci hranic)
        new_x = max(1, min(width - 2, x + direction[0]))
        new_y = max(1, min(height - 2, y + direction[1]))
        
        # Přesun na novou pozici
        x, y = new_x, new_y
        
        # Pokud je aktuální pozice zeď, přeměníme ji na podlahu
        if dungeon[y][x] == '#':
            dungeon[y][x] = '.'
            floor_tiles += 1

    # Zajistíme, že okraje jsou zdi
    for i in range(width):
        dungeon[0][i] = '#'
        dungeon[height-1][i] = '#'
    
    for i in range(height):
        dungeon[i][0] = '#'
        dungeon[i][width-1] = '#'

    return dungeon


if __name__ == "__main__":
    # Jednoduché testování
    dungeon = generate_drunkards_dungeon(60, 30)
    for row in dungeon:
        print(''.join(row))
