# FastMCP Classic Models API Wrapper

This project is a Python wrapper for the Classic Models API, designed to simplify interactions with the API and provide a more user-friendly interface.

## Project Structure

```
classic-models-mcp
├── src
│   ├── mcp
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── wrapper.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── config.py
│   └── scripts
│       └── run.py
├── tests
│   ├── test_client.py
│   └── test_wrapper.py
├── pyproject.toml
├── setup.cfg
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To use the FastMCP Classic Models API wrapper, you can initialize the `ClassicModelsWrapper` in your scripts. Here’s a basic example:

```python
from fastmcp_classicmodels.wrapper import ClassicModelsWrapper

wrapper = ClassicModelsWrapper()
models = wrapper.fetch_all_models()
print(models)
```

## Running Tests

To run the tests, you can use:

```
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.