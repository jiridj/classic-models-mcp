import unittest
from mcp.wrapper import ClassicModelsWrapper
from mcp.client import ClassicModelsClient

class TestClassicModelsWrapper(unittest.TestCase):

    def setUp(self):
        self.client = ClassicModelsClient()
        self.wrapper = ClassicModelsWrapper(self.client)

    def test_fetch_all_models(self):
        models = self.wrapper.fetch_all_models()
        self.assertIsInstance(models, list)
        self.assertGreater(len(models), 0)

    def test_add_new_model(self):
        new_model = {
            "modelName": "Test Model",
            "modelYear": 2023,
            "brand": "Test Brand",
            "category": "Test Category"
        }
        response = self.wrapper.add_new_model(new_model)
        self.assertTrue(response['success'])
        self.assertEqual(response['model']['modelName'], new_model['modelName'])

if __name__ == '__main__':
    unittest.main()