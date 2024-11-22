# Manage GitHub Project

Adds issues or pull requests to a specified GitHub project.

## Usage

Token with following permissions required:

- repo:issues: read
- repo:pullrequest: read
- org:project: readwrite

```yaml
# use inputs.app-id && inputs.private-key to generate a token from a github app
- uses: cloudeteer/actions/manage-github-project@main
  with:
    project-url: https://github.com/orgs/MyOrg/projects/1
    app-id: ${{ vars.APP_ID }}
    private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

```yaml
# use inputs.github-token to authenticate using a personal access token
- uses: cloudeteer/actions/manage-github-project@main
  with:
    project-url: https://github.com/orgs/MyOrg/projects/1
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Full example

```yaml
name: caller workflow
on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]
jobs:
  manage-github-project:
    runs-on: ubuntu-latest
    steps:
      - uses: cloudeteer/actions/manage-github-project@main
        with:
          project-url: https://github.com/orgs/MyOrg/projects/1
          app-id: ${{ vars.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}
```
