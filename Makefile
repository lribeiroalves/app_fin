.PHONY: updatereq install run run-window build

updatereq:
	pip-compile requirements.in

install:
	pip install -r requirements.txt

run:
	flask run

run-window:
	python3 ./main.py

build:
	pyinstaller --noconsole --onefile --windowed --add-data "app;app" --add-data "config;config" --collect-data webview --hidden-import webview --hidden-import flask_migrate --hidden-import flask_sqlalchemy --hidden-import dynaconf main.py
