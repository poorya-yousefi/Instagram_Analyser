import mysql.connector
from mysql.connector import Error
import datetime
import DataBase.serverConfig
from DataBase.instaUser import InstaUser

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
col_prof_img_url = 'profile_image_url'
col_bio = 'profile_bio'


def __create_table_users(db):
    stmt = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} INT AUTO_INCREMENT NOT NULL PRIMARY KEY, "
        "       {2} INT NOT NULL DEFAULT '-1', "
        "       {3} VARCHAR(32) NOT NULL DEFAULT 'N/A', "
        "       {4} BOOL DEFAULT '0', "
        "       {5} INT NOT NULL DEFAULT '-1', "
        "       {6} INT NOT NULL DEFAULT '-1', "
        "       {7} INT NOT NULL DEFAULT '-1', "
        "       {8} VARCHAR(64) DEFAULT 'N/A', "
        "       {9} VARCHAR(64) DEFAULT 'N/A', "
        "       {10} VARCHAR(255) DEFAULT 'N/A', "
        "       {11} VARCHAR(255) DEFAULT 'N/A', "
        "       {12} VARCHAR(255) DEFAULT 'N/A'"
        ")"
    ).format(table_name, col_id, col_app_user_id, col_insta_id, col_isPrivate, col_posts_count, col_followers_count,
             col_followings_count, col_followers_table, col_followings_table, col_pageType, col_prof_img_url, col_bio)
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
        user.pageType, user.img_url, user.bio
    )
    stmt = "INSERT INTO {0} " \
           "({1},{2},{3},{4},{5},{6},{7},{8},{9})" \
           " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name, col_app_user_id, col_insta_id, col_isPrivate,
                                                         col_posts_count,
                                                         col_followers_count, col_followings_count, col_pageType,
                                                         col_prof_img_url, col_bio)
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
    stmt = "UPDATE {0} SET {1} = %s,{2} = %s,{3} = %s,{4} = %s,{5} = %s,{6} = %s,{7} = %s, {8} = %s" \
           " WHERE {9} = {10}".format(table_name, col_isPrivate, col_posts_count, col_followers_count,
                                      col_followings_count, col_pageType, col_insta_id, col_prof_img_url,
                                      col_bio, col_id, user.userId)
    args = (
        user.isPrivate, user.postsCount, user.folrs_count, user.folng_count, user.pageType, user.instaId, user.img_url,
        user.bio
    )
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


def get_user(db, _id, select_arg=col_id):
    stmt = "SELECT * FROM {0} WHERE {1} = {2}".format(table_name, select_arg, _id)
    try:
        cursor = db.cursor()
        cursor.execute(stmt)
        res = cursor.fetchone()

        user = InstaUser(res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9])
        user.userId = res[0]
        return user
    except Error:
        return None


_col_insta_user_id = 'instaUser_id'


def __create_table_user_folrs(db, user: InstaUser):
    stmt = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} INT NOT NULL DEFAULT '-1'"
        ")"
    ).format(user.tbl_folrs, _col_insta_user_id)
    try:
        db.cursor().execute(stmt)
        return True
    except Error:
        raise
        return False


def __create_table_user_folng(db, user: InstaUser):
    stmt = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} INT NOT NULL DEFAULT '-1'"
        ")"
    ).format(user.tbl_folrs, _col_insta_user_id)
    try:
        db.cursor().execute(stmt)
        return True
    except Error:
        raise
        return False


def get_followers_list(db, user: InstaUser):
    if not __create_table_user_folrs(db, user):
        return None
    select_stmt = "SELECT {0} FROM {1}".format(_col_insta_user_id, user.tbl_folrs)  # get insta id
    try:
        users = []
        cursor = db.cursor().execute(select_stmt)
        res = cursor.fetchall()
        for tup in res:
            users.append(get_user(db, tup[0]))  # insta User id
        return users
    except Error:
        return None
    finally:
        cursor.close()


def get_followings_list(db, user: InstaUser):
    if not __create_table_user_folrs(db, user):
        return None
    select_stmt = "SELECT {0} FROM {1}".format(_col_insta_user_id, user.tbl_folng)
    try:
        users = []
        cursor = db.cursor().execute(select_stmt)
        res = cursor.fetchall()
        for tup in res:
            users.append(get_user(db, tup[0]))  # insta User id
        return users
    except Error:
        return None
    finally:
        cursor.close()


def add_follower(db, user: InstaUser, __id: int):
    if not __create_table_user_folrs(db, user):
        return None
    stmt = "SELECT {0} FROM {1} WHERE {2} = {3}".format(col_id, table_name, col_id, user.userId)
    stmt_insert = "INSERT INTO {0} ({1}) VALUES (%S)".format(user.tbl_folrs, _col_insta_user_id)
    args = None
    try:
        cursor = db.cursor()
        cursor.execute(stmt)
        res = cursor.fetchone()
        cursor.close()
        if res is not None:
            args = __id
        elif res is None:
            args = -1
        try:
            cursor = db.cursor()
            cursor.execute(stmt_insert, args)
            db.commit()
        except Error:
            return False
        return True
    except Error:
        raise
        return False




def main(config):
    db = mysql.connector.Connect(**config)
    # ******************************* TEST
    # date = datetime.datetime.now()
    user = InstaUser(1, True, 14, 200, 250, "normal")
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
