import os
import re
import glob


def get_directory():
    return os.environ.get("directory", ".")


def get_file():
    return os.environ.get("file", "*.tf")


def get_pattern():
    return os.environ.get("pattern", r'^\s*required_version\s*=\s*"(.*?)"')


def get_required_version() -> str:
    """
    Extract the 'required_version' from all Terraform files in a directory,
    skipping commented-out lines.

    :return: The 'required_version' found in the Terraform files
    """
    directory = get_directory()
    file = get_file()
    pattern = get_pattern()
    required_version = None

    # List all files matching the "file"-pattern in the directory
    tf_files = glob.glob(os.path.join(directory, file))

    # Regular expression to match required_version, ignoring commented lines
    regex = re.compile(
        pattern,
        re.MULTILINE
    )

    for file_path in tf_files:
        with open(file_path, "r") as file:
            content = file.read()
            # remove comments from content
            content = re.sub(r'(?m)^\s*#.*\n?', '', content)
            matches = regex.findall(content)
            for match in matches:
                version = match
                print(f'::notice::Terraform version "{version}" found in "{file_path}"')
                required_version = version
                break
            if not matches:
                print(f'::debug::"required_version" not found in "{file_path}"')

    return required_version


def set_output(name, value) -> None:
    with open(os.environ["GITHUB_OUTPUT"], "a") as file:
        print(f"Setting GitHub Actions output: {name}={value}")
        print(f"{name}={value}", file=file)


if __name__ == "__main__":
    required_version = get_required_version()

    if required_version:
        set_output("required_version", required_version)
