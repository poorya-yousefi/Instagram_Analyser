import mysql.connector
from mysql.connector import Error
import datetime
from DataBase.appUser import *
from DataBase.serverConfig import server_config
import json as js

# DataBase Constants
table_name = 'Application_Users'
col_id = 'id'
col_signupDate = 'signupDate'
col_lastLoginDate = 'lastLoginDate'
col_hasTwoStep = 'hasTwoStep'
col_country = 'country'
col_city = 'city'
col_phoneNum = 'phoneNum'
col_personalityKeyWords = 'personalityKeyWords'
col_cookie = 'cookie_file_path'
col_company_name = 'company_name'
col_activity = 'activity'
col_info = 'json_path'


def create_table_users(db):
    stmt_create = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} INT AUTO_INCREMENT NOT NULL PRIMARY KEY, "
        "       {2} timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
        "       {3} timestamp NOT NULL, "
        "       {4} BOOL NOT NULL DEFAULT '0', "
        "       {5} VARCHAR(255), "
        "       {6} VARCHAR(255), "
        "       {7} VARCHAR(20), "
        "       {8} VARCHAR(255), "
        "       {9} VARCHAR(255), "
        "       {10} VARCHAR(255), "
        "       {11} VARCHAR(255), "
        "       {12} VARCHAR(255)"
        ")"
    ).format(table_name, col_id, col_signupDate, col_lastLoginDate, col_hasTwoStep, col_country,
             col_city, col_phoneNum, col_personalityKeyWords, col_cookie, col_company_name, col_activity, col_info)
    try:
        cursor = db.cursor()
        cursor.execute(stmt_create)
        return True
    except Error:
        raise
        return False


def insert_user(db, user):
    if not create_table_users(db):
        return False
    if user is CommercialUser:
        args = (user.lastLoginDate, user.hasTwoStep, user.country, user.city, user.phoneNum,
                user.personalityKeyWords, user.cookie_path, user.js_path, user.companyName, user.activity)
    else:
        args = (user.lastLoginDate, user.hasTwoStep, user.country, user.city, user.phoneNum,
                user.personalityKeyWords, user.cookie_path, user.js_path, None, None)
    stmt = "INSERT INTO {0} " \
           "({1},{2},{3},{4},{5},{6},{7},{8},{9},{10})" \
           " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name, col_lastLoginDate, col_hasTwoStep,
                                                            col_country, col_city, col_phoneNum,
                                                            col_personalityKeyWords,
                                                            col_cookie, col_info, col_company_name, col_activity)
    try:
        cursor = db.cursor()
        cursor.execute(stmt, args)
        db.commit()
        return True
    except Error:
        raise
        return False


def update_user(db, user: AppUser):
    if not create_table_users(db):
        return False
    stmt = "UPDATE {0} SET {1} = %s,{2} = %s,{3} = %s,{4} = %s,{5} = %s," \
           "{6} = %s , {7} = %s , {8} = %s" \
           " WHERE {9} = {10}".format(table_name, col_lastLoginDate, col_hasTwoStep, col_country,
                                      col_city, col_phoneNum, col_personalityKeyWords, col_company_name,
                                      col_activity,
                                      col_id, user.userId)
    if user is CommercialUser:
        args = (user.lastLoginDate, user.hasTwoStep, user.country, user.city, user.phoneNum,
                user.personalityKeyWords, user.companyName, user.activity)
    else:
        args = (user.lastLoginDate, user.hasTwoStep, user.country, user.city, user.phoneNum,
                user.personalityKeyWords, None, None)

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


def get_user(db, user_id, select_arg=col_id):
    stmt = "SELECT * FROM {0} WHERE {1} = {2}".format(table_name, select_arg, user_id)
    try:
        cursor = db.cursor()
        cursor.execute(stmt)
        res = cursor.fetchone()
        # if res is None:
        #     return None
        user = AppUser(res[2], res[3], res[4], res[5],
                       res[6], res[7], res[8], res[11])
        user.userId = res[0]
        user.signupDate = res[1]
        if res[9] is not None:
            user.companyName = res[9]
            user.activity = res[10]
        return user
    except Error:
        return None
    # finally:
    #     cursor.close()
    #     db.close()


def main(config):
    db = mysql.connector.Connect(**config)
    date = datetime.datetime.now()
    # u = CommercialUser(date, False, "Iran", "Teh", "09355555555", "..", "/sd./sdf", "sherkat", "commercial")
    # u = AppUser(date, False, "USA", "NY", "+194262258652", "..", "//sdf")
    # ******************************* TEST
    # user = AppUser( lastLoginDate=date, hasTwoStep=True, country="Iran",
    #                city="Karaj", phoneNum="093333333333", personalityKeyWords="", cookie_path="./sad/")
    # # user.userId = 2
    # # user.signupDate = date
    # # update_user(db, user)
    # insert_user(db, u)
    users = get_all_users(db)
    for u in users:
        print(str(u))
    # ******************************* TEST


if __name__ == '__main__':
    config = server_config
    main(config)
