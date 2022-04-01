import tkinter
from pose_accuracy_repeatability import *
import win32api
import win32con

class menuBar():
    def __init__(self, win):
        self.productInfo = r'.\productInfo.txt'
        self.menubar = tkinter.Menu(win)
        self.menu_set = tkinter.Menu(self.menubar, tearoff=False)
        #产品信息设置
        menu_pInfo = tkinter.Menu(self.menubar, tearoff=False)
        menu_pInfo.add_command(label='产品信息设置', command=self.infoInput)
        self.menubar.add_cascade(label='产品信息设置', menu=menu_pInfo)
        # 导出结果菜单
        menu_export = tkinter.Menu(self.menubar, tearoff=False)
        menu_export.add_command(label='导出为Excel', command=self.outputExcel)
        menu_export.add_command(label='导出为PDF', command=self.outputPDF)
        menu_export.add_command(label='导出为txt', command=self.outputTxT)
        self.menubar.add_cascade(label='结果导出', menu=menu_export)
        # 关于菜单
        menu_about = tkinter.Menu(self.menubar, tearoff=False)
        menu_about.add_command(label='关于', command=self.abouts)
        self.menubar.add_cascade(label='关于', menu=menu_about)
        win.config(menu=self.menubar)
    #产品信息输入
    def infoInput(self):
        x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
        y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
        place_x = str(int(x/3))
        place_y = str(int(y/3))
        win_info = tkinter.Tk()
        win_info.title('产品信息录入')
        win_info.geometry('+'+place_x+'+'+place_y)
        
        label1 = Label(win_info, text='爱啥啥：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)

        input1 = StringVar(win_info, value='林北没弄')
        entry1 = Entry(win_info, font=('GB2312', 18), fg='Plum',
                       textvariable=input1
                       )
        entry1.grid(row=0, column=1)
        button1 = Button(win_info, text='确定', width=10,
                         font=('GB2312', 18),
                         background='Tan')
        button1.grid(row=1, column=0, columnspan=2,
                     sticky=E+W)

        win_info.mainloop()
    #导出Excel,后续可添加
    def outputExcel(self):
        x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
        y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
        place_x = str(int(x/3))
        place_y = str(int(y/3))
        win_excel = tkinter.Tk()
        win_excel.title('结果导出为Excel')
        win_excel.geometry('+'+place_x+'+'+place_y)
        
        label1 = Label(win_excel, text='林北没弄', font=('GB2312', 16), fg='SteelBlue')
        label1.pack()

        win_excel.mainloop()
    #导出PDF，后续可添加
    def outputPDF(self):
        x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
        y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
        place_x = str(int(x/3))
        place_y = str(int(y/3))
        win_pdf = tkinter.Tk()
        win_pdf.title('结果导出为Excel')
        win_pdf.geometry('+'+place_x+'+'+place_y)
        
        label1 = Label(win_pdf, text='林北也没弄', font=('GB2312', 16), fg='SteelBlue')
        label1.pack()

        win_pdf.mainloop()
    #导出txt，后续可添加
    def outputTxT(self):
        x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
        y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
        place_x = str(int(x/3))
        place_y = str(int(y/3))
        win_txt = tkinter.Tk()
        win_txt.title('结果导出为Excel')
        win_txt.geometry('+'+place_x+'+'+place_y)
        
        label1 = Label(win_txt, text='林北还是没弄', font=('GB2312', 16), fg='SteelBlue')
        label1.pack()

        win_txt.mainloop()
    #关于
    def abouts(self):
        x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
        y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
        place_x = str(int(x/3))
        place_y = str(int(y/3))
        win_ab = tkinter.Tk()
        win_ab.title('关于')
        win_ab.geometry('+'+place_x+'+'+place_y)
        
        label1 = Label(win_ab, text='注意事项：\n1.使用该软件计算性能测试结果需要将测得的数据文件\n  '
                        '放在桌面上，具体文件夹的设置在每个测试项目的弹窗文件中有详细内容。\n'
                        '2.画图功能和结果筛选导出功能，产品信息录入功能还未完善。\n'
                        '3.若文件选择错误则不会进行计算，待以后增加报错提示。'
                        , font=('GB2312', 16), fg='SteelBlue', justify=tkinter.LEFT)
        label1.pack()

        win_ab.mainloop()
    




