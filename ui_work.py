from tkinter import *
from tkinter import messagebox
from tkinter import font
from register import Register
# from faker import Factory
import time
import webbrowser
import threading

class Thread(threading.Thread):
    def __init__(self,target,args):
        threading.Thread.__init__(self)
        self.target = target
        self.args =args
    def run(self):
        self.target(self.args)

class CreateDataUi:
    def __init__(self):

        self.address_mmt = 'https://www.yl9158.com/enterprise/mmt/index.htm#/account/'
        self.root = Tk()
        self.root.withdraw()
        self.root.title("B+ 买卖通小助手")
        self.root.resizable(0,0)
        self.set_window_center(450,230)
        self.set_window()
        self.root.protocol("WM_DELETE_WINDOW",self.close_window)
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.mainloop()

    def set_window(self):
        '''设置控件'''
        ft1 = font.Font(family='Arial', size=15, weight=font.BOLD)


        frame_button = Frame(self.root)
        self.button_1 = Button(frame_button,text='一批账号',command=lambda:self.set_text(1))
        self.button_2 = Button(frame_button,text='二批账号',command=lambda:self.set_text(2))
        self.button_3 = Button(frame_button,text='零售账号',command=lambda:self.set_text(3))
        self.claer_button = Button(frame_button,text='清空',command=self.clear)

        self.button_1.configure(width=10 ,height=2)
        self.button_2.configure(width=10, height=2)
        self.button_3.configure(width=10, height=2)
        self.claer_button.configure(width=10,height=2,)

        self.button_1.pack(side=TOP,anchor=CENTER,fill=X,expand=YES)
        self.button_2.pack(side=TOP,anchor=CENTER,fill=X,expand=YES)
        self.button_3.pack(side=TOP,anchor=CENTER,fill=X,expand=YES)
        self.claer_button.pack(side=TOP, anchor=CENTER, fill=X, expand=YES)

        frame_button.pack(side=LEFT)
        frame_list = Frame(self.root,relief=RAISED,bd=1)
        frame_list.pack(fill=BOTH)
        scrollbar = Scrollbar(frame_list)
        scrollbar.pack(side=RIGHT,fill=Y)
        self.label = Label(frame_list,text='买卖通超级管理员')
        self.label.configure(width=5,height=2,font=ft1)

        self.label.pack(side=TOP,anchor=CENTER,fill=X,expand=YES)
        self.text = Text(frame_list,height=40)
        self.text.pack(side=RIGHT,fill=BOTH)
        scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)

    def set_text(self,types=1):
        '''文本框，显示号码信息'''
        value = self.get_account(types)
        success = value[1]
        self.text.config(state=NORMAL)
        self.text.insert(END,'B+ 买卖通地址[点击打开]\n')
        index1 = float(self.text.index(INSERT))-1.0
        self.text.tag_add('link',str(index1+0.9),str(index1+0.13))
        self.text.tag_config('link',foreground='blue',underline=True)
        self.text.tag_bind('link','<Button-1>',lambda web:webbrowser.open(self.address_mmt))
        self.text.tag_bind('link','<Enter>',lambda enter:self.text.config(cursor='hand2'))
        self.text.tag_bind('link','<Leave>',lambda leave:self.text.config(cursor='xterm'))
        self.text.insert(END,value[0])

        if success:
            self.text.configure(foreground='green')
        else:
            self.text.configure(foreground='red')
        index2 = float(self.text.index(INSERT))-2.0
        self.text.tag_add('number',str(index2+0.3),str(index2+0.14),str(index2+0.18),str(index2+0.24))
        self.text.tag_config('number',foreground='blue',underline=True)
        self.text.config(state=DISABLED)
        print(self.text.get(1.0,END))
        self.text.see(END)

    def get_account(self,type):
        '''创建账号，返回账号信息'''
        host = 'https://www.yl9158.com'
        register = Register(host)
        phone = register.random_mobile()
        password = '111111'
        yewu = {
            1: '一级批发商',
            2:'二级批发商',
            3:'零售商'
        }
        sucess = True
        try:
            # register.to_register(phone,password,type)#注册新账号
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

    def dialog(self):
        self.top = Toplevel(self.root)
        Label(self.top,text='清空数据').pack()
        self.entry = Entry(self.top)
        self.entry.pack(padx=5)
        b = Button(self.top,text='确认',command=lambda:self.top.destroy())
        b.pack(pady=5)

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
