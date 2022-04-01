import win32api
import win32con
import os
import tkinter

class dataSavesDel():
    def __init__(self):
        self.outPutChache = r'.\outputchache.txt'
        self.pathResult = r'.\result.txt'
    #保存结果
    def dataSave(self):
        r = open(self.pathResult, 'r')
        dataStr = r.read()
        r.close()

        o = open(self.outPutChache, 'a+')
        o.write(dataStr)
        o.close()
    #清楚结果
    def dataDelete(self):
        x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
        y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
        place_x = str(int(x/3))
        place_y = str(int(y/3))
        win_delete = tkinter.Tk()
        win_delete.title('数据筛选或删除')
        win_delete.geometry('+'+place_x+'+'+place_y)

        selcet_delete = tkinter.IntVar()
        radio1 = tkinter.Radiobutton(win_delete, text='林北还没弄', value=1, variable=selcet_delete)#, command=updata)
        radio1.pack()

        button_alld = tkinter.Button(win_delete, text='清除所有结果', 
                                    command=self.clearresult)
        button_alld.pack()
        button_d = tkinter.Button(win_delete, text='删除所选结果')
        button_d.pack()

        win_delete.mainloop()

    #清空结果
    def clearresult(self):
        f = open(self.outPutChache, 'a+')
        f.truncate(0)
        f.close()