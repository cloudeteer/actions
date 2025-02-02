# Set environment variables

This GitHub Action allows you to extract the version of Terraform specified in your configuration and use it as an output within your GitHub Actions workflow. This is useful for ensuring that workflows adhere to the same Terraform version specified in the project configuration.

## How It Works

1. This action reads given files in a directory for Terraform version directive.
2. It extracts the version and sets it as an output.
3. You can then use this output in other steps within your workflow.

## Use Cases

- **Version validation**: Ensure that all actions use the exact same Terraform version as defined in your project’s configuration.
- **Consistency checks**: Automate version checks for consistency across multiple repositories.
- **Terraform setup**: Use the extracted version to dynamically set up the correct version of Terraform for the workflow execution.

## Inputs

| Input Name  | Required | Default                              | Description                                                     |
|-------------|----------|--------------------------------------|-----------------------------------------------------------------|
| `directory` | No       | `.`                                  | The directory path to search for the Terraform version setting. |
| `file`      | No       | `*.tf`                               | The file pattern to search for the Terraform version setting.   |
| `pattern`   | No       | `^\s*required_version\s*=\s*"(.*?)"` | The pattern to search for the Terraform version setting.        |

## Outputs

| Output Name        | Description                                                            |
|--------------------|------------------------------------------------------------------------|
| `required_version` | The `required_version` of Terraform as specified in the configuration. |

## Usage

```yaml
- name: Get terraform version
  uses: cloudeteer/actions/get-terraform-version@main
```

### Full example

```yaml
name: Setup Terraform

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Get Terraform version
        id: terraform_version
        uses: cloudeteer/actions/get-terraform-version@main

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ steps.terraform_version.output.required_version }}
```

### Custom directory, file and pattern

The following example extracts the Terraform version from the `.terraform-version` file, which is used by tools such as [tenv](https://github.com/tofuutils/tenv) and [tfenv](https://github.com/tfutils/tfenv). In this example, the file is located in a custom directory, `path/to/terraform/config`, and contains only the Terraform version. As a result, the pattern `^(.*)$` is used to match its content.

```yaml
- name: Get Terraform version
  id: terraform_version
  uses: cloudeteer/actions/get-terraform-version@main
  with:
    directory: path/to/terraform/config
    file: ".terraform-version"
    pattern: "^(.*)$"
```

The next example extracts the Terraform version from the [asdf](https://asdf-vm.com/) configuration file `.tool-versions`. In this example, the configuration file is also located in a custom directory, `path/to/terraform/config`. The pattern used matches the [configuration](https://asdf-vm.com/manage/configuration.html) syntax of the `asdf` tool.

```yaml
- name: Get Terraform version
  id: terraform_version
  uses: cloudeteer/actions/get-terraform-version@main
  with:
    directory: path/to/terraform/config
    file: ".tool-versions"
    pattern: "^terraform (.*)$"
```
