import sqlite3
import sys

base = sqlite3.connect("./syracuse_v2.sq3")
curseur = base.cursor()
requete = "select * from termes where p_terme="

n = int(sys.argv[1])

syracuse = [n]

while n != 1:
    q = requete + str(n)
    curseur.execute(q)
    sequence = eval(curseur.fetchone()[0])
    syracuse += sequence
    n = syracuse[-1]

print(syracuse)
