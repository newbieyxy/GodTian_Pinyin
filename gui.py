# -*- coding:utf-8 -*-
# from Tkinter import * # origin
import tkinter
from tkinter.constants import *
import re
# from GodTian_Pinyin import GodTian_Pinyin
from Pinyin2Hanzi import Pinyin2Hanzi


def shift(event):
    canv.focus_set()


def update():
    global display
    canv.delete(id)
    input.delete('0.0', END)
    display = [str(j + 1) + i for j, i in
               enumerate(result[5 * (page - 1):5 * page if len(result) > 5 * page else len(result)])]
    input.insert(END, "\t".join(display))
    return canv.create_text(20, 50, text=input.get("0.0", END), anchor=W, width=300)


def shurufa(event):
    command = event.keysym # check the ket event
    m1 = re.match(r'[a-zA-Z\']', event.char)   # True / False，包括小写和大写字母以及分隔符
    m2 = re.match(r'\d',event.char)
    global py, result, a, id, page, display
    if m1:  # 输入的字母
        print("command is pinyin")
        py.append(m1.group())
        
        py_str = "".join(py)
        var.set("".join(py))
        if "".join(py) not in py2hz.cache:
            hz = py2hz.handle_current_input(py_str, 15, 15)
            py2hz.cache["".join(py)] = hz
        else:
            hz = py2hz.cache["".join(py)]
        # hz, two_part = godtian.handle_current_input("".join(py), 15, 5)
        #result = ["".join(i.path) for _, i in enumerate(hz)]
        result = ["".join(i.path) for i in hz]
        id = update()

    # elif command == 'Return':
    #     print("command is Return!")
    #     py_str = "".join(py)
    #     if len(py) > 0:
    #         if "".join(py) not in py2hz.cache:
    #             hz, two_part = py2hz.handle_current_input(py_str, 15, 15)
    #             py2hz.cache["".join(py)] = hz
    #         else:
    #             hz = py2hz.cache["".join(py)]
    #         # hz, two_part = godtian.handle_current_input("".join(py), 15, 15)
    #         result = ["".join(i.path) for _, i in enumerate(hz)]
    #         id = update()

    elif command == "Down":
        if len(result)> page*5:
            page+=1
            id = update()

    elif command == "Up":
        if page > 1:
            page -= 1
            id = update()

    elif command == 'BackSpace':
        if len(py) > 0:
            py.pop(-1)
            var.set("".join(py))
            if "".join(py) not in py2hz.cache:
                hz = py2hz.handle_current_input("".join(py), 15, 15)
                py2hz.cache["".join(py)] = hz
            else:
                hz = py2hz.cache["".join(py)]
            result = ["".join(i.path) for j, i in enumerate(hz)]
            id = update()
    elif command in ['F5']:
        py2hz.save_memo_and_cache()

    elif command == 'space':
        if len(py) > 0:
            num = 1
            if len(display) >= num:
                var.set("")
                text.insert(END, display[num - 1][1:])
                display = []
                py = []
                result = []
                canv.delete(id)
    elif m2:
        num = int(event.char)
        if len(display) >= num:
            var.set("")
            text.insert(END, display[num-1][1:])
            display = []
            py = []
            result = []
            canv.delete(id)
    else:
        pass

if __name__ == '__main__':
    id=-1
    page=1
    py=[]
    result = []
    display=[]
    # godtian = GodTian_Pinyin()
    py2hz = Pinyin2Hanzi()
    # root = Tk()
    root = tkinter.Tk()
    root.title("输入法")
    #root.geometry('300x200')
    var = tkinter.StringVar()


    # text=Text(root,yscrollcommand=1)
    text=tkinter.Text(root,yscrollcommand=1)
    text.pack(side=BOTTOM, expand=YES, fill=X)
    text.bind("<Shift_L>",shift)

    # label=Label(root, textvariable=var)
    label=tkinter.Label(root, textvariable=var)
    label.pack(side=TOP, fill=X)
    
    # canv = Canvas(root, width=400, height=100)
    canv = tkinter.Canvas(root, width=150, height=50)
    canv.pack(side=TOP, expand=YES, fill=X)

    # input = Text(canv)
    input = tkinter.Text(canv)
    canv.focus_set()
    canv.bind("<Key>", shurufa)
    root.mainloop()
