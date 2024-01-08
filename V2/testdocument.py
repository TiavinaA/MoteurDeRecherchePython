import unittest
from document import *
class TestDocuments(unittest.TestCase):

    def setUp(self):
        # Create instances of Document, RedditDocument, and ArxivDocument for testing
        self.doc = Document("Sample Document", "John Doe", "2022-01-01", "http://example.com", "Sample text")
        self.reddit_doc = RedditDocument("Reddit Post", "RedditUser", "2022-01-02", "http://reddit.com", "Reddit text")
        self.arxiv_doc = ArxivDocument("Arxiv Paper", ["Author1", "Author2", "Author3"], "2022-01-03", "http://arxiv.org", "Arxiv text")

    def test_document_info(self):
        self.assertEqual(self.doc.__info__(), "Titre : Sample Document\tAuteur : John Doe\tDate : 2022-01-01\tURL : http://example.com\tTexte : Sample text\t")

    def test_document_str(self):
        self.assertEqual(str(self.doc), "Sample Document, par John Doe")

    def test_document_get_type(self):
        self.assertEqual(self.doc.getType(), "Type de doc")

    def test_reddit_document_str(self):
        expected_str = "Reddit Post, par RedditUser Nombre de commentaires :0\n Reddit"
        self.assertEqual(str(self.reddit_doc), expected_str)

    def test_arxiv_document_str(self):
        expected_str = "Arxiv Paper, par Author1 Co-Auteurs : ['Author2', 'Author3']\n Arxiv"
        self.assertEqual(str(self.arxiv_doc), expected_str)

if __name__ == '__main__':
    unittest.main()
