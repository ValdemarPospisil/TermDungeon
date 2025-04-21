import random
from perlin_noise import PerlinNoise

def generate_perlin_dungeon(width, height, scale=15, octaves=4, threshold=0.0):
    """
    Generate a dungeon using Perlin noise.

    Args:
        width (int): Width of the dungeon
        height (int): Height of the dungeon
        scale (float): Scale of the noise (higher = more zoomed out)
        octaves (int): Number of octaves for the noise (more = more detail)
        threshold (float): Value above which tiles are walls (0.0 to 1.0)

    Returns:
        list: 2D list representing the dungeon, where '#' is a wall and '.' is a floor
    """
    # Initialize the dungeon with walls
    dungeon = [['#' for _ in range(width)] for _ in range(height)]

    # Create layered noise (for detail)
    noises = [PerlinNoise(octaves=i+1, seed=random.randint(0, 1000)) for i in range(octaves)]
    
    for y in range(height):
        for x in range(width):
            nx = x / scale
            ny = y / scale
            value = sum(noise([nx, ny]) / (2**i) for i, noise in enumerate(noises))
            value = (value + 1) / 2  # normalize to 0.0–1.0
            if value > threshold:
                dungeon[y][x] = '.'  # Floor

    # Add a border
    for y in range(height):
        dungeon[y][0] = '#'
        dungeon[y][width-1] = '#'
    for x in range(width):
        dungeon[0][x] = '#'
        dungeon[height-1][x] = '#'

    return dungeon
