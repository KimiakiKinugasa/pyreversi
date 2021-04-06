PACKAGE := pyreversi

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | \
		awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {\
			split(\$$1,A,/ /);for(i in A)print A[i]\
		}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

lint:
	@poetry run pylint -d C $(PACKAGE)
	@poetry run mypy .

clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

env-clean: clean
	@rm -rf .venv
	@rm -rf .tox

format:
	@poetry run isort .
	@poetry run black .

# GitHub dependency graph does not support poetry.lock
# https://docs.github.com/en/code-security/supply-chain-security/about-the-dependency-graph#supported-package-ecosystems
requirements:
	@poetry export --without-hashes -f requirements.txt -o requirements.txt

setup:
	@poetry install

test:
	@poetry run pytest

version:
	@sed -n 's/version = \(.*\)/__version__ = \1/p' pyproject.toml > $(PACKAGE)/_version.py

pre-commit: requirements version format lint test

# run tests against all supported python versions
tox:
	@tox
