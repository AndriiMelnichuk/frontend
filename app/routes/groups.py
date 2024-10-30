from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker
from app.models import Group
from app.routes import signin

groups = Blueprint('groups', __name__)


@groups.route('/')
def groupsRouter():
    return render_template('groups.html')

@groups.route('/create', methods=['POST'])
def createNewGroupRoute():
    # TODO Нужно будет изменить. Редирект происходит после создания групппы и ответа сервера
    groupName = request.form["GroupName"]
    print(groupName)
    InternetTalker.createGroup(groupName)
    group = Group(999, groupName, 'ADMIN')
    return redirect(f'/group/{group.name}?id={group.id}&admin={group.administrator}')

@groups.route('/elements')
def elementsRoute():
    groups = InternetTalker.getGroups()
    return jsonify([{'id': g.id, 
                     'name': g.name, 
                     'admin': g.administrator} 
                    for g in groups])
