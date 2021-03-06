'''
Author: whalefall
Date: 2021-02-20 16:53:03
LastEditTime: 2021-03-13 23:00:20
Description: 平洲二中查人function文件
'''
# from flask import *
import pymysql
import json
import datetime
import requests
import random
import time

# 数据库参数
host = "192.168.101.4"
user = "root"
password = "123456"
database = "pzez"

# 新增将长内容储存到云笔记本(jishiben.me) 输出内容链接


class Jishiben():

    def __init__(self):
        self.url = "http://jishiben.me/"
        # 请求头
        self.header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # "Content-Length": "57"
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "jsbtime=%s" % (str(int(time.time()))),
            "Host": "jishiben.me",
            "Origin": "http://jishiben.me",
            "Pragma": "no-cache",
            "Referer": "http://jishiben.me/dqfjz",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

    def content(self, content):

        try:
            # 获取301重定向的链接
            re_url = requests.get(self.url, headers=self.header, timeout=5).url
            # print(re_url)
            # 内容
            data = {
                "t": content,
            }
            resp = requests.post(
                url=re_url, data=data, timeout=5).content.decode(encoding="utf8")

            if "更改已保存" in resp:
                print("[PZEZ]文本储存成功 %s" % (re_url))
                return re_url
            else:
                print("[PZEZ]文本可能储存失败 %s" % (re_url))
                return re_url
            

        except Exception as e:
            print("[PZEZ]文本转存网络错误 %s" % (e))
            return "[PZEZ]文本转存网络错误 %s" % (e)
        
        finally:
            # 关闭链接
            resp.close()
            


# test = Jishiben()
# test.content("我系好sasa")

# 拼音缩写搜索(需要精准查询)


def check_pyname(pyname):
    try:
        # 打开数据库连接
        conn = pymysql.connect(host=host, user=user,
                               passwd=password, port=3306, database=database)
        # 获取游标
        cursor = conn.cursor()
        # print("数据库连接成功")
    except Exception as e:
        print("[PZEZ]连接数据失败", str(e))

    # 拼音缩写我就不做模糊搜索了
    # pyname = "%" + pyname + "%"
    # sql = "select * from student where name_py like %s;"
    sql = "select * from student where name_py=%s;"
    cursor.execute(sql, (pyname))
    result = cursor.fetchall()
    # print(result)
    result_long = len(result)  # 输出结果数量
    # 遍历元组,取走所有数据
    res = ""
    # 增加摘要输出
    title = ""
    for data in result:
        # print(data)
        student = data[0]
        name = "{}({})".format(data[1], data[2])
        sex = data[3]
        idcard = data[4]
        where = data[5]
        born = data[6]
        age = data[7]
        star = data[8]
        shuxian = data[9]

        # 增加初三
        new_class = data[10]
        new_class_id = data[11]
        new_class_all = "%s%s" % (new_class, str(new_class_id))
        res = "姓名:{} 班别:{}->{} 性别:{} 学籍号:{} 地区:{} 生日:{} 年龄:{} 星座:{} 属相:{}\n".format(name, student, new_class_all, sex, idcard, where,
                                                                                    born, age, star,
                                                                                    shuxian) + res
        # 加个摘要输出
        title = "{}->{}{},".format(student, new_class_all, data[1]) + title

    msg = "名字缩写:{} 共找到{}条结果".format(pyname, result_long)
    res = res.strip()  # 处理结尾的垃圾换行符
    print("[PZEZ]", msg)
    print("[PZEZ]", res)
    print("[PZEZ]", title)
    return title, msg, res


# check_pyname("fxy")

# 需要支持模糊查询
def check_name(check_name):
    try:
        # 打开数据库连接
        conn = pymysql.connect(host=host, user=user,
                               passwd=password, port=3306, database=database)
        # 获取游标
        cursor = conn.cursor()
        # print("数据库连接成功")
    except Exception as e:
        print("[PZEZ]连接数据失败", str(e))

    # 姓名模糊搜索
    name = "%" + check_name + "%"
    sql = "select * from student where name like %s;"
    # sql = "select * from student where name_py=%s;"
    cursor.execute(sql, (name))
    result = cursor.fetchall()
    result_long = len(result)  # 输出结果数量
    # 遍历元组,取走所有数据
    res = ""  # 总结果
    title = ""  # 摘要输出
    for data in result:
        # print(data)
        student = data[0]
        name = "{}({})".format(data[1], data[2])
        sex = data[3]
        idcard = data[4]
        where = data[5]
        born = data[6]
        age = data[7]
        star = data[8]
        shuxian = data[9]

        # 增加初三
        new_class = data[10]
        new_class_id = data[11]
        new_class_all = "%s%s" % (new_class, str(new_class_id))
        res = "姓名:{} 班别:{}->{} 性别:{} 学籍号:{} 地区:{} 生日:{} 年龄:{} 星座:{} 属相:{}\n".format(name, student, new_class_all, sex, idcard, where,
                                                                                    born, age, star,
                                                                                    shuxian) + res
        # 加个摘要输出
        title = "{}->{}{},".format(student, new_class_all, data[1]) + title

    msg = "名字(支持模糊查询):{} 共找到{}条结果".format(check_name, result_long)
    res = res.strip()  # 处理结尾的垃圾换行符
    print("[PZEZ]", msg)
    print("[PZEZ]", res)
    print("[PZEZ]", title)
    return title, msg, res


# 生日搜索(支持模糊查询)
def check_born(check_born):
    try:
        # 打开数据库连接
        conn = pymysql.connect(host=host, user=user,
                               passwd=password, port=3306, database=database)
        # 获取游标
        cursor = conn.cursor()
        # print("数据库连接成功")
    except Exception as e:
        print("[PZEZ]连接数据失败", str(e))

    # 姓名模糊搜索
    name = "%" + check_born + "%"
    sql = "select * from student where born like %s;"
    # sql = "select * from student where name_py=%s;"
    cursor.execute(sql, (name))
    result = cursor.fetchall()
    result_long = len(result)  # 输出结果数量
    # 遍历元组,取走所有数据
    res = ""  # 总结果
    title = ""  # 摘要输出
    for data in result:
        # print(data)
        student = data[0]
        name = "{}({})".format(data[1], data[2])
        sex = data[3]
        idcard = data[4]
        where = data[5]
        born = data[6]
        age = data[7]
        star = data[8]
        shuxian = data[9]

        # 增加初三
        new_class = data[10]
        new_class_id = data[11]
        new_class_all = "%s%s" % (new_class, str(new_class_id))
        res = "姓名:{} 班别:{}->{} 性别:{} 学籍号:{} 地区:{} 生日:{} 年龄:{} 星座:{} 属相:{}\n".format(name, student, new_class_all, sex, idcard, where,
                                                                                    born, age, star,
                                                                                    shuxian) + res
        # 加个摘要输出
        title = "{}->{}{},".format(student, new_class_all, data[1]) + title

    msg = "生日(格式:X月X日):{} 共找到{}条结果".format(check_born, result_long)
    # 处理结尾的垃圾换行符
    res = res.strip()
    title = title.strip()
    print("[PZEZ]", msg)
    print("[PZEZ]", res)
    print("[PZEZ]", title)
    return title, msg, res


# 查询log写入数据库
def write_log(check_name, ty):
    try:
        # 打开数据库连接
        conn = pymysql.connect(host=host, user=user,
                               passwd=password, port=3306, database=database)
        # 获取游标
        cursor = conn.cursor()
        # print("数据库连接成功")
    except Exception as e:
        print("[PZEZ]连接数据失败", str(e))

    # 获取当前时间
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = "INSERT INTO `log` (`check_name`,`type`,`time`) VALUES (%s,%s,%s)"
    try:
        cursor.execute(sql, (check_name, ty, time))
        # 一定要提交更改
        cursor.connection.commit()
        print("[PZEZ]查询已记录数据库".format(check_name))
        return "1"
    except Exception as e:
        print("[PZEZ]查询写入数据库错误", e)
        return "0"


# write_log("黄颖怡","564")

# check_name("乐")

# check_born("2月5日")

# 接口部分
# app = Flask(__name__)


# @app.route("/pzez/", methods=["GET", "POST"])
def run(ty, pyname_real, name_real, born_real):
    try:
    # 判断为空的情况
        if pyname_real is not None:
            print(pyname_real)
            title, msg, result = check_pyname(pyname_real)  # 以拼音查询
        elif name_real is not None:
            print(name_real)
            title, msg, result = check_name(name_real)
        elif born_real is not None:
            print(born_real)
            title, msg, result = check_born(born_real)
        else:
            pass

        # 结果集
        res_json = {"msg": "", "title": "", "result": "", "result_url": ""}
        res_json["msg"] = msg
        res_json["title"] = title
        res_json["result"] = result
        res_json["result_url"] = Jishiben().content(result)
        write_log(title, ty)
        # 这是因为json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False：
        # print(res_json)
        return res_json

    except Exception as e:
        return {"msg": "[eroor]系统出现异常,情检查请求参数:{}".format(str(name_real), str(pyname_real), str(born_real)),
                "result": "{}".format(e),"result_url": "[Empty]"}


# 一定要写上,不然用第三方调用就失败
if __name__ == "__main__":
    run(None, "hyy", None, None)
