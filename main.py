import webview
import socket
from app import create_app

if __name__ == '__main__':
    app = create_app()

    window = webview.create_window('App Financeiro', app, width=5000, height=5000, resizable=False)

    webview.start(http_server=True)