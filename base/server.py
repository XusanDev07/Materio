from contextlib import closing

from django.db import connection


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = []
    for i in cursor.description:
        columns.append(i[0])
    a = cursor.fetchall()
    img = None
    if "img" in columns:
        img = columns.index("img")
    natija = []
    for i in a:
        i = list(i)
        if img:
            i[img] = "http://127.0.0.1:8000/media/" + i[img]
        b = dict(zip(columns, i))
        natija.append(b)
    return natija


def check_phone_in_db(phone):
    sql = f"""
        SELECT * from director_User t
        where t.phone like '{phone}'
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchone(cursor)

        return result


def check_token_in_db(token):
    sql = f"""
        SELECT * from materio_otp t
        where t.key = '{token}'
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchone(cursor)

        return result


def check_user_in_token_db(user):
    sql = f"""
        SELECT key from materio_Token t
        where t.user like '{user}'  
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchone(cursor)

        return result


def check_email_in_db(email):
    sql = f"""
        SELECT * from materio_User t
        where t.email = '{email}'
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchone(cursor)

        return result


def update_token(token):

    if token['tries'] >= 4:
        token['is_expire'] = True

    sql = f"""
        UPDATE materio_otp
        SET is_conf = {token['is_conf']},
        is_expire = {token['is_expire']},
        tries = {token['tries']}
        where key  = '{token['key']}'
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)

        return True

