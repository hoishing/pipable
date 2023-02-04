# ⚠️ to be invoked by version_pump.py ⚠️

# fool proof by enforcing 1st arg to 'now'
if [ "$1" != "now" ]; then
  echo "confirm publish with arg 'now'" >&2
  exit 1
fi

# run test w/ coverage, abort publish if failed
if ! coverage run -m pytest --doctest-modules; then
  echo publish abort ⚠️
  exit 1
fi

# create coverage report
coverage report

# create html report for docs
coverage html -d docs/assets/coverage
rm docs/assets/coverage/.gitignore

# create coverage badge
coverage xml -o docs/assets/coverage-report.xml # not use `coverage.xml` to avoid ignore
genbadge coverage -i docs/assets/coverage-report.xml -o docs/assets/coverage-badge.svg

# update changelog
auto-changelog
[ -x "$(command -v prettier)" ] && prettier -w CHANGELOG.md

# commit docs and changelog Δ
git add . && git cm -am "chore: update changelog, version pump" && git push

# clear previous built assets
rm -rf dist/*

# build and publish to pypi
poetry publish --build

# update github release to the current tag
gh release create $(git describe --tags --abbrev=0) ./dist/*
