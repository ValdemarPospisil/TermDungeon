import random
import math
from perlin_noise import PerlinNoise

def generate_perlin_dungeon(width, height, scale=15, octaves=4, threshold=0.5):
    """
    Generates a 2D dungeon map using Perlin noise for natural-looking layouts.
    
    The dungeon is represented as a 2D list of characters, where '#' denotes walls and '.' denotes floors. Perlin noise is layered with multiple octaves and normalized to ensure consistent thresholding. The threshold parameter determines the cutoff above which tiles become floors. Borders are always set as walls.
    
    Args:
        width: Number of columns in the dungeon grid.
        height: Number of rows in the dungeon grid.
        scale: Controls the zoom level of the noise pattern; higher values produce larger features.
        octaves: Number of noise layers combined to add detail.
        threshold: Normalized noise value above which tiles are set as floors (range 0.0 to 1.0).
    
    Returns:
        A 2D list of strings representing the dungeon layout, with '#' for walls and '.' for floors.
    """
    # Initialize the dungeon with walls
    dungeon = [['#' for _ in range(width)] for _ in range(height)]

    # Create layered noise (for detail)
    seed = random.randint(0, 1000)
    noises = [PerlinNoise(octaves=i+1, seed=seed) for i in range(octaves)]
    
    # For normalization, find min and max values
    min_val = 1.0
    max_val = -1.0
    
    # First pass to find min and max values for better normalization
    sample_values = []
    for y in range(height):
        for x in range(width):
            nx = x / scale
            ny = y / scale
            value = sum(noise([nx, ny]) * (0.5**i) for i, noise in enumerate(noises))
            sample_values.append(value)
            min_val = min(min_val, value)
            max_val = max(max_val, value)
    
    # Calculate range for normalization
    value_range = max_val - min_val if max_val > min_val else 1.0
    
    # Second pass to generate the dungeon
    for y in range(height):
        for x in range(width):
            # Skip the border
            if x == 0 or y == 0 or x == width-1 or y == height-1:
                dungeon[y][x] = '#'  # Ensure border is wall
                continue
            
            nx = x / scale
            ny = y / scale
            value = sum(noise([nx, ny]) * (0.5**i) for i, noise in enumerate(noises))
            
            # Normalize value to 0.0-1.0 range
            normalized = (value - min_val) / value_range
            
            if normalized > threshold:
                dungeon[y][x] = '.'  # Floor
    
    return dungeon
