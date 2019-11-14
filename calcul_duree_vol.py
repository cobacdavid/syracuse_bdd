import sqlite3
import time
import envoiSMS

fichier = "syracuse_v2.sq3"

base = sqlite3.connect(fichier)
curseur = base.cursor()


def duree_vol(n):
    if n % 2 == 0:
        duree = 1
    else:
        # on construit la suite
        suite = [n]
        taille = 0
        duree = 0
        en_cours = True
        q = "select suite from termes where p_terme="
        while en_cours:
            # on récupère la suite petit à petit
            curseur.execute(q + str(n))
            r = curseur.fetchone()
            suite += eval(r[0])
            # on regarde si on a la durée
            taille = len(suite)
            while duree < taille and suite[duree] >= suite[0]:
                duree += 1
            # si on n'est pas arrivé à la fin de la liste
            # c'est qu'on a trouvé (on est passé en dessous)
            if duree < taille:
                en_cours = False
            n = suite[-1]
    return duree - 1


curseur.execute("create table if not exists dva (p_terme INTEGER, duree_vol_altitude INTEGER)")
t0 = time.time()
t = t0
for i in range(384_000, 500_001):
    if i % 1_000 == 0:
        base.commit()
        curseur.execute("select count(*) from dva")
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
    q = "select * from dva where p_terme="
    curseur.execute(q + str(i))
    if curseur.fetchone() is None:
        d = duree_vol(i)
        entree = "insert into dva values(?, ?)"
        curseur.execute(entree, (i, d))

base.commit()
base.close()
