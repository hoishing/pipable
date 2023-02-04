# ⚠️ intent to invok by pump.py ⚠️

if ! [[ "$1" =~ [0-9]+\.[0-9]+\.[0-9]+ ]]; then
  echo "publish require version argement" >&2
  exit 1
fi

# run test w/ coverage, abort publish if failed
if ! coverage run -m pytest --doctest-modules; then
  echo publish abort ⚠️
  exit 1
fi

# create coverage report
coverage report
echo coverage report for $1 updated

# create html report for docs
coverage html -d docs/assets/coverage
rm docs/assets/coverage/.gitignore

# create coverage badge
coverage xml -o docs/assets/coverage-report.xml # not use `coverage.xml` to avoid ignore
genbadge coverage -i docs/assets/coverage-report.xml -o docs/assets/coverage-badge.svg
echo coverage badge created

# update changelog
auto-changelog
[ -x "$(command -v prettier)" ] && prettier -w CHANGELOG.md
echo changelog for $1 created

# commit docs and changelog Δ
git add . && git cm -am "chore: update changelog, version pump" && git push
echo changlog pushed to github

# clear previous built assets
rm -rf dist/*

# build and publish to pypi
poetry publish --build
echo $1 published to PyPi

# update github release to the current tag
gh release create $(git describe --tags --abbrev=0) ./dist/*
echo github release pumped to $1
