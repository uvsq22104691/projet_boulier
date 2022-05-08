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
# Largeur et hauteur de l'écran
WIDTH_SCREEN = GetSystemMetrics(0)
HEIGHT_SCREEN = GetSystemMetrics(1)

# Largeur et Hauteur de la partie opératoire
WIDTH_OP = 300
HEIGHT_OP = 50

# Définition des couleurs
COLOR_DESACTIVE = [
    "#550000",
    "#005500",
    "#000055",
]
COLOR_ACTIVE = [
    "#ff0000",
    "#00ff00",
    "#0000ff",
]

# Variables globales
# Nombre de colonnes du boulier
N = 6

# Hauteur et Largeur de la fenêtre
WIDTH = 80 * (N - 1)
HEIGHT = 600

# Options
# Clignotement
opt_clignotement = True

# Vitesse des animations
Vitesse = 0.5


# Fonctions
def init(reinit=True):
    '''Fonction qui initialise le boulier ou le réinitialise'''
    global canvas, root, G_boules, G_boules_Val, mode, L_boules, L_boules_op, WIDTH, N, Line

    # On redimensionne la fenêtre
    WIDTH = 70 * (N + 1)

    sym = "+"

    if reinit:
        sym = L_boules_op[-1]['text']
        canvas.delete("all")
        for label in L_boules:
            label.destroy()
        for label in L_boules_op:
            label.destroy()

    L_boules_op = [0] * N
    L_boules_op.append(tk.Label(root, text=sym, font=("Arial", 20), bg="black", fg="white"))
    L_boules_op[-1].place(x=WIDTH / (N + 1) * 0.5 - L_boules_op[-1].winfo_reqwidth() / 2, y=HEIGHT + HEIGHT_OP - L_boules_op[-1].winfo_reqheight())
    for i in range(N):
        L_boules_op[i] = tk.Label(root, text="0", font=("Arial", 20), bg="black", fg="white")
        L_boules_op[i].place(x=WIDTH / (N + 1) * (i + 1) - L_boules_op[i].winfo_reqwidth() / 2, y=HEIGHT + HEIGHT_OP - L_boules_op[i].winfo_reqheight())

    if not reinit:
        mode = 0    # 0 = mode simulation, 1 = mode opératoire
        canvas.config(cursor="arrow")
        menu_operation(root)

    if mode == 0:
        canvas.config(width=WIDTH, height=HEIGHT)
        root.geometry(f"{WIDTH}x{HEIGHT}+{int((WIDTH_SCREEN - WIDTH) / 2)}+{int((HEIGHT_SCREEN - HEIGHT) / 2)}")
    else:
        canvas.config(width=WIDTH, height=HEIGHT + HEIGHT_OP)
        root.geometry(f"{WIDTH + WIDTH_OP}x{HEIGHT + HEIGHT_OP}+{int((WIDTH_SCREEN - (WIDTH + WIDTH_OP)) / 2)}+{int((HEIGHT_SCREEN - (HEIGHT + HEIGHT_OP)) / 2)}")

    G_boules = [[[None, False] for _ in range(5)] for _ in range(N)]
    L_boules = [0] * N
    G_boules_Val = [0] * N

    # Créer un ligne horizontal au quart de la hauteur de la fenêtre
    canvas.create_line(0, HEIGHT / 4, WIDTH, HEIGHT / 4, fill="darkgrey", width=5)

    # Créer N ligne verticales
    Line = [0] * N
    for i in range(N):
        Line[i] = canvas.create_line(WIDTH / (N + 1) * (i + 1), 0, WIDTH / (N + 1) * (i + 1), HEIGHT, fill="darkgrey", width=2)

    # Créer des points blancs entre les lignes verticales
    for i in range(3, N, 3):
        canvas.create_oval(WIDTH / (N + 1) * (N - i + 0.5) - 5, HEIGHT / 4 - 5, WIDTH / (N + 1) * (N - i + 0.5) + 5, HEIGHT / 4 + 5, fill="white")

    # Créer les boules, 1 au dessus de la ligne horizontale, 4 en dessous
    for i in range(N):
        for j in range(5):
            if j == 0:
                G_boules[i][j][0] = canvas.create_oval(
                    WIDTH / (N + 1) * (i + 1) - 30,
                    HEIGHT / 8 - HEIGHT / 16 - 30,
                    WIDTH / (N + 1) * (i + 1) + 30,
                    HEIGHT / 8 - HEIGHT / 16 + 30,
                    fill=COLOR_DESACTIVE[(N - (i + 1)) // 3 % len(COLOR_DESACTIVE)]
                )
            else:
                G_boules[i][j][0] = canvas.create_oval(
                    WIDTH / (N + 1) * (i + 1) - 30,
                    HEIGHT / 4 + ((j + 1) * HEIGHT / 8) - 30,
                    WIDTH / (N + 1) * (i + 1) + 30,
                    HEIGHT / 4 + ((j + 1) * HEIGHT / 8) + 30,
                    fill=COLOR_DESACTIVE[(N - (i + 1)) // 3 % len(COLOR_DESACTIVE)],
                )

            # Bind de la fonction active_boule sur chaque boule avec les paramètres i et j représentant la position de la boule
            canvas.tag_bind(G_boules[i][j][0], "<Button-1>", lambda _, i=i, j=j: active_boule(i, j))
        # Créer un label sous chaque ligne verticale pour afficher la valeur de la colonne
        L_boules[i] = tk.Label(root, text=G_boules_Val[i], font=("Arial", 20), bg="black", fg="white")
        L_boules[i].place(x=WIDTH / (N + 1) * (i + 1) - L_boules[i].winfo_reqwidth() / 2, y=HEIGHT - L_boules[i].winfo_reqheight())


# Fonction utiles pour le projet
def wait(t):
    '''Fonction qui attend t milisecondes, instruction non bloquante pour le GUI'''
    var = tk.IntVar()
    root.after(t, var.set, 1)
    root.wait_variable(var)


# Partie opération
def menu_operation(root):
    '''Création du menu à droite du boulier pour les opérations'''
    global type_Operation, L_sym, nb1, nb2, CB_Add, CB_Sub, CB_Mul, E_nb1, E_nb2, B_Valider

    L_nb1 = tk.Label(root, text="Nombre 1: ", font=("Arial", 12))
    L_sym = tk.Label(root, text="+", font=("Arial", 12))
    L_nb2 = tk.Label(root, text="Nombre 2: ", font=("Arial", 12))

    type_Operation = tk.IntVar(root)
    type_Operation.trace_add('write', lambda *_: operation_change())
    CB_Add = tk.Radiobutton(root, text="Addition", variable=type_Operation, value=0)
    CB_Sub = tk.Radiobutton(root, text="Soustraction", variable=type_Operation, value=1)
    CB_Mul = tk.Radiobutton(root, text="Multiplication", variable=type_Operation, value=2)
    CB_Add.select()

    nb1 = tk.StringVar(root)
    nb2 = tk.StringVar(root)

    nb1.set("0")
    nb2.set("0")

    nb1.trace_add("write", lambda *_: check(nb1))
    nb2.trace_add("write", lambda *_: check(nb2))

    E_nb1 = tk.Entry(root, font=("Arial", 12), width=21, textvariable=nb1)
    E_nb2 = tk.Entry(root, font=("Arial", 12), width=21, textvariable=nb2)

    B_Valider = tk.Button(root, text="Valider", font=("Arial", 12), command=lambda: operation(nb1.get(), nb2.get()))

    # Placement des widgets
    CB_Add.grid(row=0, column=1)
    CB_Sub.grid(row=0, column=2)
    CB_Mul.grid(row=1, column=1, columnspan=2)

    L_nb1.grid(row=2, column=1)
    L_sym.grid(row=3, column=1)
    L_nb2.grid(row=4, column=1)

    E_nb1.grid(row=2, column=2)
    E_nb2.grid(row=4, column=2)

    B_Valider.grid(row=5, column=1, columnspan=2)


def check(var):
    '''Fonction qui vérifie si le nombre entré est correct'''
    tmp = var.get()
    if len(tmp) > 0 and not tmp[-1].isdigit() or len(tmp) > 21:
        var.set(tmp[:-1])


def operation_change():
    '''modifie les labels des opérations lors du clique sur les checkbuttons'''
    global type_Operation, L_sym, L_boules_op
    op = type_Operation.get()
    if op == 0:
        L_boules_op[-1]['text'] = "+"
        L_sym['text'] = "+"
    elif op == 1:
        L_boules_op[-1]['text'] = "-"
        L_sym['text'] = "-"
    elif op == 2:
        L_boules_op[-1]['text'] = "+"
        L_sym['text'] = "*"


def operation(nb1, nb2):
    '''applique l'opération choisie, désactive les boutons pendant le calcul puis les réactive'''
    global type_Operation, CB_Add, CB_Sub, CB_Mul, E_nb1, E_nb2, B_Valider
    op = type_Operation.get()

    CB_Add.config(state=tk.DISABLED)
    CB_Sub.config(state=tk.DISABLED)
    CB_Mul.config(state=tk.DISABLED)
    E_nb1.config(state=tk.DISABLED)
    E_nb2.config(state=tk.DISABLED)
    B_Valider.config(state=tk.DISABLED)

    if op == 0:
        addition(nb1, nb2)
    elif op == 1:
        soustraction(nb1, nb2)
    elif op == 2:
        multiplication(nb1, nb2)

    CB_Add.config(state=tk.NORMAL)
    CB_Sub.config(state=tk.NORMAL)
    CB_Mul.config(state=tk.NORMAL)
    E_nb1.config(state=tk.NORMAL)
    E_nb2.config(state=tk.NORMAL)
    B_Valider.config(state=tk.NORMAL)


def affiche(nb: str):
    '''Fonction qui affiche le nombre nb dans les labels et positionne les boules au bon endroit'''
    global L_boules, G_boules, G_boules_Val, N

    init()

    n = N - len(nb)

    for i, e in enumerate(nb):
        tmp = int(e)
        if tmp >= 5:
            active_boule(n + i, 0, True)
            tmp -= 5

        if tmp > 0:
            active_boule(n + i, tmp, True)


def addition(nb1: int, nb2: int, mult=False):
    ''' Effectue l'addition des deux nombres pas à pas
        nb1: str
        nb2: str
    '''
    global N, L_boules_op

    n = len(str(int(nb1) + int(nb2)))
    nbAff = list(map(int, "0" * (n - len(nb1)) + nb1))
    nb = list(map(int, "0" * (n - len(nb2)) + nb2))
    if not mult:
        N = n
        affiche(nb1)
    for i, e in enumerate(nb):
        L_boules_op[N - len(nb) + i]['text'] = str(e)
        canvas.update()

    wait(2000)

    i = 1
    while nb != [0] * len(nb):
        if nb[-i] == 0:
            i += 1
            continue
        if nb[-i] % 5 != 0:
            if nb[-i] % 5 + nbAff[-i] % 5 < 5:
                active_boule(N - i, nb[-i] % 5 + nbAff[-i] % 5, True)
                nbAff[-i] += nb[-i] % 5
                nb[-i] -= nb[-i] % 5
                L_boules_op[-(i + 1)]['text'] = str(nb[-i])
            else:
                active_boule(N - i, nbAff[-i] % 5 - (5 - nb[-i] % 5) + 1, True)
                nbAff[-i] -= 5 - nb[-i] % 5
                nb[-i] += 5 - nb[-i] % 5
                j = i
                while j <= len(nb):
                    if nb[-j] >= 10:
                        nb[-j] -= 10
                        nb[-(j + 1)] += 1
                        L_boules_op[-(j + 1)]['text'] = str(nb[-j])
                    else:
                        L_boules_op[-(j + 1)]['text'] = str(nb[-j])
                        break
                    j += 1
        if nb[-i] // 5 == 1:
            if nbAff[-i] < 5:
                active_boule(N - i, 0, True)
                nbAff[-i] += 5
                nb[-i] -= 5
                L_boules_op[-(i + 1)]['text'] = str(nb[-i])
            else:
                active_boule(N - i, 0, True)
                nbAff[-i] -= 5
                nb[-i] -= 5
                L_boules_op[-(i + 1)]['text'] = str(nb[-i])
                nb[-i - 1] += 1
                j = i + 1
                while j <= len(nb):
                    if nb[-j] >= 10:
                        nb[-j] -= 10
                        nb[-j - 1] += 1
                        L_boules_op[-j - 1]['text'] = str(nb[-j])
                    else:
                        L_boules_op[-j - 1]['text'] = str(nb[-j])
                        break
                    j += 1

        if nb[-i] == 0:
            i += 1
        wait(1000)

    return "".join(map(str, nbAff))


def soustraction(nb1, nb2):
    ''' Effectue la soustraction des deux nombres pas à pas
        nb1: str
        nb2: str
    '''
    global N, G_boules_Val, L_boules_op
    N = max(len(nb1), len(nb2))
    nb1 = "0" * (N - len(nb1)) + nb1
    affiche(nb1)
    nbAff = list(map(int, nb1))
    nb = list(map(int, "0" * (N - len(nb2)) + nb2))
    for i, e in enumerate(nb):
        L_boules_op[i]['text'] = str(e)

    wait(2000)

    i = N - 1
    while nb != [0] * N:
        if nb[i] == 0:
            i -= 1
            continue
        if nb[i] % 5 != 0:
            if nbAff[i] % 5 - nb[i] % 5 >= 0:
                active_boule(i, nbAff[i] % 5 - nb[i] % 5 + 1, True)
                nbAff[i] -= nb[i] % 5
                nb[i] -= nb[i] % 5
                L_boules_op[i]['text'] = str(nb[i])
            else:
                active_boule(i, nbAff[i] % 5 + (5 - nb[i] % 5), True)
                nbAff[i] += 5 - nb[i] % 5
                nb[i] += 5 - nb[i] % 5
                j = i
                while j >= 0:
                    if nb[j] >= 10:
                        nb[j] -= 10
                        nb[j - 1] += 1
                        L_boules_op[j]['text'] = str(nb[j])
                    else:
                        L_boules_op[j]['text'] = str(nb[j])
                        break
                    j -= 1
        if nb[i] // 5 == 1:
            if nbAff[i] >= 5:
                active_boule(i, 0, True)
                nbAff[i] -= 5
                nb[i] -= 5
                L_boules_op[i]['text'] = str(nb[i])
            else:
                active_boule(i, 0, True)
                nbAff[i] -= 5
                nb[i] -= 5
                L_boules_op[i]['text'] = str(nb[i])
                nb[i-1] += 1
                j = i - 1
                while j >= 0:
                    if nb[j] >= 10:
                        nb[j] -= 10
                        nb[j - 1] += 1
                        L_boules_op[j]['text'] = str(nb[j])
                    else:
                        L_boules_op[j]['text'] = str(nb[j])
                        break
                    j -= 1

        if nb[i] == 0:
            i -= 1
        wait(1000)


def multiplication(nb1, nb2):
    ''' Effectue la multiplication des deux nombres pas à pas
        nb1: str
        nb2: str
    '''
    global N, G_boules_Val, L_boules_op, L_boules, Line
    n1 = len(str(int(nb1) * int(nb2)))
    n1 = (n1 // 3 + (1 if n1 % 3 else 0)) * 3

    n2 = len(nb2)
    n3 = (n2 // 3 + (1 if n2 % 3 else 0)) * 3

    N = n1 + n3 + len(nb1)

    nbAff = nb1 + "0" * (n3 - n2) + nb2 + "0" * n1
    affiche(nbAff)

    # Changement couleur des labels
    for i in range(len(nb1)):
        L_boules[i]['fg'] = "#0000ff"

    for i in range(len(nb1), len(nb1) + n3 - n2):
        L_boules[i]['fg'] = "#bbbbbb"

    for i in range(len(nb1) + n3 - n2, len(nb1) + n3 - n2 + len(nb2)):
        L_boules[i]['fg'] = "#00ff00"

    for i in range(len(nb1) + n3 - n2 + len(nb2), N):
        L_boules[i]['fg'] = "#ff0000"
        L_boules_op[i]['fg'] = "#ff0000"

    wait(2000)

    inb1 = len(nb1) - 1
    inb2 = len(nb1) + n3 - 1

    for i1, e1 in enumerate(nb2[::-1]):
        if i1 != 0:
            canvas.itemconfigure(Line[inb2 - i1 + 1], fill="darkgrey")
        canvas.itemconfigure(Line[inb2 - i1], fill="#ff0000")

        if e1 == "0":
            continue

        for i2, e2 in enumerate(nb1[::-1]):
            if i2 != 0:
                canvas.itemconfigure(Line[inb1 - i2 + 1], fill="darkgrey")
            canvas.itemconfigure(Line[inb1 - i2], fill="#ff0000")
            nbAff = addition(nbAff, str(int(e1 + "0" * i1) * int(e2 + "0" * i2)), True)
            wait(1000)
        canvas.itemconfigure(Line[inb1], fill="darkgrey")


# Partie simulation
def active_boule(i, j, force=False):
    ''' Fonction qui active ou désactive la boule en (i, j)
        i : colonne de la boule en partant de la gauche
        j : ligne de la boule en partant du haut
        force : si True, quelque soit le mode, l'action s'effectue
    '''
    global G_boules, G_boules_Val
    if mode == 0 or force:
        if not G_boules[i][j][1]:
            if j == 0:
                canvas.itemconfig(G_boules[i][j][0], fill=COLOR_ACTIVE[(N - (i + 1)) // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
                th.Thread(target=animation, args=(i, j, HEIGHT / 10)).start()
                G_boules_Val[i] += 5
                G_boules[i][j][1] = True
            else:
                for k in range(1, j + 1):
                    if not G_boules[i][k][1]:
                        canvas.itemconfig(G_boules[i][k][0], fill=COLOR_ACTIVE[(N - (i + 1)) // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
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
        if not opt_clignotement:   # option "clignotement"
            pass
        elif k % 10 == 0:
            canvas.itemconfig(G_boules[i][j][0], fill=COLOR_ACTIVE[(N - (i + 1)) // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
        elif k % 5 == 0:
            canvas.itemconfig(G_boules[i][j][0], fill=COLOR_DESACTIVE[(N - (i + 1)) // len(COLOR_DESACTIVE) % len(COLOR_DESACTIVE)])
        canvas.move(G_boules[i][j][0], 0, y / n)
        if Vitesse != 0:
            canvas.update()
        time.sleep(ti)
    if op == 1:
        canvas.itemconfig(G_boules[i][j][0], fill=COLOR_DESACTIVE[(N - (i + 1)) // len(COLOR_DESACTIVE) % len(COLOR_DESACTIVE)])


# Partie sauvegarde / chargement
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


def charger():
    '''Fonction qui charge un fichier pour affichier le boulier'''
    # Ouvre une feneêtre de dialogue pour choisir le fichier
    f = fd.askopenfile(
        initialdir=os.getcwd() + "/config/",
        title="charger une config",
        filetypes=(("fichier - projet boulier", "*.boulier"),)
    )

    if f is None:
        return None

    val = eval(f.read())
    f.close()

    global G_boules_Val, L_boules, G_boules, N, Vitesse
    Vitesse_tmp = Vitesse
    # reinitialiser le boulier
    N = len(val)
    init()

    # Affecte les valeurs aux variables globales et affiche les valeurs dans les labels
    G_boules_Val = val
    for i in range(N):
        L_boules[i]['text'] = val[i]

    # affichier les boules qui doivent etre actives
    Vitesse = 0
    for i in range(N):
        if G_boules_Val[i] >= 5:
            canvas.itemconfig(G_boules[i][0][0], fill=COLOR_ACTIVE[(N - (i + 1)) // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
            G_boules[i][0][1] = True
            animation(i, 0, HEIGHT / 6)
        for j in range(1, 5):
            if G_boules_Val[i] % 5 >= j:
                canvas.itemconfig(G_boules[i][j][0], fill=COLOR_ACTIVE[(N - (i + 1)) // len(COLOR_ACTIVE) % len(COLOR_ACTIVE)])
                G_boules[i][j][1] = True
                animation(i, j, -HEIGHT / 6)

    Vitesse = Vitesse_tmp


# Partie Options
def ouvre_fen_options():
    '''Fonction qui ouvre la fenêtre des options'''
    global fen_options
    # Si la fenêtre des options existe déjà, on la met au premier plan
    if "fen_options" in globals():
        fen_options.focus_force()
        return

    # Sinon, on crée la fenêtre
    global scale, VarClignotement, VarNbCol
    fen_options = tk.Toplevel()
    fen_options.title("Options")
    fen_options.wm_protocol("WM_DELETE_WINDOW", del_fen_options)

    # Ajouter Label "Vitesse: "
    label_vitesse = tk.Label(fen_options, text="Vitesse des boules:")

    # Ajouter un Scale pour changer la vitesse des animations
    scale = tk.Scale(fen_options, orient='horizontal', from_=0, to=1.5, resolution=0.1, tickinterval=0.5, length=150)
    scale.set(Vitesse)

    # Ajouter un Label "Nombre de colonnes: "
    label_nbr_colonnes = tk.Label(fen_options, text="nombre de colonnes")

    # Ajouter une Entry pour changer le nombre de colonnes
    VarNbCol = tk.StringVar(fen_options)
    changer_nbr_colones = tk.Entry(fen_options, text="changer nombre de colonnes", textvariable=VarNbCol)
    VarNbCol.set(N)

    # Ajouter une Checkbutton pour activer/désactiver le clignotement
    VarClignotement = tk.BooleanVar(fen_options)
    CB_clignotement = tk.Checkbutton(fen_options, text="Activer le clignotement", variable=VarClignotement)
    CB_clignotement.select() if opt_clignotement else CB_clignotement.deselect()

    # Ajouter un Boutton "Appliquer" pour appliquer les changements
    B_appliquer = tk.Button(fen_options, text="appliquer", command=applique_option)

    # Placement des widgets
    label_vitesse.grid(row=0, column=0)
    scale.grid(row=0, column=1)
    label_nbr_colonnes.grid(row=1, column=0)
    changer_nbr_colones.grid(row=1, column=1)
    CB_clignotement.grid(row=2, column=0, columnspan=2)
    B_appliquer.grid(row=5, column=0, columnspan=2)

    # Lancement de la boucle principale
    fen_options.mainloop()


def del_fen_options():
    '''Fonction qui supprime la fenêtre des options'''
    global fen_options
    # Si la fenêtre existe, on la supprime
    if "fen_options" in globals():
        fen_options.destroy()
        del fen_options


def applique_option():
    change_vitesse()
    change_clignotement()
    change_nb_col()


def change_vitesse():
    '''Fonction qui change la vitesse de l'animation'''
    global Vitesse, scale
    Vitesse = scale.get()


def change_nb_col():
    '''Fonction qui change le nombre de colonnes du boulier'''
    global N, VarNbCol, L_boules
    if int(VarNbCol.get()) != N:
        N = int(VarNbCol.get())
        init()


def change_clignotement():
    ''' Fonction qui change l'option "clignotement"
        Si l'option est active, les boules clignotent quand elles se déplacent
    '''
    global VarClignotement, opt_clignotement
    opt_clignotement = VarClignotement.get()


# Changement mode simulation ou opération
def change_mode():
    ''' Fonction qui bascule entre le mode simulation et le mode opératoire
        mode 0: simulation
        mode 1: opération
    '''
    global mode
    mode = 1 - mode
    if mode == 0:
        canvas.config(cursor="arrow")
    else:
        canvas.config(cursor="crosshair")
    init()


def main():
    '''Fonction principale, initailise le programme et l'interface graphique et lance la boucle principale'''
    # déclaration des variables globales
    global root, canvas

    # Céation de la fenêtre principale
    root = tk.Tk()
    root.title("Boulier")
    root.resizable(False, False)
    root.configure(bg="white")

    # Création du Menu
    menuBar = tk.Menu(root)

    # Création du menu Fichier
    menu_file = tk.Menu(menuBar, tearoff=0)
    menu_file.add_command(label="Réinitialiser", command=init)
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
    canvas.grid(row=0, column=0, rowspan=10)

    # Initialisation du boulier
    init(False)

    # Lancement de la boucle principale
    root.mainloop()


main()
