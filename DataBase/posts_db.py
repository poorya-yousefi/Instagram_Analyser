import mysql.connector
from mysql.connector import Error
import datetime
import serverConfig
from post import Post

# DataBase Constants
table_name = 'All_Posts'
col_id = 'id'
col_insta_id = 'insta_user_id'
col_post_url = 'url_post'
col_type = 'post_type'
col_media_url = 'url_media'
col_like_count = 'likes_count'
col_comm_count = 'comments_count'
col_capt = 'post_caption'
col_likers_tbl = 'likers_table_name'
col_comntrs_tbl = 'commenters_table_name'
col_isSaved = 'isSaved'
col_tagged_tbl = 'tagged_people_table_name'
col_keyWords = 'post_key_words'


def create_table_users(db):
    stmt_create = (
        "CREATE TABLE IF NOT EXISTS {0} ("
        "       {1} INT AUTO_INCREMENT NOT NULL PRIMARY KEY, "
        "       {2} INT NOT NULL, "
        "       {3} VARCHAR(255) NOT NULL, "
        "       {4} VARCHAR(5) NOT NULL DEFAULT 'image', "
        "       {5} VARCHAR(255) NOT NULL, "
        "       {6} INT NOT NULL DEFAULT '0', "
        "       {7} INT NOT NULL DEFAULT '0', "
        "       {8} VARCHAR, "
        "       {9} VARCHAR(64), "
        "       {10} VARCHAR(64), "
        "       {11} BOOL NOT NULL DEFAULT '0', "
        "       {12} VARCHAR(64), "
        "       {13} VARCHAR(255)"
        ")"
    ).format(table_name, col_id, col_insta_id, col_post_url, col_type, col_media_url, col_like_count, col_comm_count,
             col_capt, col_likers_tbl, col_comntrs_tbl, col_isSaved, col_tagged_tbl, col_keyWords)
    try:
        cursor = db.cursor()
        cursor.execute(stmt_create)
        return True
    except Error:
        raise
        return False


def insert_user(db, post: Post):
    if not create_table_users(db):
        return False
    args = (post.insta_id, post.post_url, post.p_type, post.media_url, post.like_count, post.comm_count,
            post.capt, post.likers_tbl, post.comntrs_tbl, post.isSaved, post.tagged_tbl, post.keyWords)
    stmt = "INSERT INTO {0} " \
           "({1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12})" \
           " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name, col_insta_id, col_post_url, col_type,
                                                                  col_media_url, col_like_count, col_comm_count,
                                                                  col_capt, col_likers_tbl, col_comntrs_tbl,
                                                                  col_isSaved, col_tagged_tbl, col_keyWords)
    try:
        cursor = db.cursor()
        cursor.execute(stmt, args)
        db.commit()
        return True
    except Error:
        raise
        return False


def update_user(db, post: Post):
    if not create_table_users(db):
        return False
    stmt = "UPDATE {0} SET {1} = %s,{2} = %s,{3} = %s,{4} = %s" \
           " WHERE {5} = {6}".format(table_name, col_like_count, col_comm_count, col_capt, col_isSaved, col_id,
                                     post.postId)
    args = (post.like_count, post.comm_count, post.capt, post.isSaved)
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
            users.append(get_user(db, tup[0]))  # user id : tup[0]
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
        post = Post(res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10], res[11], res[12])
        post.postId = res[0]
        return post
    except Error:
        return None
