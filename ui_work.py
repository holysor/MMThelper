from tkinter import *
from tkinter import messagebox
from tkinter import font
from register import Register

# from faker import Factory
import time
import webbrowser
import threading
import re
from multiprocessing.pool import ThreadPool


class Thread(threading.Thread):
    def __init__(self,target,*args):
        threading.Thread.__init__(self)
        self.target = target
        self.args =args
    def run(self):
        self.target(*self.args)

    # def __call__(self, *args, **kwargs):
    #     pass


class Thread_employees(threading.Thread):
    def __init__(self,target,*args,**keywords):
        threading.Thread.__init__(self)
        self.target = target
        self.args = args
    def run(self):
        self.value=self.target(*self.args)

class CreateDataUi:
    def __init__(self):
        self.work_complate = True
        self.user_mobile = ''
        self.user_pwd = '111111'
        self.employee_all_pwd = '111111'
        self.host = 'http://sit.yl9158.com'
        self.root = Tk()
        self.root.withdraw()
        self.root.attributes('-alpha', 0.9)

        self.root.title("B+ 买卖通小助手")
        self.root.resizable(0,0)
        self.set_window_center(480,580)
        self.set_window()
        self.root.protocol("WM_DELETE_WINDOW",self.close_window)
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.mainloop()



    def set_window(self):
        '''设置控件'''
        ft1 = font.Font(self.root,family='楷体', size=16, weight=font.BOLD)
        ft2 = font.Font(self.root,family='Arial', size=13,weight=font.BOLD)
        ft3 = font.Font(self.root, size=13)

        frame_lable = Frame(self.root)
        frame_lable.pack(side=TOP,fill=BOTH)
        self.label = Label(frame_lable, text='买卖通小助手')
        self.label.configure(width=10, height=1, font=ft1)
        self.label.pack(side=TOP,anchor=CENTER, fill=X)

        fram_entry = Frame(self.root,relief=RAISED,bd=1)
        fram_entry.pack(side=TOP,fill=X)
        self.addr_title = Label(fram_entry,text='测试地址: ')
        self.addr_title.configure(width=10,height=2,font=ft2)
        self.addr_title.pack(side=LEFT,anchor=CENTER,fill=X)
        self.env = StringVar()
        self.env_entry = Entry(fram_entry,textvariable=self.env,font=ft3)#地址
        self.env.set(self.host)
        self.env_entry.pack(side=LEFT,anchor=CENTER,fill=X,expand=YES,ipady=6)
        self.openweb_button = Button(fram_entry,text='打开网址',command=self.open_with_web)
        self.openweb_button.configure(width=8,height=2)
        self.openweb_button.pack(side=LEFT,anchor=CENTER)
        self.reset_button = Button(fram_entry, text='重置',command=self.reset)
        self.reset_button.configure(width=8, height=2)
        self.reset_button.pack(side=LEFT, anchor=CENTER)

        frame_radiobutton = Frame(self.root)
        frame_radiobutton.pack(side=TOP)
        self.var = IntVar()
        self.var.set(1)
        self.radiobutton_1 = Radiobutton(frame_radiobutton,variable=self.var,text='一批账号',value = 1)
        self.radiobutton_2 = Radiobutton(frame_radiobutton,variable=self.var,text='二批账号',value = 2)
        self.radiobutton_3 = Radiobutton(frame_radiobutton,variable=self.var,text='零售账号',value = 3)
        self.radiobutton_1.configure(width=10 ,height=2)
        self.radiobutton_2.configure(width=10, height=2)
        self.radiobutton_3.configure(width=10, height=2)

        self.radiobutton_1.pack(side=LEFT,anchor=CENTER,fill=X,expand=YES)
        self.radiobutton_2.pack(side=LEFT,anchor=CENTER,fill=X,expand=YES)
        self.radiobutton_3.pack(side=LEFT,anchor=CENTER,fill=X,expand=YES)
        #
        frame_list = Frame(self.root,relief=RAISED,bd=1)
        frame_list.pack(side=TOP,fill=BOTH)
        scrollbar = Scrollbar(frame_list)
        scrollbar.pack(side=RIGHT,fill=Y)
        self.text = Text(frame_list,height=30)
        self.text.pack(side=RIGHT,fill=BOTH)
        scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        self.text.bind('<KeyRelease-Down>')
        #底部按钮：注册、查看、清空
        frame_button = Frame(self.root)
        frame_button.pack(side=TOP)
        self.button_1= Button(frame_button,text='注册',command=self.register)
        self.button_employee = Button(frame_button,text='一键生成员工',command=self.create_employee)
        self.button_2 = Button(frame_button,text='查看验证码',command=self.get_msgcode)
        self.claer_button = Button(frame_button,text='清空信息',command=self.clear)
        self.delete_button = Button(frame_button,text='删除账号',command=self.delete_account)
        self.button_1.configure(width=10, height=2)
        self.button_2.configure(width=10, height=2)
        self.button_employee.configure(width=10, height=2)
        self.claer_button.configure(width=10,height=2)
        self.delete_button.configure(width=10,height=2)
        self.button_1.pack(side=LEFT,anchor=CENTER,fill=X,expand=YES)
        self.button_employee.pack(side=LEFT, anchor=CENTER, fill=X, expand=YES)
        self.button_2.pack(side=LEFT,anchor=CENTER,fill=X,expand=YES)
        self.claer_button.pack(side=LEFT, anchor=CENTER, fill=X, expand=YES)
        self.delete_button.pack(side=LEFT, anchor=CENTER, fill=X, expand=YES)


    def set_text(self,types=1):
        '''文本框，显示信息'''
        value = self.get_account(types)
        success = value[1]
        self.text.config(state=NORMAL)
        self.text.insert(END,'\n'+value[0])
        index2 = float(self.text.index(INSERT)) - 2.0
        if success:
            self.text.tag_add('success',index2-2,index2+1)
            self.text.tag_config('success', foreground='green')
        else:
            self.text.tag_add('fail', index2-1,index2+2)
            self.text.tag_config('fail', foreground='red')

        self.text.tag_add('number',str(index2+0.3),str(index2+0.14),str(index2+0.18),str(index2+0.24))
        self.text.tag_config('number',foreground='blue',underline=True)
        self.text.tag_config('number',foreground='blue',underline=True)
        self.text.tag_bind('number','<Enter>',lambda enter:self.text.config(cursor='hand2'))
        self.text.tag_bind('number','<Leave>',lambda leave:self.text.config(cursor='xterm'))
        self.text.config(state=DISABLED)
        print(self.text.get(1.0,END))
        self.text.see(END)

    def register(self):
        '''注册'''
        select_value = self.var.get()
        self.set_text(select_value)

    def create_employee(self):
        '''创建员工'''

        self.popup = Toplevel(self.root)
        self.popup.wm_transient(self.root)
        self.popup_width = 300
        self.popup_height = 300
        self.popup.resizable(0,0)
        self.popup.attributes('-alpha', 0.9)

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        set_x = int(int(root_x)+(root_width/2)-self.popup_width/2)
        set_y = int(int(root_y)+(root_height/2)-self.popup_height/2)
        self.popup.geometry('%sx%s+%s+%s'%(self.popup_width,self.popup_height,set_x,set_y))
        self.popup.wm_attributes("-topmost", 1)
        self.popup.title('添加员工')
        msg = Message(self.popup,text='\n  *为企业超级管理员添加所有角色的员工*\n\n',width = self.popup_width-20)
        msg.pack(side=TOP,fill=X)
        frame_user = Frame(self.popup)
        frame_user.pack(side=TOP)
        user_label = Label(frame_user,text='企业老板账号:')
        user_label.pack(side=LEFT,fill=X)
        self.user = StringVar()
        user_entry = Entry(frame_user,textvariable=self.user,text=self.user,validate='focusout',validatecommand=lambda:self.validateText('user'))
        user_entry.pack(side=LEFT,ipady=5)
        self.user.set(self.user_mobile)
        self.user_error_msg = StringVar()
        self.user_error = Message(self.popup,textvariable=self.user_error_msg,width=100)
        self.user_error.pack(side=TOP)

        frame_password = Frame(self.popup)
        frame_password.pack(side=TOP)
        password_label = Label(frame_password, text='企业老板密码:')
        password_label.pack(side=LEFT, fill=X)
        self.password = StringVar()
        self.password_error_msg = StringVar()
        self.employee_error_msg = StringVar()
        self.password_error = Message(self.popup, textvariable=self.password_error_msg,width=150)
        self.employee_error = Message(self.popup, textvariable=self.employee_error_msg,width=150)

        password_entry = Entry(frame_password, textvariable=self.password,validate='focusout', validatecommand=lambda :self.validateText('pwd'))
        password_entry.pack(side=LEFT, ipady=5)
        self.password.set(self.user_pwd)
        #企业密码错误信息
        self.password_error.pack(side=TOP)
        frame_employee = Frame(self.popup)
        frame_employee.pack(side=TOP)
        employee_label = Label(frame_employee, text='员工初始密码:')
        employee_label.pack(side=LEFT,expand=YES)
        self.employee_pwd = StringVar()
        employee_entry = Entry(frame_employee, textvariable=self.employee_pwd,text=self.employee_pwd,validate='focusout', validatecommand=lambda :self.validateText('e_pwd'))
        employee_entry.pack(side=LEFT, ipady=5)
        self.employee_pwd.set(self.employee_all_pwd)
        self.employee_error.pack()

        frame_button = Frame(self.popup)
        frame_button.pack(side=TOP,pady=10)
        sure_button = Button(frame_button,text='确认',command=self.popup_work)
        sure_button.configure(width=10,height=2)
        sure_button.pack(side=LEFT)
        clear_button = Button(frame_button, text='清空', command=self.clear_all_data)
        clear_button.configure(width=10, height=2)
        clear_button.pack(side=LEFT)
        self.popup.grab_set()



    def validateText(self,v_type):
        '''验证输入框'''
        flag =True
        if v_type=='user':
            value = self.user.get().strip()
            if value.isdigit() and len(value)==11:
                print('手机号正常')
                self.user_error_msg.set('手机号正确')
                self.user_error.configure(foreground='green')
                flag =True
            else:
                print('手机号错误')
                self.user_error_msg.set('手机号错误')
                self.user_error.configure(foreground='red')
                flag=False
        elif v_type=='pwd':
            value = self.password.get().strip()
            if len(value)>=6 and len(value)<=18:
                print('密码正常')
                self.password_error_msg.set('密码正常')
                self.password_error.configure(foreground='green')
                flag =True
            else:
                print('密码长度应在6~18之间——1')
                self.password_error_msg.set('密码长度应在6~18之间')
                self.password_error.configure(foreground='red')
                flag=False
        elif v_type=='e_pwd':
            value = self.employee_pwd.get().strip()
            if len(value)>=6 and len(value)<=18:
                self.employee_error_msg.set('密码正常')
                self.employee_error.configure(foreground='green')
                flag =True
            else:
                print('密码长度应在6~18之间--2')
                self.employee_error_msg.set('密码长度应在6~18之间')
                self.employee_error.configure(foreground='red')
                flag=False
        return flag

    def valida_all_input(self):
        '''检查所有输入框的值'''
        a= self.validateText('user')
        b= self.validateText('pwd')
        c=self.validateText('e_pwd')
        print(a,b,c)
        if a and b and c:
            return True
        else:
            return False

    def clear_all_data(self):
        '''清空输入框所有数据'''
        self.user.set('')
        self.password.set('')
        self.employee_pwd.set('')

    def popup_work(self):
        '''添加员工'''
        if not self.valida_all_input():
            self.popup.update()
            return
        self.host = self.env_entry.get()
        register = Register(self.host)
        self.user_mobile = self.user.get()
        self.user_pwd = self.password.get()
        self.employee_all_pwd = self.employee_pwd.get()
        self.insert_text('\n开始添加员工，等待完成...\n\n')

        work_thread = Thread(register.add_allroles_employees,self.user_mobile,self.user_pwd,self.employee_all_pwd,self.text)
        work_thread.setDaemon(True)
        work_thread.start()
        check_work = Thread(self.check_work_finish,work_thread)
        check_work.setDaemon(True)
        check_work.start()
        self.popup.destroy()
        # pool = ThreadPool(processes=1)
        # pool_result = pool.apply_async(register.add_allroles_employees,(self.user_mobile,self.user_pwd,self.employee_all_pwd,self.text))

    def check_work_finish(self, work):
        while work.is_alive():
            self.button_employee['state'] = DISABLED
        self.button_employee['state'] = NORMAL

    def reset(self):
        '''重置'''
        self.env.set('http://sit.yl9158.com')

    def insert_text(self,value):
        '''Text 插入数据'''
        self.text.config(state=NORMAL)
        self.text.insert(END,value)
        self.text.config(state=DISABLED)
        self.text.see(END)

    def delete_account(self):
        '''删除账号'''
        flag = messagebox.askokcancel('提示', '删除账号？')
        if flag:
            self.text.config(state=NORMAL)
            # self.text.delete(1.0, END)
            self.text.insert(END,'\n删除成功!\n')
            self.text.config(state=DISABLED)

    def get_msgcode(self):
        '''获取验证码'''
        self.host = self.env.get().strip()
        print(self.host)
        try:
            register = Register(self.host)
            self.text.config(state=NORMAL)
            results = register.get_msg_code()
            sendtime = str(results[2])[:4] + '.' +str(results[2])[4:6]+'.'+str(results[2])[6:8]+' '+str(results[2])[8:10]+':'+str(results[2])[10:12]+':'+str(results[2])[12:]
            self.text.insert(END,'手机号：%s\n'%results[3] )
            self.text.insert(END,'发送时间：%s\n'%sendtime )
            self.text.insert(END,'验证码：%s\n'%results[0] )
            self.text.insert(END,'短信密码：%s\n\n'%results[1] )
            self.text.see(END)
            index = float(self.text.index(INSERT)) - 1.0
            self.text.tag_add('code',index-4,index)
            self.text.tag_config('code', foreground='blue')
            self.text.config(state=DISABLED)
        except:
            self.text.insert(END,'\n查看验证码失败!\n\n' )
            self.text.see(END)
            index = float(self.text.index(INSERT))
            self.text.tag_add('code1', index-2,index+1)
            self.text.tag_config('code1', foreground='red')
            self.text.config(state=DISABLED)

    def open_with_web(self):
        self.host = self.env.get()
        webbrowser.open(self.host)

    def get_account(self,type):
        '''创建账号，返回账号信息'''
        register = Register(self.host)
        phone = register.random_mobile()
        password = '111111'
        yewu = {
            1: '一级批发商',
            2:'二级批发商',
            3:'零售商'
        }
        sucess = True
        try:
            work_thread = Thread(register.to_register,phone,password,type)
            work_thread.setDaemon(True)
            work_thread.start()
            text_info = '注册成功!\n业务类型:%s\n账号:%s,密码:%s\n\n'%(yewu[type],phone,password)
        except:
            text_info = '%s账号注册失败!\n\r'%phone
            sucess =False
        return text_info,sucess

    def clear(self):
        flag = messagebox.askokcancel('提示','清楚记录？')
        if flag:
            self.text.config(state=NORMAL)
            self.text.delete(1.0,END)
            self.text.config(state=DISABLED)

    def close_window(self):
        flag = messagebox.askokcancel('提示','确定关闭？')
        if flag:
            self.root.destroy()

    def get_screen_size(self):
        '''获取winodws屏幕尺寸'''
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        return screen_width,screen_height

    def set_window_center(self,width,height):
        '''设置窗口居中显示'''
        screenwidth = self.get_screen_size()[0]
        screenheight = self.get_screen_size()[1]
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(size)
        self.root.deiconify()


if __name__=='__main__':
    run = CreateDataUi()
