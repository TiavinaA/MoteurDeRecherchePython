from corpusGenerator import *
import ipywidgets as widgets
from IPython.display import display
from IPython.display import clear_output
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


def moteur_de_recherche(mainDico, mainMat, c):
    # Créer un widget de texte pour le sujet du corpus
    req_recherche = widgets.Text(
        description='Rechercher :',
    )
    filtre_auteur = widgets.Text(
        description = 'Auteur :'
    )
    # Créer un widget de bouton radio pour le choix entre créer et charger un corpus
    filtre_typedoc = widgets.RadioButtons(
        options=['Tous', 'Arxiv','Reddit'],
        description='Filtrer document:'
    )
    # Créer un bouton pour déclencher l'action de création ou de chargement du corpus
    bouton_recherche = widgets.Button(description='Rechercher')
    output_area = widgets.Output()

    def on_bouton_recherche(b):
        with output_area:
            clear_output(wait=True)  # Clear previous output
            fil, filDico, filMat = c.filtrerTypeDoc(filtre_typedoc.value)
            if filtre_auteur.value != '' :
                fil, filDico, filMat = c.rechercheAuteur(filtre_auteur.value, fil)
            c.motsCles(req_recherche.value, mainDico, mainMat, fil, filDico, filMat)    

    # Attacher la fonction à l'événement de clic du bouton
    bouton_recherche.on_click(on_bouton_recherche)

    display(req_recherche)
    display(filtre_auteur)
    display(filtre_typedoc)
    display(bouton_recherche)
    display(output_area)

