import random

class BSPNode:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.left = self.right = None
        self.room = None
        self.corridors = []
        self.parent = None

    def split(self):
        # Don't split if dimensions are too small
        if self.width < 15 or self.height < 15:
            return False

        # Choose split direction based on dimensions
        if self.width > self.height and self.width > 15:
            # Split vertically
            split_position = random.randint(self.width // 3, (self.width * 2) // 3)
            self.left = BSPNode(self.x, self.y, split_position, self.height)
            self.right = BSPNode(self.x + split_position, self.y, self.width - split_position, self.height)
            self.left.parent = self
            self.right.parent = self
        elif self.height > 15:
            # Split horizontally
            split_position = random.randint(self.height // 3, (self.height * 2) // 3)
            self.left = BSPNode(self.x, self.y, self.width, split_position)
            self.right = BSPNode(self.x, self.y + split_position, self.width, self.height - split_position)
            self.left.parent = self
            self.right.parent = self
        else:
            return False
        
        return True

    def create_rooms(self):
        """Generates a room inside each leaf node."""
        if self.left or self.right:
            # This is not a leaf node, process children
            if self.left:
                self.left.create_rooms()
            if self.right:
                self.right.create_rooms()
            
            # Connect children with corridors
            if self.left and self.right and self.left.room and self.right.room:
                self.create_corridor(self.left.room, self.right.room)
        else:
            # This is a leaf node, create a room
            # Make rooms smaller than their containing BSP node
            room_width = random.randint(self.width // 2, int(self.width * 0.7))
            room_height = random.randint(self.height // 2, int(self.height * 0.7))
            
            # Position the room within the node
            room_x = self.x + random.randint(1, self.width - room_width - 1)
            room_y = self.y + random.randint(1, self.height - room_height - 1)
            
            self.room = (room_x, room_y, room_width, room_height)

    def create_corridor(self, room1, room2):
        """Creates a corridor between two rooms."""
        # Get center points of each room
        r1x = room1[0] + room1[2] // 2
        r1y = room1[1] + room1[3] // 2
        r2x = room2[0] + room2[2] // 2
        r2y = room2[1] + room2[3] // 2
        
        # Decide randomly whether to go horizontal-then-vertical or vertical-then-horizontal
        if random.random() < 0.5:
            # Horizontal then vertical
            self.corridors.append((r1x, r1y, r2x, r1y))  # Horizontal part
            self.corridors.append((r2x, r1y, r2x, r2y))  # Vertical part
        else:
            # Vertical then horizontal
            self.corridors.append((r1x, r1y, r1x, r2y))  # Vertical part
            self.corridors.append((r1x, r2y, r2x, r2y))  # Horizontal part

def generate_bsp_dungeon(width, height, max_depth=5):
    """Generates a dungeon using Binary Space Partitioning."""
    # Initialize dungeon with walls
    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    
    # Create the root BSP node
    root = BSPNode(0, 0, width, height)
    
    # Split nodes recursively
    nodes_to_split = [root]
    depth = 0
    
    while depth < max_depth and nodes_to_split:
        next_nodes = []
        for node in nodes_to_split:
            if node.split():
                next_nodes.append(node.left)
                next_nodes.append(node.right)
        
        nodes_to_split = next_nodes
        depth += 1
    
    # Create rooms
    root.create_rooms()
    
    # Get all leaf nodes
    leaf_nodes = []
    
    def get_leaf_nodes(node):
        if not node:
            return
        if not node.left and not node.right:
            leaf_nodes.append(node)
        else:
            get_leaf_nodes(node.left)
            get_leaf_nodes(node.right)
    
    get_leaf_nodes(root)
    
    # Carve out rooms
    for node in leaf_nodes:
        if node.room:
            rx, ry, rw, rh = node.room
            for y in range(ry, ry + rh):
                if 0 <= y < height:  # Check bounds
                    for x in range(rx, rx + rw):
                        if 0 <= x < width:  # Check bounds
                            dungeon[y][x] = "."
    
    # Carve out corridors
    def get_all_corridors(node):
        corridors = node.corridors.copy()
        if node.left:
            corridors.extend(get_all_corridors(node.left))
        if node.right:
            corridors.extend(get_all_corridors(node.right))
        return corridors
    
    all_corridors = get_all_corridors(root)
    
    # Connect leaf nodes if they don't have corridors or are isolated
    if len(leaf_nodes) > 1:
        # Create a list of all rooms
        rooms = [node.room for node in leaf_nodes if node.room]
        
        # Connect each room to the next one to ensure all are accessible
        for i in range(len(rooms) - 1):
            r1 = rooms[i]
            r2 = rooms[i + 1]
            
            # Get center points of each room
            r1x = r1[0] + r1[2] // 2
            r1y = r1[1] + r1[3] // 2
            r2x = r2[0] + r2[2] // 2
            r2y = r2[1] + r2[3] // 2
            
            # Add corridors to ensure connectivity
            all_corridors.append((r1x, r1y, r1x, r2y))  # Vertical part
            all_corridors.append((r1x, r2y, r2x, r2y))  # Horizontal part
    
    # Draw all corridors
    for corridor in all_corridors:
        x1, y1, x2, y2 = corridor
        
        # Ensure corridor is within dungeon bounds
        x1 = max(0, min(x1, width - 1))
        y1 = max(0, min(y1, height - 1))
        x2 = max(0, min(x2, width - 1))
        y2 = max(0, min(y2, height - 1))
        
        # Make corridors a bit wider for better connectivity
        corridor_width = 1
        
        # Draw horizontal corridor
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for w in range(-corridor_width, corridor_width + 1):
                    if 0 <= y < height and 0 <= x1 + w < width:
                        dungeon[y][x1 + w] = "."
        # Draw vertical corridor
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for w in range(-corridor_width, corridor_width + 1):
                    if 0 <= y1 + w < height and 0 <= x < width:
                        dungeon[y1 + w][x] = "."
    
    return dungeon
