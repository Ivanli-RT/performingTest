import tkinter
import win32api
import win32con
import os
import mainWindow
from menuBar import *
import multiprocessing

x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
 
width_w = str(int(2*x/3))
height_w = str(int(2*y/3))
place_x = str(int(x/4))
place_y = str(int(y/5))
pathred = r'.\refreshd.txt'

#刷新页面
def refresh():
    with open(pathred, 'r') as ref:
        sign=ref.read()
    ref.close()
    if sign == '1':      
        with open(mw.pathData, 'r') as d:
            viewd = d.read()
        mw.data.delete(0.0, END)
        mw.data.insert(INSERT, viewd)
        mw.data.update()
        d.close()
        with open(mw.pathResult, 'r') as r:
            viewr = r.read()
        mw.result.delete(0.0, END)
        mw.result.insert(INSERT, viewr)
        mw.result.update()
        r.close()
        with open(pathred, 'a+') as ref:
            ref.truncate(0)
            ref.write('0')
            ref.flush()
            ref.close()
    win.after(100, refresh)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    win = tkinter.Tk()   #绑定窗口
    win.title('机器人性能测试')   #设置窗口标题
    win.geometry('+'+place_x+'+'+place_y)   #确定窗口尺寸width_w+'x'+height_w+
    menuBar = menuBar(win)  #引入菜单栏
    #实例化主界面类
    mw = mainWindow.mainWindows(win, width_w, height_w)
    mw.contents()
    mw.results()
    mw.commands()
    mw.datas()
    #刷新页面
    win.after(100, refresh)

    win.mainloop()

