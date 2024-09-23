# Set environment variables

This GitHub Action allows you to extract the `required_version` of Terraform specified in your configuration file (terraform.tf or another file of your choosing) and use it as an output within your GitHub Actions workflow. This is useful for ensuring that workflows adhere to the same Terraform version specified in the project configuration.

## How It Works

1. This action reads the specified file (default is terraform.tf) for the terraform.required_version directive.
2. It extracts the version and sets it as an output.
3. You can then use this output in other steps within your workflow.

## Use Cases

- **Version validation**: Ensure that all actions use the exact same Terraform version as defined in your project’s configuration.
- **Consistency checks**: Automate version checks for consistency across multiple repositories.
- **Terraform setup**: Use the extracted version to dynamically set up the correct version of Terraform for the workflow execution.

## Inputs

| Input Name  | Required | Default        | Description                                                                        |
| ----------- | -------- | -------------- | ---------------------------------------------------------------------------------- |
| `file-path` | Yes      | `terraform.tf` | The file path to the configuration file containing the `required_version` setting. |

## Outputs

| Output Name        | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| `required_version` | The `required_version` of Terraform as specified in the configuration file. |

## Usage

```yaml
- name: Get terraform version
  uses: cloudeteer/actions/get-terraform-version@get-terraform-version
  with:
    file-path: terraform.tf
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
        uses: cloudeteer/actions/get-terraform-version@get-terraform-version
        with:
          file-path: terraform.tf

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ steps.terraform_version.output.required_version }}
```
