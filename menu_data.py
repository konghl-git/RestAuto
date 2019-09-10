#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:kong
@file: menu_data.py
@time: 2019/09/08
用来创建目录列表文件
"""
import os
import sys
import sqlite3
import uuid
reload(sys)
sys.setdefaultencoding("utf-8")

path = os.path.split(os.path.realpath(__file__))[0]
path = path.decode("GBK")
path = path.encode("utf-8")
data = path + "\\Rest.db"  # 创建一个数据库


def menu_data_add(parent_id, current):
    """
    用来新增目录列表
    :param parent_id: 添加的目录的父目录id
    :param current: 添加的目录
    :return:False为当前目录下已经存在同样的目录，True为创建成功
    """

    conn = sqlite3.connect(data)
    cur = conn.cursor()

    # 创建一张表
    # IF NOT EXISTS 不会被重复创建
    cur.execute("CREATE TABLE IF NOT EXISTS menu(id VARCHAR, parent_id VARCHAR, current VARCHAR, level INTEGER)")

    # 先检索是否有重复的内容
    cur.execute("SELECT * FROM menu")
    current_menu_all = cur.fetchall()

    # 查看是否有根目录
    if "root_id" not in [x[0] for x in current_menu_all]:
        cur.execute("INSERT INTO menu VALUES('root_id','','Rest操作', 0)")
        conn.commit()
    for menu_one in current_menu_all:
        if (menu_one[1], menu_one[2]) == (parent_id, current):         # 先检索是否有重复的内容
            return False

    # 插入数据
    id = uuid.uuid1()          # 生成随机id
    # 获取上级目录层级
    cur.execute("SELECT level FROM menu WHERE id='%s'" % parent_id)
    parent_level = cur.fetchone()[0]
    level = parent_level + 1
    cur.execute("INSERT INTO menu VALUES('%s','%s', '%s', '%d')" % (id, parent_id, current, level))
    conn.commit()
    cur.close()
    conn.close()
    return True


def menu_delete_alone(current_id):
    """
    删除当前目录，不删除带有下级目录的目录
    :param current_id:当前目录id
    :return:False代表存在多层下级目录，True表示删除成功
    """
    conn = sqlite3.connect(data)
    cur = conn.cursor()

    # 先进行检测是否存在多层下级目录
    cur.execute("SELECT parent_id FROM menu")
    for parent_menu in cur.fetchall():
        if current_id in parent_menu:
            return False
    cur.execute("DELETE FROM menu WHERE id='%s'" % current_id)
    conn.commit()
    cur.close()
    conn.close()
    return True


def menu_delete_all(current_id):
    """
    删除当前目录，同时删除当前目录下所有目录
    :param current_id:当前目录id
    :return:
    """
    conn = sqlite3.connect(data)
    cur = conn.cursor()

    cur.execute("DELETE FROM menu WHERE id='%s'" % current_id)
    conn.commit()
    # 删除后循环查询所有没有父目录的子目录进行删除
    while True:
        cur.execute("SELECT * FROM menu")
        all_data = cur.fetchall()
        clean = True  # 用来表示是否删除干净
        for item in all_data:
            if item[0] == u"root_id":
                continue
            if item[1] not in [current_menu[0] for current_menu in all_data]:
                cur.execute("DELETE FROM menu WHERE id='%s'" % item[0])
                clean = False
        conn.commit()
        if clean:
            break
    cur.close()
    conn.close()


def show_menu(level):
    """
    用来返回所有菜单信息
    :param level: 层级数
    :return:
    """
    conn = sqlite3.connect(data)
    cur = conn.cursor()
    cur.execute("SELECT * FROM menu WHERE level='%d'" % level)
    all_data = cur.fetchall()
    cur.close()
    conn.close()
    return all_data


def change_menu(id, name):
    """
    修改名称
    :param id:当前目录id
    :param name: 要修改成的名字
    :return:
    """
    conn = sqlite3.connect(data)
    cur = conn.cursor()

    # 先检索是否有重复的内容
    cur.execute("SELECT * FROM menu")
    current_menu_all = cur.fetchall()
    # 获取上级id
    cur.execute("SELECT parent_id FROM menu WHERE id='%s'" % id)
    parent_id = cur.fetchone()[0]
    for menu_one in current_menu_all:
        if (menu_one[1], menu_one[2]) == (parent_id, name):         # 先检索是否有重复的内容
            return False

    cur.execute("UPDATE menu SET current = '%s' WHERE id = '%s'" % (name, id))
    conn.commit()
    cur.close()
    conn.close()
    return True


if __name__ == '__main__':
    print menu_data_add("ecb32970-d1ae-11e9-bbdc-c8215816250f", "3")
     # # print menu_delete_alone("654dd7b80fb8fa392806782d064b4087")
     # menu_delete_all("c77d8861-d1a6-11e9-8565-c8215816250f")
    print len(show_menu(2))

