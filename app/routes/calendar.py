from flask import Blueprint, render_template, request, redirect, jsonify

from app.utils import Validator, InternetTalker

calendar = Blueprint('calendar', __name__)

@calendar.route('/')
def mainCalendarRoute():
    return render_template('calendar.html')

@calendar.route('/tasks/<dateString>')
def getAllAssignedTaskRoute(dateString):
    # TODO: добавить в интернет толкер, 
    # изменить ссылку на странице, 
    # сделать мок результат
    tasks = InternetTalker.getAllAssignedTask(dateString)
    return jsonify([{'group_id': t.group_id,
                     'task_id': t.task_id,
                     'title': t.title,
                     'description': t.description,
                     'assigned': t.assigned,
                     'status': t.status,
                     'date': t.date} for t in tasks])
    