import mariadb
import bcrypt

conn = mariadb.connect(user='root',
                       host='localhost',
                       database = 'cloudcomp',
                       password='Test1234!',
                       )

dbcursor = conn.cursor()

def selectUser(username):
    select_query = "SELECT * FROM User WHERE UserName = %s"
    select_data = (username,)
    dbcursor.execute(select_query, select_data)
    user = dbcursor.fetchone()
    hashpw = str(user[2]).encode('utf-8')
    print(user)
    #print(bcrypt.checkpw("chance52".encode('utf-8'), hashpw))
    dbcursor.close()
    conn.close()

def createUser(username, password, email):
    encodedPass = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashpass = bcrypt.hashpw(encodedPass, salt)
    add_user = "INSERT INTO User (UserName, Password, Email) VALUES (%s, %s, %s)"
    user_data = (username, hashpass.decode('utf-8'), email)
    dbcursor.execute(add_user, user_data)
    conn.commit()
    dbcursor.close()
    conn.close()
    
#createUser("jurhe2", "chancy4", "bruh@gmail.com")
selectUser("jurhe2")
