from tkinter import *
from tkinter import messagebox
from tkinter import font
from register import Register


class login(Toplevel):
    def __init__(self,parent):
        self.parent = parent
        super(login, self).__init__()
        self.title('登录账号')
        self.__set_login_window()
        self.grab_set()


    def __set_login_window(self):
        self.__set_window_center()

    def __set_window_center(self):
        '''设置窗口居中于父窗口'''
        # self.wm_transient(self.parent)
        popup_width = 300
        popup_height = 300
        self.resizable(1, 1)
        self.attributes('-alpha', 0.9)

        root_x = self.parent.winfo_x()
        root_y = self.parent.winfo_y()
        root_width = self.parent.winfo_width()
        root_height = self.parent.winfo_height()

        set_x = int(int(root_x) + (root_width / 2) - popup_width / 2)
        set_y = int(int(root_y) + (root_height / 2) - popup_height / 2)
        self.geometry('%sx%s+%s+%s' % (popup_width, popup_height, set_x, set_y))
        # self.popup.geometry('%sx%s+%s+%s'%(self.popup_width,self.popup_height,set_x,set_y))
        self.wm_attributes("-topmost", 1)

if __name__ == '__main__':
    root = Tk()
    work = login(root)
    root.mainloop()