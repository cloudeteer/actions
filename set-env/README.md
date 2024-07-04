# Set environment variables

This action arises from the problem that environment variables cannot be passed to a reusable workflow. To pass environment variables from a caller workflow to a reusable workflow, it is necessary to pass them via inputs or secrets. These passed values can easily be set as environment variables in the reusable workflow using this action.

## Usage

```yaml
- name: Set environment variables from input
  uses: cloudeteer/actions/set-env@main
  with:
    env: |
      ARM_STORAGE_USE_AZUREAD: true
      TF_VAR_a_number: "5"
      TF_VAR_another_one: string value here
```

### Full example

```yaml
name: reusable workflow
on:
  workflow_call:
    inputs:
      env:
        required: false
        type: string
    secrets:
      env:
        required: false
jobs:
  reusable:
    runs-on: ubuntu-latest
    steps:
      - name: Set environment variables from input
        uses: cloudeteer/actions/set-env@main
        with:
          env: ${{ inputs.env }}
      - name: Set environment variables from secrets
        uses: cloudeteer/actions/set-env@main
        with:
          env: ${{ secrets.env }}
```

```yaml
name: caller workflow
on: workflow_dispatch
jobs:
  caller:
    uses: cloudeteer/workflows/.github/workflows/reusable.yaml
    with:
      env: |
        ARM_STORAGE_USE_AZUREAD: true
    secrets:
      env: |
        TF_VAR_github_pat: ${{ secrets.CDT_GITHUB_PAT }}
```
