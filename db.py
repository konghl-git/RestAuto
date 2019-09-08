#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:kong
@file: db.py
@time: 2019/09/04
用来对于各种数据库的连接
"""
import MySQLdb
import cx_Oracle
import os
import sys
import sqlite3

reload(sys)
sys.setdefaultencoding("utf-8")

path = os.path.split(os.path.realpath(__file__))[0]
path = path.decode("GBK")
path = path.encode("utf-8")
data = path + "\\Rest.db"  # 创建一个数据库


class DB(object):
    """
    数据库的操作
    """
    def __init__(self,ip,  userName, passWord, DB_type="Oracle", DB_name="", port=1521):
        self.ip = ip              # 数据库ip地址
        self.DB_name = DB_name    # 数据库名或者是Oracle数据的侦听orcl
        self.userName = userName  # 数据库用户名
        self.passWord = passWord  # 数据库密码
        self.DB_type = DB_type    # 数据库类型区分Oracle 、MySQL等数据库
        self.port = port          # 数据库端口

    def connect(self,name):
        """
        连接数据库
        :param name: 保存数据库的信息名如：平台7412
        :return:
        """
        try:       # 获取连接错误信息
            if self.DB_type == "Oracle":
                if self.DB_name == "":
                    self.DB_name = "orcl"      # 使用默认侦听
                os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 用来对oracle数据库查询显示中文设置，防止乱码
                db = cx_Oracle.connect(str(self.userName), str(self.passWord), str(self.ip)+":"+str(self.port)+"/"+str(self.DB_name))
            if self.DB_type == "MySQL":
                db = MySQLdb.connect(host=str(self.ip), port=self.port, user=str(self.userName), passwd=str(self.passWord)
                                       , db=str(self.DB_name),charset="utf8")
            db = db.cursor()
        except cx_Oracle.DatabaseError as e:
            return 0, e  # 返回带有状态码的元组，1为连接成功，0为连接失败
        else:
            # 连接成功保存信息
            self.save_message()
            return 1, db

    def save_message(self,name):
        """
        用来保存数据库信息
        :param name: 保存数据库的信息名如：平台7412
        :return:
        """
        conn = sqlite3.connect(data)
        cur = conn.cursor()

        # 创建一张表
        # IF NOT EXISTS 不会被重复创建
        cur.execute("CREATE TABLE IF NOT EXISTS db_message(name VARCHAR, db_type VARCHAR, DB_name VARCHAR, port INTEGER, "
                    "username VARCHAR , password varchar, ip)")

        # 先检索是否有重复的内容
        cur.execute("SELECT name FROM menu")
        all_name = cur.fetchall()
        if name in [name_one[0] for name_one in all_name]:   # 有重复的直接修改
            cur.execute("UPDATE db_message SET db_type = '%s',DB_name='%s', port='%d',username='%s',password='%s',ip='%s'  WHERE name = '%s'"
                        % (self.DB_type, self.DB_name, self.port, self.userName, self.passWord,self.ip, name))
        else:
            # 插入信息
            cur.execute("INSERT INTO db_message VALUES('%s','%s', '%s', '%d','%s','%s','%s')" % (name, self.DB_type, self.DB_name, self.port
                                                                                  ,self.userName, self.passWord,self.ip))
        conn.commit()
        cur.close()
        conn.close()


if __name__ == "__main__":
    db = DB(ip="192.168.3.170",userName="pt7412",passWord="1234")
    bb = db.connect()
    if bb[0] == 1:
        bb = bb[1]
    else:
        print(bb[1])
    bb.execute("select * from T_HZOA_APP_RSGL_USER")
    print bb.fetchall()