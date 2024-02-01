from database import mysql

class User:        
    def create_user(self, name, username, phone):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (Name, Username, Phone) VALUES (%s, %s, %s, %s)", (name, username, phone))
        mysql.connection.commit()
        cur.close()

    def get_users(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user")
        users = cur.fetchall()
        cur.close()
        return users

    def get_user_by_id(self, user_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        return user

    def delete_user(self, user_id):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user SET ActiveStatus = ? WHERE id = %s", (0, user_id,))
        mysql.connection.commit()
        cur.close()

    def checkUsername(self, username):
        cur = mysql.connection.cursor()
        cur.execute("SELECT ID FROM user WHERE Username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        return user

    def checkPhoneRegistered(self, phone):
        cur = mysql.connection.cursor()
        cur.execute('SELECT Phone FROM user WHERE Phone ="%s"', (phone))
        user = cur.fetchone()
        cur.close()
        return user