import sqlite3

base = sqlite3.connect("./syracuse_v2.sq3")
curseur = base.cursor()

dva = "select count(p_terme) from dva where duree_vol_altitude="
ordre = "order by p_terme "

print("Aucun nombre avec cette durée de vol en altitude")

for i in range(1, 101):
    curseur.execute(dva + str(i))
    r = curseur.fetchone()[0]
    if r == 0:
        print("{:2d}".format(i), end="   ")

print()
base.close()
