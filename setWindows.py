from tkinter import *
import win32api
import win32con
import os
import pose_accuracy_repeatability
import pose_accuracy_repeatability_posture
import multi_directional_pose_accuracy_variation
import distance_accuracy_repeatability
import stable_overshoot
import line_A_R
import BC_AR
import SC_AR
import CR_CO
import minPoseTime
import path_velocity_characteristics
import stable_comliance
import weaving_deviation
import simple_velocity

class setWindows():
    def __init__(self):
        self.x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
        self.y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴
        #确定窗口位置
        self.place_x = str(int(self.x/3))
        self.place_y = str(int(self.y/3))

    #位置准确度重复性
    def poseAR(self):
        master = Tk()  #导入tkinter中的tk模块
        master.title('位置准确度重复性参数设置') #设窗口标题
        master.geometry('+'+self.place_x+'+'+self.place_y)
        #字体、颜色待调整
        label1 = Label(master, text='循环次数：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master, text='点位数量：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)

        #输入框
        cycleNum = IntVar(master, value=30)
        entry1 = Entry(master, font=('GB2312', 18), fg='Plum',
                       textvariable=cycleNum
                       )
        entry1.grid(row=0, column=1)
        poseNum = IntVar(master, value=5)
        entry2 = Spinbox(master, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=poseNum
                         )
        entry2.grid(row=1, column=1)
        #选择框
        a1 = BooleanVar()
        check = Checkbutton(master, text='计算准确度', variable=a1,
                            width=10, font=('GB2312', 18))
        check.grid(row=2, column=0, columnspan=2, sticky=W)

        def PAR_Instantiate():
            pose_A_R = pose_accuracy_repeatability.pose_accuracy_repeatability(cycleNum.get(),
                                                   poseNum.get(),
                                                   a1.get())
            pose_A_R.calculate()

        button1 = Button(master, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate)
        button1.grid(row=3, column=0, columnspan=2,
                     sticky=E+W)
        label_tip = Label(master, text='Tips：\n1.测试工业机器人时按照国标要求的P5-P4-P3-P2-P1顺序循环；\n'
                        '2.测试其他类型机器人的重复性和准确度时可以通过设置窗口灵活调\n  节，计算不同数量的点位和循环次数，其他项亦如此；\n'
                        '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹；\n'
                        '4.若要计算准确度需要勾上“计算准确度”的选项，在测试数据txt文件\n  的同目录下创建名为“指令点.txt”的文本文件，将指令点\n  输入其中，每个点1行，xyz之间必须由一个空格隔开；\n'
                        '5.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显\n  示在下方结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=4, column=0, columnspan=2)
        master.mainloop()
    #位姿准确度重复性
    def poseAR2(self):
        master2 = Tk()  #导入tkinter中的tk模块
        master2.title('位姿准确度重复性参数设置') #设窗口标题
        master2.geometry('+'+self.place_x+'+'+self.place_y)
        #字体、颜色待调整
        label1 = Label(master2, text='循环次数：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master2, text='点位数量：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)

        #输入框
        cycleNum = IntVar(master2, value=30)
        entry1 = Entry(master2, font=('GB2312', 18), fg='Plum',
                       textvariable=cycleNum
                       )
        entry1.grid(row=0, column=1)
        poseNum = IntVar(master2, value=5)
        entry2 = Spinbox(master2, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=poseNum
                         )
        entry2.grid(row=1, column=1)
        #选择框
        a2 = BooleanVar()
        check = Checkbutton(master2, text='计算准确度', variable=a2,
                            width=10, font=('GB2312', 18))
        check.grid(row=2, column=0, columnspan=2, sticky=W)

        def PAR_Instantiate2():
            pose_A_R2 = pose_accuracy_repeatability_posture.posture_accuracy_repeatability(cycleNum.get(), 
                                                    poseNum.get(),
                                                    a2.get())
            pose_A_R2.calculate()

        button1 = Button(master2, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate2)
        button1.grid(row=3, column=0, columnspan=2,
                     sticky=E+W)
        label_tip = Label(master2, text='Tips：\n1.测试工业机器人时按照国标要求的P5-P4-P3-P2-P1顺序循环；\n'
                        '2.该项为T-MAC测试的有姿态的位姿准确度重复性计算，计算选择的\n  是csv表格文件；\n'
                        '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹；\n'
                        '4.若要计算准确度需要勾上“计算准确度”的选项，在测试数据txt文件\n  的同目录下创建名为“指令点.txt”的文本文件，将指令点输入其中，\n  每个点1行，xyz之间必须由一个空格隔开；\n'
                        '5.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显\n  示在下方结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=4, column=0, columnspan=2)
        master2.mainloop()
    #多方向位姿变动
    def MD_Pose(self):
        master3 = Tk()  # 导入tkinter中的tk模块
        master3.title('多方向位姿变动参数设置')  # 设窗口标题
        master3.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        label1 = Label(master3, text='循环次数：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master3, text='点位数量：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        # 输入框
        cycleNum = IntVar(master3, value=30)
        entry1 = Entry(master3, font=('GB2312', 18), fg='Plum',
                       textvariable=cycleNum
                       )
        entry1.grid(row=0, column=1)
        poseNum = IntVar(master3, value=3)
        entry2 = Spinbox(master3, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                           textvariable=poseNum
                         )
        entry2.grid(row=1, column=1)
        # 选择框
        a3 = BooleanVar()
        check = Checkbutton(master3, text='计算姿态', variable=a3,
                            width=10, font=('GB2312', 18))
        check.grid(row=2, column=0, columnspan=2, sticky=W)

        def PAR_Instantiate3():
            pose_A_R3 = multi_directional_pose_accuracy_variation.md_pose_av(
                                                    cycleNum.get(), 
                                                    poseNum.get(),
                                                    a3.get())
            pose_A_R3.calculate()

        button1 = Button(master3, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate3)
        button1.grid(row=3, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master3, text='Tips：\n1.测试工业机器人时按照国标要求在每一个点位进行多方位循环，可\n  以将几个点的数据放在一个txt文件里；\n'
                        '2.若为T-MAC测试的有姿态的数据，计算选择的是csv表格文件；\n'
                        '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹勾上\n  “计算姿态”的选项；\n'
                        '4.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显\n  示在下方结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=4, column=0, columnspan=2)
        master3.mainloop()
    #距离准确度重复性
    def d_AR(self):
        master4 = Tk()  # 导入tkinter中的tk模块
        master4.title('距离准确度重复性参数设置')  # 设窗口标题
        master4.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        label1 = Label(master4, text='循环次数：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master4, text='点位数量：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        # 输入框
        cycleNum = IntVar(master4, value=30)
        entry1 = Entry(master4, font=('GB2312', 18), fg='Plum',
                       textvariable=cycleNum
                       )
        entry1.grid(row=0, column=1)
        poseNum = IntVar(master4, value=2)
        entry2 = Spinbox(master4, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                           textvariable=poseNum
                         )
        entry2.grid(row=1, column=1)
        # 选择框
        a4 = BooleanVar()
        check = Checkbutton(master4, text='计算姿态', variable=a4,
                            width=10, font=('GB2312', 18))
        check.grid(row=2, column=0, columnspan=2, sticky=W)

        def PAR_Instantiate4():
            D_A_R = distance_accuracy_repeatability.distance_ar(cycleNum.get(), 
                                poseNum.get(),
                                a4.get())
            D_A_R.calculate()

        button1 = Button(master4, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate4)
        button1.grid(row=3, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master4, text='Tips：\n1.测试工业机器人时按照国标要求的P2-P4顺序循环；\n'
                        '2.若为T-MAC测试的有姿态的数据，计算选择的是csv表格文件；\n'
                        '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹；\n'
                        '4.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显\n  示在下方结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=4, column=0, columnspan=2)
        master4.mainloop()
    #位置稳定时间与位置超调量
    def Stable_Overshoot(self):
        master5 = Tk()  # 导入tkinter中的tk模块
        master5.title('位置稳定时间与位置超调量参数设置')  # 设窗口标题
        master5.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        label1 = Label(master5, text='采集频率(Hz)：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master5, text='门限带(mm)：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        label3 = Label(master5, text='测量次数：', font=('C71585', 16), fg='SteelBlue')
        label3.grid(row=2, column=0)
        # 输入框
        frequencys = DoubleVar(master5, value=1000)
        entry1 = Entry(master5, font=('GB2312', 18), fg='Plum',
                       textvariable=frequencys
                       )
        entry1.grid(row=0, column=1)
        threshold = DoubleVar(master5, value=0.1)
        entry2 = Entry(master5, font=('GB2312', 18), fg='DarkCyan',
                       textvariable=threshold
                       )
        entry2.grid(row=1, column=1)
        cycleNum = IntVar(master5, value=3)
        entry3 = Entry(master5, font=('GB2312', 18), fg='DarkCyan',
                       textvariable=cycleNum
                       )
        entry3.grid(row=2, column=1)

        def PAR_Instantiate5():
            S_O = stable_overshoot.stable_overshoot(frequencys.get(), threshold.get(), cycleNum.get())
            S_O.calculate()

        button1 = Button(master5, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate5)
        button1.grid(row=3, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master5, text='Tips：\n1.测试工业机器人时按照国标要求的稳定到P1运动；\n'
                         '2.测量频率，门限带和测量组数可设置；\n'
                         '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹；\n'
                         '4.测量时先用点云追踪运动路径，再马上切换到单点测试记录实到位置；\n'
                         '5.点云的文件名根据测量次数为“1.txt”，“2.txt”···以此类推，实到位置的\n  文件名为“实到位置1.txt”，“实到位置2.txt”···以此类推；\n'
                         '6.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显示\n  在下方结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=4, column=0, columnspan=2)
        master5.mainloop()
    #位姿特性漂移
    def drift(self):
        master6 = Tk()  # 导入tkinter中的tk模块
        master6.title('位姿特性漂移参数设置')  # 设窗口标题
        master6.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        label1 = Label(master6, text='略\n使用位置(姿)准确度与重复性进行计算即可',
                       font=('GB2312', 16), fg='SteelBlue', justify=LEFT)
        label1.pack()
        master6.mainloop()
    #直线轨迹准确度重复性
    def line_AR(self):
        master7 = Tk()  # 导入tkinter中的tk模块
        master7.title('直线轨迹准确度重复性设置')  # 设窗口标题
        master7.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        label1 = Label(master7, text='采集频率(Hz)：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master7, text='截面数量：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        label3 = Label(master7, text='测量次数', font=('C71585', 16), fg='SteelBlue')
        label3.grid(row=2, column=0)
        # 输入框
        frequencys = DoubleVar(master7, value=1000)
        entry1 = Entry(master7, font=('GB2312', 18), fg='Plum',
                       textvariable=frequencys
                       )
        entry1.grid(row=0, column=1)
        sectionNum = IntVar(master7, value=10)
        entry2 = Spinbox(master7, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=sectionNum
                         )
        entry2.grid(row=1, column=1)
        cycleNum = IntVar(master7, value=10)
        entry3 = Spinbox(master7, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=cycleNum
                         )
        entry3.grid(row=2, column=1)

        def PAR_Instantiate7():
            L_AR = line_A_R.line_accuracy_repearability(frequencys.get(), sectionNum.get(), cycleNum.get())
            L_AR.calculate()

        button1 = Button(master7, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate7)
        button1.grid(row=3, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master7, text='Tips：\n1.测试工业机器人时按照国标要求P2-P4循环；\n'
                         '2.测量频率和测量次数可设置；\n'
                         '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹，文件名根据测\n  量次数为“1.txt”，“2.txt”···以此类推；\n'
                         '4.txt文件的同目录下创建名为“理论直线轨迹.txt”的文本文件，指令点为两个点，\n  每个点1行，xyz之间必须由一个空格隔开；\n'
                         '5.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显示在下方结\n  果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=4, column=0, columnspan=2)
        master7.mainloop()
    #大圆轨迹准确度重复性
    def bcircle_AR(self):
        master8 = Tk()  # 导入tkinter中的tk模块
        master8.title('大圆轨迹准确度重复性参数设置')  # 设窗口标题
        master8.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        label1 = Label(master8, text='采集频率(Hz)：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master8, text='截面数量：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        label3 = Label(master8, text='测量次数', font=('C71585', 16), fg='SteelBlue')
        label3.grid(row=2, column=0)
        # 输入框
        frequencys = DoubleVar(master8, value=1000)
        entry1 = Entry(master8, font=('GB2312', 18), fg='Plum',
                       textvariable=frequencys
                       )
        entry1.grid(row=0, column=1)
        sectionNum = IntVar(master8, value=10)
        entry2 = Spinbox(master8, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=sectionNum
                         )
        entry2.grid(row=1, column=1)
        cycleNum = IntVar(master8, value=10)
        entry3 = Spinbox(master8, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=cycleNum
                         )
        entry3.grid(row=2, column=1)

        def PAR_Instantiate8():
            bc_AR = BC_AR.circleB_accuracy_repearability(frequencys.get(), sectionNum.get(), cycleNum.get())
            bc_AR.calculate()

        button1 = Button(master8, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate8)
        button1.grid(row=3, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master8, text='Tips：\n1.测试工业机器人时按照国标要求循环划大圆；\n'
                         '2.测量频率和测量次数可设置；\n'
                         '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹，文件名根据\n  测量次数为“1.txt”，“2.txt”···以此类推；\n'
                         '4.txt文件的同目录下创建名为“理论点大圆.txt”的文本文件，指令点为三个点，\n  每个点1行，xyz之间必须由一个空格隔开，三点必须超过半圆；\n'
                         '5.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显示在下方\n  结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=4, column=0, columnspan=2)
        master8.mainloop()
    #小圆轨迹准确度重复性
    def scircle_AR(self):
        master9 = Tk()  # 导入tkinter中的tk模块
        master9.title('小圆轨迹准确度重复性参数设置')  # 设窗口标题
        master9.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        label1 = Label(master9, text='采集频率(Hz)：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master9, text='截面数量：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        label3 = Label(master9, text='测量次数', font=('C71585', 16), fg='SteelBlue')
        label3.grid(row=2, column=0)
        # 输入框
        frequencys = DoubleVar(master9, value=1000)
        entry1 = Entry(master9, font=('GB2312', 18), fg='Plum',
                       textvariable=frequencys
                       )
        entry1.grid(row=0, column=1)
        sectionNum = IntVar(master9, value=10)
        entry2 = Spinbox(master9, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=sectionNum
                         )
        entry2.grid(row=1, column=1)
        cycleNum = IntVar(master9, value=10)
        entry3 = Spinbox(master9, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=cycleNum
                         )
        entry3.grid(row=2, column=1)

        def PAR_Instantiate9():
            sc_AR = SC_AR.circleS_accuracy_repearability(frequencys.get(), sectionNum.get(), cycleNum.get())
            sc_AR.calculate()

        button1 = Button(master9, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate9)
        button1.grid(row=3, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master9, text='Tips：\n1.测试工业机器人时按照国标要求循环划小圆；\n'
                         '2.测量频率和测量次数可设置；\n'
                         '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹，文件名根据\n  测量次数为“1.txt”，“2.txt”···以此类推；\n'
                         '4.txt文件的同目录下创建名为“理论点小圆.txt”的文本文件，指令点为三个点，\n  每个点1行，xyz之间必须由一个空格隔开，三点必须超过半圆；\n'
                         '5.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显示在下方\n  结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=4, column=0, columnspan=2)
        master9.mainloop()
    #圆角误差与拐角超调
    def CRCO_AR(self):
        master10 = Tk()  # 导入tkinter中的tk模块
        master10.title('圆角误差与拐角超调参数设置')  # 设窗口标题
        master10.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        
        label1 = Label(master10, text='测量次数', font=('C71585', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        # 输入框
        cycleNum = IntVar(master10, value=3)
        entry1 = Spinbox(master10, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=cycleNum
                         )
        entry1.grid(row=0, column=1)

        def PAR_Instantiate10():
            ro_AR = CR_CO.CR_COs(cycleNum.get())
            ro_AR.calculate()

        button1 = Button(master10, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate10)
        button1.grid(row=1, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master10, text='Tips：\n1.测试工业机器人时按照国标要求P2-P3-P4-P5循环划框；\n'
                         '2.测量频率和测量次数可设置；\n'
                         '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹；\n  文件名根据测量次数为“1.txt”，“2.txt”···以此类推；\n'
                         '4.txt文件的同目录下创建名为“指令点.txt”的文本文件，指令点为\n  四个端点，每个点1行，xyz之间必须由一个空格隔开；\n'
                         '5.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会\n  显示在下方结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=2, column=0, columnspan=2)
        master10.mainloop()
    #最小定位时间 
    def min_time(self):
        master11 = Tk()  # 导入tkinter中的tk模块
        master11.title('最小定位时间参数设置')  # 设窗口标题
        master11.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        
        label1 = Label(master11, text='采集频率：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master11, text='点位数量：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        label3 = Label(master11, text='测量次数：', font=('C71585', 16), fg='SteelBlue')
        label3.grid(row=2, column=0)
        label3 = Label(master11, text='门限带(mm)：', font=('C71585', 16), fg='SteelBlue')
        label3.grid(row=3, column=0)
        # 输入框
        frequencys = DoubleVar(master11, value=1000)
        entry1 = Entry(master11, font=('GB2312', 18), fg='Plum',
                       textvariable=frequencys
                       )
        entry1.grid(row=0, column=1)
        poseNum = IntVar(master11, value=5)
        entry2 = Spinbox(master11, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=poseNum
                         )
        entry2.grid(row=1, column=1)
        cycleNum = IntVar(master11, value=3)
        entry3 = Spinbox(master11, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=cycleNum
                         )
        entry3.grid(row=2, column=1)
        thresholds = DoubleVar(master11, value=0.1)
        entry4 = Entry(master11, font=('GB2312', 18), fg='Plum',
                       textvariable=thresholds
                       )
        entry4.grid(row=3, column=1)

        def PAR_Instantiate11():
            minpt = minPoseTime.mptime(frequencys.get(), poseNum.get(), 
                          cycleNum.get(), thresholds.get())
            minpt.calculate()

        button1 = Button(master11, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate11)
        button1.grid(row=4, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master11, text='Tips：\n1.测试工业机器人时按照国标要求P1，P1+1···运动；\n'
                         '2.测量频率和测量次数可设置；\n'
                         '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹，文件名\n  根据测量次数为“1.txt”，“2.txt”···以此类推；\n'
                         '4.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显示\n  在下方结果框里；\n'
                         '5.该项目有测量失败的可能，需要通过简单速度测试进行纠正；\n'
                        , justify=LEFT)
        label_tip.grid(row=5, column=0, columnspan=2)
        master11.mainloop()
    #轨迹速度特性
    def Track_Speed(self):
        master12 = Tk()  # 导入tkinter中的tk模块
        master12.title('轨迹速度特性参数设置')  # 设窗口标题
        master12.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        
        label1 = Label(master12, text='采集频率：', font=('GB2312', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master12, text='指令速度(mm/s)：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        label3 = Label(master12, text='测量次数：', font=('C71585', 16), fg='SteelBlue')
        label3.grid(row=2, column=0)
        # 输入框
        frequencys = DoubleVar(master12, value=1000)
        entry1 = Entry(master12, font=('GB2312', 18), fg='Plum',
                       textvariable=frequencys
                       )
        entry1.grid(row=0, column=1)
        insVelocity = DoubleVar(master12, value=1600)
        entry2 = Entry(master12, font=('GB2312', 18), fg='Plum',
                       textvariable=insVelocity
                       )
        entry2.grid(row=1, column=1)
        cycleNum = IntVar(master12, value=10)
        entry3 = Spinbox(master12, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=cycleNum
                         )
        entry3.grid(row=2, column=1)
        def PAR_Instantiate12():
            speedTrack = path_velocity_characteristics.pathVelocityCharacteristics(frequencys.get(), 
                                insVelocity.get(), 
                                cycleNum.get())
            speedTrack.calculate()

        button1 = Button(master12, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate12)
        button1.grid(row=4, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master12, text='Tips：\n1.测试工业机器人时按照国标要求运动，确保稳定在最高速运行的部分能达到\n  整个轨迹的50%；\n'
                         '2.测量频率，指令速度和测量次数可设置；\n'
                         '3.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹，文件名根据测\n  量次数为“1.txt”，“2.txt”···以此类推；\n'
                         '4.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显示在下方结\n  果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=5, column=0, columnspan=2, sticky=W + E)
        master12.mainloop()
    #静态柔顺性
    def Stable_Compliance(self):
        master13 = Tk()  # 导入tkinter中的tk模块
        master13.title('静态柔顺性参数设置')  # 设窗口标题
        master13.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        
        label1 = Label(master13, text='负载(kg)：', font=('C71585', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master13, text='测量次数：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        # 输入框
        loads = DoubleVar(master13, value=20)
        entry1 = Entry(master13, font=('GB2312', 18), fg='Plum',
                       textvariable=loads
                       )
        entry1.grid(row=0, column=1)
        cycleNum = IntVar(master13, value=3)
        entry2 = Spinbox(master13, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=cycleNum
                         )
        entry2.grid(row=1, column=1)

        def PAR_Instantiate13():
            stable_C = stable_comliance.stableCompliance(loads.get(), cycleNum.get())
            stable_C.calculate()

        button1 = Button(master13, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate13)
        button1.grid(row=2, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master13, text='Tips：\n1.测试工业机器人时按照国标要求卸掉负载，停在P1点；\n'
                         '2.负载和测量次数可设置；\n'
                         '3.使用弹簧测力计按照x+-x-y+-y-z+-z-的顺序进行测试，一个方向全\n  部测完后再换方向；\n'
                         '4.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹，该项为\n  1个txt文件；\n'
                         '5.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显示\n  在下方结果框里；\n'
                        , justify=LEFT)
        label_tip.grid(row=3, column=0, columnspan=2, sticky=E + W)
        master13.mainloop()
    #摆动偏差
    def weaving(self):
        master14 = Tk()  # 导入tkinter中的tk模块
        master14.title('摆动偏差参数设置')  # 设窗口标题
        master14.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        
        label1 = Label(master14, text='测试频率：', font=('C71585', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        label2 = Label(master14, text='指令摆幅(mm)：', font=('C71585', 16), fg='SteelBlue')
        label2.grid(row=1, column=0)
        label3 = Label(master14, text='指令摆频(Hz)：', font=('C71585', 16), fg='SteelBlue')
        label3.grid(row=2, column=0)
        label4 = Label(master14, text='测量次数：', font=('C71585', 16), fg='SteelBlue')
        label4.grid(row=3, column=0)
        label5 = Label(master14, text='摆动间隔(mm)：', font=('C71585', 16), fg='SteelBlue')
        label5.grid(row=4, column=0)
        # 输入框
        frequencys = DoubleVar(master14, value=1000)
        entry1 = Entry(master14, font=('GB2312', 18), fg='Plum',
                       textvariable=frequencys
                       )
        entry1.grid(row=0, column=1)
        scIns = DoubleVar(master14, value=20)
        entry2 = Entry(master14, font=('GB2312', 18), fg='Plum',
                       textvariable=scIns
                       )
        entry2.grid(row=1, column=1)
        fcIns = DoubleVar(master14, value=10)
        entry3 = Entry(master14, font=('GB2312', 18), fg='Plum',
                       textvariable=fcIns
                       )
        entry3.grid(row=2, column=1)
        cycleNum = IntVar(master14, value=3)
        entry4 = Spinbox(master14, from_=0, to=100, increment=1,
                         font=('GB2312', 18), fg='DarkCyan',
                         textvariable=cycleNum
                         )
        entry4.grid(row=3, column=1)
        fd = DoubleVar(master14, value=10)
        entry5 = Entry(master14, font=('GB2312', 18), fg='Plum',
                       textvariable=fd
                       )
        entry5.grid(row=4, column=1)
        def PAR_Instantiate14():
            wsf = weaving_deviation.weavingsf(frequencys.get(), scIns.get(), fcIns.get(), 
                            cycleNum.get(), fd.get())
            wsf.calculate()

        button1 = Button(master14, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate14)
        button1.grid(row=5, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master14, text='Tips：\n1.测试工业机器人时按照国标要求运动；\n'
                         '2.负载和测量次数可设置；\n'
                         '3.txt文件的同目录下创建名为“指令点.txt”的文本文件，指令点为起始点P1，\n  与中线平行的P2，P3，xyz之间必须由一个空格隔开；\n'
                         '4.SA软件的测量数据导出的位置必须为桌面或者桌面的文件夹，文件名根据\n  测量次数为“1.txt”，“2.txt”···以此类推；\n'
                         '5.测试数据和计算参数确认无误后点击“确认并计算”按钮，结果会显示在下\n  方结果框里；\n'
                         '6.该项目未经过验证，慎用！！！'
                        , justify=LEFT)
        label_tip.grid(row=6, column=0, columnspan=2, sticky=E + W)
        label_warning = Label(master14, text='该项目未经过验证，慎用！！！'
                        , font=('C71585', 16), fg='Red'
                        , justify=LEFT)
        label_warning.grid(row=7, column=0, columnspan=2, sticky=E + W)
        master14.mainloop()
    #重定向轨迹准确度
    def reorientation_A(self):
        master15 = Tk()  # 导入tkinter中的tk模块
        master15.title('重定向轨迹准确度参数设置')  # 设窗口标题
        master15.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        label1 = Label(master15, text='略\n使用直线轨迹准确度与重复性进行计算即可',
                       font=('GB2312', 16), fg='SteelBlue', justify=LEFT)
        label1.pack()
        master15.mainloop()
    #简单速度测试
    def simple_v(self):
        master16 = Tk()  # 导入tkinter中的tk模块
        master16.title('简单速度测试参数设置')  # 设窗口标题
        master16.geometry('+'+self.place_x+'+'+self.place_y)
        # 字体、颜色待调整
        
        label1 = Label(master16, text='测试频率(Hz)：', font=('C71585', 16), fg='SteelBlue')
        label1.grid(row=0, column=0)
        # 输入框
        frequencys = DoubleVar(master16, value=1000)
        entry1 = Entry(master16, font=('GB2312', 18), fg='Plum',
                       textvariable=frequencys
                       )
        entry1.grid(row=0, column=1)
        def PAR_Instantiate16():
            sv = simple_velocity.simpleVlocity(frequencys.get())
            sv.calculate()
        button1 = Button(master16, text='确定并计算', width=10,
                         font=('GB2312', 18),
                         background='Tan', command=PAR_Instantiate16)
        button1.grid(row=1, column=0, columnspan=2,
                     sticky=E + W)
        label_tip = Label(master16, text='Tips：\n1.该项处理的是点云生成的单个txt文件；\n'
                         '2.测量频率可设置；\n'
                         '3.可根据图像选择运动段计算某一段的平均速度；\n'
                        , justify=LEFT)
        label_tip.grid(row=2, column=0, columnspan=2, sticky=E + W)
        master16.mainloop()
