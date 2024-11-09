from flask import Blueprint, render_template, request, redirect, jsonify

from app.utils import InternetTalker
from app.models import Group

groups = Blueprint('groups', __name__)


@groups.route('/')
def groupsRouter():
    return render_template('groups.html')

@groups.route('/create', methods=['POST'])
def createNewGroupRoute():
    groupName = request.form["GroupName"]
    group_id = InternetTalker.createGroup(groupName)
    return redirect(f'/group/{groupName}?id={group_id}')

@groups.route('/elements')
def elementsRoute():
    groups = InternetTalker.getGroups()
    return jsonify([{
        'id': g.id, 
        'name': g.name, 
    } for g in groups])

@groups.route('/search/')
def searchGroupRoute():
    group_name = request.args.get('group_name')
    groups = InternetTalker.getGroupsBySearch(group_name)
    return jsonify([{
        'id': g.id, 
        'name': g.name, 
    } for g in groups])