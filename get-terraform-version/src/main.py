import os
import re
import glob


def get_directory():
    return os.environ["directory"]


def get_required_version():
    directory = get_directory()  # Access "directory" here
    required_version = None
    """
    Extract the 'required_version' from all Terraform files in a directory.
    
    :param directory: Path to the directory containing Terraform files
    :return: The 'required_version' found in the Terraform files
    """
    tf_files = glob.glob(os.path.join(directory, "*.tf"))  # List all .tf files in the directory

    for file_path in tf_files:
        with open(file_path, "r") as file:
            content = file.read()
            match = re.search(r'required_version\s*=\s*"(.*?)"', content)
            if match:
                version = match.group(1)
                print(f'::notice::Terraform version "{version}" found in "{file_path}"')
                required_version = version
            else:
                print(f'::debug::"required_version" not found in "{file_path}"')

    return required_version


def set_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as file:
        print(f"Setting GitHub Actions output: {name}={value}")
        print(f"{name}={value}", file=file)


if __name__ == "__main__":
    required_version = get_required_version()

    if required_version:
        set_output("required_version", required_version)
