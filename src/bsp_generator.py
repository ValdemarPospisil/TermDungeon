import random

class BSPNode:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.left = self.right = None
        self.room = None

    def split(self):
        if self.width > self.height:
            if self.width < 30:  # Zabrání příliš malému dělení
                return False
            split = random.randint(6, self.width - 6)
            self.left = BSPNode(self.x, self.y, split, self.height)
            self.right = BSPNode(self.x + split, self.y, self.width - split, self.height)
        else:
            if self.height < 30:
                return False
            split = random.randint(6, self.height - 6)
            self.left = BSPNode(self.x, self.y, self.width, split)
            self.right = BSPNode(self.x, self.y + split, self.width, self.height - split)
        return True

    def create_rooms(self):
        """Generuje místnost uvnitř rozděleného uzlu."""
        if self.left or self.right:
            if self.left:
                self.left.create_rooms()
            if self.right:
                self.right.create_rooms()
        else:
            min_width = max(2, self.width // 2)
            max_width = max(min_width, self.width - 2)

            min_height = max(2, self.height // 2)
            max_height = max(min_height, self.height - 2)

            # ✅ Opravené generování náhodné velikosti místnosti
            room_width = random.randint(min_width, max_width)
            room_height = random.randint(min_height, max_height)

            room_x = self.x + random.randint(1, max(1, self.width - room_width - 1))
            room_y = self.y + random.randint(1, max(1, self.height - room_height - 1))

            self.room = (room_x, room_y, room_width, room_height)

def generate_bsp_dungeon(width, height, max_depth=4):
    """Generuje dungeon pomocí Binary Space Partitioning."""
    root = BSPNode(0, 0, width, height)
    nodes = [root]

    for _ in range(max_depth):
        new_nodes = []
        for node in nodes:
            if node.split():
                new_nodes.append(node.left)
                new_nodes.append(node.right)
        nodes.extend(new_nodes)
    
    for node in nodes:
        node.create_rooms()

    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    
    for node in nodes:
        if node.room:
            print(node.room)
            rx, ry, rw, rh = node.room
            for y in range(ry, ry + rh):
                for x in range(rx, rx + rw):
                    dungeon[y-3][x-3] = "."

    return dungeon
