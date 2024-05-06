from userAuth import User
import bcrypt
import mariadb

class Db:
    def openConnection(self):
        self.conn = mariadb.connect(
                               user='root',
                               host='localhost',
                               database = 'cloudcomp',
                               password='Chance527!'
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

    def getUserId(self, username):
        self.openConnection()
        username = str(username).strip()
        find_user = "SELECT * FROM User WHERE UserName = %s"
        self.dbcursor.execute(find_user, (username,))
        user = self.dbcursor.fetchone()
        return user[0]

    def insertCity(self, username, cityname):
        self.openConnection()
        userId = self.getUserId(username)
        if userId:
            data = (cityname, userId)
            delete_query = "DELETE FROM Cities WHERE CityName=%s AND userid=%s"
            insert_query = "INSERT INTO Cities (CityName, userid) VALUES (%s, %s)"
            self.dbcursor.execute(delete_query, data)
            self.dbcursor.execute(insert_query, data)
            self.conn.commit()
        self.closeConnection()

    def getRecentCities(self, username):
        cities = []
        self.openConnection()
        userId = self.getUserId(username)
        if userId:
            select_query = "SELECT * FROM Cities WHERE userid=%s ORDER BY city_id desc LIMIT 5"
            self.dbcursor.execute(select_query, (userId,))
            cities = self.dbcursor.fetchall()
            cities = [i[1] for i in cities]
        
        self.closeConnection()
        return cities

    