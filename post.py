#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:kong
@file: post.py
@time: 2019/09/04
接口的操作
"""
import json
import requests
import yaml,chardet
import os
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

path = os.path.split(os.path.realpath(__file__))[0]
path = path.decode("GBK")
path = path.encode("utf-8")


def post(name, url, pm):
    """
    我们只使用post方式来进行接口操作
    :param name:操作名称
    :param url:地址
    :param pm:参数
    :return:字典格式
    """
    try:
        pm = json.dumps(pm)
        receive = requests.post(url, pm)
        result = json.loads(receive.content)
        return 1, result
    except (ValueError, requests.exceptions.ConnectionError) as e:
        return 0, e


def classify(ip, port_name):
    """
    用来对于接口url后缀进行填写，目前我们只考虑流程操作
    :param ip: url例如：192.168.5.4:8099/workflow
    :param port_name:接口名字：流程操作
    :return:
    """
    classify_name = {
        u"打开流程": "horizon/workflow/rest/flow/support/open.wf",
        u"流程操作": "horizon/workflow/rest/flow/support/action.wf",
        u"登录": "/horizon/workflow/rest/user/login.wf"
    }         # 存放操作url后缀
    url = "http://" + ip + classify_name[port_name]
    return url


def restful(ip, port_name, name, pm, record=0, address=""):
    """
    调用上面两个方法来进行接口的操作
    :param ip: url例如：192.168.5.4:8099/workflow
    :param port_name:接口名字：流程操作
    :param name:操作名称
    :param pm:参数
    :param record: 是否生成日志默认不生成
    :param address: 日志生成目录，默认为本地文件夹
    :return:
    """
    url = classify(ip, port_name)
    result = post(name, url, pm)
    data = path + "\\" + port_name + "_" + name + ".yaml"  # 保存传入参数和返回信息的
    pm_dict = {u"传入参数": pm}          # 参数字典
    result_dict = {u"返回字段": result}  # 返回字段字典
    with open(data, "w") as f:
        yaml.dump(pm_dict, f)
        yaml.dump(result_dict, f)

    if record == 1:
        time_now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        time_now_1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print chardet.detect(time_now)
        if address == "":
            address = path + "\\" + port_name + "_" + name + "_" + time_now + ".txt"
        else:
            address = address + "\\" + port_name + "_" + name + "_" + time_now + ".txt"
        with open(address, "a") as f:
            # 为了在文件中显示出中文，我们对于Unicode编码进行修改
            pm_dict = str(pm_dict).replace('u\'', '\'')
            pm_dict = pm_dict.decode("unicode-escape").encode("utf-8")
            result_dict = str(result_dict).replace('u\'', '\'')
            result_dict = result_dict.decode("unicode-escape").encode("utf-8")

            # 修改换行
            pm_dict = pm_dict.replace("}", "}\n")
            pm_dict = pm_dict.replace(",", ",\n")
            result_dict = result_dict.replace("}", "}\n")
            result_dict = result_dict.replace(",", ",\n")

            f.write(time_now_1+":  ")
            f.write(pm_dict)
            f.write("\n"*2)
            f.write(time_now_1 + ":  ")
            f.write(result_dict)
    return result


if __name__ == "__main__":
    a = restful("192.168.5.4:8099/workflow",u"登录",u"好好登陆",{"loginName":"admin","password":"1234","tenantCode":""},1)
    print a