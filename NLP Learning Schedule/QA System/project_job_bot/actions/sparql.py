from SPARQLWrapper import SPARQLWrapper, JSON
import json
import re

sparql = SPARQLWrapper("http://localhost:3030/kg_demo_job/query")
# 159.75.19.210
id2all = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.kgdemo.com#> 
SELECT *
WHERE {
<file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#dbo/employee/my_id> ?n ?value

}
"""
job2id = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.kgdemo.com#> 
PREFIX employee: <file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#>
SELECT ?s
WHERE {
?s :employee_quar ?o
filter regex(?o,'jobName')
}
"""

cy2job = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.kgdemo.com#> 
PREFIX employee: <file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#>
SELECT ?s
WHERE {
?s :employee_unitName ?o
filter regex(?o,'companyName')
}
"""
ads2job = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.kgdemo.com#> 
PREFIX employee: <file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#>
SELECT*
WHERE {
?s :employee_address ?o
filter regex(?o,'_address')
}
"""
weal2Wid = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.kgdemo.com#> 
PREFIX employee: <file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#>
SELECT ?s
WHERE {
?s :welfare_weal ?o
filter regex(?o,'wealfare')
}
"""
Wid2job = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.kgdemo.com#> 
PREFIX employee: <file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#>
SELECT*
WHERE {
?s :employee_welfareIds ?o
filter regex(?o,'weal_id')
}
"""


def searchjobID(id):  # id查询岗位，返回一个字典

    query = id2all.replace("my_id", id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    job = dict()
    for result in results["results"]["bindings"]:
        s = result["n"]["value"].replace("http://www.kgdemo.com#", "")
        if (s == "employee_TextFd1") | (s == "employee_TextFd2") | (s == "employee_TextFd3"):
            html = result["value"]["value"]
            text = re.sub(r'<[^>]+>', '', html)
            text = text.replace("&nbsp;", "")
            text = text.replace("福利待遇^#^", "")
            job[s] = text
        else:
            job[s] = result["value"]["value"]
    return job


def searchjobName(name):
    res = []
    query = job2id.replace("jobName", name)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        id = result["s"]["value"].replace("file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#dbo/employee/", "")
        res.append(json.dumps(searchjobID(id), ensure_ascii=False))
    return res


def searchjobCompany(name):
    res = []
    query = cy2job.replace("companyName", name)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        id = result["s"]["value"].replace("file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#dbo/employee/", "")
        res.append(json.dumps(searchjobID(id), ensure_ascii=False))
    return res


def searchWealID(id):
    res = []
    query = Wid2job.replace("weal_id", id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        id = result["s"]["value"].replace("file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#dbo/employee/", "")
        res.append(json.dumps(searchjobID(id), ensure_ascii=False))
    return res


def searchjobWealfare(weal):
    res = []
    query = weal2Wid.replace("wealfare", weal)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        id = result["s"]["value"].replace("file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#dbo/welfare/", "")
        res = searchWealID(id)
    return res


def searchjobAddress(address):
    res = []
    query = ads2job.replace("_address", address)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        id = result["s"]["value"].replace("file:///C:/Users/xingke/Desktop/自动问答/d2rq-0.8.1/qa2.nt#dbo/employee/", "")
        res.append(json.dumps(searchjobID(id), ensure_ascii=False))
    return res


def str2Salary(salary):
    l = 0  # 下限
    r = 0  # 上限
    flag = True
    for i in salary:
        if i.isdigit():
            if flag:
                l = l * 10 + int(i)
            else:
                r = r * 10 + int(i)
        else:
            flag = False

    if l > r:
        tmp = l
        l = r
        r = tmp
    return l, r


def conn(quar, company, address, salary, wealfare):
    result = set()
    if (quar != None) & (quar != ""):
        result = set(searchjobName(quar))
    if (company != None) & (company != ""):
        result = result.intersection(set(searchjobCompany(company)))
    if (address != None) & (address != ""):
        result = result.intersection(set(searchjobAddress(address)))
    if (wealfare != None) & (wealfare != ""):
        result = result.intersection(set(searchjobWealfare(wealfare)))
    if (salary != None) & (salary != ""):
        t_res = set()
        l, r = str2Salary(salary)

        if l == 0:  # 只有一个数，就是以上，左右这种
            for i in result:
                job = json.loads(i)
                slary = job["employee_salary"]
                l1, r1 = str2Salary(slary.lstrip())
                if l1 == 0 & r1 == 0:
                    continue
                if l1 == 0:  # 只有一个
                    if l1 >= r:
                        t_res.add(i)

                else:
                    if l1 < 100:
                        l1 = l1 * 1000
                        r1 = r1 * 1000
                    if r1 >= r:
                        t_res.add(i)

        else:  # 两个数，就是区间
            for i in result:
                job = json.loads(i)
                slary = job["employee_salary"]
                l1, r1 = str2Salary(slary.lstrip())
                if l1 == 0 & r1 == 0:
                    continue
                if l1 == 0:
                    if l1 >= 1 & l1 <= r:
                        t_res.add(i)
                else:
                    if l1 < 100:
                        l1 = l1 * 1000
                        r1 = r1 * 1000
                    if r1 >= l & l1 <= r:
                        t_res.add(i)

        return t_res

    return result
    
if __name__ == '__main__':
    result=conn("助理","","","8000以上","")
    len1 = len(result)
    print(len(result))
    if len1 == 12:
        data = "共为您找到{}条信息，请通过微信公众号查看".format(len1)
        print(data)
    else:
        for i  in result:
            txt = json.loads(i)
            print(txt['employee_Industry'])
            print(txt['employee_salary'])  # 工资
            print(txt['employee_quar'])  # 岗位名字
            print(txt['employee_unitName'])  # 公司名字
            print(txt.get('employee_TextFd3', " ")) # 福利待遇
'''     for i in result:
        txt = json.loads(i)  #json对象转化为字典
        
        #print(txt['employee_firmid']) #企业后台用户Id
        #print(txt['employee_welfareIds'])#福利待遇id
        print(txt['employee_perHour'])#时薪
        print(txt['employee_status'])#状态，0=未提交；1=已提交；2=已审核
        print(txt['employee_submitTime'])#提交时间
        print(txt['employee_Industry'])#所属行业
        print(txt['employee_id'])# id
        
        print(txt['employee_phone'])#电话
        print(txt['employee_salary'])# 工资
        print(txt['employee_createTime'])#创建时间
        print(txt['employee_linkman'])#联系人
        print(txt['employee_TextFd1'])#公司简介
        print(txt['employee_quar'])# 岗位名字
        print(txt['employee_unitName'])# 公司名字
        print(txt['employee_onoff'])# 招聘信息显示开关	0=关；1=开
        print(txt['employee_people'])#招聘人数
        print(txt['employee_address'])#地址
        #print(txt['employee_TextFd3']) #具体福利
        print(txt.get('employee_TextFd1'," "))#公司简介
        print(txt.get('employee_TextFd2'," "))#岗位要求
        print(txt.get('employee_TextFd3'," "))#福利待遇
 '''


  

    
    

    
