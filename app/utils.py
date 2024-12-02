from flask import session
from app.models import *
from app.rabbitMQ import RpcClient
import requests as req
import jwt as pyjwt
import urllib.parse
from dotenv import load_dotenv
import os



USER_QUEUE = 'user_service_queue'

SEARCH_QUEUE = 'search_queue'
CALENDAR_QUEUE = 'calendar_queue'


dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=dotenv_path)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')



class InternetTalker:
    """
        Class for work with other services
    """

    def __init__(self):
        super().__init__()
        

    @staticmethod
    def isAccesToken():
        a = session.get('jwt', None)
        return a != None


    @staticmethod
    def getGroups():
        data = {
            'type': 'get_groups',
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        res = []
        for i in range(len(resp_data['group_id'])):
            res.append(Group(resp_data['group_id'][i], resp_data['group'][i]))
        return res


    @staticmethod
    def isSignUpCorrect(username, email, password):
        data = {
            'type': 'registration',
            'username': username,
            'password': password,
            'email': email
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        
        if 'error' in resp_data.keys():
            return resp_data['error']
        else:
            jwt = resp_data['jwt']
            updateSession(username, jwt)
            return ''


    @staticmethod
    def isSignInCorrect(username, password):
        data = {
            'type': 'login',
            'username': username,
            'password': password
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        if 'error' in resp_data.keys():
            return resp_data['error']
        else:
            jwt = resp_data['jwt']
            updateSession(username, jwt)
            return ''
    

    @staticmethod
    def getTasksFromGroup(id):
        data = {
            'type': 'get_tasks_for_group',
            'group_id': id,
            'jwt': session['jwt']
        }

        print(f'hello 1 from get tasks from group: {data}')
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        print(f'hello from get tasks from group: {resp_data}')
        task_id = resp_data['task_id']
        task_name = resp_data['task_name']
        description = resp_data['description']
        deadline = resp_data['deadline']
        members = resp_data['members']
        todo_task = resp_data['todo_task']
        tasks = [
            Task(task_id[i], task_name[i], description[i], members[i], todo_task[i], deadline[i])
        for i in range(len(task_id))]

        return tasks 

    @staticmethod
    def completeTask(task_id, group_id):
        data = {
            'type': 'delete_task',
            'group_id': group_id,
            'task_id': task_id,
            'jwt': session['jwt']
        }

        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        pass
        # resp_data = resp.json()


    @staticmethod
    def deleteTask(group_id, task_id):
        data = {
            'type': 'delete_task',
            'group_id': group_id,
            'task_id': task_id,
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        pass
        # resp_data = resp.json()


    @staticmethod
    def updateTask(group_id, data):
        deadline = '2099-01-01' if data['date'] == '' else data['date']
        data = {
            'type': 'update_task',
            "group_id": int(group_id),
            "task_id": data["id"],
            "task_name": data['title'],
            "description": data['description'],
            "deadline": deadline,
            "todo_task": 'True' if data['status'] == 'true' else 'False',
            "members": data['assigned'],
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        pass


    @staticmethod
    def createGroup(groupName):   
        data = {
            'type': 'add_group',
            'group': groupName,
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        return resp_data['group_id']
 

    @staticmethod
    def isAdministrator(id):
        id = int(id)
        
        data = {
            'type': 'is_admin',
            'group_id': id,
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        return resp_data['is_admin']
    

    @staticmethod 
    def deleteGroup(group_id):
        data = {
            'type': 'delete_group',
            'group_id': group_id,
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        pass


    @staticmethod
    def getUsersAtGroup(group_id):
        data = {
            'type': 'get_group_users',
            'group_id': group_id,
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        res = resp_data['users']
        return res

    @staticmethod
    def deleteUserFromGroup(group_id, username):
        data = {
            'type': 'delete_member_from_group',
            'group_id': group_id,
            'member': username,
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        pass
    

    @staticmethod
    def addUserToGroup(group_id, name):
        data = {
            'type': 'add_member_to_group',
            'group_id': int(group_id),
            'member': name,
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        pass


    @staticmethod
    def getGroupsBySearch(text):
        data = {
            'type': 'group',
            'text': text,
            'jwt': session['jwt']
        }
        rpc_client = RpcClient()
        resp = rpc_client.call(data, SEARCH_QUEUE)
        l = len(resp['id'])
        id = resp['id']
        name = resp['group']
        res = [
            Group(
                id[i],
                name[i]
            )
        for i in range(l)]
        return res 


    @staticmethod
    def getAllAssignedTask():
        # TODO add connection to real service
        tasks =  [
            Task(1, 'title 999', 'des 1', ['user 1', 'user 2'], 'st 1', '2024-12-02'),
            Task(2, 'title 1', 'des 1', ['user 1'], 'cr 1', '2024-02-02'),
            Task(3, 'title 2', 'des 2', ['user 1'], 'cr 2', '2024-02-02'),
            Task(4, 'title 2', 'des 2', ['user 1'], 'cr 2', '2024-02-02'),
            Task(5, 'title 2', 'des 2', ['user 1'], 'cr 2', '2024-02-02'),
            Task(6, 'title 2', 'des 2', ['user 1'], 'st 1', '2024-02-02'),
            Task(7, 'title 2', 'des 2', ['user 1'], 'st 1', '2024-02-02'),
            Task(8, 'title 14', 'des 41', ['user 12'], 'cr 11', 'st 91', '2024-02-02')
        ]
        return tasks
    

    @staticmethod
    def add_task(group_id, task_name, description, deadline, todo_task, members):
        
        data = {
            'type': 'add_task',
            "group_id": int(group_id),
            "task_name": task_name,
            "description": description,
            "deadline": deadline,
            "todo_task": todo_task,
            "members": members,
            'jwt': session['jwt']
        }

        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        pass


    @staticmethod
    def searchTasksInGroup(q, assigned_to, complete_before, status, is_date, groupId):
        
        data = {
            'type': 'task',
            'jwt': session['jwt'],
            "group_id": groupId,
            "text": q,
            "assigned_to": assigned_to,
            "complete_before": complete_before,
            "status": status,
            "is_date": is_date
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, SEARCH_QUEUE)
        
        task_id = resp_data['id']
        task_name = resp_data['title']
        description = resp_data['description']
        deadline = resp_data['deadline']
        members = resp_data['assigned']
        todo_task = resp_data['status']
        tasks = [
            Task(task_id[i], task_name[i], description[i], members[i], todo_task[i], deadline[i])
        for i in range(len(task_id))]
        return tasks


    @staticmethod
    def isGoogleCorrect(username, jwt):
        data = {
            'type': 'google_sign_up',
            'username': username,
            'jwt': jwt,
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        if 'error' in resp_data.keys():
            return resp_data['error']
        else:
            jwt = resp_data['jwt']
            updateSession(username, jwt)
            return ''
        

    @staticmethod
    def isEmailExist(jwt):
        def decode_jwt(jwt_token):
            token = pyjwt.decode(jwt_token, 'OK_6SOME_SE5CRET', algorithms=['HS256'])
            return token['username']

        data = {
            'type': 'google_sign_up',
            'username': '',
            'jwt': jwt,
        }
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, USER_QUEUE)
        if 'error' in resp_data.keys():
            return False
        else:
            jwt = resp_data['jwt']
            username = decode_jwt(jwt)
            updateSession(username, jwt)
            return True
        

    @staticmethod
    def task2calendar(data):
        data['type'] = 'add_event_to_calendar'
        data['jwt'] = session['jwt']
        data['access_token'] = session['access_token']
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, CALENDAR_QUEUE)


    @staticmethod
    def is_task_at_google(data):
        data['type'] = 'is_event_at_calendar'
        data['access_token'] = session['access_token']
        rpc_client = RpcClient()
        resp_data = rpc_client.call(data, CALENDAR_QUEUE)
        return resp_data



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
 

    @staticmethod
    def getGoogleError(username, jwt):
        error_ans = ''
        if len(username) < 4:
            error_ans = 'Username too short. '
        else:
            error_ans = InternetTalker.isGoogleCorrect(username, jwt)
        return error_ans


def decode_group(group_str):
    group_str = group_str.replace("Group(", "").replace(')',"")
    id, name, administrator = map(str.strip, group_str.split(', '))
    return Group(id=int(id), name=name.split(), administrator=administrator.strip())


def get_code_url():
    
    auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'nonce' : 'nonce',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid profile email https://www.googleapis.com/auth/calendar.events',
        'access_type': 'offline'
    }
    return f'{auth_url}?{urllib.parse.urlencode(params)}'


def get_jwt(code):
    if not code:
        return "Ошибка: код авторизации не найден", 400
    
    # Обменяем код на токены
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    # Отправляем запрос на получение токенов
    token_response = req.post(token_url, data=token_data)
    token_json = token_response.json()

    if 'error' in token_json:
        return f"Ошибка: {token_json['error']}", 400
    
    # access_token = token_json.get('access_token')
    id_token = token_json.get('id_token') # jwt
    access_token = token_json.get('access_token') # for calendar
    add_calendar_acces(access_token)

    return id_token


def updateSession(username, token):
        session['jwt'] = token
        session['username'] = username


def add_calendar_acces(access_token):
    session['access_token'] = access_token




