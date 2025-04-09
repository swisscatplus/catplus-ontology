import json
import os
import argparse

def transform_numeric_lists(data):
    """
    Recursively transforms lists with only numeric values to lists of size 1.

    Args:
        data: The JSON data (dict, list, or primitive).

    Returns:
        The transformed JSON data.
    """
    if isinstance(data, list):
        if all(isinstance(item, (int, float)) for item in data):
            if data:
                return [data[0]]  # Keep only the first element
            else:
                return [] #if the list is empty, keep it empty.
        else:
            return [transform_numeric_lists(item) for item in data]
    elif isinstance(data, dict):
        return {key: transform_numeric_lists(value) for key, value in data.items()}
    else:
        return data

def process_json_file(input_file, output_file):
    """
    Reads a JSON file, transforms it, and writes the transformed JSON to output.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file.
    """
    try:
        with open(input_file, 'r') as infile:
            json_data = json.load(infile)

        transformed_data = transform_numeric_lists(json_data)

        with open(output_file, 'w') as outfile:
            json.dump(transformed_data, outfile, indent=4)

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")

def main():
    """Parses command-line arguments and processes the JSON file."""
    parser = argparse.ArgumentParser(description="Transforms numeric lists in JSON.")
    parser.add_argument("input_file", help="Path to the input JSON file.")

    args = parser.parse_args()
    input_file = args.input_file

    # Derive output file name
    base_name, extension = os.path.splitext(input_file)
    output_file = f"{base_name}-no-data{extension}"

    process_json_file(args.input_file, output_file)

if __name__ == "__main__":
    main()
