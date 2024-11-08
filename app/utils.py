from flask import session
from app.models import *
import requests as req

def updateSession(username, token):
        session['jwt'] = token
        session['username'] = username

url = 'http://localhost:5001/'
class InternetTalker:
    """
        Class for work with other services
    """

    def __init__(self):
        super().__init__()


    @staticmethod
    def isAccesToken():
        return session.get('jwt', None) != None


    @staticmethod
    def getGroups():
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'get_groups',
            'jwt': session['jwt']
        }
        resp = req.post(
            url= url,
            headers=head,
            json=data
        )
        resp_data = resp.json()
        res = []
        for i in range(len(resp_data['group_id'])):
            res.append(Group(resp_data['group_id'][i], resp_data['group_name'][i]))
        return res


    @staticmethod
    def isSignUpCorrect(username, email, password):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'registration',
            'username': username,
            'password': password,
            'email': email
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
        resp_data = resp.json()
        if 'error' in resp_data.keys():
            return resp_data['error']
        else:
            jwt = resp_data['jwt']
            updateSession(username, jwt)
            return ''


    @staticmethod
    def isSignInCorrect(username, password):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'login',
            'username': username,
            'password': password
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
        resp_data = resp.json()
        if 'error' in resp_data.keys():
            return resp_data['error']
        else:
            jwt = resp_data['jwt']
            updateSession(username, jwt)
            return ''
    

    @staticmethod
    def getTasksFromGroup(id):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'get_tasks_for_group',
            'group_id': id,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
        resp_data = resp.json()
        task_id = resp_data['task_id']
        task_name = resp_data['task_name']
        description = resp_data['description']
        deadline = resp_data['deadline']
        members = resp_data['members']
        todo_task = resp_data['todo_task']
        # TODO Task created
        tasks = [
            Task(task_id[i], task_name[i], description[i], members[i], '...', todo_task[i], deadline[i])
        for i in range(len(task_id))]

        # return [
        #     Task(1, 'title 999', 'des 1', ['user 1', 'user 2'], 'cr 1', 'st 1', '2024-12-02'),
        #     Task(2, 'title 1', 'des 1', ['user 1'], 'cr 1', 'st 1', '2024-02-02'),
        #     Task(3, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
        #     Task(4, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
        #     Task(5, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
        #     Task(6, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
        #     Task(7, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
        #     Task(8, 'title 14', 'des 41', ['user 12'], 'cr 11', 'st 91', '2024-02-02')
        # ]
    

    @staticmethod
    def completeTask(task_id, group_id):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'delete_task',
            'group_id': group_id,
            'task_id': task_id,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
        # resp_data = resp.json()


    @staticmethod
    def deleteTask(group_id, task_id):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'delete_task',
            'group_id': group_id,
            'task_id': task_id,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
        # resp_data = resp.json()


    @staticmethod
    def updateTask(group_id, task_id, data):
        pass


    @staticmethod
    def createGroup(groupName):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'add_group',
            'group_id': groupName,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
        resp_data = resp.json()
        return resp_data['groupd_id']
 

    @staticmethod
    def isAdministrator(groupName):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'is_admin',
            'group_id': groupName,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
        resp_data = resp.json()
        # TODO Could be problems
        return resp_data
    
    @staticmethod 
    def deleteGroup(group_id):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'delete_group',
            'group_id': group_id,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )


    @staticmethod
    def getUsersAtGroup(group_id):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'get_group_users',
            'group_id': group_id,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
        return resp.json()['users']

    @staticmethod
    def deleteUserFromGroup(group_id, username):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'delete_member_from_group',
            'group_id': group_id,
            'member': username,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )
    

    @staticmethod
    def addUserToGroup(group_id, name):
        head = {'Content-Type': 'application/json'}
        data = {
            'type': 'add_member_to_group',
            'group_id': group_id,
            'member': name,
            'jwt': session['jwt']
        }
        resp = req.post(
            url=url,
            headers=head,
            json=data
        )


class Validator:
    """Класс для валидации данных"""
    @staticmethod
    def getSignUpErrorMessage(username, email, password, password2):
        error_messages = []
        error_ans = ''

        if len(username) < 4:
            error_messages.append('Username too short.')
        if len(password) < 4:
            error_messages.append('Password too short.')
        if password != password2:
            error_messages.append('Password and confirming password not equal.')
        if error_messages == []:
            mes = InternetTalker.isSignUpCorrect(username, email, password)
            if mes != '':
                error_messages.append(mes)

        if error_messages != []:
            error_ans = ' '.join(error_messages)
        return error_ans
    

    @staticmethod
    def getSignInErrorMessage(username, password):
        error_ans = ''
        if len(username) < 4 or len(password) < 4:
            error_ans = 'Not correct username or password'
        if error_ans == '':
            error_ans += InternetTalker.isSignInCorrect(username, password)
        return error_ans
    



        

def decode_group(group_str):
    group_str = group_str.replace("Group(", "").replace(')',"")
    id, name, administrator = map(str.strip, group_str.split(', '))
    return Group(id=int(id), name=name.split(), administrator=administrator.strip())









