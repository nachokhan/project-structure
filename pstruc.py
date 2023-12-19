import argparse
import os
import sys
from directory_structure import generate_directory_structure
from directory_structure import save_structure_to_file
from pretty_structure import pretty_print


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a directory structure in different formats.")
    parser.add_argument("directory", nargs="?", default=os.getcwd(), help="The directory to inspect.")
    parser.add_argument("-o", "--output", help="The output file name.")
    parser.add_argument("-f", "--format", choices=["json", "yaml", "txt"], default="yaml", help="The output file format.")
    parser.add_argument("-p", "--print", action="store_true", help="Print the directory structure without saving it.")
    parser.add_argument("-ns", "--not-save", action="store_true", help="Structure won't be saved in output file.")

    args = parser.parse_args()

    start_path = args.directory
    output_file = args.output
    output_format = args.format

    if output_file is None:
        # Use the directory name as the default output file name
        directory_name = os.path.basename(os.path.normpath(start_path))
        output_file = directory_name

    # Convert relative path to absolute path if necessary
    start_path = os.path.abspath(start_path)

    if output_format == "json":
        output_file += '.json'
    elif output_format == "yaml":
        output_file += '.yaml'
    elif output_format == "txt":
        output_file += '.txt'

    structure = generate_directory_structure(start_path, output_format)

    if structure is not None:

        if args.print:
            print_strcuture = generate_directory_structure(start_path, "json")
            pretty_print(print_strcuture)

        if "Error" in structure:
            print(structure)  # Print the error message
            sys.exit(1)
        else:
            if not args.not_save:
                error = save_structure_to_file(output_file, structure)
                if error:
                    print(error)  # Print the error message
                else:
                    print(f"Directory structure has been generated and saved to '{output_file}'.")
