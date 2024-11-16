from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker
from app.models import Group
from app.routes import signin

task = Blueprint('task', __name__)

@task.route('/<groupId>')
def getTasks(groupId):
    tasks = InternetTalker.getTasksFromGroup(groupId)
    # TODO modify feature 
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
    # TODO Настроить обработку данных и их отпраку
    InternetTalker.completeTask(task, id)
    return redirect(f'/group/{group_name}?id={id}')


@task.route('/complete/<groupName>/<taskId>/<groupId>')
def completeTask(grouName, taskId, groupId):
    InternetTalker.completeTask(taskId, groupId)
    return redirect(f'/group/{grouName}/?id={groupId}')


@task.route('/delete/<groupName>/<taskId>/<groupId>')
def deleteTask(groupName, taskId, groupId):
    InternetTalker.deleteTask(taskId, groupId)
    return redirect(f'/group/{groupName}/?id={groupId}')


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
    todo_task = request.args.get('todo_task')
    members = request.args.get('members')
    InternetTalker.add_task(groupId,task_name, description, deadline, todo_task, members)
    return redirect(f'/group/{groupName}/?id={groupId}')
    
