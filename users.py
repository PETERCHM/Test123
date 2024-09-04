# users.py
class User:
    def __init__(self, name):
        self.name = name
        self.expenses = 0

    def __str__(self):
        return self.name
