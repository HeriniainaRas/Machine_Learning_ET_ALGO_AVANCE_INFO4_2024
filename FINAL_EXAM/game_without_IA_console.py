import random

# Déclarations globales
Table = [[' ' for _ in range(3)] for _ in range(3)]
Player = 'X'
Computer = 'O'

# Fonctions
def reset_table():
    global Table
    Table = [[' ' for _ in range(3)] for _ in range(3)]

def print_table():
    print("  1   2   3")
    for i in range(3):
        print(" " + "---+" * 2 + "---")
        row = " | ".join(Table[i])
        print(f"{i+1}| {row} |")
    print(" " + "---+" * 2 + "---")

def action_player():
    while True:
        try:
            x = int(input("Ligne (1-3): ")) - 1
            y = int(input("Colonne (1-3): ")) - 1
            if 0 <= x < 3 and 0 <= y < 3 and Table[x][y] == ' ':
                Table[x][y] = Player
                break
            else:
                print("Position invalide ou déjà occupée.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer des nombres.")

def action_computer():
    if not find_free_place():
        return
    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if Table[x][y] == ' ':
            Table[x][y] = Computer
            break

def transition():
    print_table()
    while not game_over():
        action_player()
        if game_over():
            break
        action_computer()
        print_table()
    print("GAME OVER!")
    print_table()

def find_free_place():
    for i in range(3):
        for j in range(3):
            if Table[i][j] == ' ':
                return True
    return False

def diagonal():
    return (
        (Table[0][0] == Table[1][1] == Table[2][2] != ' ') or
        (Table[0][2] == Table[1][1] == Table[2][0] != ' ')
    )

def horizontal():
    for row in Table:
        if row[0] == row[1] == row[2] != ' ':
            return True
    return False

def vertical():
    for i in range(3):
        if Table[0][i] == Table[1][i] == Table[2][i] != ' ':
            return True
    return False

def game_over():
    return diagonal() or horizontal() or vertical() or not find_free_place()



# Fonction principale
def main():
    while True:
        reset_table()
        transition()
        choix = input("Rejouer ? (Y/N): ").strip().upper()
        if choix != 'Y':
            break

if __name__ == "__main__":
    main()
