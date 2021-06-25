





[PEP 8](https://www.python.org/dev/peps/pep-0008/):

* Entre deux fonctions, il est recommandé de placer 2 lignes vides.
* Pour séparer les éléments d'une liste, il est recommandé de suivre la synrax suivante: "`(e1, e2, e3)`" et non, par exemple "`(e1 , e2 , e3)`".
* L'indentiation devrait être de 4 espaces.

# Principe du rasoir d'Ockham:

> "Entiae non sunt multiplicanda praeter necessitatem."
> "Il ne faut pas multiplier les entités sauf nécessité."

Tu as copié le tableau "INPUT" depuis le fichier "agora.py" vers "graph_drawer.py" => duplication (unitile) de la donnée. Ceci est une violation du principe du rasoir d'Ockham.

Pourquoi respecter cette règle ?: car sinon, s'il faut modifier la variable, alors il faut la modifier partout dans le code...

# Utilisation d'une variable globale inutilement

Utilisation d'une variable globale alors que cela n'est pas nécessaire: la variable globale "INPUT" est utilisée dans la fonction "draw_transactions_year". Il suffit de passer la valeur de la variable "INPUT" est paramètre de la fonction. Mais, il y a mieux: "une datframe est associée à un mois" ou "un mois est associé à une dataframe" => structure de dictinnaire ordonné (car l'ordre des mois comptes).

Pourquoi est-ce mauvais ?: car les variables globales introduisent des couplages inutiles au sein du code => plat de spaghettis.

# Utilisation des "expensions"

    sub_data = []
    for i in range(len(data)):
        sub_data.append(data[i]['btc'])

S'écrit:

    sub_data = [df['btc'] for df in data]

# Définition d'un paramètre qui n'a pas de sens

Dans la fonction "`draw_transactions_year`", tu passes le paramètre "`ref_name`"...
mais tu codes en dur "`btc`".

Donc, la seule valeur possible pour "`ref_name`" est "`btc`" (sinon la fonction fait n'importe quoi).

Le cas échéant, il ne faudrait pas définir ce paramètre, car il induit l'utilisateur de ta fonction en erreur.
Il pense qu'il peut indiquer n'importe quelle valeur, mais c'est faux...

CF: [affordance](https://www.usabilis.com/definition-affordance/) Il faut concevoir les API en adoptant
le point de vue de l'utilisateur de l'API.

# Comment générer le chemin vers le graphe ?

Le code pour générer le chemin vers le fichier de sortie est écrit dans les quelques lignes au-dessus (à deux reprises).

    gd_path = "{}/transaction/{}".format(output_path, "boxplot-year.html")
    create_directory(gd_path)

