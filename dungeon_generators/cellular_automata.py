"""
Cellular Automata Dungeon Generator
----------------------------------

Tento modul implementuje generování dungeonů pomocí celulárních automatů.
Celulární automaty jsou model inspirovaný chováním buněk, kde aktualizujeme
stav buněk v mřížce na základě stavu jejich sousedů podle specifických pravidel.

Základní princip:
1. Začneme s náhodně inicializovanou mřížkou (buňky = zdi nebo podlaha)
2. Aplikujeme pravidla pro každou buňku na základě počtu sousedních zdí
3. Proces opakujeme několikrát
4. Výsledkem je organicky vypadající jeskynní systém

Výhodou celulárních automatů je vytváření přirozeně vypadajících jeskyní a prostor.
"""

import random
from typing import List, Tuple


def initialize_map(width: int, height: int, wall_prob: float = 0.45) -> List[List[str]]:
    """
    Vytvoří počáteční mapu s náhodně rozmístěnými zdmi.
    
    Args:
        width (int): Šířka mapy
        height (int): Výška mapy
        wall_prob (float): Pravděpodobnost, že buňka bude zeď (0.0 až 1.0)
    
    Returns:
        List[List[str]]: 2D mapa s náhodně rozmístěnými zdmi
    """
    return [
        ["#" if random.random() < wall_prob else "." for _ in range(width)]
        for _ in range(height)
    ]


def count_neighbors(dungeon: List[List[str]], x: int, y: int) -> int:
    """
    Spočítá počet zdí (#) v okolí buňky na pozici (x, y).
    
    Args:
        dungeon (List[List[str]]): Mapa dungeonu
        x (int): X-ová souřadnice buňky
        y (int): Y-ová souřadnice buňky
    
    Returns:
        int: Počet zdí v okolí buňky
    """
    count = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(dungeon[0]) and 0 <= ny < len(dungeon):
                if dungeon[ny][nx] == "#":
                    count += 1
            else:
                count += 1  # Okrajové buňky jsou vždy stěny
    return count


def cellular_automata_step(dungeon: List[List[str]], birth_limit: int = 4, death_limit: int = 3) -> List[List[str]]:
    """
    Provede jeden krok celulárního automatu na základě pravidel birth_limit a death_limit.
    
    Args:
        dungeon (List[List[str]]): Mapa dungeonu
        birth_limit (int): Počet sousedů potřebných pro vytvoření zdi
        death_limit (int): Počet sousedů potřebných pro zachování zdi
    
    Returns:
        List[List[str]]: Aktualizovaná mapa dungeonu
    """
    new_map = [row[:] for row in dungeon]
    for y in range(len(dungeon)):
        for x in range(len(dungeon[0])):
            neighbors = count_neighbors(dungeon, x, y)
            if dungeon[y][x] == "#":
                new_map[y][x] = "#" if neighbors >= death_limit else "."
            else:
                new_map[y][x] = "#" if neighbors > birth_limit else "."
    return new_map


def generate_cellular_automata_dungeon(width: int, height: int, iterations: int = 5, wall_prob: float = 0.45) -> List[List[str]]:
    """
    Vygeneruje dungeon pomocí celulárního automatu.
    
    Args:
        width (int): Šířka dungeonu
        height (int): Výška dungeonu
        iterations (int): Počet iterací celulárního automatu
        wall_prob (float): Počáteční pravděpodobnost zdi (0.0 až 1.0)
    
    Returns:
        List[List[str]]: 2D mapa dungeonu, kde '#' představuje stěnu a '.' podlahu
    """
    dungeon = initialize_map(width, height, wall_prob)
    for _ in range(iterations):
        dungeon = cellular_automata_step(dungeon)
    
    # Zajistíme, že okraje jsou zdi
    for i in range(width):
        dungeon[0][i] = "#"
        dungeon[height-1][i] = "#"
    
    for i in range(height):
        dungeon[i][0] = "#"
        dungeon[i][width-1] = "#"
        
    return dungeon


if __name__ == "__main__":
    # Jednoduché testování
    dungeon = generate_cellular_automata_dungeon(60, 30)
    for row in dungeon:
        print(''.join(row))
