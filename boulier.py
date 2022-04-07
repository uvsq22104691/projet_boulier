# coding: utf-8

# INFORMATION GROUPE
# GROUPE MI TD 03
# Mathis ALLOUCHE
# jennifer said
# xavier koubonou
# https://github.com/uvsq22104691/projet_boulier


# Import des modules
import tkinter as tk


# Constantes
# Largeur et hauteur de la fenêtre
WIDTH = 1200
HEIGHT = 600

# Nombre de colonnes du boulier
N = 9

# Définition des couleurs
COLOR_DESACTIVE = [
    "#550000",
    "#005500",
    "#000055"
]
COLOR_ACTIVE = [
    "#ff0000",
    "#00ff00",
    "#0000ff"
]


# Fonction
def init():
    '''Fonction qui initialise le boulier'''
    global canvas, G_boules, G_boules_Val, mode
    canvas.delete("all")
    G_boules = [[0] * 5 for _ in range(N)]
    G_boules_Val = [0] * N
    mode = 0    # 0 = mode simulation, 1 = mode opération

    # Créer un ligne horizontal au quart de la hauteur de la fenêtre
    canvas.create_line(0, HEIGHT / 4, WIDTH, HEIGHT / 4, fill="darkgrey", width=5)

    # Créer N ligne verticales
    for i in range(N):
        canvas.create_line(WIDTH / (N + 1) * (i + 1), 0, WIDTH / (N + 1) * (i + 1), HEIGHT, fill="darkgrey", width=2)

    # Créer des point noirs entre les lignes verticales
    for i in range(3, N, 3):
        canvas.create_oval(WIDTH / (N + 1) * (N - i + 0.5) - 5, HEIGHT / 4 - 5, WIDTH / (N + 1) * (N - i + 0.5) + 5, HEIGHT / 4 + 5, fill="black")

    # Créer les boules, 1 au dessus de la ligne horizontale, 4 en dessous
    for i in range(N):
        for j in range(5):
            if j == 0:
                G_boules[i][j] = canvas.create_oval(
                    WIDTH / (N + 1) * (N - i) - 30,
                    HEIGHT / 8 - HEIGHT / 16 - 30,
                    WIDTH / (N + 1) * (N - i) + 30,
                    HEIGHT / 8 - HEIGHT / 16 + 30,
                    fill=COLOR_DESACTIVE[min(i // 3, len(COLOR_DESACTIVE) - 1)]
                )
            else:
                G_boules[i][j] = canvas.create_oval(
                    WIDTH / (N + 1) * (N - i) - 30,
                    HEIGHT / 4 + ((j + 1) * HEIGHT / 8) - 30,
                    WIDTH / (N + 1) * (N - i) + 30,
                    HEIGHT / 4 + ((j + 1) * HEIGHT / 8) + 30,
                    fill=COLOR_DESACTIVE[min(i // 3, len(COLOR_DESACTIVE) - 1)],
                )

            # Bind de la fonction click sur chaque boule avec les paramètres i et j représentant la position de la boule
            canvas.tag_bind(G_boules[i][j], "<Button-1>", lambda _, i=i, j=j: click(i, j))


def click(i, j):
    ''' Fonction qui gère le clic sur la boule en (i, j)
        i : colonne de la boule en partant de la droite
        j : ligne de la boule en partant du haut'''
    global G_boules, G_boules_Val
    # TODO


def charger():
    '''Fonction qui charge un fichier'''
    # TODO
    pass


def sauvegarder():
    '''Fonction qui sauvegarde le boulier dans un fichier'''
    # TODO
    pass


def open_fen_options():
    '''Fonction qui ouvre la fenêtre des options'''
    global fen_options
    # Si la fenêtre des options existe déjà, on la met au premier plan
    if "fen_options" in globals():
        fen_options.focus_force()
        return
    # Sinon, on crée la fenêtre
    fen_options = tk.Toplevel()
    fen_options.title("Options")
    fen_options.wm_protocol("WM_DELETE_WINDOW", del_fen_options)

    # Lancement de la boucle principale
    fen_options.mainloop()


def del_fen_options():
    '''Fonction qui supprime la fenêtre des options'''
    global fen_options
    # Si la fenêtre existe, on la supprime
    if "fen_options" in globals():
        fen_options.destroy()
        del fen_options


def main():
    '''Fonction principale, initailise le programme et l'interface graphique et lance la boucle principale'''
    # déclaration des variables globales
    global root, canvas

    # Céation de la fenêtre principale
    root = tk.Tk()
    root.title("Boulier")
    root.resizable(False, False)
    root.configure(bg="darkgrey")

    # Création des widgets
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)

    B_charger = tk.Button(root, text="Charger", command=charger)
    B_sauvegarder = tk.Button(root, text="Sauvegarder", command=sauvegarder)
    B_reinitialiser = tk.Button(root, text="Réinitialiser", command=init)
    B_options = tk.Button(root, text="Options", command=open_fen_options)

    # Placement des widgets
    canvas.grid(row=0, column=0, columnspan=4)
    B_reinitialiser.grid(row=1, column=0)
    B_charger.grid(row=1, column=1)
    B_sauvegarder.grid(row=1, column=2)
    B_options.grid(row=1, column=3)

    # Bind des événements

    # Initialisation du boulier
    init()

    # Lancement de la boucle principale
    root.mainloop()


main()
