# de https://python.developpez.com/cours/apprendre-python3/?page=page_18
import sqlite3
import sys

fichier = sys.argv[1]

base = sqlite3.connect(fichier)
curseur = base.cursor()

while 1:
    print("Requête SQL :")
    requete = input()
    if requete == "":
        break
    try:
        curseur.execute(requete)
    except:
        print('*** Requête SQL incorrecte ***')
    else:
        for enreg in curseur:
            print(enreg)
    print()
 
choix = input("Confirmez-vous l'enregistrement de l'état actuel (o/n) ? ")
if choix[0] == "o" or choix[0] == "O":
    base.commit()
else:
    base.close()

# quelques requêtes à copier/coller
'''
select * from termes where p_terme<=100 and purete=1 order by p_terme
select * from termes where p_terme=15 or p_terme=127
select p_terme from termes where purete=1 order by p_terme
select p_terme from termes where p_terme<1000 and purete=1 order by duree_relative desc limit 10
'''
