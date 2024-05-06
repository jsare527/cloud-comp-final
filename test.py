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
    return user


def createUser(username, password, email):
    encodedPass = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashpass = bcrypt.hashpw(encodedPass, salt)
    add_user = "INSERT INTO User (UserName, Password, Email) VALUES (%s, %s, %s)"
    user_data = (username, hashpass.decode('utf-8'), email)
    dbcursor.execute(add_user, user_data)
    conn.commit()
    
def insertCity(username, cityname):
    user = selectUser(username)
    if user:
        userId = user[0]
        data = (cityname, userId)
        delete_query = "DELETE FROM Cities WHERE CityName=%s AND userid=%s"
        insert_query = "INSERT INTO Cities (CityName, userid) VALUES (%s, %s)"
        dbcursor.execute(delete_query, data)
        dbcursor.execute(insert_query, data)
        conn.commit()

def getUserCities(username):
    user = selectUser(username)
    if user:
        userId = user[0]
        select_query = "SELECT * FROM Cities WHERE userid=%s ORDER BY city_id desc LIMIT 5"
        dbcursor.execute(select_query, (userId,))
        cities = dbcursor.fetchall()
        print(cities)

insertCity("jsare", "Omaha")
getUserCities("jsare")

dbcursor.close()
conn.close()
#createUser("jurhe2", "chancy4", "bruh@gmail.com")
#selectUser("jurhe2")
