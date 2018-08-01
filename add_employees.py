import requests
import register
import xlrd
from faker import Factory
import threading

host = 'https://www.yl9158.com'
mobile = '13805719756'
password = '123456'

r = register.Register(host)
session = r.login_session(mobile,password)
compid = session[1]['module']['compId']

def get_role_id(name):
    roles = r.get_roleid(session[0])
    for item in roles:
        if item['roleName'] == name:
            return item['roleId']

storeid = r.get_sotreid(session[0])[0]['storeId']
storeName = r.get_sotreid(session[0])[0]['storeName']

# fake = Factory.create('zh_CN')
# employees_phone = fake.phone_number()
# employees_name = '丽娜'

def add_employess(employees_phone,rolename,employees_name,pwd):
    try:
        r.add_employee_api(session[0],compid,employees_phone,storeid,get_role_id(rolename),employees_name)
        password = r.get_forget_password(employees_phone)
        employees_session=r.login_session(employees_phone,password)[0]
        r.updata_password(employees_session, employees_phone,pwd)
        print('\n%s:%s-成功\n'%(employees_name,employees_phone))
    except:
        print('\n添加员工 %s:%s-失败了失败！！\n' % (employees_name, employees_phone))

def get_data_from_excel():
    workbook = xlrd.open_workbook(r'employees.xlsx')
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    employees = []
    for r in range(rows):
        array = []
        for n in range(cols):
            value = sheet.cell(r, n).value
            if n == 1:
                value = value.split('-')[1]
            array.append(value)
        employees.append(array)
    return employees

count = 0
# for item in get_data_from_excel():
#     add_employess(item[1],'店长',item[0],'111111')
add_employess('李玉娇','店长','18868779989',111111)



