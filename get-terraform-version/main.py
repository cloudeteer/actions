import hcl2
import os


def get_required_version():
    file_path = os.environ["file_path"]
    with open(file_path, "r") as file:
        conf = hcl2.load(file)

        if "terraform" not in conf:
            raise Exception(
                f'"terraform" configuration block not found in "{file_path}"'
            )

        elif "required_version" not in conf["terraform"][0]:
            raise Exception(f'"required_version" not found in "{file_path}"')

        else:
            required_version = conf["terraform"][0]["required_version"]
            print(f'Terraform version "{required_version}" found in "{file_path}"')
            return required_version


def set_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as file:
        print(f"Setting GitHub Actions output: {name}={value}")
        print(f"{name}={value}", file=file)


required_version = get_required_version()

if required_version:
    set_output("required_version", required_version)
