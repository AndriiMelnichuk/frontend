from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker
from app.models import Group


group = Blueprint('group', __name__)


@group.route('/<name>')
def selectGroup(name):
    id = request.args.get('id')
    isAdmin= InternetTalker.isAdministrator(group)
    return render_template("group.html", group_name=name, group_id=id, isAdmin=isAdmin)


@group.route('/delete/<groupId>')
def deleteGroupRoute(groupId):
    InternetTalker.deleteGroup(groupId)
    return redirect('/groups')

@group.route('/users/')
def userAtGroupRoute():
    id = request.args.get('id')
    users = InternetTalker.getUsersAtGroup(id)
    return users 


@group.route('/addUser/<group_id>/<group_name>')
def addUserRoute(group_id, group_name):
    name = request.args.get('user')
    InternetTalker.addUserToGroup(group_id, name)
    return redirect(f'/group/{group_name}/?id={group_id}')



@group.route('/delete/<group_id>/<group_name>/<username>')
def deleteUserFromGroupRoute(group_id, group_name, username):
    InternetTalker.deleteUserFromGroup(group_id, username)
    return redirect(f'/group/{group_name}/?id={group_id}')
