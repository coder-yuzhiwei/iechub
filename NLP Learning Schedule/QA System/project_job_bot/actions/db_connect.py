import pymssql  # 引入pymssql模块
import pandas as pd


def conn(job, company):
    conn = pymssql.connect('(local)', 'sa', 'cjm521', 'QA')  # 服务器名,账户,密码,数据库名
    if conn:
        print("连接成功!")
    cursor = conn.cursor()
    f_job = False
    f_company = False
    if job is None and company is None:
        return "请重新输入"
    if job is not None:
        # sql= "select A.ID,quar from ceb_recruit as A ,ceb_quarters as B where firmId=B.Id and quar like '%学徒%'"
        sql = "select A.ID,quar,unitName,salary from ceb_recruit as A ,ceb_quarters as B where hiringId=B.Id and quar like '%{0}%'".format(
            job)
        cursor.execute(sql)

        resList = cursor.fetchall()
        # cols为字段信息 例如((''))
        cols = cursor.description
        col = []
        for i in cols:
            col.append(i[0])
        data = list(map(list, resList))
        data1 = pd.DataFrame(data, columns=col)
        f_job = True
    if company is not None:
        sql = "select A.ID,quar,unitName,salary from ceb_recruit as A ,ceb_quarters as B where firmId=B.Id and unitName like '%{0}%'".format(
            company)
        cursor.execute(sql)

        resList = cursor.fetchall()
        # cols为字段信息 例如((''))
        cols = cursor.description
        col = []
        for i in cols:
            col.append(i[0])
        data = list(map(list, resList))
        data2 = pd.DataFrame(data, columns=col)
        f_company = True

    if f_job and f_company:
        data = pd.merge(data1, data2)
    elif f_job and not f_company:
        data = data1
    else:
        data = data2
    # 查询完毕后必须关闭连接
    conn.close()
    print(data)
    return data


if __name__ == '__main__':
    conn("培训", None)
