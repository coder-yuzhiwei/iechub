from django.db import models
from common.database import OraclePool
import time
# Create your models here.


def get_password(username):
    orcl = OraclePool()
    sql = "select password from users where username='%s'" % username
    password = orcl.fetch_all_array(sql)
    return password


def check_user(username):
    orcl = OraclePool()
    sql = "select count(1) from users where username = '%s'" % username
    data = orcl.fetch_all_array(sql)
    return data


def register_user(username, password):
    orcl = OraclePool()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into users(username, password, register_time) values('%s','%s','%s')" %(username, password, now_time)
    orcl.execute_sql(sql)
    return

