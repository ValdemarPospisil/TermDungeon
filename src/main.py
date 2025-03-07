import sys
import shutil
from bsp_generator import generate_bsp_dungeon
from cellular_automata import generate_cellular_automata_dungeon
# from drunkards_walk import generate_drunkards_dungeon
#from wave_function_collapse import generate_wfc_dungeon
#from perlin_noise import generate_perlin_dungeon

# Slovník s vysvětlením algoritmů
ALGO_INFO = {
    "BSP": "Binary Space Partitioning: Dělí prostor na menší oblasti\n"
           "a vytváří místnosti a chodby mezi nimi.",
    "Cellular Automata": "Simulace jeskyně: Každý bod se mění podle\n"
                         "okolních bodů, čímž vzniká organická struktura.",
    "Drunkard's Walk": "Náhodná procházka: Postava náhodně chodí po mapě\n"
                       "a postupně vytváří cesty a místnosti.",
    "Wave Function Collapse": "Složitý algoritmus, který používá vzory\n"
                              "k generování souvislých map.",
    "Perlin Noise": "Použití šumu pro vytvoření přirozeně vypadající krajiny\n"
                    "nebo dungeonů s hladkými přechody."
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

        choice = input("Vyber algoritmus (1-6): ").strip()
        width = 75 
        height = 25 
            
        if choice == "1":
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

    for i, row in enumerate(dungeon):
        row_str = "".join(row)
        if i < len(info.split("\n")):
            info_line = info.split("\n")[i]
        else:
            info_line = ""
        print(f"{row_str.ljust(split_pos)} {info_line}")

if __name__ == "__main__":
    main()
