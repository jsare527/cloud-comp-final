import bcrypt

class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def checkPass(self, passInput):
        passInput = str(passInput).strip().encode('utf-8')
        return bcrypt.checkpw(passInput, self.password)