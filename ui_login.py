from tkinter import *
from tkinter import messagebox
import register
import ui_work
import time

class LoginStart(Tk):
    def __init__(self):
        self.host = 'https://www.yl9158.com'
        super(LoginStart, self).__init__()
        self.title('登录账号')
        self.width = 300
        self.height = 300
        self.set_window_center(self.width,self.height)
        self.set_window_element()
        self.protocol("WM_DELETE_WINDOW",self.close_window)
        self.mainloop()


    def set_window_element(self):

        msg = Message(self,text='\n  *登录超级管理员账号*\n\n',width = self.width-20)
        msg.pack(side=TOP,fill=X)
        frame_user = Frame(self)
        frame_user.pack(side=TOP)
        user_label = Label(frame_user,text='账号:')
        user_label.pack(side=LEFT,fill=X)
        self.user = StringVar()
        self.user_error_msg = StringVar()
        self.password = StringVar()
        self.password_error_msg = StringVar()
        self.fail_info = StringVar()
        self.password_error = Message(self, textvariable=self.password_error_msg, width=150)
        self.user_error = Message(self, textvariable=self.user_error_msg, width=100)
        self.login_fail = Message(self,textvariable=self.fail_info, width=150)

        user_entry = Entry(frame_user,textvariable=self.user,text=self.user,validate='focusout',validatecommand=lambda:self.validateText('user'))
        user_entry.pack(side=LEFT,ipady=5)
        self.user.set('')
        self.user_error.pack(side=TOP)
        frame_password = Frame(self)
        frame_password.pack(side=TOP)
        password_label = Label(frame_password, text='密码:')
        password_label.pack(side=LEFT, fill=X)


        password_entry = Entry(frame_password, textvariable=self.password,validate='focusout', validatecommand=lambda :self.validateText('pwd'))
        password_entry.pack(side=LEFT, ipady=5)
        self.password.set('')
        #企业密码错误信息
        self.password_error.pack(side=TOP)
        self.login_fail.pack(side=TOP)

        frame_button = Frame(self)
        frame_button.pack(side=TOP,pady=10)
        sure_button = Button(frame_button,text='登录',command=self.login)
        sure_button.configure(width=10,height=2)
        sure_button.pack(side=LEFT)

    def get_screen_size(self):
        '''获取winodws屏幕尺寸'''
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        return screen_width,screen_height

    def set_window_center(self,width,height):
        '''设置窗口居中显示'''
        screenwidth = self.get_screen_size()[0]
        screenheight = self.get_screen_size()[1]
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(size)
        self.deiconify()
    def login(self):
        if not self.valida_all_input():
            self.fail_info.set('登录失败！')
            self.login_fail.configure(foreground='red')
            self.update()
            return
        reg = register.Register(self.host)
        print(self.user.get(),self.password.get())
        try:
            self.fail_info.set('正在登录')
            self.login_fail.configure(foreground='blue')
            self.update()
            time.sleep(3)
            reg.login_session(self.user.get(),self.password.get())
            self.destroy()
            ui_work.CreateDataUi()
        except:
            print('登录失败')
            self.fail_info.set('登录失败！')
            self.login_fail.configure(foreground='red')

    def validateText(self,v_type):
        '''验证输入框'''
        flag =True
        if v_type=='user':
            value = self.user.get().strip()
            if value.isdigit() and len(value)==11:
                # print('手机号正常')
                self.user_error_msg.set('')
                # self.user_error.configure(foreground='green')
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
                self.password_error_msg.set('')
                # self.password_error.configure(foreground='green')
                flag =True
            else:
                print('密码长度应在6~18之间——1')
                self.password_error_msg.set('密码长度应在6~18之间')
                self.password_error.configure(foreground='red')
                flag=False
        elif v_type=='e_pwd':
            value = self.employee_pwd.get().strip()
            if len(value)>=6 and len(value)<=18:
                # self.employee_error_msg.set('密码正常')
                # self.employee_error.configure(foreground='green')
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
        print(a,b)
        if a and b:
            return True
        else:
            return False

    def close_window(self):
        flag = messagebox.askokcancel('提示','确定关闭？')
        if flag:
            self.destroy()


if __name__ == '__main__':
    work = LoginStart()
