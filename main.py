from tkinter import * 
from tkinter import messagebox
from PIL import Image,ImageTk
import re #正则表达式
import requests
import time
from PIL import Image, ImageGrab
import tkinter
from baidu import get_text
#用来显示全屏幕截图并响应二次截图的窗口类
print(123)
class MyCapture:
    def __init__(self, png):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        #屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        #创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=screenWidth, height=screenHeight)
        #不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top,bg='white', width=screenWidth, height=screenHeight)
        #显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=png)
        self.text =""
        self.canvas.create_image(screenWidth//2, screenHeight//2, image=self.image)
        #鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            #开始截图
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)
        #鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='black')
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)
        #获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel = False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            time.sleep(0.1)
            #考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left+1, top+1, right, bottom))
            fileName ="temp.jpg"
            print('1')
            pic.save(fileName)
            print('2')
            self.text = get_text('./'+fileName)
            #关闭当前窗口
            self.top.destroy()
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
#让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
 #开始截图
def buttonCaptureClick():
    #最小化主窗口
#     root.state('icon')
    root.withdraw()
    time.sleep(0.4)
    filename = 'temp.png'
    #grab()方法默认对全屏幕进行截图
    im = ImageGrab.grab()
    im.save(filename)
    im.close()
    #显示全屏幕截图
    w = MyCapture(filename)
    root.wait_window(w.top)
    #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
    root.update()
    root.deiconify()
    text1.config(state = NORMAL)
    text1.delete(0.0,END)
    text1.insert('insert',w.text)
    text1.config(state = DISABLED)
    text1.pack()
    os.remove(filename)
    

    
root = Tk() 
root.title("小新的OCR")
# 创建一个顶级菜单
menubar = Menu(root)
# 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label="OCR", command=buttonCaptureClick, accelerator='Ctrl+N')
#filemenu.add_command(label="帮助",command=helpClick)
filemenu.add_command(label="退出", command=root.quit)
menubar.add_cascade(label="操作", menu=filemenu)
# 显示菜单
root.config(menu=menubar)
root.bind_all("<Control-d>", lambda event: buttonCaptureClick())
#启动消息主循环
root.mainloop()




