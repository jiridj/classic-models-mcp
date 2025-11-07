# This file serves as an entry point for running the application or scripts. 
# It may include code to initialize the wrapper and execute specific API calls.

from mcp.wrapper import ClassicModelsWrapper

def main():
    # Initialize the wrapper
    wrapper = ClassicModelsWrapper()

    # Example API calls
    all_models = wrapper.fetch_all_models()
    print("All Models:", all_models)

    # Add a new model (example data)
    new_model = {
        "modelName": "New Model",
        "modelYear": 2023,
        "brand": "Brand Name",
        "category": "Category Name",
        "supplier": "Supplier Name"
    }
    created_model = wrapper.add_new_model(new_model)
    print("Created Model:", created_model)

if __name__ == "__main__":
    main()