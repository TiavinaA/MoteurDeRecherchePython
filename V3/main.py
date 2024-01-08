from corpusGenerator import *
from corpus import *
corpus_charge = Corpus('CorpusTest')
c = corpus_charge.load('V2/france.pkl')
# print(repr(c))

###
# print(c.search('latitude')) 
# print(c.search('city')) 
# print(c.concorde('latitude', 15))

# mots = c.stats()
dico = c.createVocab()
X = c.createTFIDF()
conc = c.concorde("france", 20)
print(conc)
# print(len(c.id2doc))
# print(X)

# On récupère la saisie de l'utilisateur : 
# req = input("what are you looking for?")
# c.motsCles(req, dico, X)




