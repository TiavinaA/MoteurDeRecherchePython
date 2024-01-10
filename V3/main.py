from corpusGenerator import *
from corpus import *

#Cette page sert uniquement de brouillon et zone de test


corpus_charge = Corpus('CorpusTest')
# c = corpus_charge.load('V2/france.pkl')
c = corpus_charge.load('V2/france.pkl')
print(repr(c))

###
# print(c.search('latitude')) 
# print(c.search('city')) 
# print(c.concorde('latitude', 15))

# mots = c.stats()

# matrice et dictionnaire sans filtre : 
mainDico = c.createVocab()
mainMat = c.createTFIDF()

# test des filtres : 
# On créer une nouvelle matrice et un nouveau dico qui prennent en compte les filtres : 
fil, filDico, filMat = c.filtrerTypeDoc('Arxiv') # test du filtre sur le type de doc : 
print(filDico)
print(filMat)

# test du filtre sur les auteurs : 
# fil, filDico, filMat = c.rechercheAuteur('Kraus', fil)

# # Gestion de la requête de l'utilisateur : 
req = input("what are you looking for?")


# fil = c.delFiltre(fil) # permet de supprimer les filtres en cours

c.motsCles(req, mainDico, mainMat, fil, filDico, filMat)




"""
X = c.createTFIDF()
conc = c.concorde("france", 20)
print(conc)
"""
"""
# print(len(c.id2doc))
# print(X)

# On récupère la saisie de l'utilisateur : 
req = input("what are you looking for?")
# Fonction de filtre selon le type de doc (à préciser s'il s'agit d'un doc Arxiv ou Reddit)
fil = c.filtrerTypeDoc('Arxiv')
# Recherche d'articles en fonction du nom des auteurs (le paramètre 'fil' est facultatif, il est a utiliser seulement pour filtrer les textes selon le type de doc)
c.rechercheAuteur(req, fil)
# c.motsCles(req, dico, X)
"""









