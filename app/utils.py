from flask import session
from app.models import *

def updateSession(username, token):
        session['acces_token'] = token
        session['username'] = username

class InternetTalker:
    """
        Класс отвечающий за общение с другими микросервисами
    """
    def __init__(self):
        super().__init__()


    @staticmethod
    def isAccesToken():
        return session.get('acces_token', None) != None


    @staticmethod
    def getGroups():
        return [
            Group(1, 'title', 'admin'), 
            Group(2, 'Group 2', 'user 1'),
            Group(3, 'Group 3', 'user 2'),
            Group(4, 'Group 4', 'user 3')
        ]

    @staticmethod
    def isSignUpCorrect(username, email, password, password2):
        # TODO Здесь будет связь с микросервисом.
        updateSession(username,'someT')
        return True


    @staticmethod
    def isSignInCorrect(username, password):
        # TODO Здесь будет связь с микросервисом.
        updateSession(username,'someT2')
        return True
    

    @staticmethod
    def getTasksFromGroup(groupName):
        # TODO Здесь будет связь с микросервисом.
        return [
            Task(1, 'title 999', 'des 1', ['user 1', 'user 2'], 'cr 1', 'st 1', '2024-12-02'),
            Task(2, 'title 1', 'des 1', ['user 1'], 'cr 1', 'st 1', '2024-02-02'),
            Task(3, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
            Task(4, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
            Task(5, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
            Task(6, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
            Task(7, 'title 2', 'des 2', ['user 1'], 'cr 2', 'st 1', '2024-02-02'),
            Task(8, 'title 14', 'des 41', ['user 12'], 'cr 11', 'st 91', '2024-02-02')
        ]
    
    
    

    @staticmethod
    def completeTask(task, groupName):
        # TODO Связываемся с сервисом, после получения ответа отмечаем таску как выполненую.
        pass

    @staticmethod
    def deleteTask(task, groupName):
        # TODO Связываемся с сервисом, после получения ответа отмечаем таску как выполненую.
        pass

    @staticmethod
    def createGroup(groupName):
        # TODO Отправляем запрос и добавляем группу
        pass
    

    @staticmethod
    def isAdministrator(groupName):
        # TODO проверяем статус пользователя
        return True
    
    @staticmethod 
    def deleteGroup(groupName):
        # TODO Запрос на сервер.
        # Если одминистратор -> Полное удаление группы
        # Иначе -> Выход из группы.
        pass

    @staticmethod
    def getUsersAtGroup(groupName):
        # TODO
        return['user 1', 'user 2', 'user 3', 'user 12', 'user 22', 'user 32']

    @staticmethod
    def deleteUserFromGroup(groupName, username):
        # TODO
        pass


    @staticmethod
    def getGroupById(id):
       # TODO
       return Group(id, 'GroupById', 'AdminId')

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
        if error_messages == [] and not InternetTalker.isSignUpCorrect(username, email, password, password2):
            error_messages.append('User alredy exists')

        if error_messages != []:
            for x in error_messages:
                error_ans += ' ' + x

        return error_ans
    

    @staticmethod
    def getSignInErrorMessage(username, password):
        error_ans = ''
        if len(username) < 4 or len(password) < 4:
            error_ans = 'Not correct username or password'
        elif not InternetTalker.isSignInCorrect(username, password):
            error_ans = 'Not correct username or password'
        return error_ans
        

def decode_group(group_str):
    group_str = group_str.replace("Group(", "").replace(')',"")
    id, name, administrator = map(str.strip, group_str.split(', '))
    return Group(id=int(id), name=name.split(), administrator=administrator.strip())









