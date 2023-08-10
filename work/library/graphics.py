"""
Этот скрипт содержит набор функций для визуализации работы с базой данных.\n
"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import filedialog
import datab as db
from pathlib import Path

path = Path.cwd()
workDir = str(path.parent.absolute())

#Стили для кнопок, лейблов и т.д.
frameStyle = {"bg":"#F2EDF6"}

canvasStyle = {"bg":frameStyle["bg"]}

def parseUI():
    """
    Функция для загрузи настроек из файла setting.ini в папке Data\n
    """
    global frameStyle
    global buttonStyle
    global labelStyle
    global entryStyle
    global canvasStyle
    frameStyle = {"bg":"#F2EDF6","bd":4,"relief":"groove"}
    buttonStyle = {"bg":"#FF6F69","fg":"#000000", "padx": 3, "pady": 5, "font" : ("Arial",10, "bold"), "bd" : 3}
    labelStyle = {"bg":"#b66562","fg":"#000000", "font" : ("Arial",10, "bold"), "relief" : "ridge", "bd" : 2}
    entryStyle = {"bg":"#FFCC5C","fg":"#000000", "font" : ("Arial",10, "bold"), "relief" : "ridge", "bd" : 2}
# def parseUI():
#     """
#     Функция для загрузи настроек из файла setting.ini в папке Data\n
#     """
#     global frameStyle
#     global buttonStyle
#     global labelStyle
#     global entryStyle
#     global canvasStyle
#
#     try:
#         f = open(workDir+"data\\settings.ini","r")
#     except:
#         tk.Label(None, text = "Не найден файл settings", font = ("Arial",30, "bold")).pack()
#         return
#
#     for i in f:
#         j = i.split(sep=" = ")
#         if j[0]=="frameStyle":
#             frameStyle = eval(j[1])
#         elif j[0] =="buttonStyle":
#             buttonStyle = eval(j[1])
#         elif j[0] =="labelStyle":
#             labelStyle = eval(j[1])
#         elif j[0] =="entryStyle":
#             entryStyle = eval(j[1])
#
# canvasStyle = {"bg":frameStyle["bg"]}


def ShowMainWindow(mainWindow,other):
    """
    Удаляет текущее окно (other) и восстанавливает основное окно (mainWindow)\n

    """
    mainWindow.deiconify() 
    other.destroy()

def HideMainWindow(mainWindow):
    """
    Скрывает текущее окно (mainWindow), но не удаляет его\n

    """
    mainWindow.withdraw()

#--------------------------------------Find File window------------------------------------#
"""
Следующие функции описывают функционал окна выбора базы данных\n

"""
#директория для бд по умолчанию
dataDir = workDir+"data\\GDS.pic"

def FindFile(entry,dataBase):
    """
    Загружает dataBase в оперативную память (функция ReadBase в dataBase.py) по пути, написанном в поле entry\n

    """
    global dataDir
    dataDir = entry.get()
    db.ReadBase(dataBase, dataDir)
    
def BrowseFile(entry,dataBase,pathW):
    """
    Загружает dataBase в оперативную память (функция ReadBase в dataBase.py) по пути, выбранном с помощью функции filedialog.Open()\n

    """
    global dataDir
    dataDir = filedialog.Open(initialdir=dataDir, filetypes=[("*.pic files", ".pic")]).show()
    db.ReadBase(dataBase,dataDir)
    entry.delete(0,"end")
    entry.insert(0,dataDir)
    
    
def FindPathW(mainWindow,dataBase):
    """
    Открывает окно выбора базы данных\n

    """
    pathW = tk.Toplevel(mainWindow)
    
    HideMainWindow(mainWindow)
    
    frame = tk.Frame(pathW, frameStyle)
    frame.pack(fill=tk.BOTH,expand=tk.YES)
    
    pathW.title("База данных - выбор базы данных")
    pathW.geometry("530x250+300+250")
    pathW.minsize(475,170)
    pathW.iconbitmap(workDir+"library\\icon.ico")
    #Переназначение кнопки закрыть: функция аналогична нажатию на кнопку "Назад"
    pathW.protocol("WM_DELETE_WINDOW",lambda: ShowMainWindow(mainWindow,pathW))

    text = tk.Label(frame,labelStyle,text="Введите полный путь к файлу:", width=30)
    entry = tk.Entry(frame, entryStyle,width=50)
    entry.insert(0,workDir+"data\\GDS.pic")
    
    text2 = tk.Label(frame,labelStyle,text="Или выберите его через проводник:", width=50)
    browseB = tk.Button(frame,buttonStyle,text="Выбрать", width=50, command=lambda: BrowseFile(entry,dataBase,pathW))
    
    findB = tk.Button(frame,buttonStyle,text="Загрузить", width=15, command=lambda: FindFile(entry,dataBase))
    closeB = tk.Button(frame,buttonStyle, text="Назад", width=5, command=lambda: ShowMainWindow(mainWindow,pathW))

    text.grid(row=0,column=1)
    entry.grid(row=1,column=1)
    findB.grid(row=1,column=2)

    text2.grid(row=2,column=1)
    browseB.grid(row=3,column=1)
    
    closeB.grid(row=0,column=0)

#--------------------------------------Show Data Base window------------------------------------#
"""
Следующие функции описывают функционал окна показа и редактирования базы данных\n

"""

def DataBaseW(mainWindow,MainDataBase,dataBase): 
    """
    Открывает окно показа и редактирования по базе данных\n
    \tПараметры: \n
    \t\tmainWindow - главное окно, которое будет скрыто и на основании которого будет создано это дочернее окно (функция Toplevel())\n
    \t\tMainDataBase - база данных (словарь словарей)\n
    \t\tdataBase - база данных выводимых элементов (словарь словарей)\n
    """
    dbW = tk.Toplevel(mainWindow)
    
    HideMainWindow(mainWindow)
    
    dbW.title("База данных - показ/редактирование базы данных")
    dbW.geometry("1000x500+100+100")
    dbW.minsize(1000,250)
    dbW.iconbitmap(workDir+"library\\icon.ico")
    #Переназначение кнопки закрыть: функция аналогична нажатию на кнопку "Назад"
    dbW.protocol("WM_DELETE_WINDOW",lambda: ShowMainWindow(mainWindow,dbW))
    
    #ВНУТРЕННЯЯ ФУНКЦИЯ
    def myfunction(event):
        """
        Внутрення функция. не для вызова. Привязывает scrollbar к canvas.
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    #Создание внешнего фрейма. В него будут вставлены верхний фрейм с основноыми кнопками управления и canvas под верхним фреймом
    myframe = tk.Frame(dbW, frameStyle)
    myframe.pack(anchor="nw",fill=tk.BOTH,expand=tk.YES)
    #Создание верхнего фрейма
    topframe=tk.Frame(myframe,canvasStyle)
    topframe.pack(anchor="nw")
    
    tk.Button(topframe, buttonStyle, text="Назад", command = lambda: ShowMainWindow(mainWindow,dbW)).grid(row=0,column=0)
    tk.Button(topframe, buttonStyle, text = "Сохранить изменения", command = lambda: RewriteBase(MainDataBase,tkAll)).grid(row=0,column=1)
    tk.Button(topframe, buttonStyle, text = "Добавить", command = lambda: AddToBase(frame,MainDataBase,tkAll)).grid(row=0,column=2)

    #Создание canvas
    canvas = tk.Canvas(myframe,canvasStyle,bd=0)
    frame = tk.Frame(canvas,canvasStyle)
    #Создание скроллбара, настроенного на прокрутку canvas
    myscrollbar = tk.Scrollbar(myframe,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    myscrollbar.pack(side="right",fill="y")


    myscrollbar1 = tk.Scrollbar(myframe, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=myscrollbar1.set)
    myscrollbar1.pack(side="bottom", fill="x")
    canvas.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)
    #Рисование еще одного фрейма на canvas. В этом фрейме будут располагаться элементы
    canvas.create_window((0,0),window=frame,anchor="nw")
    frame.bind("<Configure>",myfunction)
    
    #Заполнение frame, содержащегося в canvas
    r = 2
    
    tk.Label(frame, labelStyle, text = "№", width=3).grid(row=1, column=0)
    tk.Label(frame, labelStyle, text = "Фамилия", width=13).grid(row=1, column=1)
    tk.Label(frame, labelStyle, text = "Имя", width=10).grid(row=1, column=2)
    tk.Label(frame, labelStyle, text = "Телефон", width=10).grid(row=1, column=3)
    tk.Label(frame, labelStyle, text = "Номер отдела", width=18).grid(row=1, column=4)
    tk.Label(frame, labelStyle, text = "Название отдела", width=30).grid(row=1, column=5)
    tk.Label(frame, labelStyle, text = "Номер корпуса", width=15).grid(row=1, column=6)
    tk.Label(frame, labelStyle, text = "Должность", width=30).grid(row=1, column=7)
    tk.Label(frame, labelStyle, text="Улица", width=10).grid(row=1, column=8)
    tk.Label(frame, labelStyle, text="Дом", width=5).grid(row=1, column=9)
    tk.Label(frame, labelStyle, text="Зарплата", width=18).grid(row=1, column=10)
    #tkAll - двумерный список всех объектов tkinter (Label, Entry, Checkbox)
    #tkArray - строка в tkAll, описывает один элемент базы данных
    #Нужен для изменения и сохраения бд
    tkAll = []
    for c in dataBase:
        tkArray =[]
        i=0
        for e in dataBase[c]:
            if e == "№":
                m = tk.Label(frame, labelStyle, text = str(dataBase[c]["Индекс"]+1), width=3)
                m.grid(row=r, column=0)
                tkArray.append(m)
            else:
                if e == "Фамилия" or e == "Имя":
                    m = tk.Entry(frame, entryStyle, width=15)
                elif e == "Должность":
                    m = tk.Entry(frame, entryStyle, width=23)
                elif e == "Улица":
                    m = tk.Entry(frame, entryStyle, width=25)
                elif e == "Название отдела":
                    m = tk.Entry(frame, entryStyle, width=30)
                elif e == "Дом":
                    m = tk.Entry(frame, entryStyle, width=5)
                else:
                    m = tk.Entry(frame, entryStyle, width=15)
                s = str(dataBase[c][e])
                m.insert(0,s)
                m.grid(row=r, column=i)
                tkArray.append(m)
            i+=1
        flag = tk.IntVar()
        cb = tk.Checkbutton(frame, buttonStyle,width=2, variable=flag)
        cb.grid(row=r,column=i)
        cb.select()
        tkArray.append(flag)
        r+=1
        tkAll.append(tkArray)
    
def AddToBase(window,dataBase,tkAll):
    """
    Добавляет в окно показа и редактирования по базе данных новое поле для новой записи\n

    """
    data = { "Фамилия":"","Имя":"","Телефон":000-000,"Номер отдела":0,"Название отдела":"","Номер корпуса":0,"Должность":"", "Улица":"", "Дом":0, "Зарплата":0, "Индекс":len(dataBase)}
    i=1
    tkArray=[]
    #Создание объектов tkinter для нового элемента бд и занесение их в tkAll
    for e in data:
            if e == "Индекс":
                m = tk.Label(window, labelStyle, text = str(len(dataBase) + 1), width=3)
                m.grid(row=len(dataBase) + 2, column=0)
                tkArray.append(m)
            else:
                if e == "Фамилия":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0," ")
                elif e == "Имя":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0," ")
                elif e == "Телефон":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0,"000-000")
                elif e == "Номер отдела":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0,"0")
                elif e == "Название отдела":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0," ")
                elif e == "Номер корпуса":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0,"0")
                elif e == "Должность":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0,"")
                elif e == "Улица":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0,"")
                elif e == "Дом":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0,"0")
                elif e == "Зарплата":
                    m = tk.Entry(window, entryStyle, width=10)
                    m.insert(0,"0")
                m.grid(row=len(dataBase) + 2, column=i)
                tkArray.append(m)
                i+=1
    flag = tk.IntVar()
    cb = tk.Checkbutton(window, buttonStyle, width=2, variable=flag)
    cb.grid(row=len(dataBase) + 2,column=i+1)
    cb.select()
    tkArray.append(flag)
    tkAll.append(tkArray)
    dataBase[len(dataBase)] = data
    
def RewriteBase(dataBase,tkAll):
    """
    Сохраняет в оперативную память базу данных, отредактированную в Entry Полях tkArray\n

    """
    i=0
    TD = { 
        "Фамилия":"",
        "Имя":"",
        "Телефон":000-000,
        "Номер отдела":0,
        "Название отдела":"",
        "Номер корпуса":0,
        "Должность":"",
        "Улица": "",
        "Дом": 0,
        "Зарпалата": 0,
        "Индекс":0
         }
    #Цикл пробегает по строке в tkAll и формирует элемент TD (один элемент в основной бд) из данных в tkinter-объектах из tkAll
    #Далее элемент или удаляется из основной бд через индекс (если галочка удаления была снята), или перезаписывает текущий элемент бд
    for tkArray in tkAll:
        for tkElement in tkArray:
            if i!=7:
                z = tkElement.get()
                if i==0:
                    TD["Фамилия"] = z
                elif i==1:
                    z = z.split(", ")
                    TD["Имя"] = z
                elif i==2:
                    TD["Телефон"] = int(z)
                elif i==3:
                    z = z.split(", ")
                    TD["Номер отдела"] = int(z)
                elif i==4:
                    TD["Название отдела"] = z
                elif i==5:
                    TD["Номер корпуса"] = int(z)
                elif i==6:
                    TD["Должность"] = z
                elif i==7:
                    TD["Улица"] = z
                elif i==8:
                    TD["Дом"] = int(z)
                elif i==9:
                    TD["Зарпалата"] = int(z)
            elif i==10:
                TD["Индекс"] = int(tkElement["text"])-1
            
            i+=1
        if tkArray[8].get() == 1:
            dataBase[TD["Индекс"]] = TD.copy()
        else:
            del dataBase[TD["Индекс"]]
        i=0
        
    db.ReIndexate(dataBase)



#--------------------------------------About app window------------------------------------#

def AboutW(mainWindow):
    """
    Открывает окно \"О приложении\"\n

    """
    aboutW = tk.Toplevel(mainWindow)
    
    HideMainWindow(mainWindow)
    
    aboutW.title("База данных - о приложении")
    aboutW.geometry("500x250+300+250")
    aboutW.minsize(280,160)
    aboutW.iconbitmap(workDir+"library\\icon.ico")
    #Переназначение кнопки закрыть: функция аналогична нажатию на кнопку "Назад"
    aboutW.protocol("WM_DELETE_WINDOW",lambda: ShowMainWindow(mainWindow,aboutW))
    
    frame = tk.Frame(aboutW,frameStyle)
    frame.pack(fill=tk.BOTH,expand=tk.YES)

    tk.Label(frame, labelStyle, text="Хорошая штука").grid(row=1, column=2)
    
    tk.Label(frame, labelStyle, text="О приложении:").grid(row=0,column=1,columnspan=2)
    tk.Button(frame, buttonStyle, text="Назад", command = lambda: ShowMainWindow(mainWindow,aboutW)).grid(row=0,column=0)

#--------------------------------------Stats window------------------------------------#
"""
Следующие функции описывают функционал окна подведения итогов (статистика)\n
"""   
def StatsW(mainWindow, dataBase):
    """
    Открывает окно подведения итогов (статистика)\n
    """
    statsW = tk.Toplevel(mainWindow)
    
    HideMainWindow(mainWindow)
    
    statsW.title("База данных - подведение итога (статистика)")
    statsW.geometry("520x250+300+250")
    statsW.minsize(520,230)
    statsW.iconbitmap(workDir+"library\\icon.ico")

    #Переназначение кнопки закрыть: функция аналогична нажатию на кнопку "Назад"
    statsW.protocol("WM_DELETE_WINDOW",lambda: ShowMainWindow(mainWindow,statsW))

    frame = tk.Frame(statsW, frameStyle)
    frame.pack(fill=tk.BOTH, expand=tk.YES)

    tk.Label(frame, labelStyle, text="Итог записан в папках graphics, output").pack()
    # вызов функции, формирующей статистику

    df = db.df
    d = db.d

    def stolb():
        list1 = d['НОМ_СОТР'].tolist()

        list2 = d['ЗАРПЛАТА'].tolist()
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).bar(list1, list2)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def hist():
        fig = Figure(figsize=(5, 4), dpi=100)

        fig.add_subplot(111).hist(df, bins=50)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def bv():
        list1 = d['ФАМ'].tolist()

        list2 = d['ЗАРПЛАТА'].tolist()
        list4 = d['НОМ_ОТД'].tolist()
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).scatter(list1, list2, list4)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    tk.Button(frame, buttonStyle, text="отчет1", width=20, command=lambda: db.pr_ot()).pack()
    tk.Button(frame, buttonStyle, text="отчет2", width=20, command=lambda: db.stat_ot()).pack()
    tk.Button(frame, buttonStyle, text="отчет3", width=20, command=lambda: db.sv_ot()).pack()
    tk.Button(frame, buttonStyle, text="graph1", width=20, command=lambda: stolb()).pack()
    tk.Button(frame, buttonStyle, text="graph2", width=20, command=lambda: hist()).pack()
    tk.Button(frame, buttonStyle, text="graph3", width=20, command=lambda: bv()).pack()


    tk.Button(frame, buttonStyle, text="Назад", command=lambda: ShowMainWindow(mainWindow, statsW)).pack(side= "left")


   
#--------------------------------------Save base window------------------------------------#
"""
Следующие функции описывают функционал окна выбора базы данных\n
"""
#директория для файла с сохраненной бд   
saveDir = workDir+"data\\GDS.pic"

def SaveFile(entry,dataBase):
    """
    Сохраняет dataBase в файл (функция SaveBase в dataBase.py) по пути, написанном в поле entry\n
    """
    global saveDir
    saveDir = entry.get()
    db.SaveBase(dataBase,saveDir)
    
def BrowseAndSaveFile(entry,dataBase,sbW):
    """
    Сохраняет dataBase в файл (функция SaveBase в dataBase.py) по пути, выбранном с помощью функции filedialog.asksaveasfilename()\n

    """
    global saveDir
    saveDir = filedialog.asksaveasfilename(initialdir=saveDir, filetypes=[("*.txt files", ".txt")])
    db.SaveBase(dataBase,saveDir)
    entry.delete(0,"end")
    entry.insert(0,saveDir)
    
def SaveBaseW(mainWindow,dataBase):
    """
    Открывает окно сохранения базы данных\n
    """
    sbW = tk.Toplevel(mainWindow)
    
    HideMainWindow(mainWindow)
    
    sbW.title("База данных  - сохранение базы данных")
    sbW.geometry("500x250+300+250")
    sbW.minsize(475,170)
    sbW.iconbitmap(workDir+"library\\icon.ico")
    #Переназначение кнопки закрыть: функция аналогична нажатию на кнопку "Назад"
    sbW.protocol("WM_DELETE_WINDOW",lambda: ShowMainWindow(mainWindow,sbW))
    
    frame = tk.Frame(sbW,frameStyle)
    frame.pack(fill=tk.BOTH,expand=tk.YES)

    text = tk.Label(frame, labelStyle, text="Введите полный путь к файлу:", width=30)
    entry = tk.Entry(frame, entryStyle, width=30)
    entry.insert(0,saveDir)
    
    text2 = tk.Label(frame, labelStyle, text="Или выберите его через проводник:", width=30)
    browseB = tk.Button(frame, buttonStyle, text="Выбрать", width=30, command=lambda: BrowseAndSaveFile(entry,dataBase,sbW))
    
    findB = tk.Button(frame, buttonStyle, text="Сохранить файл", width=15, command=lambda: SaveFile(entry,dataBase))
    closeB = tk.Button(frame, buttonStyle, text="Назад", width=5, command=lambda: ShowMainWindow(mainWindow,sbW))

    text.grid(row=0,column=1)
    entry.grid(row=1,column=1)
    findB.grid(row=1,column=2)

    text2.grid(row=2,column=1)
    browseB.grid(row=3,column=1)
    
    closeB.grid(row=0,column=0)
