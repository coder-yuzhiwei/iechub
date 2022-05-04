import pymssql #引入pymssql模块
import json
import requests
import re

def my_conn():
    connect = pymssql.connect('8.129.99.224', 'root', '12345678', 'hc_ddlwpq') #服务器名,账户,密码,数据库名
    return connect

"""
select A.ID from dbo.ceb_recruit as A ,ceb_quarters as B  where quar like '%助理%' and hiringId=B.Id and onoff=1
"""

sql2id = """
select A.ID from dbo.ceb_recruit as A ,ceb_quarters as B  where A.Id=my_id and hiringId=B.Id and onoff=1
"""
sql2quar = """
select A.ID from dbo.ceb_recruit as A ,ceb_quarters as B  where quar like '%my_quar%' and hiringId=B.Id and onoff=1
"""

sql2company ="""
select A.ID from dbo.ceb_recruit as A ,ceb_quarters as B  where unitName like '%company%' and hiringId=B.Id and onoff=1
"""

sq2address ="""
select A.ID from dbo.ceb_recruit as A ,ceb_quarters as B  where address like '%dizhi%' and hiringId=B.Id and onoff=1
"""
wel2id ="""
select id from dbo.ceb_welfare where weal like '%fuli%' 
"""

sql2weal="""
select A.ID from dbo.ceb_recruit as A ,ceb_quarters as B  where welfareIds like '%weal%' and hiringId=B.Id and onoff=1
"""

sql2res="""
select A.ID,quar,unitName,linkman,phone,address,salary,TextFd3 from dbo.ceb_recruit as A ,dbo.ceb_quarters as B  where A.ID= 'myID' and hiringId=B.Id and onoff=1
"""
def rawdata(resList):
    res =[]
    for i in resList:
        res.append(i[0])
    return res

def rawdata2(resList):
    job = dict()
    res =[]
    for i in resList:
        job['employee_id'] = i[0]
        job['employee_quar'] = i[1]
        job['employee_unitName'] = i[2]
        job['employee_linkman'] = i[3]
        job['employee_phone'] = i[4]
        job['employee_address'] = i[5]
        job['employee_salary'] = i[6]
        text = re.sub(r'<[^>]+>', '', i[7].encode('latin-1').decode('gbk'))
        text = text.replace("&nbsp;","")
        text = text.replace("^#^","")
        text = text.replace("\r\n","")
        text = text.replace("\xa0","")
        text = text.replace("\t","")
        job['employee_Texd3'] = text
        res.append(json.dumps(job, ensure_ascii=False))
    return res[0]

def searchjobName(name):
    res = []
    conn = my_conn()
    cursor = conn.cursor()
    query = sql2quar.replace("my_quar",name)
    cursor.execute(query)
    resList = cursor.fetchall()
    conn.close()
    res = rawdata(resList)    
    return res

def searchjobCompany(name):
    res = []
    conn = my_conn()
    cursor = conn.cursor()
    query = sql2company.replace("company",name)
    cursor.execute(query)
    resList = cursor.fetchall()
    conn.close()
    res = rawdata(resList)    
    return res


def searchjobAddress(address):
    res = []
    conn = my_conn()
    cursor = conn.cursor()
    query = sq2address.replace("dizhi",address)
    cursor.execute(query)
    resList = cursor.fetchall()
    conn.close()
    res = rawdata(resList)    
    return res


def id2Wealfare(id):
    res = []
    conn = my_conn()
    cursor = conn.cursor()
    query = sql2weal.replace("weal",id)
    cursor.execute(query)
    resList = cursor.fetchall()
    conn.close()
    res = rawdata(resList)    
    return res


def searchjobWealfare(weal):
    res = []
    conn = my_conn()
    cursor = conn.cursor()
    query = wel2id.replace("fuli",address)
    cursor.execute(query)
    resList = cursor.fetchall()
    conn.close()
    for i in resList:
        id = i[0]
        res = id2Wealfare(id)   
    return res

def str2Salary(salary):
    l=0 #下限
    r=0 #上限
    flag = True
    for i in salary:
        if i.isdigit():
            if flag:
                l=l*10+int(i)
            else:
                r=r*10+int(i)
        else:
            flag=False
    
    if l>r:
        tmp=l
        l=r
        r=tmp
    return l,r

def conn(quar,company,address,salary,wealfare):
    result = set()
    if (quar !=None)&(quar!=""):
        result=set(searchjobName(quar))
    if (company !=None)&(company!=""):
        result=result.intersection(set(searchjobCompany(company)))
    if (address !=None)&(address!=""):
        result=result.intersection(set(searchjobAddress(address)))
    if (wealfare !=None)&(wealfare!=""):
        result=result.intersection(set(searchjobWealfare(wealfare)))
    if (salary !=None)&(salary!=""):
        t_res = set()
        l,r = str2Salary(salary)
        
        if l==0: #只有一个数，就是以上，左右这种
            for i in result:
                job = json.loads(i)
                slary = job["employee_salary"]
                l1,r1 =  str2Salary(slary.lstrip())
                if l1==0&r1==0:
                    continue
                if l1==0: #只有一个
                    if l1>=r:
                        t_res.add(i)
                
                else:
                    if l1<100:
                        l1=l1*1000
                        r1=r1*1000
                    if r1>=r:
                        t_res.add(i)        
               
        else: #两个数，就是区间
            for i in result:
                job = json.loads(i)
                slary = job["employee_salary"]
                l1,r1 =  str2Salary(slary.lstrip())
                if l1==0&r1==0:
                    continue
                if l1==0:
                    if l1>=1&l1<=r:
                        t_res.add(i)
                else:
                    if l1<100:
                        l1=l1*1000
                        r1=r1*1000
                    if r1>=l&l1<=r:
                        t_res.add(i)
                        
        return t_res
    url = "http://tintinrenli.xn--fiqs8s/data/wxapp.ashx"
    params = {"op":"1000","gjc":str(result)}
    res = requests.get(url=url,params=params)
    return result

def Myconn(quar,company,address,salary,wealfare):

    tmp = conn(quar,company,address,salary,wealfare)
    res = []
    con = my_conn()
    cursor = con.cursor()
    for i in tmp:
        query = sql2res.replace("myID",str(i))
        cursor.execute(query)
        resList = cursor.fetchall()
        t_res = rawdata2(resList)
        res.append(t_res)
    con.close()
    return res
 
    

if __name__ == '__main__':

    res=Myconn("软件工程师","","","","")
    print(res)
    result=conn("木工","","","","")
    print(len(result))
    for i in result:
        print(i)
    for i in res:
        txt = json.loads(i)
        # print(txt['employee_Industry'])
        print(txt['employee_salary'])  # 工资
        print(txt['employee_quar'])  # 岗位名字
        print(txt['employee_unitName'])  # 公司名字
        # print(txt.get('employee_TextFd3', " "))  # 福利待遇
  
