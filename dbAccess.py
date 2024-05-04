from userAuth import User
import bcrypt
import mariadb

class Db:
    def openConnection(self):
        self.conn = mariadb.connect(
                               user='root',
                               host='localhost',
                               database = 'cloudcomp',
                               password='Test1234!'
                                )

        self.dbcursor = self.conn.cursor()
    
    def closeConnection(self):
        self.dbcursor.close()
        self.conn.close()

    def saveUser(self, username, password, email):
        self.openConnection()
        encodedPass = str(password).encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(encodedPass, salt)
        add_user = "INSERT INTO User (UserName, Password, Email) VALUES(%s, %s, %s)"
        user_data = (username, hash.decode('utf-8'), email)
        self.dbcursor.execute(add_user, user_data)
        self.conn.commit()
        self.closeConnection()


    def getUser(self, username):
        self.openConnection()
        username = str(username).strip()
        find_user = "SELECT * FROM User WHERE UserName = %s"
        self.dbcursor.execute(find_user, (username,))
        user = self.dbcursor.fetchone()
        self.closeConnection()
        hashPw = str(user[2]).encode('utf-8')
        return User(user[3], user[1], hashPw)
