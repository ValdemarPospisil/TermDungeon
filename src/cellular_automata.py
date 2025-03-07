import random

def initialize_map(width, height, wall_prob=0.45):
    """ Vytvoří mapu s náhodnými stěnami. """
    return [
        ["#" if random.random() < wall_prob else "." for _ in range(width)]
        for _ in range(height)
    ]

def count_neighbors(dungeon, x, y):
    """ Spočítá počet stěn (#) v okolí buňky (x, y). """
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

def cellular_automata_step(dungeon, birth_limit=4, death_limit=3):
    """ Provede jeden krok cellular automata. """
    new_map = [row[:] for row in dungeon]
    for y in range(len(dungeon)):
        for x in range(len(dungeon[0])):
            neighbors = count_neighbors(dungeon, x, y)
            if dungeon[y][x] == "#":
                new_map[y][x] = "#" if neighbors >= death_limit else "."
            else:
                new_map[y][x] = "#" if neighbors > birth_limit else "."
    return new_map

def generate_cellular_automata_dungeon(width, height, iterations=5):
    """ Vygeneruje dungeon pomocí cellular automata. """
    dungeon = initialize_map(width, height)
    for _ in range(iterations):
        dungeon = cellular_automata_step(dungeon)
    return dungeon
