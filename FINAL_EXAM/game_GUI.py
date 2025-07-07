import tkinter as tk
import random
from tkinter import messagebox
import pickle
from sklearn.preprocessing import LabelEncoder
# Déclarations globales
Table = [[' ' for _ in range(3)] for _ in range(3)]
Player = 'X'
Computer = 'O'
buttons = [[None for _ in range(3)] for _ in range(3)]

def reset_table():
    global Table
    Table = [[' ' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = ' '
            buttons[i][j]['state'] = 'normal'

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
    for i in range(3):
        if Table[i][0] == Table[i][1] == Table[i][2] != ' ':
            return True
    return False

def vertical():
    for i in range(3):
        if Table[0][i] == Table[1][i] == Table[2][i] != ' ':
            return True
    return False

def game_over():
    return diagonal() or horizontal() or vertical() or not find_free_place()

# def action_computer(): #aleatoire
#     if not find_free_place():
#         return
#     while True:
#         x = random.randint(0, 2)
#         y = random.randint(0, 2)
#         if Table[x][y] == ' ':
#             Table[x][y] = Computer
#             buttons[x][y]['text'] = Computer
#             buttons[x][y]['state'] = 'disabled'
#             break
#     if game_over():
#         end_game()

def action_player(x, y):
    if Table[x][y] == ' ':
        Table[x][y] = Player
        buttons[x][y]['text'] = Player
        buttons[x][y]['state'] = 'disabled'
        if game_over():
            end_game()
        else:
            root.after(300, action_computer)

def end_game():
    winner = None
    if diagonal() or horizontal() or vertical():
        winner = "Vous" if any(Table[i][j] == Player for i in range(3) for j in range(3)) else "Ordinateur"
        message = f"{winner} avez gagné !" if winner == "Vous" else "L'ordinateur a gagné !"
    else:
        message = "Match nul !"

    messagebox.showinfo("Fin du jeu", message)
    if messagebox.askyesno("Rejouer ?", "Voulez-vous rejouer ?"):
        reset_table()
    else:
        root.quit()


# -------------------------------
#  Nouvelle fonction IA : Minimax
# -------------------------------
def minimax(is_maximizing):
    if diagonal() or horizontal() or vertical():
        if is_maximizing:
            return -1  # joueur gagne
        else:
            return 1   # ordinateur gagne
    if not find_free_place():
        return 0  # match nul

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if Table[i][j] == ' ':
                    Table[i][j] = Computer
                    score = minimax(False)
                    Table[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if Table[i][j] == ' ':
                    Table[i][j] = Player
                    score = minimax(True)
                    Table[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

# -------------------------------------
# TA FONCTION ActionComputer AMÉLIORÉE  #minmax
# -------------------------------------
# def action_computer():
#     best_score = -float('inf')
#     best_move = None
#     for i in range(3):
#         for j in range(3):
#             if Table[i][j] == ' ':
#                 Table[i][j] = Computer
#                 score = minimax(False)
#                 Table[i][j] = ' '
#                 if score > best_score:
#                     best_score = score
#                     best_move = (i, j)
#     if best_move:
#         x, y = best_move
#         Table[x][y] = Computer
#         buttons[x][y]['text'] = Computer
#         buttons[x][y]['state'] = 'disabled'
#     if game_over():
#         end_game()

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Tic Tac Toe - Version GUI")

# Création de la grille de boutons
for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text=' ', font=("Arial", 40), width=5, height=2,
                        command=lambda x=i, y=j: action_player(x, y))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn

#partie preprocessung
mapping = {'X': 1, 'O': -1, ' ': 0}  # pour transformer la table en vecteur

def flatten_table(table):
    return [mapping[cell] for row in table for cell in row]


#action_computer IA
def action_computer():
    with open('model/tic_tac_toe_model.pkl', 'rb') as f:
        model = pickle.load(f)
    best_score = -1
    best_move = None

    for i in range(3):
        for j in range(3):
            if Table[i][j] == ' ':
                Table[i][j] = Computer  # tester ce coup
                flat = flatten_table(Table)
    
                score = model.predict_proba([flat])[0][0]  # proba d’être class=1 (gagnant)
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
                Table[i][j] = ' '  # annuler le coup
    if best_move:
        x, y = best_move
        Table[x][y] = Computer
        buttons[x][y]['text'] = Computer
        buttons[x][y]['state'] = 'disabled'

    if game_over():
        end_game()

# Lancement du jeu
reset_table()
root.mainloop()
