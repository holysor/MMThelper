import requests
from RedPacket import api
from RedPacket import config
import threading
import random
import time
import string
from concurrent.futures import ThreadPoolExecutor,wait, ALL_COMPLETED, FIRST_COMPLETED

class RedPacket(object):
    def __init__(self,user,password,wm_text):
        self.mobile = user
        self.password = password
        self.host = config.host
        self.session = api.login_session(self.mobile,self.password)
        self.wm_text = wm_text
        self.inviteuser_pass = []
        self.inviteuser_fail = []
    def random_number(self,len):
        '''生成设定长度的随机数'''
        random_char_list = []
        for _ in range(len):
            random_char = random.choice(string.digits)
            random_char_list.append(random_char)
        random_string = ''.join(random_char_list)
        return random_string

    def get_currentdate(self):
        '''获取当前时间节点'''
        date = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())  # 当前时间格式2018-07-31 09:37:00
        return date


    def wm_insert_text(self,wm_text,value):
        if wm_text:
            wm_text.config(state='normal')
            wm_text.insert('end', value)
            wm_text.config(state='disabled')
            wm_text.see('end')

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

    def add_charge_user(self,mobile):
        '''被邀请者添加付费'''
        data = {
            'sourceOrderNo': 'FW'+self.random_number(12),
            'payTime': self.get_currentdate(),
            'payPersonLogin': "alipay@alipay.com",
            'payPersonName': 'tester',
            'payType': 4,
            'payMoney': 58800,
            'compId': api.get_company_id(mobile,'111111'),
            'payContent': '使用权365天'
        }

        user = config.user_administrator['mobile']
        pwd = config.user_administrator['password']
        try:
            session_adm = api.sys_admin_login(user, pwd)
        except:
            print('资费管理员登录失败：%s-%s\n' % (user, pwd))
            self.wm_insert_text(self.wm_text,'资费管理员登录失败：%s-%s\n' % (user, pwd))

            return
        try:
            res = api.charge_members(session_adm, data)
            orderid = res['module']['orderId']
            if not res['success']:
                assert False
            # print('客户:%s,添加付费成功！\n' % (mobile))
        except:
            print('客户:%s,添加付费失败，请检查！\n'%(mobile))
            self.wm_insert_text(self.wm_text,'客户:%s,添加付费失败，请检查！\n'%(mobile))
            return
        user1 = config.user_auditor['mobile']
        pwd1 = config.user_auditor['password']
        try:
            session_auditor = api.sys_admin_login(user1, pwd1)
        except:
            print('资费审核员登录失败：%s-%s\n' % (user1, pwd1))
            self.wm_insert_text(self.wm_text,'资费审核员登录失败：%s-%s\n' % (user1, pwd1))

            return
        try:
            data = {
                'orderId':orderid,
                'version':'0'
            }
            res = api.auditing_members(session_auditor, data)
            if not res['success']:
                assert False
            # print('客户:%s,审核收费成功！\n' % (mobile))
        except:
            print('客户:%s,审核收费失败，请检查！\n'%(mobile))
            self.wm_insert_text(self.wm_text,'客户:%s,审核收费失败，请检查！\n'%(mobile))
            return
    def get_success_inviteuser(self):
        '''返回邀请成功的用户列表'''
        return self.inviteuser_pass
    def get_fail_inviteuser(self):
        '''返回邀请注册失败的用户列表'''
        return self.inviteuser_fail

    def run_packet(self):
        request_code = api.invite_person(self.session)['module'].get('requestCode')#获取邀请者的邀请码
        mobile = self.random_mobile()#随机生成号码
        api.send_register_code(self.session,mobile,request_code)#注册发送验证码
        ct_id = api.get_company_typelist()['module'][1]['ctId']#获取业务类型：一批
        business_category = ','.join([str(i['gcId']) for i in api.get_business_category()['module']])#获取经营类目
        #注册账号，POST传参
        data = {
            'personPwd': api.md5('111111'),
            'registType':2,
            'mobile': mobile,
            'mobileCode': '123456',
            'ctId': ct_id,
            'ctName': '二级批发商',
            'businessCategory': business_category,
            'channel': 'website',
            'requestCode': request_code,
            'userId':'',
            'type':1
        }
        try:
            register_res = api.register_person(data)#注册账号
            if not register_res['success']:
                assert False
            print('邀请客户:%s,注册成功！\n'%(mobile))
            self.inviteuser_pass.append(mobile)
            # self.wm_insert_text(self.wm_text,'邀请客户:%s,注册成功！\n'%(mobile))
        except:
            print('邀请客户:%s,注册失败！\n' % (mobile))
            self.inviteuser_fail.append(mobile)
            self.wm_insert_text(self.wm_text,'邀请客户:%s,注册失败！\n' % (mobile))
            return
        try:
            self.add_charge_user(mobile)  # 被邀请者付费
        except:
            print('被邀请者:%s,运营平台管理员付费及审核流程失败！\n'%(mobile))
            self.wm_insert_text('被邀请者:%s,运营平台管理员付费及审核流程失败！\n'%(mobile))

    def work_thread_redpacket(self,total):
        executor = ThreadPoolExecutor(max_workers=20)
        all_task = []
        for _ in  range(total):
           all_task.append(executor.submit(self.run_packet))
        wait(all_task,return_when=ALL_COMPLETED)

if __name__=='__main__':
    rp = RedPacket()
    # rp.work_thread_redpacket(30)
    rp.run_packet()
