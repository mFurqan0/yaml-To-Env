import yaml
import pathlib
import shutil

def convert_yaml_to_env():
    # Set up paths to match your structure
    root_dir = pathlib.Path(__file__).parent
    yaml_files_dir = root_dir / "yamlFiles"  # Lowercase to match your image
    output_env_dir = root_dir / "ConvertedEnv"  # Capitalized to match your image

    # Clear existing output directory and recreate
    shutil.rmtree(output_env_dir, ignore_errors=True)
    output_env_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nConverting YAML from {yaml_files_dir} to .env in {output_env_dir}")

    # Process each YAML file
    for yaml_file in yaml_files_dir.glob("*.yaml"):
        try:
            print(f"\nProcessing: {yaml_file.name}")  
            
            # Read YAML with validation
            with yaml_file.open('r', encoding='utf-8') as f:
                configmap = yaml.safe_load(f) or {}
            
            # Verify structure
            if not isinstance(configmap.get("data"), dict):
                print(f"Skipping: No valid 'data' section in {yaml_file.name}. Ensure the YAML file contains a 'data' section with key-value pairs.")
                continue

            # Convert to .env format
            env_lines = []
            for key, value in configmap["data"].items():
                value = str(value)
                needs_quotes = any(c in value for c in {' ', '$', '=', '#', '\n', '\t'})
                env_lines.append(f'{key}="{value}"' if needs_quotes else f'{key}={value}')

            # Write output
            output_file = output_env_dir / f"{yaml_file.stem}.env"
            output_file.write_text("\n".join(env_lines), encoding='utf-8')
            print(f"✅ Created: {output_file.name}")

        except yaml.YAMLError as e:
            print(f"❌ Invalid YAML in {yaml_file.name}: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error with {yaml_file.name}: {str(e)}")

if __name__ == "__main__":
    convert_yaml_to_env()