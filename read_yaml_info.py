import os
import yaml

def read_schema_info_from_resources(resources_dir="resources", output_file="schema_summary.yaml"):
    """
    Reads all YAML files in a given directory, extracts the title and 
    description from the 'schema_info' section, and saves them to a YAML file.

    Args:
        resources_dir (str): The path to the directory containing YAML files.
        output_file (str): The path to the output YAML file.
    """
    if not os.path.isdir(resources_dir):
        print(f"Error: Directory '{resources_dir}' not found.")
        return

    print(f"Scanning for YAML files in '{resources_dir}'...")
    
    all_schemas_info = []

    for filename in sorted(os.listdir(resources_dir)):
        if filename.endswith((".yaml", ".yml")) and filename != "MIE_template.yaml":
            file_path = os.path.join(resources_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    data = yaml.safe_load(f)
                    
                    if isinstance(data, dict):
                        schema_info = data.get('schema_info')
                        if isinstance(schema_info, dict):
                            title = schema_info.get('title')
                            description = schema_info.get('description')

                            if title:
                                db_name = os.path.splitext(filename)[0]
                                all_schemas_info.append({
                                    'database': db_name,
                                    'title': title,
                                    'description': description or "No description found."
                                })
                            else: 
                                print(f"Warning: No 'title' in 'schema_info' for {filename}.")
                        else:
                            print(f"Warning: No 'schema_info' section in {filename}.")
                    else:
                        print(f"Warning: YAML file {filename} is empty or not a dictionary.")

            except yaml.YAMLError as e:
                print(f"Error parsing YAML file {filename}: {e}")
            except Exception as e:
                print(f"An error occurred with file {filename}: {e}")

    try:
        with open(output_file, 'w') as f:
            yaml.dump(all_schemas_info, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"\nSuccessfully saved schema information to '{output_file}'.")
    except Exception as e:
        print(f"\nError writing to output file '{output_file}': {e}")

if __name__ == "__main__":
    # Assuming the script is run from the root of the project directory
    read_schema_info_from_resources()