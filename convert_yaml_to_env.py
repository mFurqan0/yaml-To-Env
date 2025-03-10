import yaml
import pathlib

def convert_yaml_to_env():
    # Define paths (use relative paths for GitHub Actions compatibility)
    yaml_files_dir = pathlib.Path("YAML_FILES")  # Input YAML files
    output_env_dir = pathlib.Path("CONVERTED_YAML_TO_ENV")  # Output .env files
    
    # Create output directory (force creation if missing)
    output_env_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {output_env_dir}")  # Debug line

    # Process each YAML file
    for yaml_file in yaml_files_dir.glob("*.yaml"):
        try:
            print(f"Processing file: {yaml_file}")  # Debug line
            with yaml_file.open('r', encoding='utf-8') as f:
                configmap = yaml.safe_load(f)
            
            # Extract data section
            data = configmap.get("data", {})
            print(f"Extracted data: {data}")  # Debug line
            
            # Create .env content
            env_content = []
            for key, value in data.items():
                if any(char in value for char in {' ', '$', '=', '#'}):
                    env_content.append(f'{key}="{value}"')
                else:
                    env_content.append(f"{key}={value}")
            
            # Write .env file
            env_filename = output_env_dir / f"{yaml_file.stem}.env"
            with env_filename.open('w', encoding='utf-8') as env_f:
                env_f.write("\n".join(env_content))
            
            print(f"Converted: {yaml_file.name} => {env_filename.name}")

        except Exception as e:
            print(f"Error processing {yaml_file.name}: {str(e)}")

if __name__ == "__main__":
    convert_yaml_to_env()