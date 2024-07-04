from os import getenv
from yaml import safe_load

env = safe_load(getenv("env", "")) or {}
github_env_file = getenv("GITHUB_ENV")

# Write each env as "key=value" into GITHUB_ENV file
with open(github_env_file, "a") as f:
    for key, value in env.items():
        if value:
            if isinstance(value, bool):
                value = str(value).lower()
            f.write(key + "=" + str(value) + "\n")
