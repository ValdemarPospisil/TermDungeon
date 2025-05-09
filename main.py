#!/usr/bin/env python3
"""
TermDungeon - Terminálový generátor dungeonů
--------------------------------------------
Projekt TermDungeon umožňuje generovat a vizualizovat procedurálně generované dungeony
s využitím různých algoritmů.
"""

import sys
import shutil
import os
from typing import List, Dict, Tuple, Callable

# Importy generátorů dungeonů
from dungeon_generators.bsp_generator import generate_bsp_dungeon
from dungeon_generators.cellular_automata import generate_cellular_automata_dungeon
from dungeon_generators.drunkards_walk import generate_drunkards_dungeon
from dungeon_generators.wave_function_collapse import generate_wfc_dungeon
from dungeon_generators.perlin_generator import generate_perlin_dungeon

# Konstanty
DEFAULT_WIDTH = 75
DEFAULT_HEIGHT = 25

# Detailní popisy algoritmů
ALGO_INFO = {
    "BSP": """Binary Space Partitioning (BSP)
-----------------------------
Jak funguje:
- Rekurzivně dělí prostor na menší části (binární strom)
- V každé části vytváří místnost s náhodnou velikostí
- Propojuje sousední místnosti chodbami

Výhody:
- Vytváří strukturovaný layout místností a chodeb
- Dobrá kontrola nad velikostí místností
- Výsledek vždy obsahuje plně propojené místnosti

Nevýhody:
- Méně organický vzhled, působí uměle
- Někdy vytváří příliš přímočaré chodby

Využití:
- Klasické dungeony v RPG hrách
- Interiéry budov a sklepení
- Základní struktura pro komplexnější dungeony""",

    "Cellular Automata": """Cellular Automata
----------------
Jak funguje:
- Začíná s náhodně generovaným šumem
- Aplikuje pravidla pro "přežití" a "narození" buněk
- Opakovaným aplikováním pravidel vznikají organické tvary

Výhody:
- Vytváří přirozeně vypadající jeskyně
- Jednoduché na implementaci
- Možnost generovat různé druhy terénu změnou pravidel

Nevýhody:
- Výsledek může být nepředvídatelný
- Někdy vytváří izolované oblasti
- Může vyžadovat dodatečné zpracování pro herní použití

Využití:
- Přírodní jeskyně
- Organické struktury
- Podzemní komplexy""",

    "Drunkard's Walk": """Drunkard's Walk (Náhodná procházka)
--------------------------------
Jak funguje:
- Začíná v náhodném bodě
- "Opilý" chodec se náhodně pohybuje po mapě
- Kde projde, tam vytváří volný prostor
- Pokračuje, dokud není vygenerován požadovaný poměr volného prostoru

Výhody:
- Velmi jednoduchý na implementaci
- Vytváří organické nepravidelné chodby
- Generuje zajímavé průchozí trasy

Nevýhody:
- Může vytvářet příliš chaotické struktury
- Často vznikají slepé uličky
- Není vhodný pro strukturované dungeony

Využití:
- Bludiště
- Tunely mezi místnostmi
- Organické struktury jako doplněk k jiným algoritmům""",

    "Wave Function Collapse": """Wave Function Collapse (WFC)
------------------------
Jak funguje:
- Inspirováno kvantovou mechanikou
- Používá předem definované vzory nebo pravidla
- Iterativně kolapsuje možnosti každé buňky podle okolí
- Vytváří koherentní vzory respektující lokální omezení

Výhody:
- Generuje vysoce strukturované výsledky
- Může vytvářet velmi specifické typy dungeonů
- Dobře funguje se šablonami a vzory

Nevýhody:
- Složitější na implementaci
- Může uvíznout v neřešitelných konfiguracích
- Vyžaduje dobře definované vzory nebo pravidla

Využití:
- Komplexní strukturované dungeony
- Kombinace různých biómů nebo architektonických stylů
- Procedurální generování s konzistentními vzory""",

    "Perlin Noise": """Perlin Noise
-----------
Jak funguje:
- Generuje souvislý šum s kontrolovatelnou úrovní detailů
- Využívá matematické funkce pro vytvoření hladkých přechodů
- Kombinuje více vrstev šumu pro různé úrovně detailů (oktávy)

Výhody:
- Přirozené a plynulé přechody
- Dobře se škáluje pro různé velikosti map
- Vhodný pro generování terénu a krajin

Nevýhody:
- Není ideální pro strukturované dungeony
- Vyžaduje dodatečné zpracování pro vytvoření chodeb
- Může být výpočetně náročnější

Využití:
- Krajiny a venkovní prostředí
- Jeskynní systémy
- Podzemní labyrinty s přirozenými prvky"""
}

def main() -> None:
    """Hlavní funkce programu."""
    while True:
        term_width, _ = shutil.get_terminal_size()
        divider = "─" * term_width

        print("\n╔" + "═" * (term_width - 2) + "╗")
        print("║" + " TermDungeon Generator ".center(term_width - 2) + "║")
        print("╠" + "═" * (term_width - 2) + "╣")
        print("║ 1) BSP Dungeon".ljust(term_width - 2) + "║")
        print("║ 2) Cellular Automata".ljust(term_width - 2) + "║")
        print("║ 3) Drunkard's Walk".ljust(term_width - 2) + "║")
        print("║ 4) Wave Function Collapse".ljust(term_width - 2) + "║")
        print("║ 5) Perlin Noise".ljust(term_width - 2) + "║")
        print("║ 6) Exit".ljust(term_width - 2) + "║")
        print("╚" + "═" * (term_width - 2) + "╝")

        prompt = "Vyber algoritmus (1-6), 'číslo_i' pro info, 'číslo_s' pro zdrojový kód, 'číslo_p' pro parametry: "
        choice = input(prompt).strip()
        
        # Defaultní rozměry dungeonu
        width = DEFAULT_WIDTH
        height = DEFAULT_HEIGHT
        
        # Zpracování informací o algoritmu
        if choice.endswith('i'):
            algo_num = choice[:-1]
            if algo_num in ["1", "2", "3", "4", "5"]:
                algo_name = get_algo_name(algo_num)
                show_algorithm_info(algo_name)
            else:
                print("Neplatná volba, zkus to znovu.")
            continue
        
        # Zobrazení zdrojového kódu algoritmu
        elif choice.endswith('s'):
            algo_num = choice[:-1]
            show_source_code(algo_num)
            continue
            
        # Zadání specifických parametrů
        elif choice.endswith('p'):
            algo_num = choice[:-1]
            if algo_num in ["1", "2", "3", "4", "5"]:
                algo_name = get_algo_name(algo_num)
                dungeon = generate_with_params(algo_num, width, height)
                if dungeon:
                    show_dungeon(dungeon, algo_name)
            else:
                print("Neplatná volba, zkus to znovu.")
            continue
            
        # Generování dungeonu s výchozími parametry
        elif choice in ["1", "2", "3", "4", "5"]:
            algo_name = get_algo_name(choice)
            try:
                dungeon = generate_dungeon(choice, width, height)
                print(divider)
                show_dungeon_with_info(dungeon, ALGO_INFO[algo_name])
            except Exception as e:
                print(f"Chyba při generování dungeonu: {e}")
                
        # Ukončení programu
        elif choice == "6":
            print("Ukončuji program. Na shledanou!")
            sys.exit(0)
            
        # Neplatná volba
        else:
            print("Neplatná volba, zkus to znovu.")
            continue

def get_algo_name(choice: str) -> str:
    """Vrátí název algoritmu podle čísla volby."""
    algorithms = {
        "1": "BSP",
        "2": "Cellular Automata", 
        "3": "Drunkard's Walk",
        "4": "Wave Function Collapse",
        "5": "Perlin Noise"
    }
    return algorithms.get(choice, "")

def show_algorithm_info(algo_name: str) -> None:
    """Zobrazí detailní informace o algoritmu."""
    if algo_name in ALGO_INFO:
        term_width, _ = shutil.get_terminal_size()
        divider = "─" * term_width
        
        print(divider)
        print(ALGO_INFO[algo_name])
        print(divider)
        input("Stiskni Enter pro pokračování...")
    else:
        print("Neplatná volba algoritmu.")

def show_source_code(algo_num: str) -> None:
    """Zobrazí zdrojový kód vybraného algoritmu."""
    file_paths = {
        "1": "dungeon_generators/bsp_generator.py",
        "2": "dungeon_generators/cellular_automata.py",
        "3": "dungeon_generators/drunkards_walk.py",
        "4": "dungeon_generators/wave_function_collapse.py",
        "5": "dungeon_generators/perlin_generator.py"
    }
    
    if algo_num in file_paths:
        file_path = file_paths[algo_num]
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                print("\n" + "─" * 80)
                print(f"Zdrojový kód: {file_path}")
                print("─" * 80)
                print(file.read())
                print("─" * 80)
                input("Stiskni Enter pro pokračování...")
        except FileNotFoundError:
            print(f"Soubor {file_path} nebyl nalezen.")
    else:
        print("Neplatná volba algoritmu.")

def generate_with_params(algo_num: str, width: int, height: int) -> List[List[str]]:
    """Generuje dungeon se specifickými parametry od uživatele."""
    generators = {
        "1": (generate_bsp_dungeon, "BSP", ["max_depth (int): Maximální hloubka dělení"]),
        "2": (generate_cellular_automata_dungeon, "Cellular Automata", 
              ["iterations (int): Počet iterací", "wall_prob (float): Pravděpodobnost zdi"]),
        "3": (generate_drunkards_walk, "Drunkard's Walk", 
              ["floor_ratio (float): Poměr podlahy k celkové ploše"]),
        "4": (generate_wfc_dungeon, "Wave Function Collapse", 
              ["room_attempts (int): Počet pokusů o místnost", 
               "room_min_size (int): Minimální velikost místnosti", 
               "room_max_size (int): Maximální velikost místnosti"]),
        "5": (generate_perlin_dungeon, "Perlin Noise", 
              ["scale (float): Měřítko šumu", "octaves (int): Počet oktáv", 
               "threshold (float): Práh pro generování zdí"])
    }
    
    if algo_num in generators:
        generator_func, algo_name, param_descriptions = generators[algo_num]
        
        print(f"\nParametry pro {algo_name}:")
        for desc in param_descriptions:
            print(f"- {desc}")
            
        params_input = input("\nZadejte parametry oddělené čárkami (např. 5,0.45): ").strip()
        
        try:
            # Převod vstupních parametrů na správné typy
            params = []
            if params_input:
                for i, param in enumerate(params_input.split(',')):
                    # Detekce typu parametru podle popisu
                    if "int" in param_descriptions[min(i, len(param_descriptions)-1)]:
                        params.append(int(param))
                    elif "float" in param_descriptions[min(i, len(param_descriptions)-1)]:
                        params.append(float(param))
                    else:
                        params.append(param)
            
            # Generování dungeonu s parametry
            return generator_func(width, height, *params)
        except Exception as e:
            print(f"Chyba při zpracování parametrů: {e}")
            return None
    else:
        print("Neplatná volba algoritmu.")
        return None

def generate_dungeon(choice: str, width: int, height: int) -> List[List[str]]:
    """Generuje dungeon podle vybrané metody s výchozími parametry."""
    generators = {
        "1": generate_bsp_dungeon,
        "2": generate_cellular_automata_dungeon,
        "3": generate_drunkards_walk,
        "4": generate_wfc_dungeon,
        "5": generate_perlin_dungeon
    }
    
    generator = generators.get(choice)
    if generator:
        return generator(width, height)
    else:
        raise ValueError("Neplatná volba algoritmu")

def show_dungeon(dungeon: List[List[str]], algo_name: str) -> None:
    """Zobrazí vygenerovaný dungeon."""
    term_width, _ = shutil.get_terminal_size()
    divider = "─" * term_width
    
    print(divider)
    print(f"Algoritmus: {algo_name}")
    print(divider)
    
    for row in dungeon:
        print("".join(row))
    
    print(divider)
    input("Stiskni Enter pro pokračování...")

def show_dungeon_with_info(dungeon: List[List[str]], info: str) -> None:
    """Zobrazí dungeon vlevo a vysvětlení vpravo."""
    term_width, _ = shutil.get_terminal_size()
    split_pos = max(30, term_width // 2)  # Pozice oddělení dungeonu a textu

    # Rozdělení info textu na řádky
    info_lines = info.split("\n")
    
    # Zobrazení dungeonu a info vedle sebe
    for i, row in enumerate(dungeon):
        row_str = "".join(row)
        info_line = info_lines[i] if i < len(info_lines) else ""
        print(f"{row_str.ljust(split_pos)} {info_line}")
    
    # Pokud je info delší než dungeon, zobrazí se zbývající řádky
    if len(info_lines) > len(dungeon):
        for i in range(len(dungeon), len(info_lines)):
            print(" " * split_pos + " " + info_lines[i])
    
    input("\nStiskni Enter pro pokračování...")

if __name__ == "__main__":
    # Vytvoření adresářové struktury, pokud neexistuje
    os.makedirs("dungeon_generators", exist_ok=True)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram byl ukončen uživatelem.")
        sys.exit(0)
