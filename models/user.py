from random import random

class User():
    def __init__(self, email, username, password, images=None):
        """

        :param email: str
        :param username: str
        :param password: str
        :param images: list
        """
        self.email = email
        self.username = username
        self.password = password
        self.images = images
        
    def json(self):
        return {
    'email': self.email,
    'username': self.username,
    'password': self.password,
    'images': self.images,
    }

    
class Task():
    def __init__(self, help, username, description, email, accepted = False, acceptor = None):
        self.help=help
        self.taskauthor=username
        self.description = description
        self.email = email
        self.accepted = accepted
        self.acceptor = acceptor
        self.id = random()


    def json(self):
        return{
            'help': self.help,
            'taskauthor':self.taskauthor,
            'description':self.description,
            'email': self.email,
            'accepted':self.accepted,
            'acceptor':self.acceptor,
            '_id': self.id
        }
