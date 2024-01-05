import praw
import urllib
import xmltodict
import pandas as pd
from document import *
from author import *
from corpus import *
import datetime

docs = [] #Liste des textes des articles
docs_bruts = [] #Liste des documents bruts récupérés et leur origine
docs_obj = []#Liste contenant les objets documents
iddoc = {}#Index de documents
query = "geography" #Sujet des docs

#Récupération des documents de Reddit
reddit = praw.Reddit(client_id='nzJcQWMzVE8P6uYYll0-Bg', client_secret='s3M97y4jzMOiNr1L4rQantxDXnpI_w', user_agent='TD3Python')
hot_posts = reddit.subreddit(query).hot(limit=100)
for post in hot_posts:
    texteSubr = post.selftext
    texteSubr = texteSubr.replace("\n", " ")
    if len(texteSubr) >= 20:
        docs.append(texteSubr)
        docs_bruts.append(('Reddit', post))

# Récupération des documents de Arxiv
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()
data = url_read.decode()
dico = xmltodict.parse(data)
arxivArticle = dico['feed']['entry']

for i, entry in enumerate(arxivArticle):
    if len(entry["summary"]) >= 20:
        docs.append(entry["summary"].replace("\n", ""))
        docs_bruts.append(("ArXiv", entry))

#Creation des objets Document
for origine, doc in docs_bruts : 
    #Récupération des variables
    if origine == "Reddit" :
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")
        #Creation des objets
        docObj = RedditDocument(titre, auteur, date, url, texte)
        docObj.nbCom = doc.num_comments

        docs_obj.append(docObj)
    
    elif origine == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #Création d'un objet Document venant d'un article Arxiv
        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        try:
            authors = [a["name"] for a in doc["author"]] # On fait une liste d'auteurs
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

        docObj = ArxivDocument(titre, authors, date, doc["id"], summary)  # Création du Document
        docs_obj.append(docObj)  # Ajout du Document à la liste.

# Création de l'index de documents
for i, doc in enumerate(docs_obj):
    iddoc[i] = doc.titre

#Création d'un dictionnaire idauthor pour attrribuer a chaque auteur un identifiant unique
authors = {}
aut2id = {}
id_auteurs_unique = 0

# Création de la liste+index des Auteurs
for doc in docs_obj:#On parcours les auteurs de chaque document 
    if doc.auteur not in aut2id: 
        id_auteurs_unique += 1 #On génère l'id de l'auteur en ajoutant 1 à chaque fois qu'on croise un nouvel auteur
        authors[id_auteurs_unique] = Author(doc.auteur)#Création d'un objet dans la liste authors
        aut2id[doc.auteur] = id_auteurs_unique #on ajoute sont id dans la liste indexée

    authors[aut2id[doc.auteur]].add(doc.texte) #pour chaque document écris par cet auteur, on l'ajoute dans son nb de production

corpus = Corpus("Mon corpus")

# Construction du corpus à partir des documents
for doc in docs_obj:
    corpus.add(doc)

corpus.save('corpus.pkl')

