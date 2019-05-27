import mysql.connector
from mysql.connector import Error
import datetime
from DataBase.appUser import AppUser
from DataBase.serverConfig import server_config

# DataBase Constants
table_name = 'Application_Users'
col_id = 'id'
col_instagramId = 'instagramId'
col_signupDate = 'signupDate'
col_lastLoginDate = 'lastLoginDate'
col_hasTwoStep = 'hasTwoStep'
col_country = 'country'
col_city = 'city'
col_phoneNum = 'phoneNum'
col_personalityKeyWords = 'personalityKeyWords'


def create_table_users(db):
    stmt_create = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} INT AUTO_INCREMENT NOT NULL PRIMARY KEY, "
        "       {2} VARCHAR(255) NOT NULL, "
        "       {3} timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
        "       {4} timestamp NOT NULL, "
        "       {5} BOOL NOT NULL DEFAULT '0', "
        "       {6} VARCHAR(255), "
        "       {7} VARCHAR(255), "
        "       {8} VARCHAR(20), "
        "       {9} VARCHAR(255)"
        ")"
    ).format(table_name, col_id, col_instagramId, col_signupDate, col_lastLoginDate, col_hasTwoStep, col_country,
             col_city, col_phoneNum, col_personalityKeyWords)
    try:
        cursor = db.cursor()
        cursor.execute(stmt_create)
        return True
    except Error:
        raise
        return False


def insert_user(db, user: AppUser):
    if not create_table_users(db):
        return False
    args = (user.instagramId, user.lastLoginDate, user.hasTwoStep, user.country, user.city, user.phoneNum,
            user.personalityKeyWords)
    stmt = "INSERT INTO {0} " \
           "({1},{2},{3},{4},{5},{6},{7})" \
           " VALUES (%s,%s,%s,%s,%s,%s,%s)".format(table_name, col_instagramId, col_lastLoginDate, col_hasTwoStep,
                                                   col_country, col_city, col_phoneNum, col_personalityKeyWords)
    try:
        cursor = db.cursor()
        cursor.execute(stmt, args)
        db.commit()
        return True
    except Error:
        raise
        return False
    # finally:
    #     cursor.close()
    #     db.close()


def update_user(db, user: AppUser):
    if not create_table_users(db):
        return False
    stmt = "UPDATE {0} SET {1} = %s,{2} = %s,{3} = %s,{4} = %s,{5} = %s," \
           "{6} = %s,{7} = %s" \
           " WHERE {8} = {9}".format(table_name, col_instagramId, col_lastLoginDate, col_hasTwoStep, col_country,
                                     col_city, col_phoneNum, col_personalityKeyWords, col_id, user.userId)
    args = (
        user.instagramId, user.lastLoginDate, user.hasTwoStep, user.country, user.city, user.phoneNum,
        user.personalityKeyWords)
    try:
        cursor = db.cursor()
        cursor.execute(stmt, args)
        db.commit()
        return True
    except Error:
        raise
        return False


def delete_user(db, user_id: int):
    pass


def get_all_users(db: mysql.connector, order_by=col_id, sort_arg='ASC'):
    # 'DSC'
    if not create_table_users(db):
        return None
    stmt = "SELECT * FROM {0} ORDER BY {1} {2}".format(table_name, order_by, sort_arg)
    try:
        users = []
        cursor = db.cursor()
        cursor.execute(stmt)
        res = cursor.fetchall()
        for tup in res:
            users.append(get_user(db, tup[0]))  # user id
        return users
    except Error:
        return None
    finally:
        cursor.close()
        db.close()


def get_user(db, user_id, select_arg=col_id):
    stmt = "SELECT * FROM {0} WHERE {1} = {2}".format(table_name, select_arg, user_id)
    try:
        cursor = db.cursor()
        cursor.execute(stmt)
        res = cursor.fetchone()
        # if res is None:
        #     return None
        user = AppUser(res[1], res[3], res[4], res[5],
                       res[6], res[7], res[8])
        user.userId = res[0]
        user.signupDate = res[2]
        return user
    except Error:
        return None
    # finally:
    #     cursor.close()
    #     db.close()


def main(config):
    db = mysql.connector.Connect(**config)
    # ******************************* TEST
    date = datetime.datetime.now()
    user = AppUser(instagramId="pooorya_234124", lastLoginDate=date, hasTwoStep=True, country="Iran",
                    city="Karaj", phoneNum="093333333333", personalityKeyWords="")
    # user.userId = 2
    # user.signupDate = date
    # update_user(db, user)
    insert_user(db, user)
    users = get_all_users(db)
    for u in users:
        print(u)
    # ******************************* TEST


if __name__ == '__main__':
    config = server_config
    main(config)
