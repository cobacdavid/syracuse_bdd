import sqlite3

base = sqlite3.connect("./syracuse_v2.sq3")
curseur = base.cursor()

maxi = 200_000
bloc = 20_000

purete = "select count(p_terme) from termes where purete=1 "
intervalle = "and p_terme>=? and p_terme<? "
ordre = "order by p_terme "


for i in range(maxi//bloc):
    inferieur = i * bloc
    superieur = inferieur + bloc
    curseur.execute(purete + intervalle + ordre, (inferieur, superieur))
    presentation ="de {:6d} à {:6d} :".format(inferieur, superieur)
    print(presentation, curseur.fetchone()[0])

base.close()
