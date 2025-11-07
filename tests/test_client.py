import unittest
from mcp.client import ClassicModelsClient

class TestClassicModelsClient(unittest.TestCase):

    def setUp(self):
        self.client = ClassicModelsClient()

    def test_get_all_models(self):
        models = self.client.get_all_models()
        self.assertIsInstance(models, list)

    def test_get_model_by_id(self):
        model_id = 1
        model = self.client.get_model_by_id(model_id)
        self.assertEqual(model['id'], model_id)

    def test_create_model(self):
        new_model = {
            'name': 'Test Model',
            'category': 'Test Category',
            'supplier': 'Test Supplier'
        }
        response = self.client.create_model(new_model)
        self.assertIn('id', response)

if __name__ == '__main__':
    unittest.main()