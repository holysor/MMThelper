import requests
import hashlib
# from faker import Factory
from time import sleep
import base64
import connect_mysql as sql
import random

class Register:
    def __init__(self,host):
        self.host = host
        self.USER_AGENT =  'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
    def random_mobile(self):
        '''随机生成号码'''
        # 第二位数字
        second = [3, 4, 5, 7, 8][random.randint(0, 4)]

        # 第三位数字
        third = {
            3: random.randint(0, 9),
            4: [5, 7, 9][random.randint(0, 2)],
            5: [i for i in range(10) if i != 4][random.randint(0, 8)],
            7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
            8: random.randint(0, 9),
        }[second]
        # 最后八位数字
        suffix = random.randint(9999999, 100000000)
        # 拼接手机号
        return "1{}{}{}".format(second, third, suffix)

    def send_msg(self,mobile,type='register'):
        '''发送短信'''
        url = self.host + '/msg/msg/send'
        data = {
            'mobile':mobile,
            'type':type,
        }
        res = requests.post(url,data=data)
        return res.json()

    def get_msg_code(self):
        '''获取短信'''
        url = self.host + '/msg/msg/list'
        if 'https' in self.host:
            url = 'http:'+self.host.split(':')[-1]+'/msg/msg/list'
        res = requests.get(url)
        random_pwd= res.json()['module']['list'][0]['smsContent']
        sendtime = res.json()['module']['list'][0]['sendTime']
        msgcode = res.json()['module']['list'][0]['validCode']
        mobile = res.json()['module']['list'][0]['mobile']
        return msgcode,random_pwd,sendtime,mobile

    def get_password_md5(self,pwd):
        '''密码md5加密处理'''
        m = hashlib.md5()
        m.update(pwd.encode("UTF-8"))
        m_password = m.hexdigest()
        return m_password

    def login_session(self,mobile,pwd):
        '''企业用户登录账号，返回session，账户信息'''
        url = self.host+ '/gateway/login/checkLogin'

        data = {
            'personLoginOrMobile': mobile,
            'personPassword':self.get_password_md5(pwd),
            'scope': 'person',
        }
        headers = {
            'User-Agent': self.USER_AGENT,
        }
        session = requests.Session()
        res = session.post(url,headers=headers,data=data)
        if res.json()['success']==False:
            print(res.json()['errMsg'])
            assert False
        return session,res.json()

    def get_roleid(self,session):
        '''获取角色ID  api'''
        url = host + '/mmt/role/list?limit=100&offset=0'
        res = session.get(url)
        data = res.json()
        # total = len(data['module']['list'])
        return data['module']['list']

    def get_sotreid(self,session):
        '''获取门店id-api'''
        url = self.host + '/mmt/store/list?limit=100&offset=0'
        res =session.get(url)
        data = res.json()
        return data['module']['list']

    def add_employee_api(self,session,compid,mobile,storeid,roleid,rolename):
        '''添加员工api'''
        url = self.host + '/gateway/user/baseinfoPersonCompanyOrgWriteRpcService/addAppPerson/b1fa22023c344c5599b01c7650330200'
        data = {
            'personName': rolename,
            'mobile': mobile,
            'personPwd':'',
            'storeIds':storeid,
            'compRoleIds': roleid,
            'compId': compid,
            'avatar':'',
            'email':'',
            'sex':'',
            'compTitle':'',
            'address':'',
            'idcard':'',
            'birthday':'',
            'entryDate':'',
            'partnerType': 0,
            'channel': 'app',
            'province':'',
            'city':'',
            'zone':'',
        }
        headers = {
            'User-Agent': self.USER_AGENT,
        }
        session.post(url,data=data,headers=headers)

    def get_forget_password(self,mobile):
        '''忘记密码api'''
        url = self.host + '/msg/msg/send'
        if 'https' in self.host:
            url = 'http:' + self.host.split(':')[-1] + '/msg/msg/send'
        data = {
            'mobile': mobile,
            'type': 'forget'
        }
        requests.post(url, data=data)
        password = ''
        sleep(1)
        if mobile == self.get_msg_code()[3]:
            if self.get_msg_code()[0]:
                msg_code = self.get_msg_code()[0]
                modify_pass_url = self.host+'/mmt/user/modify_pass'
                if 'https' in self.host:
                    modify_pass_url = 'http:'+ self.host.split(':')[-1] + '/mmt/user/modify_pass'
                data1 = {
                    'mobile':mobile,
                    'code':msg_code,
                    'type':'forget',
                }
                headers = {
                    'User-Agent': self.USER_AGENT,
                }
                requests.post(modify_pass_url,data1,headers=headers)
                sleep(1)
                if mobile == self.get_msg_code()[3]:
                    if self.get_msg_code()[1]:
                        password = self.get_msg_code()[1]
        return password

    def updata_password(self,session,mobile,pwd):
        '''修改密码api'''
        self.send_msg(mobile,type='modify')
        sleep(2)
        msg_code = ''
        if mobile == self.get_msg_code()[3]:
            if self.get_msg_code()[0]:
                msg_code = self.get_msg_code()[0]
        url = self.host+'/gateway/user/baseinfoPersonCompanyOrgWriteRpcService/updatePersonPwd'
        if 'https' in self.host:
            url = 'http:' + self.host.split(':')[-1] + '/gateway/user/baseinfoPersonCompanyOrgWriteRpcService/updatePersonPwd'
        data = {
            'personMobile': mobile,
            'mobileCode': msg_code,
            'newPersonPwd': self.get_password_md5(pwd)
        }
        headers = {
            'User-Agent': self.USER_AGENT,
            'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
            'Host':self.host.split('/')[-1],
            'Pragma':'no-cache'
        }
        session.post(url,data,headers=headers)
        self.login_session(mobile,pwd)

    def updata_person_password_sql(self,compid,mobile):
        '''数据库，修改用户密码'''
        tablename = 'baseinfo_person_company_org_' + str(int(str(compid)[-4:])%15)
        opsql = sql.OperationSQL('user_central')
        opsql.execute_sql('select * from %s where comp_id=%s'%(tablename,compid))
        value = opsql.get_all_data()
        opsql.close()



    def add_allroles_employees(self,mobile,pwd,ey_pwd):
        '''
            添加所有对应角色的员工[合伙人、店长、店员、工厂管理员、商品管理员]
            超级管理员账号：mobile
            超级管理员密码：pwd
            员工设定密码：ey_pwd
        '''
        password = pwd
        login = self.login_session(mobile,password)
        session = login[0]
        compid = login[1]['module']['compId']
        roles = self.get_roleid(session)
        storeid = self.get_sotreid(session)[0]['storeId']
        employees = {}
        for role in roles:
            roleid = role['roleId']
            rolename = role['roleName']
            phone = fake.phone_number()
            try:
                self.add_employee_api(session,compid,phone,storeid,roleid,rolename)
                password = self.get_forget_password(phone)
                employees_session=self.login_session(phone,password)[0]
                self.updata_password(employees_session, phone,ey_pwd)
                employees[phone]=[rolename,ey_pwd]
            except:
                print('添加员工 %s:%s 失败'%(str(phone),rolename))
        return employees

    def to_register(self,mobile,pwd,id):
        '''注册账号
        账号：mobile
        密码：pwd
        业务类型：
            (1).id =1 ,一批
            (2).id=2，二批
            (3).id=3，零售 
        '''
        business = {
            1:'一批',
            2:'二批',
            3:'零售',
        }
        self.send_msg(mobile)
        msg_code = self.get_msg_code()
        register_url = self.host + '/gateway/user/baseinfoPersonCompanyOrgWriteRpcService/enrollPerson/c1c9468431aa463897bcedb8ad49d30b'
        data = {
            'mobile': mobile,
            'mobileCode': msg_code,
            'personPwd':self.get_password_md5(pwd),
            'ctId': id,
            'ctName': business[id],
            'businessCategory': '1,2,3,4,5',
            'channel': 'website',
            'requestCode': ''
        }
        res = requests.post(register_url,data=data,timeout=30)
        if res.status_code == 200:
            print('注册成功！')
            print('新账号：',mobile)
            print('初设密码：',pwd)
        else:
            print('注册失败！')
        return mobile,pwd

def updata_user_password(self,mobile,pwd):
    '''手机号，直接修改密码'''
    session = self.login_session(mobile,self.get_forget_password(mobile))[0]
    self.updata_password(session,mobile,pwd)

if __name__=='__main__':
    host = 'https://www.yl9158.com'
    # host = 'http://sit.yl9158.com'
    r = Register(host)
    # fake = Factory.create('zh_CN')
    # phone = fake.phone_number()
    password = '111111'
    # r.to_register(phone,password,1)#注册新账号
    # print(get_forget_password('13396573421'))#忘记密码方式获取随机生成密码
    # print(add_allroles_employees(to_register(phone,password,1)[0],'111111','111111'))#创建员工
    # print(add_allroles_employees(to_register(phone,password,1)[0],'111111','111111'))#创建员工
    # print(add_allroles_employees(to_register(phone,password,2)[0],'111111','111111'))#创建员工
    # print(add_allroles_employees(to_register(phone,password,3)[0],'111111','111111'))#创建员工
    # print(add_allroles_employees('14567285398','111111','111111'))#创建员工

    # updata_user_password('18982402602','111111')
    r.send_msg('15020044445')
    # r.login_session('13630941998','111111')
    print('手机号：',r.get_msg_code()[3])
    print('发送时间：',r.get_msg_code()[2])
    print('验证码：',r.get_msg_code()[0])
    print('短信密码：',r.get_msg_code()[1])
