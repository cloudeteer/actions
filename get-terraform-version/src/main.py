import hcl2
import os
import glob


def get_directory():
    return os.environ["directory"]


def get_required_version():
    directory = get_directory()  # Access "directory" here
    required_version = None
    for file_path in glob.glob(f"{directory}/*.tf"):
        with open(file_path, "r") as file:
            conf = hcl2.load(file)

            if "terraform" not in conf:
                print(
                    f'::debug::"terraform" configuration block not found in "{file_path}"'
                )

            elif "required_version" not in conf["terraform"][0]:
                print(f'::debug::"required_version" not found in "{file_path}"')

            else:
                required_version = conf["terraform"][0]["required_version"]
                print(
                    f'::notice::Terraform version "{required_version}" found in "{file_path}"'
                )

    if not required_version:
        raise Exception(f'::warning::"required_version" not found in "{directory}"')
    else:
        return required_version


def set_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as file:
        print(f"Setting GitHub Actions output: {name}={value}")
        print(f"{name}={value}", file=file)


if __name__ == "__main__":
    required_version = get_required_version()

    if required_version:
        set_output("required_version", required_version)
