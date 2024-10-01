from flask import session

class InternetTalker:
    """
        Класс отвечающий за общение с другими микросервисами
    """
    def __init__(self):
        super().__init__()


    @staticmethod
    def isAccesToken():
        print(session.get('acces_token', None))
        print(session.get('acces_token', None) != None)
        return session.get('acces_token', None) != None
    

    @staticmethod
    def getGroupsNames():
        # TODO Данный метод будет связываться с сервисом. Сейчас вернутся псевдо группы.
        return ['group 1', 'group 2', 'group 3']
    

    @staticmethod
    def isSignUpCorrect(username, email, password, password2):
        # TODO Здесь будет связь с микросервисом.
        session['acces_token'] = 'some token'
        return True


    @staticmethod
    def isSignInCorrect(username, password):
        # TODO Здесь будет связь с микросервисом.
        session['acces_token'] = 'some token'
        return True
    

class Validator:
    """Класс для валидации данных"""
    @staticmethod
    def getSignUpErrorMessage(username, email, password, password2):
        error_messages = []
        error_ans = ''

        if len(username) < 6:
            error_messages.append('Username too short.')
        if len(password) < 6:
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
        if len(username) < 6 or len(password) < 6:
            error_ans = 'Not correct username or password'
        elif not InternetTalker.isSignInCorrect(username, password):
            error_ans = 'Not correct username or password'
        return error_ans
        











