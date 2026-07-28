.PHONY: updatereq install run run-window build linux-janela

updatereq:
	pip-compile requirements.in

install:
	pip install -r requirements.txt

run:
	flask run

run-window:
	python3 ./main.py

build:
	pyinstaller --onefile --add-data "app;app" --add-data "config;config" --add-data "migrations;migrations" --collect-data webview --hidden-import webview --hidden-import flask_migrate --hidden-import flask_sqlalchemy --hidden-import dynaconf --hidden-import logging.config main.py

linux-janela:
	pip install PyQt6 PyQt6-WebEngine qtpy
