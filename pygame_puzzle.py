# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:53:03 2024

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:31:49 2024

@author: user
"""

import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("n-Puzzle k-Swap")
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)

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
        # Le premier déplacement effectué par le joueur est numéroté 𝑑 = 1. Si 𝑑 𝑚𝑜𝑑 𝑘 = 0, le 𝑑-ième déplacement est un
swap
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
    global rows, cols, tile_size, k_swap
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

                if button_4x4.collidepoint(mouse_pos):
                    selected_size = 4
                    rows, cols = 4, 4
                    tile_size = WIDTH // 4

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                elif event.key == pygame.K_RETURN:
                    if selected_size and input_text.isdigit():  # Vérifie que tout est sélectionné
                        k_swap = int(input_text)
                        menu_running = False

                elif event.unicode.isdigit():
                    input_text += event.unicode

# Boucle principale
def main_game():
    global swap_mode, move_count, grid
    grid = create_grid(rows, cols)
    running = True
    selected_tiles = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // tile_size, x // tile_size

                if swap_mode:
                    # Mode swap actif : Sélection de deux tuiles
                    selected_tiles.append((row, col))
                    if len(selected_tiles) == 2:
                        swap_tiles(grid, selected_tiles[0], selected_tiles[1])
                        swap_mode = False
                        selected_tiles = []
                else:
                    # Mode normal : déplacement
                    move_tile(grid, row, col)

        draw_grid(grid, selected_tiles)
        
        # Afficher le mode actuel
        if swap_mode:
            swap_text = font.render("Swap Mode Active!", True, RED)
            screen.blit(swap_text, (10, HEIGHT - 50))
        
        if check_win(grid):
            win_text = font.render("You Win!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))

        pygame.display.flip()

# Lancer le menu
show_start_menu()
main_game()

pygame.quit()
