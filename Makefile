venv:
	python3 -m venv venv

activate:
	. venv/bin/activate

install:
	pip install -r requirements.txt

precommit:
	git init
	git add .gitignore
	git add .pre-commit-config.yaml
	git add Config.py
	git add LICENSE
	git add main.py
	git add requirements.txt
	git add Makefile
	pre-commit install

setup: venv activate install precommit

clean:
	rm -rf venv

.PHONY: venv activate install precommit setup clean
