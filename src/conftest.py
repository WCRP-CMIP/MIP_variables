import json
import os
import sys
import glob
from jsonschema import validate, ValidationError
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # Import tqdm for progress tracking

# Set a default path for the directory
DEFAULT_DIR = sys.argv[1]  # Directory specified by command line argument

def load_schema(schema_path):
    """Load the JSON schema from the specified file."""
    with open(schema_path, 'r') as f:
        return json.load(f)

def get_json_files(dir_path):
    """Get a list of JSON files for testing."""
    return [f for f in glob.glob(os.path.join(dir_path, '*.json')) if not os.path.basename(f).startswith('_')]

def validate_file(schema, filename):
    """Validate a single JSON file against the schema."""
    with open(filename, 'r') as f:
        file_content = json.load(f)

    # Validate and return the result
    try:
        validate(instance=file_content, schema=schema)
        return filename, None  # No error
    except ValidationError as e:
        return filename, e  # Return the validation error

def main(schema_path, dir_path):
    """Main function to validate JSON files against the schema."""
    schema = load_schema(schema_path)
    json_files = get_json_files(dir_path)

    # Use ThreadPoolExecutor for parallel validation
    with ThreadPoolExecutor() as executor:
        # Create futures for all files
        futures = {executor.submit(validate_file, schema, filename): filename for filename in json_files}

        # Use tqdm to show progress
        for future in tqdm(as_completed(futures), total=len(futures), desc="Validating JSON files"):
            filename = futures[future]
            try:
                result = future.result()
                if result[1] is not None:  # If there was an error
                    filename, error = result
                    print(f">>> Validation error in {filename}: {error.message}")
            except Exception as e:
                print(f">>> Error processing file {filename}: {str(e)}")

if __name__ == "__main__":
    # Define the schema file and directory path
    schema_path = os.path.join(DEFAULT_DIR, '_schema')
    dir_path = os.path.abspath(DEFAULT_DIR)  # You can modify this to any directory
    main(schema_path, dir_path)
