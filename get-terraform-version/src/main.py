import os
import re
import glob


def get_directory():
    return os.environ["directory"]


def get_required_version():
    """
    Extract the 'required_version' from all Terraform files in a directory,
    skipping commented-out lines.

    :return: The 'required_version' found in the Terraform files
    """
    directory = get_directory()  # Access "directory" here
    required_version = None

    # List all .tf files in the directory
    tf_files = glob.glob(os.path.join(directory, "*.tf"))

    # Regular expression to match required_version, ignoring commented lines
    regex = re.compile(
        r'^(?!\s*(#|//))\s*required_version\s*=\s*"(.*?)"',
        re.MULTILINE
    )

    for file_path in tf_files:
        with open(file_path, "r") as file:
            content = file.read()
            matches = regex.findall(content)
            for match in matches:
                version = match[1]
                print(f'::notice::Terraform version "{version}" found in "{file_path}"')
                required_version = version
                break
            if not matches:
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
