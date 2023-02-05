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
from click import argument, Choice, option, command, secho
from subprocess import getstatusoutput
from functools import reduce

CHOICES = ["major", "minor", "patch"]


# === uti ===
def abort(msg: str = "") -> None:
    secho(msg or "Aborted.", fg="red")
    exit(1)


def run(cmd: str) -> None:
    """run shell command"""
    secho(cmd)
    if getstatusoutput(cmd)[0]:
        abort()


# === main ===


@command()
@argument("section", type=Choice(CHOICES))
@option("--tag/--no-tag", help="tag local commit with new version", default=False)
@option(
    "--publish/--no-publish",
    help="publish to pypi and update github release",
    default=False,
)
def main(section, tag, publish):
    # print(section, tag, publish)

    # parse toml
    data = toml.load("pyproject.toml")
    version = data["tool"]["poetry"]["version"]
    ver_dict = {k: int(v) for k, v in zip(CHOICES, version.split("."))}

    # pump version
    ver_dict[section] += 1
    new_version = reduce("{}.{}".format, ver_dict.values())
    data["tool"]["poetry"]["version"] = new_version

    print(version, "->", new_version)

    if tag:
        with open("pyproject.toml", "w") as f:
            toml.dump(data, f)
            print(f"pyproject.toml pumped to {new_version}")

        run(f"git tag {new_version}")

        # publish to pypi, update github release, commit changelog
        if publish:
            cmds = [
                "git push --tag",
                # run test w/ coverage
                "coverage run -m pytest --doctest-modules",
                "coverage report",
                # create html report for docs
                "coverage html -d docs/assets/coverage",
                "rm docs/assets/coverage/.gitignore",
                # not use `coverage.xml` to avoid ignore
                "coverage xml -o docs/assets/coverage-report.xml",
                # create coverage badge
                "genbadge coverage -i docs/assets/coverage-report.xml -o docs/assets/coverage-badge.svg",
                # update changelog
                "auto-changelog",
                '[ -x "$(command -v prettier)" ] && prettier -w CHANGELOG.md',
                # commit docs and changelog Δ
                'git add . && git cm -am "chore: update changelog, version pump" && git push',
                # clear previous built assets
                "rm -rf dist/*",
                # build and publish to pypi
                "poetry publish --build",
                f"echo {new_version} published to PyPi",
                # update github release to the current tag
                "gh release create $(git describe --tags --abbrev=0) ./dist/*"
                f"echo github release pumped to {new_version}",
            ]

            for cmd in cmds:
                run(cmd)
