import sys
from pathlib import Path
import sqlite3
import envoiSMS
import time


def terme_suivant(n):
    if n % 2 == 0:
        n //= 2
    else:
        n = 3 * n + 1
    return n


def termes(p_terme, actifs, cur):
    actifs.append(p_terme)
    q = "select suite from termes where p_terme=" + str(p_terme)
    cur.execute(q)
    r = cur.fetchone()
    if p_terme == 1 or r is not None:
        # ici c'est fini !
        duree_relative = len(actifs) - 1
        # 2 n'est pas pur
        purete = 1 if actifs[0] != 2 else 0
        altitude_max_relative = max(actifs)
        ajout_base(cur, actifs[0], str(actifs[1:]),
                   duree_relative, purete, altitude_max_relative)
        #
        actifs = actifs[1:]
        for i in range(len(actifs)-1):
            premier = actifs[i]
            suite = actifs[i+1]
            duree_relative = 1
            purete = 0
            altitude_max_relative = max(premier, suite)
            ajout_base(cur, premier, str([suite]),
                       duree_relative, purete, altitude_max_relative)
    else:
        # actifs contient tous les termes de la suite
        # dans l'ordre jusqu'à atteindre un qui est connu
        termes(terme_suivant(p_terme), actifs, cur)


def duree_vol_altitude(liste):
    indice = 0
    taille = len(liste)
    while indice < taille and liste[indice] >= liste[0]:
        indice += 1
    return indice - 1


def ajout_base(cur, *args):
    # cet ajout ne se fait que sur les nombres "actifs"
    # c'est-à-dire découvert lors du processus
    # print("ajout base", args[0])
    cur.execute("insert into termes values (?, ?, ?, ?, ?)", args)



n = int(sys.argv[1])

fichier_base = "./syracuse_v2.sq3"
syracuse = {}

# création de la base si elle n'existe pas
if not Path(fichier_base).is_file():
    # constitution de la base
    base = sqlite3.connect(fichier_base)
    curseur = base.cursor()
    curseur.execute("create table termes (p_terme INTEGER, suite TEXT, duree_relative INTEGER, purete INTEGER, altitude_max_relative INTEGER)")
else:
    base = sqlite3.connect(fichier_base)
    curseur = base.cursor()
#
t0 = time.time()
t = t0
for i in range(500_000, n):
    if i % 10_000 == 0:
        base.commit()
        #
        curseur.execute("select count(*) from termes")
        N = curseur.fetchall()[0][0]
        texte = str(i) + " est atteint\n"
        texte += str(N) + " entrées dans la base"
        #
        maintenant = time.time()
        moment = time.localtime()
        # heure = str(moment.tm_hour) + ":" + "{:02d}".format(moment.tm_min)
        bouclem, boucles = divmod(round(maintenant - t), 60)
        boucle = str(bouclem) + "min" + "{:02d}".format(boucles) + "s"
        dejam, dejas = divmod(round(maintenant - t0), 60)
        deja = str(dejam) + "min" + "{:02d}".format(dejas) + "s"
        t = maintenant
        texte += "\n" + boucle + " " + deja
        envoiSMS.message(texte)
        print(i)
    # on ne refait pas ce qui est déjà fait
    q = "select * from termes where p_terme = " + str(i)
    curseur.execute(q)
    if curseur.fetchone() is None:
        termes(i, [], curseur)
#
base.commit()
curseur.execute("select count(*) from termes")
N = curseur.fetchall()[0][0]
print(N, "entrées dans la base")
base.close()
