import random
import noise

def generate_perlin_dungeon(width, height, scale=15, octaves=8, persistence=0.5, lacunarity=2.0, threshold=0.0):
    """
    Generate a dungeon using Perlin noise.
    
    Args:
        width (int): Width of the dungeon
        height (int): Height of the dungeon
        scale (float): Scale of the noise (higher = more zoomed out)
        octaves (int): Number of octaves for the noise (more = more detail)
        persistence (float): How much each octave contributes to the overall shape
        lacunarity (float): How much detail is added at each octave
        threshold (float): Value above which tiles are walls (-1.0 to 1.0)
    
    Returns:
        list: 2D list representing the dungeon, where '#' is a wall and '.' is a floor
    """
    # Initialize the dungeon with walls
    dungeon = [['#' for _ in range(width)] for _ in range(height)]
    
    # Random offset to make each generation unique
    seed = random.randint(0, 1000)
    
    # Generate Perlin noise and convert to dungeon tiles
    for y in range(height):
        for x in range(width):
            # Generate noise value between -1.0 and 1.0
            nx = x / scale
            ny = y / scale
            value = noise.pnoise2(nx + seed, ny + seed, 
                                  octaves=octaves, 
                                  persistence=persistence, 
                                  lacunarity=lacunarity, 
                                  repeatx=width, 
                                  repeaty=height, 
                                  base=seed)
            # Convert noise to dungeon tiles based on threshold
            if value > threshold:
                dungeon[y][x] = '.'  # Floor
    
    # Add a border around the dungeon to ensure enclosed space
    for y in range(height):
        dungeon[y][0] = '#'
        dungeon[y][width-1] = '#'
    for x in range(width):
        dungeon[0][x] = '#'
        dungeon[height-1][x] = '#'
    
    return dungeon

