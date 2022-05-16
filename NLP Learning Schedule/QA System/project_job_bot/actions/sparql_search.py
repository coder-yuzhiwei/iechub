import requests
import json
import redis
import uuid
# 159.75.19.210


url = "http://159.75.19.210:20068/hello"
keys = {'0':0,
        '1': 1, '2': 2, '3':3, '4':4 , '5':5 ,'6':6,'7':7,'8':8,'9':9,
        'a':10,'b':50,'c':100,'d':200,'e':400,'f':10000,'-':0}
def trans(st):
    print(st[10])
    re = 0
    for i  in st:
        re = re + keys[i]
    return re

def conn(quar, company, address, salary, wealfare):
    params = {}
    params['quar'] = quar
    if company is not None:
        params['company'] = company
    else:
        params['company'] = ""
    if address is not None:
        params['address'] = address
    else:
        params['address'] = ""
    if salary is not None:
        params['salary'] = salary
    else:
        params['salary'] = ""
    if wealfare is not None:
        params['wealfare'] = wealfare
    else:
        params['wealfare'] = ""
    response = requests.get(url=url, params=params)

    job = response.text
    j = eval(job)
    conn1 = redis.Redis(host="159.75.19.210", port=6379, decode_responses=True, password="xingke419")
    id1 = str(uuid.uuid1())
    id  = str(trans(id1))
    # conn1.set(id, job)  # ex代表seconds，px代表ms
    for i in j.values():
        txt = eval(i)
        # print(txt['employee_firmid']) #企业后台用户Id
        # print(txt['employee_welfareIds'])#福利待遇id
        # print(txt['employee_perHour'])  # 时薪
        # print(txt['employee_status'])  # 状态，0=未提交；1=已提交；2=已审核
        # print(txt['employee_submitTime'])  # 提交时间
        # print(txt['employee_Industry'])  # 所属行业
        # print(txt['employee_id'])  # id

        # print(txt['employee_phone'])  # 电话
        # print(txt['employee_salary'])  # 工资
        # print(txt['employee_createTime'])  # 创建时间
        # print(txt['employee_linkman'])  # 联系人
        # print(txt['employee_TextFd1'])  # 公司简介
        # print(txt['employee_quar'])  # 岗位名字
        print(txt['employee_unitName'])  # 公司名字
        # print(txt['employee_onoff'])  # 招聘信息显示开关	0=关；1=开
        # print(txt['employee_people'])  # 招聘人数
        print(txt['employee_address'])  # 地址
        # print(txt['employee_TextFd3']) #具体福利
        # print(txt.get('employee_TextFd1', " "))  # 公司简介
        # print(txt.get('employee_TextFd2', " "))  # 岗位要求
        print(type(txt.get('employee_TextFd3', " ")))
        print(txt.get('employee_TextFd3', " "))  # 福利待遇
        if ("年终奖金" in txt.get('employee_TextFd3', " ")):
            print("ni")
        # print(txt.get('employee_TextFd4', " "))  # 联系方式
    print(id)
    return j,id
if __name__ == '__main__':
    result,id =conn("软件工程师","","","5000以上","")
    len1 = len(result)
    # print(id)