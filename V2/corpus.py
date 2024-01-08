from author import *
from document import *
import pickle
import re
import pandas
from nltk import *
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


class Corpus :
    def __init__(self, nom) :
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0 

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
    
    def showDocSortedByTitle(self, n_docs):
        docs = list(self.id2doc.values())
        docs = list(sorted(self.id2doc.values(), key=lambda x: x.titre.lower()))[:n_docs]
        for doc in docs:
            print(f"Document: {doc.titre} - Date: {doc.date}")
    
    def showDocSortedByDate(self, n_docs):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]
        for doc in docs:
            print(f"Document: {doc.titre} - Date: {doc.date} -Origine : {doc.type}")

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        return "\n".join(list(map(str, docs)))  

    def save(self, file_path):
        # Serialize the entire corpus object using pickle
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    def load(self, file_path):
        # Deserialize the corpus object from the pickle file
        with open(file_path, 'rb') as file:
            loaded_corpus = pickle.load(file)
            return loaded_corpus
    
    # Transformation du corpus en une unique chaine de caractère, seulement si cela n'a pas déjà été fait : 
    def createUnique(self):
        global unique_initialized 
        if 'unique' not in globals() or not unique_initialized: # On vérifie si le texte unique existe déjà  :
            global unique
            unique = ""
            for x in self.id2doc.values():
                unique += str(x.texte) # on créer un texte unique s'il n'existe pas encore
            unique_initialized = True

    # Renvoi des positions de début et de fins des caractères trouvés : 
    def search(self, mot_cle):  
        self.createUnique()
        pass_trouv = []
        for match in re.finditer(mot_cle, unique):
            pass_trouv.append('début : ' + str(match.start()) + '/ fin : ' + str(match.end()))
        return pass_trouv
    
    # Création du concordancier : 
    def concorde(self, mot_cle, taille):
        self.createUnique()
        list_mot= []
        for match in re.finditer(mot_cle, unique):
            mot_rech = []
            if (int(match.start()) - int(taille) >= 0): # Création du contexte gauche : 
                context_gauche = int(match.start() - taille)
            else:
                context_gauche = 0 
            if (int(match.end()) + int(taille) <= len(unique)): # Création du contexte droit : 
                context_droit = int(match.end() + taille)
            else:
                context_droit = len(unique)
            # Création du concordancier : 
            mot_rech.append(unique[context_gauche:match.start()]) 
            mot_rech.append(unique[match.start():match.end()])
            mot_rech.append(unique[match.end():context_droit])
            list_mot.append(mot_rech)
        df = pandas.DataFrame(list_mot, columns = ['contexte gauche', 'motif trouvé', 'contexte droit']) # Transformation du concordancier en dataframe : 
        return df
    
    # Nettoyage du texte : 
    def nettoyer_texte(self, texteBrut): 
        #tokenisation
        tokens = word_tokenize(texteBrut)
        # Mise en minuscule : 
        tokens = [word.lower() for word in tokens]
        # Suppression de la ponctuation : 
        words = [word for word in tokens if word.isalpha()]
        # suppresion des caractères non-alphanumériques
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        stripped = [re_punc.sub('', w) for w in tokens]
        words = [word for word in stripped if word.isalpha()] 
        #Supression des stop words
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        return words


    # Calcule de l'occurence des mots dans le corpus  : 
    def calcOccurrence(self):
        vocab = {}
        for x in self.id2doc.values():
            y = self.nettoyer_texte(x.texte)
            for mot in y:
                if mot in vocab:
                    vocab[mot]+=1
                else:
                    vocab[mot]=1
        return vocab


    # Calcule de la fréquence des mots par texte : 
    def calcFreq(self):
        vocFreq = {}
        for x in self.id2doc.values():
            y = self.nettoyer_texte(x.texte)
            ens = set(y)
            for mot in ens:
                if mot in vocFreq:
                    vocFreq[mot]+=1
                else:
                    vocFreq[mot]=1
        return vocFreq
    
    # Fonction qui renvoie des statistiques sur le corpus : 
    def stats(self):
        vocab = self.calcOccurrence()
        vocFreq = self.calcFreq()
        list_mot = []
        freq_mot = []
        for x in sorted(vocab.keys()):
            list_mot.append(x)
            freq_mot.append(vocab[x])
        # Modifications a partir de maintenant :
            
        doc_cleaned = []
        for x in self.id2doc.values():
            y = self.nettoyer_texte(x.texte)
            doc_cleaned.append(y)

        # Tokenisation pour chaque document
        tokenized_docs = [' '.join(doc) for doc in doc_cleaned]

        list_freq = []
        for x in sorted(vocFreq.keys()):
            list_freq.append(vocFreq[x])

        vocab2 = {}
        vocab2['mot'] = list_mot
        vocab2['occurence'] = freq_mot
        vocab2['frequence'] = list_freq
        df = pandas.DataFrame(vocab2)
        print(df)


    # Crétion du dictionnaire sur lequel le moteur de recherche va reposer : 
    def createVocab(self):
        # On tri les dictionnaires d'occurence et de fréquence :
        vocab = self.calcOccurrence()
        vocFreq = self.calcFreq()
        realVocab = {}
        i = 0
        for x in sorted(vocab.keys()): # On ajoute des informations spécifiques à chaque mots dans un dictionnaire : 
            secondVocab = {}
            secondVocab['id'] = i
            secondVocab['occurence'] = vocab[x]
            secondVocab['nbr_texte'] = vocFreq[x]
            realVocab[x] = secondVocab # On associe le dictionnaire ainsi crée à un mot : 
            i += 1
        return realVocab
    

    # Création de la matrice TFIDF : 
    def createTFIDF (self):
        doc_cleaned = []
        for x in self.id2doc.values(): # On récupère et nettoie chaque texte du corpus :  
            y = self.nettoyer_texte(x.texte)
            doc_cleaned.append(y)
        vectorizer = TfidfVectorizer(lowercase=False, tokenizer=lambda x: x)
        X = vectorizer.fit_transform(doc_cleaned)
        # On vérifie si les termes sont dans le bon ordre :
        feature_names = vectorizer.get_feature_names_out()
        for i in range(10):
            print(f"Identifiant : {i}, Fonctionnalité : {feature_names[i]}")
        print(type(X))
        print(X.shape)
        print(type(X.toarray()))
        return X
    
    
    # Gestion de la requête de l'utilisateur : 
    def motsCles (self, request, vocabulary, tfidf):
        # On nettoie la requête pour pouvoir l'analyser : 
        word = self.nettoyer_texte(request)
        # on récupère les identifiants des mots-clés s'ils existent dnas le dictionnaire : 
        list_founds = []
        for x in vocabulary.keys():
            for y in word:
                if (x == y):
                    list_founds.append(vocabulary[x]['id'])
        if list_founds: # On continue si la liste est non-vide : 
            df = pandas.DataFrame() # Création d'un dataframe qui ne contient que les colonnes des mots-clés et récupérés depuis la matrice tfidf : 
            num_lines = tfidf.shape[0]
            df['id'] = range(num_lines)
            for x in list_founds:
                df[str(x)] = tfidf[:, x].toarray().ravel()
            df['Score'] = df.loc[:, df.columns != 'id'].sum(axis=1) # on calcul dans un champs 'Score' la somme des valeurs de chaque ligne : 
            print(df['Score'])
            df_trie = df.sort_values(by='Score', ascending=False)
            print(df_trie)
            for i in range(0, 10): # On affiche les 10 résultats ayant le score le plus élevé : 
                print(self.id2doc[(df_trie['id'].iloc[i])+1])
                print((df_trie['id'].iloc[i])+1)

            return df_trie
            
