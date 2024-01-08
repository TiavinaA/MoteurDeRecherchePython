from corpusGenerator import *
# Fonction à appeler lorsque le choix de corpus change
def on_choix_change(change,choix_corpus,sujet_corpus,nombre_articles,chemin_corpus):
    if change['type'] == 'change' and change['name'] == 'value':
        if choix_corpus.value == 'Créer un corpus':
            # Activer les champs de texte pour le sujet et le nombre d'articles
            sujet_corpus.disabled = False
            nombre_articles.disabled = False
            chemin_corpus.disabled = True
        elif choix_corpus.value == 'Charger un corpus':
            # Activer le champ de texte pour le chemin du corpus
            sujet_corpus.disabled = True
            nombre_articles.disabled = True
            chemin_corpus.disabled = False

