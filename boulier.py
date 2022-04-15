                                                                                                                        # coding: utf-8

# INFORMATION GROUPE
# GROUPE MI TD 03
# Mathis ALLOUCHE
# jennifer said
# xavier koubonou
# https://github.com/uvsq22104691/projet_boulier


# Import des modules
import tkinter as tk
import tkinter.filedialog as fd
import time
import os
import threading as th
from win32api import GetSystemMetrics

# Constantes
# Nombre de colonnes du boulier
N = 6

# Largeur et hauteur de l'écran
WIDTH_SCREEN = GetSystemMetrics(0)
HEIGHT_SCREEN = GetSystemMetrics(1)

# Hauteur de la fenêtre
WIDTH = 80 * (N - 1)
HEIGHT = 600

# Vitesse des animations
Vitesse = 0.5

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
def init(reinit=False):
    '''Fonction qui initialise le boulier'''
    global canvas, root, G_boules, G_boules_Val, mode, L_boules, WIDTH, N
    # On redimensionne la fenêtre
    WIDTH = 80 * (N - 1)
    root.geometry(f"{WIDTH}x{HEIGHT}+{int((WIDTH_SCREEN - WIDTH) / 2)}+{int((HEIGHT_SCREEN - HEIGHT) / 2)}")
    canvas.config(width=WIDTH, height=HEIGHT)
    if reinit:
        canvas.delete("all")
        for label in L_boules:
            label.destroy()

    G_boules = [[[None, False] for _ in range(5)] for _ in range(N)]
    L_boules = [0] * N
    G_boules_Val = [0] * N
    mode = 0    # 0 = mode simulation, 1 = mode opératoire
    canvas.config(cursor="arrow")

    # Créer un ligne horizontal au quart de la hauteur de la fenêtre
    canvas.create_line(0, HEIGHT / 4, WIDTH, HEIGHT / 4, fill="darkgrey", width=5)

    # Créer N ligne verticales
    for i in range(N):
        canvas.create_line(WIDTH / (N + 1) * (i + 1), 0, WIDTH / (N + 1) * (i + 1), HEIGHT, fill="darkgrey", width=2)

    # Créer des points blancs entre les lignes verticales
    for i in range(3, N, 3):
        canvas.create_oval(WIDTH / (N + 1) * (N - i + 0.5) - 5, HEIGHT / 4 - 5, WIDTH / (N + 1) * (N - i + 0.5) + 5, HEIGHT / 4 + 5, fill="white")

    # Créer les boules, 1 au dessus de la ligne horizontale, 4 en dessous
    for i in range(N):
        for j in range(5):
            if j == 0:
                G_boules[i][j][0] = canvas.create_oval(
                    WIDTH / (N + 1) * (N - i) - 30,
                    HEIGHT / 8 - HEIGHT / 16 - 30,
                    WIDTH / (N + 1) * (N - i) + 30,
                    HEIGHT / 8 - HEIGHT / 16 + 30,
                    fill=COLOR_DESACTIVE[i // len(COLOR_DESACTIVE) % len(COLOR_DESACTIVE)]
                )
            else:
                G_boules[i][j][0] = canvas.create_oval(
                    WIDTH / (N + 1) * (N - i) - 30,
                    HEIGHT / 4 + ((j + 1) * HEIGHT / 8) - 30,
                    WIDTH / (N + 1) * (N - i) + 30,
                    HEIGHT / 4 + ((j + 1) * HEIGHT / 8) + 30,
                    fill=COLOR_DESACTIVE[i // len(COLOR_DESACTIVE) % len(COLOR_DESACTIVE)],
                )

            # Bind de la fonction click sur chaque boule avec les paramètres i et j représentant la position de la boule
            canvas.tag_bind(G_boules[i][j][0], "<Button-1>", lambda _, i=i, j=j: click(i, j))
        # Créer un label sous chaque ligne verticale pour afficher la valeur de la colonne
        L_boules[i] = tk.Label(root, text=G_boules_Val[i], font=("Arial", 20), bg="black", fg="white")
        L_boules[i].place(x=WIDTH / (N + 1) * (N - i) - L_boules[i].winfo_reqwidth() / 2, y=HEIGHT - L_boules[i].winfo_reqheight())


def click(i, j):
    ''' Fonction qui gère le clic sur la boule en (i, j)
        i : colonne de la boule en partant de la droite
        j : ligne de la boule en partant du haut'''
    global G_boules, G_boules_Val
    if mode == 0:
        if not G_boules[i][j][1]:
            if j == 0:
                canvas.itemconfig(G_boules[i][j][0], fill=COLOR_ACTIVE[i // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
                th.Thread(target=animation, args=(i, j, HEIGHT / 10)).start()
                G_boules_Val[i] += 5
                G_boules[i][j][1] = True
            else:
                for k in range(1, j + 1):
                    if not G_boules[i][k][1]:
                        canvas.itemconfig(G_boules[i][k][0], fill=COLOR_ACTIVE[i // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
                        th.Thread(target=animation, args=(i, k, -HEIGHT / 6)).start()
                        G_boules_Val[i] += 1
                        G_boules[i][k][1] = True
            L_boules[i].config(text=G_boules_Val[i])
        else:
            if j == 0:
                th.Thread(target=animation, args=(i, j, -HEIGHT / 10, 1)).start()
                G_boules_Val[i] -= 5
                G_boules[i][j][1] = False
            else:
                for k in range(j, 5):
                    if G_boules[i][k][1]:
                        th.Thread(target=animation, args=(i, k, HEIGHT / 6, 1)).start()
                        G_boules_Val[i] -= 1
                        G_boules[i][k][1] = False
            L_boules[i].config(text=G_boules_Val[i])


def animation(i, j, y, op=0):
    '''Bouge la boule en (i, j) de (x, y) pixels de facon progressive'''
    global G_boules, canvas
    n = 25
    ti = round((Vitesse) / n, 2)
    for k in range(n):
        if 1:   # TODO: option "clignotement"
            pass
        elif k % 10 == 0:
            canvas.itemconfig(G_boules[i][j][0], fill=COLOR_ACTIVE[i // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
        elif k % 5 == 0:
            canvas.itemconfig(G_boules[i][j][0], fill=COLOR_DESACTIVE[i // len(COLOR_DESACTIVE) % len(COLOR_DESACTIVE)])
        canvas.move(G_boules[i][j][0], 0, y / n)
        if Vitesse != 0:
            canvas.update()
        time.sleep(ti)
    if op == 1:
        canvas.itemconfig(G_boules[i][j][0], fill=COLOR_DESACTIVE[i // len(COLOR_DESACTIVE) % len(COLOR_DESACTIVE)])


def charger():
    '''Fonction qui charge un fichier'''
    # Ouvre une feneêtre de dialogue pour choisir le fichier
    f = fd.askopenfile(
        initialdir=os.getcwd() + "/config/",
        title="charger une config",
        filetypes=(("fichier - projet boulier", "*.boulier"),)
    )

    if f is None:
        return None

    val = eval(f.read())

    global G_boules_Val, L_boules, G_boules, N, Vitesse
    Vitesse_tmp = Vitesse
    # reinitialiser le boulier
    N = len(val)
    init(True)

    # Affecte les valeurs aux variables globales et affiche les valeurs dans les labels
    G_boules_Val = val[::-1]
    for i in range(N):
        L_boules[-(i + 1)]['text'] = val[i]

    # affichier les boules qui doivent etre actives
    Vitesse = 0
    for i in range(N):
        if G_boules_Val[i] >= 5:
            canvas.itemconfig(G_boules[i][0][0], fill=COLOR_ACTIVE[i // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
            G_boules[i][0][1] = True
            animation(i, 0, HEIGHT / 6)
        for j in range(1, 5):
            if G_boules_Val[i] % 5 >= j:
                canvas.itemconfig(G_boules[i][j][0], fill=COLOR_ACTIVE[i // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
                G_boules[i][j][1] = True
                animation(i, j, -HEIGHT / 6)

    Vitesse = Vitesse_tmp


def sauvegarder():
    '''Fonction qui sauvegarde le boulier dans un fichier'''
    fichier = fd.asksaveasfilename(
        initialdir=os.getcwd() + "/config/",
        title="Sauvergarder une config",
        defaultextension=(".boulier"),
        filetypes=(("fichier - projet boulier", "*.boulier"),)
    )

    if not fichier:
        return

    chemin = fichier.split('.')
    if len(chemin) != 2:
        return

    chemin, ext = chemin[:]
    if ext != 'boulier':
        return

    with open(fichier, "w") as f:
        f.write(str(G_boules_Val[::-1]).replace(' ', ''))
        f.close()


def change_vitesse(v):
    '''Fonction qui change la vitesse de l'animation'''
    # TODO: changer la vitesse de l'animation


def change_nb_col(n):
    '''Fonction qui change le nombre de colonnes du boulier'''
    # TODO: changer le nombre de colonnes du boulier


def ouvre_fen_options():
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
    fen_options.geometry("300x200")

    # TODO Ajouter Label "Vitesse: "

    # TODO Ajouter un Scale pour changer la vitesse des animations

    # TODO Ajouter un Label "Nombre de colonnes: "

    # TODO Ajouter une Entry pour changer le nombre de colonnes


    # TODO Ajouter une Checkbutton pour activer/désactiver le clignotement
    CB_clignotement = tk.Checkbutton(fen_options, text="Activer le clignotement")


    # TODO Ajouter un Boutton "Appliquer" pour appliquer les changements
    B_appliquer = tk.Button(fen_options, text = "appliquer")


    # Placement des widgets
    CB_clignotement.grid(row=0, column=0)
    B_appliquer.grid(row=5, column=0)

    # Lancement de la boucle principale
    fen_options.mainloop()


def del_fen_options():
    '''Fonction qui supprime la fenêtre des options'''
    global fen_options
    # Si la fenêtre existe, on la supprime
    if "fen_options" in globals():
        fen_options.destroy()
        del fen_options


def change_mode():
    '''Fonction qui bascule entre le mode simulation et le mode opératoire'''
    global mode
    mode = (mode + 1) % 2
    if mode == 0:
        canvas.config(cursor="arrow")
    else:
        canvas.config(cursor="crosshair")


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
    menu_file.add_command(label="Réinitialiser", command=lambda: init(True))
    menu_file.add_command(label="Charger", command=charger)
    menu_file.add_command(label="Sauvegarder", command=sauvegarder)

    # Création du menu Options
    menu_options = tk.Menu(menuBar, tearoff=0)
    menu_options.add_command(label="Options", command=ouvre_fen_options)

    # Création du menu Mode
    menu_mode = tk.Menu(menuBar, tearoff=0)
    menu_mode.add_command(label="Changer mode", command=change_mode)

    # Ajout des menus au menuBar
    menuBar.add_cascade(label="Fichier", menu=menu_file)
    menuBar.add_cascade(label="Options", menu=menu_options)
    menuBar.add_cascade(label="Mode", menu=menu_mode)

    root.config(menu=menuBar)
    # Création des widgets
    canvas = tk.Canvas(root, bg="black", highlightthickness=0)

    # Placement des widgets
    canvas.grid()

    # Bind des événements

    # Initialisation du boulier
    init()

    # Lancement de la boucle principale
    root.mainloop()


main()
