from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker
from app.models import Group
from app.routes import signin

task = Blueprint('task', __name__)

@task.route('/<groupId>')
def getTasks(groupId):
    tasks = InternetTalker.getTasksFromGroup(groupId)
    
    return jsonify([{'id': t.id,
                     'title': t.title,
                     'description': t.description,
                     'assigned': t.assigned,
                     'created': t.created,
                     'status': t.status,
                     'data': t.date} for t in tasks])

@task.route('/update/')
def updateTask():
    id = request.args.get('id')
    data = request.args.get('data')
    group = Group(id, 'name', 'administrator')
    InternetTalker.completeTask(task, group)
    return redirect(f'/group/{group.name}?id={group.id}&admin={group.administrator}')

@task.route('/complete/<taskId>/<groupId>')
def completeTask(taskId, groupId):
    InternetTalker.completeTask(task, groupId)
    group = InternetTalker.getGroupById(groupId)
    return redirect(f'/group/{group.name}?id={group.id}&admin={group.administrator}')

@task.route('/delete/<taskId>/<groupId>')
def deleteTask(taskId, groupId):
    group = InternetTalker.getGroupById(groupId)
    InternetTalker.deleteTask(task, group)
    return redirect(f'/group/{group.name}?id={group.id}&admin={group.administrator}')

@task.route('/search/<groupId>')
def searchTasksInGroupRoute(groupId):
    # tasks = InternetTalker.searchTasksInGroup()
    group = InternetTalker.getGroupById(groupId)
    return redirect(f'/group/{group.name}?id={group.id}&admin={group.administrator}')
    # return render_template("group.html", groupName=groupName, tasks=tasks, isAdmin=InternetTalker.isAdministrator(groupName))

@task.route('/create/<groupId>')
def createTaskRoute(groupId):
    # TODO
    group = InternetTalker.getGroupById(groupId)
    return redirect(f'/group/{group.name}?id={group.id}&admin={group.administrator}')
    
