from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker
from app.models import Group


group = Blueprint('group', __name__)


@group.route('/<name>')
def selectGroup(name):
    id = request.args.get('id')
    admin = request.args.get('admin')
    group = Group(id, name, admin)
    return render_template("group.html", group=group, isAdmin=InternetTalker.isAdministrator(group))


@group.route('/delete/<groupId>')
def deleteGroupRoute(groupId):
    InternetTalker.deleteGroup(groupId)
    return redirect('/groups')

@group.route('/users/')
def userAtGroupRoute():
    id = request.args.get('id')
    name = request.args.get('name')
    admin = request.args.get('admin')
    group = Group(id, name, admin)
    users = InternetTalker.getUsersAtGroup(group)
    isAdmin = InternetTalker.isAdministrator(group)
    return jsonify(users, isAdmin)


@group.route('/delete/<group>/<username>')
def deleteUserFromGroupRoute(group, username):
    InternetTalker.deleteUserFromGroup(group, username)
    return redirect(url_for('group.selectGroup', group=group))
