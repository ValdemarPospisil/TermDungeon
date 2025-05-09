"""
Binary Space Partitioning (BSP) Dungeon Generator
------------------------------------------------

Tento modul implementuje generování dungeonů metodou Binary Space Partitioning (BSP).
BSP je algoritmus, který rekurzivně rozděluje prostor na menší části a následně v nich
vytváří místnosti a propojuje je chodbami.

Základní princip:
1. Začneme s jedním velkým obdélníkovým prostorem
2. Rekurzivně dělíme prostor buď horizontálně nebo vertikálně
3. Vytváříme místnosti uvnitř vzniklých listových uzlů
4. Propojujeme sousední místnosti chodbami

Výhodou BSP je, že vytváří strukturované dungeony s jasnými místnostmi a chodbami,
které jsou vždy plně propojené.
"""

import random
from typing import List, Tuple, Optional, Union


class BSPNode:
    """
    Třída reprezentující uzel v BSP stromu.
    
    Každý uzel reprezentuje obdélníkovou oblast v dungeonu, která může být buď
    dále rozdělena (vnitřní uzel) nebo obsahovat místnost (listový uzel).
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Inicializace uzlu BSP stromu.
        
        Args:
            x (int): X-ová souřadnice levého horního rohu oblasti
            y (int): Y-ová souřadnice levého horního rohu oblasti
            width (int): Šířka oblasti
            height (int): Výška oblasti
        """
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.left: Optional[BSPNode] = None
        self.right: Optional[BSPNode] = None
        self.room: Optional[Tuple[int, int, int, int]] = None  # (x, y, width, height)
        self.corridors: List[Tuple[int, int, int, int]] = []  # Seznam chodeb (x1, y1, x2, y2)
        self.parent: Optional[BSPNode] = None

    def split(self) -> bool:
        """
        Rozdělí tento uzel na dva poduzly (levý a pravý).
        
        Rozdělení se provádí buď horizontálně nebo vertikálně, podle toho,
        který rozměr oblasti je větší.
        
        Returns:
            bool: True pokud bylo rozdělení úspěšné, jinak False
        """
        # Pokud jsou rozměry příliš malé, nerozdělujeme
        if self.width < 15 or self.height < 15:
            return False

        # Rozhodnutí, zda dělit vertikálně nebo horizontálně
        if self.width > self.height and self.width > 15:
            # Vertikální rozdělení (dělíme šířku)
            split_position = random.randint(self.width // 3, (self.width * 2) // 3)
            self.left = BSPNode(self.x, self.y, split_position, self.height)
            self.right = BSPNode(self.x + split_position, self.y, self.width - split_position, self.height)
            self.left.parent = self
            self.right.parent = self
        elif self.height > 15:
            # Horizontální rozdělení (dělíme výšku)
            split_position = random.randint(self.height // 3, (self.height * 2) // 3)
            self.left = BSPNode(self.x, self.y, self.width, split_position)
            self.right = BSPNode(self.x, self.y + split_position, self.width, self.height - split_position)
            self.left.parent = self
            self.right.parent = self
        else:
            return False
        
        return True

    def create_rooms(self) -> None:
        """
        Rekurzivně vytváří místnosti v listových uzlech stromu a spojuje je chodbami.
        
        V listových uzlech vytvoří náhodně umístěnou místnost. V vnitřních uzlech
        rekurzivně zpracuje potomky a vytvoří chodby mezi místnostmi potomků.
        """
        if self.left or self.right:
            # Vnitřní uzel - zpracování potomků
            if self.left:
                self.left.create_rooms()
            if self.right:
                self.right.create_rooms()
            
            # Propojení místností potomků chodbami
            if self.left and self.right and self.left.room and self.right.room:
                self._create_corridor(self.left.room, self.right.room)
        else:
            # Listový uzel - vytvoření místnosti
            # Místnost bude menší než obsahující BSP uzel
            room_width = random.randint(self.width // 2, int(self.width * 0.7))
            room_height = random.randint(self.height // 2, int(self.height * 0.7))
            
            # Umístění místnosti v rámci uzlu
            room_x = self.x + random.randint(1, self.width - room_width - 1)
            room_y = self.y + random.randint(1, self.height - room_height - 1)
            
            # Uložení místnosti jako tuple (x, y, width, height)
            self.room = (room_x, room_y, room_width, room_height)

    def _create_corridor(self, room1: Tuple[int, int, int, int], room2: Tuple[int, int, int, int]) -> None:
        """
        Vytvoří chodbu spojující dvě místnosti.
        
        Args:
            room1 (tuple): První místnost ve formátu (x, y, width, height)
            room2 (tuple): Druhá místnost ve formátu (x, y, width, height)
        """
        # Nalezení středových bodů místností
        r1x = room1[0] + room1[2] // 2
        r1y = room1[1] + room1[3] // 2
        r2x = room2[0] + room2[2] // 2
        r2y = room2[1] + room2[3] // 2
        
        # Náhodné rozhodnutí o směru chodby
        if random.random() < 0.5:
            # Nejprve horizontální část, pak vertikální
            self.corridors.append((r1x, r1y, r2x, r1y))  # Horizontální část
            self.corridors.append((r2x, r1y, r2x, r2y))  # Vertikální část
        else:
            # Nejprve vertikální část, pak horizontální
            self.corridors.append((r1x, r1y, r1x, r2y))  # Vertikální část
            self.corridors.append((r1x, r2y, r2x, r2y))  # Horizontální část


def generate_bsp_dungeon(width: int, height: int, max_depth: int = 5) -> List[List[str]]:
    """
    Generuje dungeon pomocí algoritmu Binary Space Partitioning.
    
    Args:
        width (int): Šířka dungeonu
        height (int): Výška dungeonu
        max_depth (int, optional): Maximální hloubka BSP stromu. Výchozí hodnota je 5.
    
    Returns:
        List[List[str]]: 2D mapa dungeonu, kde '#' představuje stěnu a '.' podlahu
    """
    # Inicializace dungeonu se zdmi
    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    
    # Vytvoření kořenového uzlu BSP
    root = BSPNode(0, 0, width, height)
    
    # Rekurzivní dělení uzlů
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
    
    # Vytvoření místností v listových uzlech
    root.create_rooms()
    
    # Získání všech listových uzlů
    leaf_nodes = []
    
    def get_leaf_nodes(node: Optional[BSPNode]) -> None:
        """Rekurzivně sbírá všechny listové uzly."""
        if not node:
            return
        if not node.left and not node.right:
            leaf_nodes.append(node)
        else:
            get_leaf_nodes(node.left)
            get_leaf_nodes(node.right)
    
    get_leaf_nodes(root)
    
    # Vyřezání místností do dungeonu
    for node in leaf_nodes:
        if node.room:
            rx, ry, rw, rh = node.room
            for y in range(ry, ry + rh):
                if 0 <= y < height:  # Kontrola hranic
                    for x in range(rx, rx + rw):
                        if 0 <= x < width:  # Kontrola hranic
                            dungeon[y][x] = "."
    
    # Vyřezání chodeb do dungeonu
    def get_all_corridors(node: Optional[BSPNode]) -> List[Tuple[int, int, int, int]]:
        """Rekurzivně sbírá všechny chodby."""
        if not node:
            return []
        corridors = node.corridors.copy()
        if node.left:
            corridors.extend(get_all_corridors(node.left))
        if node.right:
            corridors.extend(get_all_corridors(node.right))
        return corridors
    
    all_corridors = get_all_corridors(root)
    
    # Propojení listových uzlů, pokud nemají chodby nebo jsou izolované
    if len(leaf_nodes) > 1:
        # Vytvoření seznamu všech místností
        rooms = [node.room for node in leaf_nodes if node.room]
        
        # Propojení každé místnosti s následující pro zajištění dostupnosti
        for i in range(len(rooms) - 1):
            r1 = rooms[i]
            r2 = rooms[i + 1]
            
            # Středové body místností
            r1x = r1[0] + r1[2] // 2
            r1y = r1[1] + r1[3] // 2
            r2x = r2[0] + r2[2] // 2
            r2y = r2[1] + r2[3] // 2
            
            # Přidání chodeb pro zajištění propojení
            all_corridors.append((r1x, r1y, r1x, r2y))  # Vertikální část
            all_corridors.append((r1x, r2y, r2x, r2y))  # Horizontální část
    
    # Vykreslení všech chodeb
    for corridor in all_corridors:
        x1, y1, x2, y2 = corridor
        
        # Zajištění, že chodba je v mezích dungeonu
        x1 = max(0, min(x1, width - 1))
        y1 = max(0, min(y1, height - 1))
        x2 = max(0, min(x2, width - 1))
        y2 = max(0, min(y2, height - 1))
        
        # Vytvoření širší chodby pro lepší propojení
        corridor_width = 1
        
        # Vykreslení horizontální chodby
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for w in range(-corridor_width, corridor_width + 1):
                    if 0 <= y < height and 0 <= x1 + w < width:
                        dungeon[y][x1 + w] = "."
        # Vykreslení vertikální chodby
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for w in range(-corridor_width, corridor_width + 1):
                    if 0 <= y1 + w < height and 0 <= x < width:
                        dungeon[y1 + w][x] = "."
    
    return dungeon


if __name__ == "__main__":
    # Jednoduché testování
    dungeon = generate_bsp_dungeon(80, 30)
    for row in dungeon:
        print(''.join(row))
