import unittest
from document import Document
from corpus import Corpus
import io
from unittest.mock import patch
import os
import pandas as pd
class TestCorpus(unittest.TestCase):
    def setUp(self) :
        self.corpus = Corpus("Test Corpus")
        self.doc1 = Document("Titre 1", "Auteur 1","2022-01-01", "reddit.com","Hello World!","Reddit")
        self.doc2 = Document("Titre 2", "Auteur 2","2022-01-02", "reddit2.com","Hello World!2","Reddit")
        self.doc3 = Document("Titre 3", "Auteur 1","2022-01-03", "arxiv.com","Hello World!3","Arxiv")
    
    def test_add_document(self):
        self.corpus.add(self.doc1)
        self.assertEqual(self.corpus.ndoc, 1)
        self.assertEqual(self.corpus.naut, 1)

        self.corpus.add(self.doc2)
        self.assertEqual(self.corpus.ndoc, 2)
        self.assertEqual(self.corpus.naut, 2)

        #L'auteur déjà connu ne devrai pas etre incrementé
        self.corpus.add(self.doc3)
        self.assertEqual(self.corpus.ndoc, 3)
        self.assertEqual(self.corpus.naut, 2)

    def test_showDocSortedByTitle(self):
        self.corpus.add(self.doc2)
        self.corpus.add(self.doc1)
        self.corpus.add(self.doc3)

        expected_output = "Document: Titre 1 - Date: 2022-01-01\n"\
                          "Document: Titre 2 - Date: 2022-01-02\n"\
                          "Document: Titre 3 - Date: 2022-01-03"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.corpus.showDocSortedByTitle(3)
            self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    def test_showDocSortedByDate(self):
        self.corpus.add(self.doc2)
        self.corpus.add(self.doc1)
        self.corpus.add(self.doc3)

        # Test sorting by date
        expected_output = "Document: Titre 1 - Date: 2022-01-01\n"\
                          "Document: Titre 2 - Date: 2022-01-02\n"\
                          "Document: Titre 3 - Date: 2022-01-03"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.corpus.showDocSortedByTitle(3)
            self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    def test_save(self):
        self.corpus.add(self.doc1)
        self.corpus.add(self.doc2)

        file_path = "test_corpus_save.pkl"
        self.corpus.save(file_path)

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path))

    def tearDown(self):
        # Clean up any resources or files created during testing
        file_paths = ["test_corpus_save.pkl", "test_corpus_load.pkl"]
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_concordance(self):
        self.corpus.add(self.doc1)
        self.corpus.add(self.doc2)
        self.corpus.add(self.doc3)

        result = self.corpus.concorde("Hello", 5)
        # Ensure the result is a DataFrame with the expected columns
        self.assertIsInstance(result, pd.DataFrame)
        self.assertListEqual(result.columns.tolist(), ['contexte gauche', 'motif trouvé', 'contexte droit'])

    def test_clean_text(self):
        raw_text = "Hello World! This is a test."
        cleaned_text = self.corpus.nettoyer_texte(raw_text)
        self.assertEqual(cleaned_text, ["hello", "world", "test"])
if __name__ == '__main__' :
    unittest.main()