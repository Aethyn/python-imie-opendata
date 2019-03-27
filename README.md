# python-imie-opendata
@TODO : doc

## Configuration
Il manque au projet un fichier situé à la racine du répertoire, nommé "env.py", il contient les variables d'environnement "sensibles" du projet (host, username, password).  
Pour que le projet fonctionne il faut récupérer le fichier env.py.example, le renommer en retirant le ".example" et remplir les variables qu'il contient.

## Utilisation
Une fois la configuration terminée :  
- Dans la console, taper "python initdb" (le résultat attendu doit être "tables True")  
- Taper "python irigo.py" (le résultat obtenu doit être un nombre de lignes éventuellement suivi d'une poignée d'erreur de duplications d'entrées inhérentes aux données collectées)