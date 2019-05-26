import mysql.connector
from mysql.connector import Error
import appUsers_db

table_name = "online_users"
col_id = "id"
col_object = "user_object"
col_driver = "user_driver"


def create_table(db):
    stmt_create = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} INT AUTO_INCREMENT PRIMARY KEY NOT NULL, "
        "       {2} BLOB NOT NULL, "
        "       {3} BLOB NOT NULL)"
    ).format(table_name, col_id, col_object, col_driver)
    try:
        cursor = db.cursor()
        cursor.execute(stmt_create)
        return True
    except Error as e:
        print(e)
        raise
        return False


def insert_user(db, obj):
    if not create_table(db):
        return False
    stmt = "INSERT INTO {0} ({1},{2}) VALUES (%s,%s)".format(table_name, obj[0], obj[1])
    try:
        cursor = db.cursor()
        cursor.execute(stmt, obj)
        db.commit()
        return True
    except Error:
        raise
        return False
    finally:
        cursor.close()
        db.close()


def get_all_users(db: mysql.connector, order_by=col_id, sort_arg=' ASC'):
    if not create_table(db):
        return None
    stmt = "SELECT * FROM {} ORDER BY ".format(table_name) + order_by + sort_arg
    try:
        users = []
        cursor = db.cursor()
        cursor.execute(stmt)
        res = cursor.fetchall()
        for tup in res:
            users.append(get_user(db, tup[0]))  # user id
        return users
    except Error as e:
        print(e)
        return None
    finally:
        cursor.close()
        db.close()


def get_user(db, user_id, select_arg=col_id):
    stmt = "SELECT * FROM {} WHERE ".format(table_name) + select_arg + " = {}".format(user_id)
    try:
        cursor = db.cursor()
        cursor.execute(stmt)
        obj = cursor.fetchone()
        return obj
    except Error as e:
        print(e)
        return None


def main(config):
    db = mysql.connector.Connect(**config)
    user = appUsers_db.get_user(db, 1)
    obj = [user, "tttttttttteeeeeeeessssssssssst"]
    insert_user(db, obj)
    for o in get_all_users(db):
        print(o[0])


if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'user': 'admin_poorya',
        'password': 'password123',
        'database': 'instagramanalyser_db'
    }
    main(config)

# object2varchar = lambda obj: unicode(base64.encode(cPickle.dumps(obj)))
# store(object2varchar([1, 'foo']))
