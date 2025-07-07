import pygame
import random
from heapq import heappush, heappop
import heapq
import time
import csv
from datetime import datetime
import os
from nodes import Node
from algo_Astar import a_star
from heuristic import *
from algo_Astar import get_neighbors
# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("n-Puzzle k-Swap")
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Variables globales
tile_size = WIDTH // 3  # Taille initiale pour 3x3
rows, cols = 3, 3       # Valeurs par défaut
k_swap = 3              # Valeur par défaut pour k
move_count = 0
swap_mode = False

# Initialisation de la grille
def create_grid(rows, cols):
    numbers = list(range(1, rows * cols)) + [""]
    random.shuffle(numbers)
    grid = [numbers[i * cols:(i + 1) * cols] for i in range(rows)]
    return grid

grid = []

# Dessin de la grille
def draw_grid(grid, selected_tiles=None):
    screen.fill(WHITE)
    for i in range(rows):
        for j in range(cols):
            x, y = j * tile_size, i * tile_size
            color = GRAY
            if selected_tiles and (i, j) in selected_tiles:
                color = BLUE  # Marquer les tuiles sélectionnées pour le swap
            pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
            if grid[i][j] != "":
                num_text = font.render(str(grid[i][j]), True, BLACK)
                screen.blit(num_text, (x + tile_size // 2 - 10, y + tile_size // 2 - 20))

# Déplacement de pièces
def move_tile(grid, row, col):
    global move_count, swap_mode
    # Trouver l'espace vide
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "":
                empty_row, empty_col = i, j

    # Vérifier si le déplacement est valide (adjacent)
    if abs(empty_row - row) + abs(empty_col - col) == 1:
        grid[empty_row][empty_col], grid[row][col] = grid[row][col], grid[empty_row][empty_col]
        move_count += 1
        if k_swap == 0:
            swap_mode = False
        elif move_count % k_swap == 0:  
            swap_mode = True  # Activer le mode swap

# Mode Swap
def swap_tiles(grid, pos1, pos2):
    grid[pos1[0]][pos1[1]], grid[pos2[0]][pos2[1]] = grid[pos2[0]][pos2[1]], grid[pos1[0]][pos1[1]]

# Vérification de victoire
def check_win(grid):
    correct = list(range(1, rows * cols)) + [""]
    flat_grid = [tile for row in grid for tile in row]
    return flat_grid == correct

# Menu de démarrage avec boutons radio
def show_start_menu():
    global rows, cols, tile_size, k_swap, puzzle_size_selected  # Ajoutez cette variable
    menu_running = True
    input_text = ""  # Pour la saisie de k
    selected_size = None  # Pour savoir si 3x3 ou 4x4 est sélectionné

    # Définir les positions des boutons
    button_3x3 = pygame.Rect(WIDTH // 2 - 150, 150, 300, 50)
    button_4x4 = pygame.Rect(WIDTH // 2 - 150, 250, 300, 50)

    while menu_running:
        screen.fill(WHITE)

        # Afficher le titre
        title = font.render("Choisissez la configuration", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 250, 50))

        # Dessiner les boutons radio
        pygame.draw.rect(screen, GREEN if selected_size == 3 else GRAY, button_3x3)
        pygame.draw.rect(screen, GREEN if selected_size == 4 else GRAY, button_4x4)

        # Ajouter les textes sur les boutons
        option_3x3 = small_font.render("Puzzle 3x3", True, BLACK)
        option_4x4 = small_font.render("Puzzle 4x4", True, BLACK)
        screen.blit(option_3x3, (WIDTH // 2 - 100, 165))
        screen.blit(option_4x4, (WIDTH // 2 - 100, 265))

        # Champ pour entrer k
        prompt_k = font.render("Entrez la valeur de k :", True, BLACK)
        screen.blit(prompt_k, (WIDTH // 2 - 200, 400))
        input_surface = font.render(input_text, True, BLUE)
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 100, 450, 200, 50))
        screen.blit(input_surface, (WIDTH // 2 - 90, 460))

        # Instructions pour démarrer
        start_game_text = font.render("Appuyez sur Entrée pour commencer", True, BLACK)
        screen.blit(start_game_text, (WIDTH // 2 - 250, 550))

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if button_3x3.collidepoint(mouse_pos):
                    selected_size = 3
                    rows, cols = 3, 3
                    tile_size = WIDTH // 3
                    puzzle_size_selected = False  # Puzzle 3x3 sélectionné

                if button_4x4.collidepoint(mouse_pos):
                    selected_size = 4
                    rows, cols = 4, 4
                    tile_size = WIDTH // 4
                    puzzle_size_selected = True  # Puzzle 4x4 sélectionné

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                elif event.key == pygame.K_RETURN:
                    if selected_size and input_text.isdigit():  # Vérifie que tout est sélectionné
                        k_swap = int(input_text)
                        menu_running = False

                elif event.unicode.isdigit():
                    input_text += event.unicode


# Résolution avec l'algorithme A*
def solve_puzzle(grid, screen):
    # Initialisation du chronomètre
    start_time = time.time()
    
    # Tentative de résolution
    solution = a_star(grid, k_swap)
    
    # Calcul du temps d'exécution
    execution_time = time.time() - start_time
    
    # Préparation des données pour le CSV
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = solution is not None
    nb_moves = len(solution) - 1 if solution else 0
    
    # Données à enregistrer
    data = {
        'date': current_date,
        'taille_grille': f"{rows}x{cols}",
        'k_swap': k_swap,
        'temps_execution': round(execution_time, 3),
        'nb_mouvements': nb_moves,
        'succes': 'Oui' if success else 'Non'
    }
    
    # Export vers CSV
    csv_filename = 'puzzle_solutions.csv'
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    
    # Affichage de la solution si elle existe
    if solution:
        for step in solution:
            draw_grid(step)
            pygame.display.update()
            pygame.time.delay(200)
        
        # Afficher le message "You Win!"
        win_text = font.render("You Win!", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
        
        # Afficher les statistiques
        stats_text = small_font.render(f"Temps: {round(execution_time, 2)}s | Mouvements: {nb_moves}", True, BLUE)
        screen.blit(stats_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        
        pygame.display.update()
        pygame.time.delay(2000)
        return True
    else:
        print("Aucune solution trouvée.")
        return False
    solution = a_star(grid, k_swap)
    if solution:
        for step in solution:
            draw_grid(step)
            pygame.display.update()
            pygame.time.delay(200)
        
        # Afficher le message "You Win!" à la fin
        win_text = font.render("You Win!", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(1000)  # Afficher le message pendant 1 seconde
        return True
    else:
        print("Aucune solution trouvée.")
        return False

# Choix du mode de jeu
def choose_game_mode():
    mode_selected = None
    menu_running = True

    button_manual = pygame.Rect(WIDTH // 2 - 150, 200, 300, 50)
    button_auto = pygame.Rect(WIDTH // 2 - 150, 300, 300, 50)

    while menu_running:
        screen.fill(WHITE)

        # Afficher le titre
        title = font.render("Choisissez le mode de jeu", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 250, 100))

        # Dessiner les boutons
        pygame.draw.rect(screen, GREEN if mode_selected == "manual" else GRAY, button_manual)
        pygame.draw.rect(screen, GREEN if mode_selected == "auto" else GRAY, button_auto)

        # Ajouter le texte pour les deux modes
        option_manual = small_font.render("Mode Manuel", True, BLACK)
        option_auto = small_font.render("Mode Automatique", True, BLACK)
        screen.blit(option_manual, (WIDTH // 2 - 100, 215))
        screen.blit(option_auto, (WIDTH // 2 - 100, 315))

        # Instructions pour démarrer
        start_game_text = font.render("Appuyez sur Entrée pour continuer", True, BLACK)
        screen.blit(start_game_text, (WIDTH // 2 - 250, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if button_manual.collidepoint(mouse_pos):
                    mode_selected = "manual"

                if button_auto.collidepoint(mouse_pos):
                    mode_selected = "auto"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and mode_selected:
                return mode_selected
    mode_selected = None
    menu_running = True

    button_manual = pygame.Rect(WIDTH // 2 - 150, 200, 300, 50)
    button_auto = pygame.Rect(WIDTH // 2 - 150, 300, 300, 50)

    while menu_running:
        screen.fill(WHITE)

        # Afficher le titre
        title = font.render("Choisissez le mode de jeu", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 250, 100))

        # Dessiner les boutons
        pygame.draw.rect(screen, GREEN if mode_selected == "manual" else GRAY, button_manual)

        # Afficher le bouton "Mode Automatique" seulement si puzzle 3x3 est sélectionné
        if not puzzle_size_selected:  # Si puzzle 3x3 est sélectionné
            pygame.draw.rect(screen, GREEN if mode_selected == "auto" else GRAY, button_auto)

            # Ajouter le texte du bouton "Mode Automatique"
            option_auto = small_font.render("Mode Automatique", True, BLACK)
            screen.blit(option_auto, (WIDTH // 2 - 100, 315))

        # Ajouter le texte pour le mode manuel
        option_manual = small_font.render("Mode Manuel", True, BLACK)
        screen.blit(option_manual, (WIDTH // 2 - 100, 215))

        # Instructions pour démarrer
        start_game_text = font.render("Appuyez sur Entrée pour continuer", True, BLACK)
        screen.blit(start_game_text, (WIDTH // 2 - 250, 400))

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if button_manual.collidepoint(mouse_pos):
                    mode_selected = "manual"

                if not puzzle_size_selected and button_auto.collidepoint(mouse_pos):  # Condition pour mode auto seulement si puzzle 3x3
                    mode_selected = "auto"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and mode_selected:
                return mode_selected

# Boucle principale
def main_game():
    global swap_mode, move_count, grid
    grid = create_grid(rows, cols)
    game_mode = choose_game_mode()

    if game_mode == "auto":
        if solve_puzzle(grid, screen):
            return True
        return False

    running = True
    selected_tiles = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and not check_win(grid):
                x, y = pygame.mouse.get_pos()
                row, col = y // tile_size, x // tile_size

                if swap_mode:
                    selected_tiles.append((row, col))
                    if len(selected_tiles) == 2:
                        swap_tiles(grid, selected_tiles[0], selected_tiles[1])
                        swap_mode = False
                        selected_tiles = []
                else:
                    move_tile(grid, row, col)

        draw_grid(grid, selected_tiles)

        if swap_mode:
            swap_text = font.render("Swap Mode Active!", True, GREEN)
            screen.blit(swap_text, (10, HEIGHT - 50))

        if check_win(grid):
            # Afficher le message "You Win!" avant de retourner au menu
            win_text = font.render("You Win!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(1000)  # Afficher le message pendant 1 seconde
            return True

        pygame.display.flip()

def run_game():
    running = True
    while running:
        show_start_menu()
        restart = main_game()
        if not restart:
            running = False

if __name__ == "__main__":
    run_game()
    pygame.quit()
    run_game()
    pygame.quit()
