from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker
from app.models import Group

# TODO Добавить регистрацию через гугл
main = Blueprint('main', __name__)



@main.route('/')
def index():
    if InternetTalker.isAccesToken():
        return render_template('main.html')
    return render_template('sign-in-or-up.html')

@main.route('/test')
def test():
    return render_template('sign-in-or-up.html')
