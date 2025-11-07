class ClassicModelsWrapper:
    def __init__(self, client):
        self.client = client

    def fetch_all_models(self):
        return self.client.get_all_models()

    def add_new_model(self, model_data):
        return self.client.create_model(model_data)