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


class DB(object):
    """
    数据库的操作
    """
    def __init__(self,ip,  userName, passWord, DB_type="Oracle", DB_name="",port=1521):
        self.ip = ip              # 数据库ip地址
        self.DB_name = DB_name    # 数据库名或者是Oracle数据的侦听orcl
        self.userName = userName  # 数据库用户名
        self.passWord = passWord  # 数据库密码
        self.DB_type = DB_type    # 数据库类型区分Oracle 、MySQL等数据库
        self.port = port          # 数据库端口

    def connect(self):
        """
        连接数据库
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
            return 1, db


if __name__ == "__main__":
    db = DB(ip="192.168.3.170",userName="pt7412",passWord="1234")
    bb = db.connect()
    if bb[0] == 1:
        bb = bb[1]
    else:
        print(bb[1])
    bb.execute("select * from T_HZOA_APP_RSGL_USER")
    print bb.fetchall()