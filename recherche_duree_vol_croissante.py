import sys
import sqlite3

n = int(sys.argv[1])

fichier_base = "./syracuse_v2.sq3"
base = sqlite3.connect(fichier_base)
curseur = base.cursor()

record = 0
for i in range(1, n+1):
    curseur.execute("select duree_vol from dv where p_terme=" + str(i))
    actuel = curseur.fetchone()[0]
    if actuel > record:
        record = actuel
        print(i, actuel)
