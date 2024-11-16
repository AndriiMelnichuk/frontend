from flask import Blueprint, render_template, session
from app.utils import InternetTalker

# TODO Добавить регистрацию через гугл
main = Blueprint('main', __name__)



@main.route('/')
def index():
    if not InternetTalker.isAccesToken():
        return render_template('sign-in-or-up.html')
    return render_template('main.html')
    

@main.route('/exit')
def exit_route():
    session.clear()
    return 'ok'


