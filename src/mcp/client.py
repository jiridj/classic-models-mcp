class ClassicModelsClient:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    def get_all_models(self):
        response = requests.get(f"{self.base_url}/models", auth=self.auth)
        response.raise_for_status()
        return response.json()

    def get_model_by_id(self, model_id):
        response = requests.get(f"{self.base_url}/models/{model_id}", auth=self.auth)
        response.raise_for_status()
        return response.json()

    def create_model(self, model_data):
        response = requests.post(f"{self.base_url}/models", json=model_data, auth=self.auth)
        response.raise_for_status()
        return response.json()