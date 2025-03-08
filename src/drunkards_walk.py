import random

def generate_drunkards_dungeon(width, height, floor_ratio=0.35):
    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    x = random.randint(2, width - 2) 
    y = random.randint(2, height - 2)
    
    dungeon[y-1][x-1] = '.'
    print(y,x)
    floor_tiles = 1
    target_floor = int(width * height * floor_ratio)
    
    while floor_tiles < target_floor:
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Nahoru, dolů, doprava, doleva
        x = max(2, min(width - 3, x + direction[0]))  # Udržení v mezích
        y = max(2, min(height - 3, y + direction[1]))
        if dungeon[y-1][x-1] == '#':  # Pokud byla zeď, změnit na podlahu
            dungeon[y-1][x-1] = '.'
            floor_tiles += 1

    return dungeon

