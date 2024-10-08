from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.utils import Validator, InternetTalker

# TODO Добавить регистрацию через гугл

main = Blueprint('main', __name__)

@main.route('/signin')
def signin():
    return render_template('sign-in.html')


@main.route('/signup')
def signup():
    return render_template('sign-up.html')


@main.route('/validate-sign-up', methods=['POST'])
def validateSignUp():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['confirm-password']

    error_ans = Validator.getSignUpErrorMessage(username, email, password, password2)
    if error_ans != '':
        return render_template('sign-up.html', error_message=error_ans, name=username, email=email, password=password, password2=password2)
    return redirect('/')


@main.route('/validate-sign-in', methods=['POST'])
def validateSignIn():
    username = request.form['username']
    password = request.form['password']

    error_ans = Validator.getSignInErrorMessage(username, password)
    if error_ans != '':
        return render_template('sign-in.html', error_message=error_ans, username=username, password=password)
    return redirect('/')

@main.route('/groups')
def groupsRouter():
    groupNames = InternetTalker.getGroupsNames()
    return render_template('groups.html', groupNames=groupNames)

@main.route('/search')
def searchRoute():
    return render_template('search.html')

@main.route('/group/<groupName>')
def selectGroup(groupName):
    tasks = InternetTalker.getTasksFromGroup(groupName)
    return render_template("group.html", groupName=groupName, tasks=tasks, isAdmin=InternetTalker.isAdministrator(groupName))

@main.route('/completeTask/<task>/<groupName>')
def completeTask(task, groupName):
    InternetTalker.completeTask(task, groupName)
    return redirect(url_for('main.selectGroup', groupName=groupName))

@main.route('/createGroup', methods=['POST'])
def createNewGroupRoute():
    groupName = request.form["GroupName"]
    InternetTalker.createGroup(groupName)
    print(groupName)
    return redirect(url_for('main.selectGroup', groupName=groupName))

@main.route('/deleteGroup/<groupName>')
def deleteGroupRoute(groupName):
    InternetTalker.deleteGroup(groupName)
    return redirect('/groups')

@main.route('/users-at-group/<groupName>')
def userAtGroupRoute(groupName):
    users = InternetTalker.getUsersAtGroup(groupName)
    isAdmin = InternetTalker.isAdministrator(groupName)
    return jsonify(users, isAdmin)


@main.route('/deleteTask/<task>/<groupName>')
def deleteTask(task, groupName):
    InternetTalker.deleteTask(task, groupName)
    return redirect(url_for('main.selectGroup', groupName=groupName))

                    
@main.route('/deleteUserFromGroup/<groupName>/<username>')
def deleteUserFromGroupRoute(groupName, username):
    InternetTalker.deleteUserFromGroup(groupName, username)
    return redirect(url_for('main.selectGroup', groupName=groupName))

@main.route('/')
def index():
    if InternetTalker.isAccesToken():
        return render_template('main.html')
    return render_template('sign-in-or-up.html')

