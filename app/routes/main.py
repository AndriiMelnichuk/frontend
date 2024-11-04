from flask import Blueprint, render_template

from app.utils import InternetTalker

# TODO Добавить регистрацию через гугл
main = Blueprint('main', __name__)



@main.route('/')
def index():
    if InternetTalker.isAccesToken():
        return render_template('main.html')
    return render_template('sign-in-or-up.html')

