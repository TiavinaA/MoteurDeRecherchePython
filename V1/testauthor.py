import unittest
from author import Author
class TestAuthor(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Author class for testing
        self.author = Author("John Doe")

    def test_author_add(self):
        # Test the add method of the Author class
        self.assertEqual(self.author.ndoc, 0)
        self.assertEqual(len(self.author.production), 0)

        # Add a production
        self.author.add("Sample Production")

        # Check if the number of documents and the production list are updated
        self.assertEqual(self.author.ndoc, 1)
        self.assertEqual(len(self.author.production), 1)
        self.assertEqual(self.author.production[0], "Sample Production")

    def test_author_str(self):
        # Test the __str__ method of the Author class
        expected_str = "Auteur : John Doe\t# productions : 0"
        self.assertEqual(str(self.author), expected_str)

if __name__ == '__main__':
    unittest.main()
