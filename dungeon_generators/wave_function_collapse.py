import random


def generate_wfc_dungeon(width, height, room_attempts=15, room_min_size=5, room_max_size=10):
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

def connect_horizontal(dungeon, x1, x2, y):
    """ Vytvoří vodorovnou chodbu mezi x1 a x2 na řádku y """
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon[y][x] = "." 

def connect_vertical(dungeon, y1, y2, x):
    """ Vytvoří svislou chodbu mezi y1 a y2 ve sloupci x """
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon[y][x] = "." 

