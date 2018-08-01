import requests
import hashlib
from RedPacket import config
import random

def md5(key):
    '''MD5加密'''
    m = hashlib.md5()
    m.update(key.encode("UTF-8"))
    return m.hexdigest()



def login_session(user,password):
    '''登录账号，获取session'''

    session = requests.Session()
    data = {
        'scope': 'person',
        'personPassword': md5(password),
        'personLoginOrMobile': user
    }
    url_login = config.host + '/gateway/login/checkLogin'
    session.post(url_login, data=data)
    return session

def invite_person(session,type=1,flag=1):
    url = config.host + '/gateway/user/baseinfoPersonCompanyOrgReadRpcService/queryInviteCompPerson'
    params = {
        'type':type,
        'flag':flag
    }
    res = session.get(url,params=params)
    return res.json()

def send_register_code(session,mobile,code):
    url = config.host+ '/gateway/user/baseinfoPersonCompanyOrgReadRpcService/sendRegisterMobileCode'
    data = {
        'mobile': mobile,
        'type': 'register',
        'requestCode': code,
        'typeFlag': 1
    }
    res = session.post(url,data=data)
    return res.json()

def get_company_typelist():
    '''获取业务类型'''
    url = config.host+'/gateway/company/sysCompanyTypeRpcService/queryAllSysCompanyType'
    res = requests.get(url)
    return res.json()

def get_business_category():
    '''获取经营类目'''
    url = config.host+'/gateway/item/sysGoodsCategoryRpcService/findFirstLevelGoodsCategoryList/ddfbc6fad4cb40be8fb95a97a972a1dc'
    res = requests.get(url)
    return res.json()

def register_person(data):
    '''被邀请者注册账号'''
    url = config.host+'/gateway/user/baseinfoPersonCompanyOrgWriteRpcService/invitePerson'
    data = data
    res = requests.post(url,data=data)
    return res.json()
def sys_admin_login(mobile,pwd):
    '''运营后台-资费管理员登录'''
    session = requests.Session()

    url = config.adm_host + '/gateway/login/checkLogin'
    data = {
        'personLoginOrMobile':mobile,
        'personPassword':md5(pwd),
        'scope': 'sys'
    }
    session.post(url,data)
    return session
def charge_members(session,data):
    '''资费管理员-为被邀请者添加付费成为会员'''

    url = config.adm_host+'/gateway/company/orderCompanyJournalWriteRpcService/addOrderCompanyJournal'
    data =data
    res = session.post(url,data=data)
    return res.json()

def auditing_members(session,data):
    '''资费管理员-审核被邀请者付费成为会员'''
    url = config.adm_host+'/gateway/company/orderCompanyJournalWriteRpcService/passReviewOrder'
    data = data
    res = session.post(url,data=data)
    return res.json()

def get_company_id(mobile,pwd):
    '''获取企业ID'''
    data = {
        'scope': 'person',
        'personPassword': md5(pwd),
        'personLoginOrMobile': mobile
    }
    url = config.host+'/gateway/login/checkLogin'
    res = requests.post(url, data=data)
    return res.json()['module']['compId']


if __name__=='__main__':
    # login_session(config.user['mobile'],'111111')
    # sys_admin_login('15221685494','111111')
    id=get_company_id('15956080837','111111')
    print(id)