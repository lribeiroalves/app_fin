from flask import render_template, abort

def index():
    return render_template('index.html')