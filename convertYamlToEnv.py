import yaml
import pathlib

def convert_yaml_to_env():
    # Define paths
    yaml_files_dir = pathlib.Path("yamlFiles")  # Input YAML files directory
    output_env_dir = pathlib.Path("convertedYamlToEnv")  # Output .env files directory

    # Create output directory if it doesn't exist
    output_env_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {output_env_dir}")

    # Process each YAML file
    for yaml_file in yaml_files_dir.glob("*.yaml"):
        try:
            print(f"Processing file: {yaml_file}")

            # Read the YAML file
            with yaml_file.open('r', encoding='utf-8') as f:
                configmap = yaml.safe_load(f)

            # Extract the 'data' section
            data = configmap.get("data", {})
            if not data:
                print(f"No 'data' section found in {yaml_file.name}. Skipping.")
                continue

            print(f"Extracted data: {data}")

            # Prepare .env content
            env_content = []
            for key, value in data.items():
                # Handle special characters by quoting the value if necessary
                if any(char in str(value) for char in {' ', '$', '=', '#', '\n', '\t'}):
                    env_content.append(f'{key}="{value}"')
                else:
                    env_content.append(f"{key}={value}")

            # Write to .env file
            env_filename = output_env_dir / f"{yaml_file.stem}.env"
            with env_filename.open('w', encoding='utf-8') as env_f:
                env_f.write("\n".join(env_content))

            print(f"Successfully converted: {yaml_file.name} => {env_filename.name}")

        except Exception as e:
            print(f"Error processing {yaml_file.name}: {str(e)}")
            continue

if __name__ == "__main__":
    convert_yaml_to_env()