from flask import Blueprint, render_template, request, redirect, jsonify
import json
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
    
@calendar.route('/task/update/')
def updateTask():
    id = request.args.get('id')
    data = request.args.get('data')
    data = json.loads(data)
    InternetTalker.updateTask(id, data)
    return redirect('/calendar')


@calendar.route('/task/complete/<taskId>/<groupId>')
def completeTask(taskId, groupId):
    InternetTalker.completeTask(taskId, groupId)
    return redirect('/calendar')


@calendar.route('/task/delete/<taskId>/<groupId>')
def deleteTask(taskId, groupId):
    InternetTalker.deleteTask(groupId, taskId)
    return redirect('/calendar')