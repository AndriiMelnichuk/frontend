from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker
from app.models import Group
from app.routes import signin

import json

task = Blueprint('task', __name__)

@task.route('/<groupId>')
def getTasks(groupId):
    tasks = InternetTalker.getTasksFromGroup(groupId)
    return jsonify([{'id': t.id,
                     'title': t.title,
                     'description': t.description,
                     'assigned': t.assigned,
                     'status': t.status,
                     'date': t.date} for t in tasks])


@task.route('/update/<group_name>')
def updateTask(group_name):
    id = request.args.get('id')
    data = request.args.get('data')
    data = json.loads(data)
    InternetTalker.updateTask(id, data)
    return redirect(url_for('group.selectGroup',name=group_name, id=id))


@task.route('/complete/<groupName>/<taskId>/<groupId>')
def completeTask(groupName, taskId, groupId):
    InternetTalker.completeTask(taskId, groupId)
    return redirect(url_for('group.selectGroup',name=groupName, id=groupId))


@task.route('/delete/<groupName>/<taskId>/<groupId>')
def deleteTask(groupName, taskId, groupId):
    InternetTalker.deleteTask(groupId, taskId)
    return redirect(url_for('group.selectGroup',name=groupName, id=groupId))


@task.route('/search/<groupId>')
def searchTasksInGroupRoute(groupId):
    # tasks = InternetTalker.searchTasksInGroup()
    # TODO: Нужно будет удалить этот роут. Во время запроса заданий будет проверятся поиск и фильтр
    pass

@task.route('/create/<groupName>/<groupId>')
def createTaskRoute(groupName, groupId):
    
    task_name = request.args.get('task_name')
    description = request.args.get('description')
    deadline = request.args.get('deadline')
    todo_task = 'True' if request.args.get('todo_task') == 'true' else 'False'
    members = request.args.get('members')
    if members == '':
        members = []
    if not isinstance(members, list):
        members = [members]
    if deadline == '':
        deadline = '2099-01-01'

    InternetTalker.add_task(groupId,task_name, description, deadline, todo_task, members)
    return redirect(url_for('group.selectGroup',name=groupName, id=groupId))

    
