import random

def generate_digger_dungeon(width, height, num_diggers=3, dig_length=100):
    # Nejprve vytvoříme mapu plnou zdí
    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    
    # Vytvoříme počáteční místnost uprostřed
    center_x, center_y = width // 2, height // 2
    room_size = 5
    for y in range(center_y - room_size // 2, center_y + room_size // 2 + 1):
        for x in range(center_x - room_size // 2, center_x + room_size // 2 + 1):
            if 0 <= y < height and 0 <= x < width:
                dungeon[y][x] = "."
    
    # Seznam počátečních pozic diggerů
    diggers_positions = [
        (center_x, center_y - room_size // 2),  # nahoře
        (center_x + room_size // 2, center_y),  # vpravo
        (center_x, center_y + room_size // 2),  # dole
        (center_x - room_size // 2, center_y)   # vlevo
    ]
    
    # Použijeme pouze počet diggerů, který jsme specifikovali
    diggers = random.sample(diggers_positions, min(num_diggers, len(diggers_positions)))
    
    # Každý digger provede svůj "výkop"
    for digger_pos in diggers:
        x, y = digger_pos
        # Digger se bude pohybovat v náhodných směrech, ale s větší pravděpodobností 
        # bude pokračovat ve svém aktuálním směru
        cur_direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        
        for _ in range(dig_length):
            # S pravděpodobností 70% pokračuje ve stejném směru
            if random.random() > 0.3:
                pass  # Zachováváme aktuální směr
            else:
                # Změníme směr, ale nikdy ne o 180 stupňů
                possible_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                opposite = (-cur_direction[0], -cur_direction[1])
                possible_directions.remove(opposite)
                cur_direction = random.choice(possible_directions)
            
            # Posuneme se v aktuálním směru
            x += cur_direction[0]
            y += cur_direction[1]
            
            # Zajistíme, že zůstáváme v mapě
            x = max(1, min(width - 2, x))
            y = max(1, min(height - 2, y))
            
            # Vykopáme průchod
            dungeon[y][x] = "."
            
            # Občas vytvoříme malou místnost
            if random.random() < 0.1:
                room_size = random.randint(2, 4)
                for room_y in range(y - room_size // 2, y + room_size // 2 + 1):
                    for room_x in range(x - room_size // 2, x + room_size // 2 + 1):
                        if (1 <= room_y < height - 1 and 
                            1 <= room_x < width - 1):
                            dungeon[room_y][room_x] = "."
    
    return dungeon
