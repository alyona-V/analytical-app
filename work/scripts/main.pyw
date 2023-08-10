"""
Этот скрипт является стартовой точкой программы - ее главном окном.\n

"""
import sys
from pathlib import Path
path = Path.cwd()
workDir = str(path.parent.absolute())

try:
    sys.path.insert(0,workDir+"library")
    import library.graphics as gr

except:
    workDir = "../"
    sys.path.insert(0,workDir+"library")
    from library import graphics as gr


import tkinter as tk

path = Path.cwd()
workDir = str(path.parent.absolute())+'\\'

gr.workDir = workDir
gr.db.workDir = workDir

#загрузка настроек графики из setting.ini
gr.parseUI()

dataBase = {}
#загрузка бд в оперативную память
gr.db.ReadBase(dataBase, workDir+"data\\GDS.pic")

mainWindow = tk.Tk()
mainWindow.title("База данных ")
mainWindow.geometry("700x250+300+250")
mainWindow.minsize(700,160)
mainWindow.iconbitmap(workDir+"library\\icon.ico")

frame= tk.Frame(mainWindow,gr.frameStyle)
frame.pack(fill=tk.BOTH,expand=tk.YES)

tk.Label(frame,gr.labelStyle, text="Выберите функцию для работы с базой данных").grid(row=0,column=0,columnspan=3)

findB = tk.Button(frame, gr.buttonStyle, text="Выбрать базу данных",width=20,
                  command = lambda: gr.FindPathW(mainWindow,dataBase))
findB.grid(row=1,column=0)
  
showB = tk.Button(frame, gr.buttonStyle, text="Показать/Редактировать базу данных",width=35,
                  command = lambda: gr.DataBaseW(mainWindow, dataBase, dataBase))
showB.grid(row=1,column=1)

statsB = tk.Button(frame,gr.buttonStyle, text="Отчет", width=20,
                  command = lambda: gr.StatsW(mainWindow,dataBase))
statsB.grid(row=1,column=2)

flushB = tk.Button(frame,gr.buttonStyle, text="Сбросить базу данных",width=20, 
                   command = dataBase.clear)
flushB.grid(row=2,column=0)

saveB = tk.Button(frame,gr.buttonStyle, text="Сохранить базу данных в файл",width=35,
                  command = lambda: gr.SaveBaseW(mainWindow,dataBase))
saveB.grid(row=2, column=1)

infoB = tk.Button(frame,gr.buttonStyle, text="О приложении", width=20,
                  command = lambda: gr.AboutW(mainWindow))
infoB.grid(row=2,column=2)

closeAppB = tk.Button(frame,gr.buttonStyle, text="Выйти из приложения",width=20,
                      command = lambda: mainWindow.quit())
closeAppB.grid(row=3,column=2)     

mainWindow.mainloop()
