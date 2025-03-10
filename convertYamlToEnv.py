import yaml
import pathlib

def convertYamlToEnv():
    # Define paths (use relative paths for GitHub Actions compatibility)
    yamlFilesDir = pathlib.Path("yamlFiles")  # Input YAML files
    outputEnvDir = pathlib.Path("convertedYamlToEnv")  # Output .env files
    
    # Create output directory (force creation if missing)
    outputEnvDir.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {outputEnvDir}")  # Debug line

    # Process each YAML file
    for yamlFile in yamlFilesDir.glob("*.yaml"):
        try:
            print(f"Processing file: {yamlFile}")  # Debug line
            with yamlFile.open('r', encoding='utf-8') as f:
                configmap = yaml.safe_load(f)
            
            # Extract data section
            data = configmap.get("data", {})
            print(f"Extracted data: {data}")  # Debug line
            
            # Create .env content
            envContent = []
            for key, value in data.items():
                if any(char in value for char in {' ', '$', '=', '#'}):
                    envContent.append(f'{key}="{value}"')
                else:
                    envContent.append(f"{key}={value}")
            
            # Write .env file
            envFilename = outputEnvDir / f"{yamlFile.stem}.env"
            with envFilename.open('w', encoding='utf-8') as envF:
                envF.write("\n".join(envContent))
            
            print(f"Converted: {yamlFile.name} => {envFilename.name}")

        except Exception as e:
            print(f"Error processing {yamlFile.name}: {str(e)}")

if __name__ == "__main__":
    convertYamlToEnv()