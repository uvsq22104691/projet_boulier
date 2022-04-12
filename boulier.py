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
    global canvas, root, G_boules, G_boules_Val, mode, L_boules
    canvas.delete("all")
    G_boules = [[0] * 5 for _ in range(N)]
    L_boules = [0] * N
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
        # Créer un label sous chaque ligne verticale pour afficher la valeur de la colonne
        L_boules[i] = tk.Label(root, text=G_boules_Val[i], font=("Arial", 20), bg="black", fg="white")
        L_boules[i].place(x=WIDTH / (N + 1) * (N - i) - L_boules[i].winfo_reqwidth() / 2, y=HEIGHT - L_boules[i].winfo_reqheight())


def click(i, j):
    ''' Fonction qui gère le clic sur la boule en (i, j)
        i : colonne de la boule en partant de la droite
        j : ligne de la boule en partant du haut'''
    global G_boules, G_boules_Val
    if mode == 0:
        if canvas.itemcget(G_boules[i][j], 'fill') in COLOR_DESACTIVE:
            if j == 0:
                if canvas.itemcget(G_boules[i][j], 'fill') in COLOR_DESACTIVE:
                    canvas.itemconfig(G_boules[i][j], fill=COLOR_ACTIVE[min(i // 3, len(COLOR_ACTIVE) - 1)])
                    canvas.move(G_boules[i][j], 0, HEIGHT / 8)
                    G_boules_Val[i] += 5
            else:
                for k in range(1, j + 1):
                    if canvas.itemcget(G_boules[i][k], 'fill') in COLOR_DESACTIVE:
                        canvas.itemconfig(G_boules[i][k], fill=COLOR_ACTIVE[min(i // 3, len(COLOR_ACTIVE) - 1)])
                        canvas.move(G_boules[i][k], 0, -HEIGHT / 8)
                        G_boules_Val[i] += 1
            L_boules[i].config(text=G_boules_Val[i])
        else:
            if j == 0:
                if canvas.itemcget(G_boules[i][j], 'fill') in COLOR_ACTIVE:
                    canvas.itemconfig(G_boules[i][j], fill=COLOR_DESACTIVE[min(i // 3, len(COLOR_DESACTIVE) - 1)])
                    canvas.move(G_boules[i][j], 0, -HEIGHT / 8)
                    G_boules_Val[i] -= 5
            else:
                for k in range(j, 5):
                    if canvas.itemcget(G_boules[i][k], 'fill') in COLOR_ACTIVE:
                        canvas.itemconfig(G_boules[i][k], fill=COLOR_DESACTIVE[min(i // 3, len(COLOR_DESACTIVE) - 1)])
                        canvas.move(G_boules[i][k], 0, HEIGHT / 8)
                        G_boules_Val[i] -= 1
            L_boules[i].config(text=G_boules_Val[i])


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

    # Création du Menu
    menuBar = tk.Menu(root)

    # Création du menu Fichier
    menu_file = tk.Menu(menuBar, tearoff=0)
    menu_file.add_command(label="Réinitialiser", command=init)
    menu_file.add_command(label="Charger", command=charger)
    menu_file.add_command(label="Sauvegarder", command=sauvegarder)

    # Création du menu Options
    menu_options = tk.Menu(menuBar, tearoff=0)
    menu_options.add_command(label="Options", command=open_fen_options)

    # Ajout des menus au menuBar
    menuBar.add_cascade(label="Fichier", menu=menu_file)
    menuBar.add_cascade(label="Options", menu=menu_options)

    root.config(menu=menuBar)
    # Création des widgets
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)

    # Placement des widgets
    canvas.grid(row=0, column=0, columnspan=4)

    # Bind des événements

    # Initialisation du boulier
    init()

    # Lancement de la boucle principale
    root.mainloop()


main()
