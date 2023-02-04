#!/usr/bin/env python3
"""Version Pump Automation

- update pyproject.toml
- run pytest and doctest
- generate coverage report and github badges
- update changelog
- create new github commit, tag and release
- publish new version to PyPi

Examples: 
    - dry run
    ./pump.py patch
    
    - update pyproject.toml and local git tag
    ./pump.py patch --tag 

    - update everything and publish new version
    ./pump.py patch --tag --publish
"""

import toml
import argparse
from subprocess import getoutput


# handle arguments
parser = argparse.ArgumentParser(description="Pump Version")
parser.add_argument(
    "to_pump",
    choices=["major", "minor", "patch"],
    help="version part to pump",
)
parser.add_argument(
    "--tag",
    required=False,
    action="store_true",
    help="tag local commit with new version",
)
parser.add_argument(
    "--publish",
    required=False,
    action="store_true",
    help="publish to pypi and update github release",
)

args = parser.parse_args()


# parse toml
data = toml.load("pyproject.toml")
version = data["tool"]["poetry"]["version"]
major, minor, patch = map(int, version.split("."))


# pump version
locals()[args.to_pump] += 1
new_version = f"{major}.{minor}.{patch}"
data["tool"]["poetry"]["version"] = new_version

print(version, "->", new_version)

if args.tag:
    with open("pyproject.toml", "w") as f:
        toml.dump(data, f)
        print(f"pyproject.toml pumped to {new_version}")

    getoutput(f"git tag {new_version}")
    print(f"tag {new_version} added")

    # publish to pypi, update github release, commit changelog
    if args.publish:
        print("will publish")
        getoutput(f"git push --tag")
        print(f"pushed tag {new_version} to github")
        getoutput("./publish.sh now")
