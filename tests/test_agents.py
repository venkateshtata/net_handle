import unittest
from agents.shopping_agent import ShoppingHandler

class TestShoppingHandler(unittest.TestCase):
    def setUp(self):
        self.agent = ShoppingHandler()

    def test_search(self):
        results = self.agent.search("laptops")
        self.assertTrue(len(results) > 0)

if __name__ == "__main__":
    unittest.main()
