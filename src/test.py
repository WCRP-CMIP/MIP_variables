import pytest
import json
import os
from jsonschema import validate, ValidationError

'''
 pytest conftest.py --dir ../data_descriptors/variables/
'''

# Set a default path for the directory
DEFAULT_DIR = './'  # Change this to your desired default directory

def pytest_addoption(parser):
    parser.addoption("--dir", action="store", default=DEFAULT_DIR, help="Path to directory containing the schema & files")

@pytest.fixture(scope='session')
def dir(request):
    # Get the directory from the command line argument or use the default
    return os.path.abspath(request.config.getoption("--dir"))

@pytest.fixture(scope='session')
def schema(dir):
    schema_path = os.path.join(dir, '_schema.jsonld')
    with open(schema_path, 'r') as f:
        content = json.load(f)
    return content

def test_all_files(schema, dir):
    # Iterate over each file in the specified directory
    print('--------',dir)
    # for filename in os.listdir(dir):
    #     if filename.endswith('.json'):  # Assuming you want to validate .json files
    #         file_path = os.path.join(dir, filename)
    #         with open(file_path, 'r') as f:
    #             file_content = json.load(f)

    #         # Validate the file content against the schema
    #         try:
    #             validate(instance=file_content, schema=schema)
    #         except ValidationError as e:
    #             pytest.fail(f"Validation error in file {filename}: {e.message}")
