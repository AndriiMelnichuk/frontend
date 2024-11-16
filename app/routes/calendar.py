from flask import Blueprint, render_template, request, redirect

from app.utils import Validator 

calendar = Blueprint('calendar', __name__)

@calendar.route('/')
def mainCalendarRoute():
    return render_template('calendar.html')

calendar.route('/tasks/<dateString>')
def getAllAssignedTaskRoute(dateString):
    # TODO: добавить в интернет толкер, 
    # изменить ссылку на странице, 
    # сделать мок результат
    pass