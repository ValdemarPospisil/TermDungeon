import random

def generate_drunkards_dungeon(width, height, floor_ratio=0.35):
    """
    Generate a dungeon using the drunkard's walk algorithm.
    
    Args:
        width (int): Width of the dungeon
        height (int): Height of the dungeon
        floor_ratio (float): Percentage of the dungeon that should be floor (0.0 to 1.0)
        
    Returns:
        list: 2D list representing the dungeon, where '#' is a wall and '.' is a floor
    """
    # Initialize dungeon with walls
    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    
    # Start position (avoiding edges)
    x = random.randint(1, width - 2) 
    y = random.randint(1, height - 2)
    
    # Set starting position as floor
    dungeon[y][x] = '.'
    floor_tiles = 1
    
    # Calculate target number of floor tiles
    target_floor = int(width * height * floor_ratio)
    
    # Main loop - continue until we have enough floor tiles
    while floor_tiles < target_floor:
        # Choose random direction: up, down, right, left
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        
        # Calculate new position (keep within bounds)
        new_x = max(1, min(width - 2, x + direction[0]))
        new_y = max(1, min(height - 2, y + direction[1]))
        
        # Move to new position
        x, y = new_x, new_y
        
        # If current position is a wall, convert to floor
        if dungeon[y][x] == '#':
            dungeon[y][x] = '.'
            floor_tiles += 1

    # Ensure edges are walls
    for i in range(width):
        dungeon[0][i] = '#'
        dungeon[height-1][i] = '#'
    
    for i in range(height):
        dungeon[i][0] = '#'
        dungeon[i][width-1] = '#'

    return dungeon
