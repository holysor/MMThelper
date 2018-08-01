from tkinter import *

root = Tk()
e = StringVar()


def validateText():
    val = entry.get()
    if val == '654321':
        print("正确!")
        return True
    else:
        ''''' 
        删除内容,-- 删除参数 first 到 last 范围内（包含 first 和 last）的所有内容 
        -- 如果忽略 last 参数，表示删除 first 参数指定的选项 
        -- 使用 delete(0, END) 实现删除输入框的所有内容 
       '''
        entry.delete(0, END)
        print('invalidcommand:我被调用了')
        return False


def test():
    print('invalidcommand:我被调用了')
    return True


entry = Entry(root, textvariable=e, validate='focusout', validatecommand=validateText)
entry.pack()
Entry(root, text='sure').pack()
root.mainloop()