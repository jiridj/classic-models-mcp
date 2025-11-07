class Model:
    def __init__(self, model_id: int, model_name: str, category_id: int, supplier_id: int):
        self.model_id = model_id
        self.model_name = model_name
        self.category_id = category_id
        self.supplier_id = supplier_id


class Category:
    def __init__(self, category_id: int, category_name: str):
        self.category_id = category_id
        self.category_name = category_name


class Supplier:
    def __init__(self, supplier_id: int, supplier_name: str, contact_name: str):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.contact_name = contact_name