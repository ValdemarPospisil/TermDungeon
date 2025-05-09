"""
Wave Function Collapse Dungeon Generator
---------------------------------------

Tento modul implementuje zjednodušenou verzi algoritmu Wave Function Collapse (WFC)
pro generování dungeonů. WFC je algoritmus inspirovaný kvantovou mechanikou,
který vytváří struktury na základě lokálních omezení a vzorů.

V této implementaci používáme zjednodušený přístup, kdy:
1. Náhodně generujeme místnosti
2. Propojujeme je chodbami
3. Zajišťujeme, aby všechny místnosti byly dosažitelné

WFC algoritmus je obecně složitější, ale tato zjednodušená verze
demonstruje základní princip jeho fungování pro generování dungeonů.
"""

import random
from typing import List, Tuple


def generate_wfc_dungeon(width: int, height: int, room_attempts: int = 15, 
                        room_min_size: int = 5, room_max_size: int = 10) -> List[List[str]]:
    """
    Generuje dungeon pomocí zjednodušené verze algoritmu Wave Function Collapse.
    
    Args:
        width (int): Šířka dungeonu
        height (int): Výška dungeonu
        room_attempts (int): Počet pokusů o vytvoření místnosti
        room_min_size (int): Minimální velikost místnosti
        room_max_size (int): Maximální velikost místnosti
    
    Returns:
        List[List[str]]: 2D mapa dungeonu, kde '#' představuje stěnu a '.' podlahu
    """
    # Vytvoříme základní mapu plnou zdí
    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    rooms = []

    # Náhodné generování místností
    for _ in range(room_attempts):
        w = random.randint(room_min_size, room_max_size)
        h = random.randint(room_min_size, room_max_size)
        x = random.randint(1, width - w - 1)
        y = random.randint(1, height - h - 1)

        # Kontrola kolize s jinou místností
        if any(dungeon[yy][xx] == "." for yy in range(y, y+h) for xx in range(x, x+w)):
            continue

        # Přidání místnosti
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                dungeon[yy][xx] = "." 
        rooms.append((x + w // 2, y + h // 2))  # Uložíme střed místnosti

    # Spojení místností pomocí chodeb
    random.shuffle(rooms)
    for i in range(len(rooms) - 1):
        x1, y1 = rooms[i]
        x2, y2 = rooms[i + 1]

        # Náhodně vybereme směr propojení (vodorovně nebo svisle první)
        if random.choice([True, False]):
            connect_horizontal(dungeon, x1, x2, y1)
            connect_vertical(dungeon, y1, y2, x2)
        else:
            connect_vertical(dungeon, y1, y2, x1)
            connect_horizontal(dungeon, x1, x2, y2)

    return dungeon


def connect_horizontal(dungeon: List[List[str]], x1: int, x2: int, y: int) -> None:
    """
    Vytvoří vodorovnou chodbu mezi x1 a x2 na řádku y.
    
    Args:
        dungeon (List[List[str]]): Mapa dungeonu
        x1 (int): Počáteční X souřadnice
        x2 (int): Koncová X souřadnice
        y (int): Y souřadnice řádku
    """
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon[y][x] = "." 


def connect_vertical(dungeon: List[List[str]], y1: int, y2: int, x: int) -> None:
    """
    Vytvoří svislou chodbu mezi y1 a y2 ve sloupci x.
    
    Args:
        dungeon (List[List[str]]): Mapa dungeonu
        y1 (int): Počáteční Y souřadnice
        y2 (int): Koncová Y souřadnice
        x (int): X souřadnice sloupce
    """
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon[y][x] = "." 


if __name__ == "__main__":
    # Jednoduché testování
    dungeon = generate_wfc_dungeon(60, 30)
    for row in dungeon:
        print(''.join(row))
