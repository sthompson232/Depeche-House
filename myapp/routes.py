from app import app
from flask import request, render_template, flash, redirect,url_for
from models import User


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')