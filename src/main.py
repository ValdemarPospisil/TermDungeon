import sys
import shutil
from bsp_generator import generate_bsp_dungeon
from cellular_automata import generate_cellular_automata_dungeon
from drunkards_walk import generate_drunkards_dungeon
from wave_function_collapse import generate_wfc_dungeon
from perlin_generator import generate_perlin_dungeon

# Slovník s vysvětlením algoritmů
ALGO_INFO = {
    "BSP": "Binary Space Partitioning:\n"
           "Rekurzivně dělí prostor na menší oblasti a vytváří v nich\n"
           "místnosti. Následně generuje chodby mezi nimi.\n\n"
           "Výhody: Strukturované dungeony s jasnými místnostmi a chodbami.\n"
           "Nevýhody: Může působit uměle a příliš pravidelně.\n\n"
           "Použití: Typické pro klasické RPG dungeony, podzemní komplexy\n"
           "nebo budovy. Ideální pro roguelike hry jako NetHack nebo Angband.",
           
    "Cellular Automata": "Buněčný automat simulující tvorbu jeskyní:\n"
                         "Začíná s náhodným šumem a opakovaně aplikuje pravidla\n"
                         "podobná Conway's Game of Life pro vytvoření organických struktur.\n\n"
                         "Výhody: Velmi přirozené, organické jeskyně s plynulými tvary.\n"
                         "Nevýhody: Obtížná kontrola výsledku, může vytvářet izolované oblasti.\n\n"
                         "Použití: Přírodní jeskyně, podzemní komplexy, lávové tunely.\n"
                         "Populární v hrách jako Dwarf Fortress nebo Minecraft.",
                         
    "Drunkard's Walk": "Algoritmus náhodné procházky (opilcův krok):\n"
                       "Virtuální 'opilec' se náhodně pohybuje po mapě a všude,\n"
                       "kam vstoupí, vytvoří průchozí cestu nebo místnost.\n\n"
                       "Výhody: Jednoduchý na implementaci, vytváří nepředvídatelné vzory.\n"
                       "Nevýhody: Méně kontroly nad strukturou, může být neefektivní.\n\n"
                       "Použití: Organické jeskyně, bludiště, chaotické struktury.\n"
                       "Často k vidění v hrách jako The Binding of Isaac nebo Enter the Gungeon.",
                       
    "Wave Function Collapse": "Komplexní algoritmus založený na lokálních vzorech:\n"
                              "Začíná s neurčitým stavem a postupně 'kolabuje' možnosti\n"
                              "podle předem definovaných pravidel, podobně jako kvantová mechanika.\n\n"
                              "Výhody: Generuje velmi komplexní, souvislé a koherentní struktury.\n"
                              "Nevýhody: Složitá implementace, potřeba definovat vzory předem.\n\n"
                              "Použití: Komplexní a detailní světy, města nebo oblasti s jasnými pravidly.\n"
                              "Používán v Bad North, Caves of Qud a experimentálních projektech.",
                              
    "Perlin Noise": "Algoritmus využívající gradientní šum pro generování terénu:\n"
                    "Vytváří plynulý, přirozeně vypadající šum který se převádí na herní prvky.\n"
                    "Hodnoty šumu nad určitou hranicí jsou podlahy, pod ní zdi.\n\n"
                    "Výhody: Hladké přechody, přirozený vzhled, předvídatelná spojitost.\n"
                    "Nevýhody: Bez dalších úprav nevytváří jasné místnosti nebo chodby.\n\n"
                    "Použití: Terénní mapy, jeskynní systémy, ostrovy, biomové přechody.\n"
                    "Používán v Minecraft, No Man's Sky, mnoha procedurálních hrách."
}

def main():
    while True:
        term_width, _ = shutil.get_terminal_size()
        divider = "─" * term_width

        print("\n=== TermDungeon Generator ===")
        print("1) BSP Dungeon")
        print("2) Cellular Automata")
        print("3) Drunkard's Walk")
        print("4) Wave Function Collapse")
        print("5) Perlin Noise")
        print("6) Exit")
        print(divider)

        choice = input("Vyber algoritmus (1-6) nebo zadejte 'číslo_s' pro skript nebo 'číslo_p' pro parametry: ").strip()
        width = 75 
        height = 25 
        
        if choice.endswith('s'):
            algo_num = choice[:-1]
            if algo_num == "1":
                with open('bsp_generator.py', 'r') as file:
                    print(file.read())
            elif algo_num == "2":
                with open('cellular_automata.py', 'r') as file:
                    print(file.read())
            elif algo_num == "3":
                with open('drunkards_walk.py', 'r') as file:
                    print(file.read())
            elif algo_num == "4":
                with open('wave_function_collapse.py', 'r') as file:
                    print(file.read())
            elif algo_num == "5":
                with open('perlin_noise.py', 'r') as file:
                    print(file.read())
            else:
                print("Neplatná volba, zkus to znovu.")
            continue
        elif choice.endswith('p'):
            algo_num = choice[:-1]
            if algo_num == "1":
                params = input("Zadejte specifické parametry pro BSP (např. min_room_size,max_room_size): ").strip()
                # Process params as needed
                dungeon = generate_bsp_dungeon(width, height, *map(int, params.split(',')))
            elif algo_num == "2":
                params = input("Zadejte specifické parametry pro Cellular Automata (např. iterations,chance_to_start_alive): ").strip()
                # Process params as needed
                dungeon = generate_cellular_automata_dungeon(width, height, *map(int, params.split(',')))
            elif algo_num == "3":
                params = input("Zadejte specifické parametry pro Drunkard's Walk (např. floor_ratio): ").strip()
                # Process params as needed
                params_float = float(params) if params else 0.35
                dungeon = generate_drunkards_dungeon(width, height, params_float)
            elif algo_num == "4":
                params = input("Zadejte specifické parametry pro Wave Function Collapse: ").strip()
                # Process params as needed
                dungeon = generate_wfc_dungeon(width, height, *map(int, params.split(',')))
            elif algo_num == "5":
                params = input("Zadejte specifické parametry pro Perlin Noise (např. scale,octaves,threshold): ").strip()
                if params:
                    param_list = params.split(',')
                    if len(param_list) == 3:
                        scale = float(param_list[0])
                        octaves = int(param_list[1])
                        threshold = float(param_list[2])
                        dungeon = generate_perlin_dungeon(width, height, scale, octaves, threshold)
                    else:
                        print("Neplatné parametry! Použití výchozích hodnot.")
                        dungeon = generate_perlin_dungeon(width, height)
                else:
                    dungeon = generate_perlin_dungeon(width, height)
            else:
                print("Neplatná volba, zkus to znovu.")
            continue
        elif choice == "1":
            algo_name = "BSP"
            dungeon = generate_bsp_dungeon(width, height)
        elif choice == "2":
            algo_name = "Cellular Automata"
            dungeon = generate_cellular_automata_dungeon(width, height)
        elif choice == "3":
            algo_name = "Drunkard's Walk"
            dungeon = generate_drunkards_dungeon(width, height)
        elif choice == "4":
            algo_name = "Wave Function Collapse"
            dungeon = generate_wfc_dungeon(width, height)
        elif choice == "5":
            algo_name = "Perlin Noise"
            dungeon = generate_perlin_dungeon(width, height)
        elif choice == "6":
            print("Ukončuji program.")
            sys.exit()
        else:
            print("Neplatná volba, zkus to znovu.")
            continue

        # Zobrazení mapy a vysvětlení algoritmu vedle sebe
        print(divider)
        print_dungeon_with_info(dungeon, ALGO_INFO[algo_name])

def print_dungeon_with_info(dungeon, info):
    """ Zobrazí dungeon vlevo a vysvětlení vpravo. """
    term_width, _ = shutil.get_terminal_size()
    split_pos = max(30, term_width // 2)  # Kde se oddělí dungeon a text

    info_lines = info.split("\n")
    for i, row in enumerate(dungeon):
        row_str = "".join(row)
        if i < len(info_lines):
            info_line = info_lines[i]
        else:
            info_line = ""
        print(f"{row_str.ljust(split_pos)} {info_line}")

if __name__ == "__main__":
    main()
