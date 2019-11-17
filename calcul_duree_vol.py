import sqlite3
import time
import envoiSMS

fichier = "syracuse_v2.sq3"

base = sqlite3.connect(fichier)
curseur = base.cursor()


def duree_vol(n):
    duree = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        duree += 1
    return duree

curseur.execute("create table if not exists dv (p_terme INTEGER, duree_vol INTEGER)")
t0 = time.time()
t = t0
for i in range(500_001, 1_000_001):
    if i % 10_000 == 0:
        base.commit()
        curseur.execute("select count(*) from dv")
        N = curseur.fetchall()[0][0]
        texte = str(i) + " est atteint\n"
        texte += str(N) + " entrées dans la base"
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
    # q = "select * from dv where p_terme="
    # curseur.execute(q + str(i))
    # if curseur.fetchone() is None:
    d = duree_vol(i)
    entree = "insert into dv values(?, ?)"
    curseur.execute(entree, (i, d))

base.commit()
base.close()
