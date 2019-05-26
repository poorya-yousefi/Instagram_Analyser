import mysql.connector
from mysql.connector import Error
import datetime
import serverConfig
from instaUser import InstaUser

# DataBase Constants
table_name = 'Instagram_Users'
col_id = 'id'
col_app_user_id = 'app_user_id'
col_insta_id = 'instagram_id'
col_isPrivate = 'is_private'
col_posts_count = 'posts_count'
col_followers_count = 'followers_count'
col_followings_count = 'followings_count'
col_followers_table = 'followers_table_name'
col_followings_table = 'followings_table_name'
col_pageType = 'page_types'


def __create_table_users(db):
    stmt = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} INT AUTO_INCREMENT NOT NULL PRIMARY KEY, "
        "       {2} INT NOT NULL DEFAULT '-1', "
        "       {3} VARCHAR(255) NOT NULL, "
        "       {4} BOOL NOT NULL, "
        "       {5} INT NOT NULL DEFAULT '-1', "
        "       {6} INT NOT NULL DEFAULT '-1', "
        "       {7} INT NOT NULL DEFAULT '-1', "
        "       {8} VARCHAR(64), "
        "       {9} VARCHAR(64), "
        "       {10} VARCHAR(255)"
        ")"
    ).format(table_name, col_id, col_app_user_id, col_insta_id, col_isPrivate, col_posts_count, col_followers_count,
             col_followings_count,
             col_followers_table, col_followings_table, col_pageType)
    try:
        cursor = db.cursor()
        cursor.execute(stmt)
        return True
    except Error:
        raise
        return False


def insert_user(db, user: InstaUser):
    if not __create_table_users(db):
        return False
    args = (
        user.appUserId, user.instaId, user.isPrivate, user.postsCount, user.folrs_count, user.folng_count,
        user.pageType)
    stmt = "INSERT INTO {0} " \
           "({1},{2},{3},{4},{5},{6},{7})" \
           " VALUES (%s,%s,%s,%s,%s,%s,%s)".format(table_name, col_app_user_id, col_insta_id, col_isPrivate,
                                                   col_posts_count,
                                                   col_followers_count, col_followings_count, col_pageType)
    try:
        cursor = db.cursor()
        cursor.execute(stmt, args)
        db.commit()
        return True
    except Error:
        raise
        return False


def update_user(db, user: InstaUser):
    if not __create_table_users(db):
        return False
    stmt = "UPDATE {0} SET {1} = %s,{2} = %s,{3} = %s,{4} = %s,{5} = %s,{6} = %s" \
           " WHERE {7} = {8}".format(table_name, col_isPrivate, col_posts_count, col_followers_count,
                                     col_followings_count, col_pageType, col_insta_id, col_id, user.userId)
    args = (user.isPrivate, user.postsCount, user.folrs_count, user.folng_count, user.pageType, user.instaId)
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
    if not __create_table_users(db):
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


def get_user(db, _id, select_arg=col_id):
    stmt = "SELECT * FROM {0} WHERE {1} = {2}".format(table_name, select_arg, _id)
    try:
        cursor = db.cursor()
        cursor.execute(stmt)
        res = cursor.fetchone()

        user = InstaUser(res[1], res[2], res[3], res[4], res[5], res[6], res[7])
        user.userId = res[0]
        return user
    except Error:
        return None


_col_id = 'instaUser_id'


def __create_table_user_folrs(db, user: InstaUser):
    stmt = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} VARCHAR(255) NOT NULL PRIMARY KEY"
        ")"
    ).format(user.tbl_folrs, _col_id)
    try:
        db.cursor().execute(stmt)
        return True
    except Error:
        raise
        return False


def __create_table_user_folng(db, user: InstaUser):
    stmt = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} VARCHAR(255) NOT NULL PRIMARY KEY"
        ")"
    ).format(user.tbl_folng, _col_id)
    try:
        db.cursor().execute(stmt)
        return True
    except Error:
        raise
        return False


def get_followers_list(db, user: InstaUser):
    if not __create_table_user_folrs(db, user):
        return None
    select_stmt = "SELECT {0} FROM {1}".format(_col_id, user.tbl_folrs)
    try:
        users = []
        cursor = db.cursor().execute(select_stmt)
        res = cursor.fetchall()
        for tup in res:
            users.append(get_user(db, tup[0]))  # user id
        return users
    except Error:
        return None
    finally:
        cursor.close()
        db.close()


def get_followings_list(db, user: InstaUser):
    if not __create_table_user_folrs(db, user):
        return None
    select_stmt = "SELECT {0} FROM {1}".format(_col_id, user.tbl_folng)
    try:
        users = []
        cursor = db.cursor().execute(select_stmt)
        res = cursor.fetchall()
        for tup in res:
            users.append(get_user(db, tup[0]))  # user id
        return users
    except Error:
        return None
    finally:
        cursor.close()
        db.close()


def add_follower(db, user: InstaUser, insta_id):


def main(config):
    db = mysql.connector.Connect(**config)
    # ******************************* TEST
    # date = datetime.datetime.now()
    user = InstaUser(1, True, 14, 200, 250, "", "", "normal")
    # user.userId = 2
    # user.signupDate = date
    # update_user(db, user)

    # insert_user(db, user)
    users = get_all_users(db)
    for u in users:
        print(u.userId, u.appUserId)
        # print(u)
    # ******************************* TEST


if __name__ == '__main__':
    config = serverConfig.server_config
    main(config)
