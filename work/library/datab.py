# -*- coding: utf-8 -*-


import tkinter as tk
import pickle as pk

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# os.chdir("C:/Users/advor/work/")

from pathlib import Path
path = Path.cwd()
workDir = str(path.parent.absolute())


df = pd.read_excel(workDir+'\\data\\python_hw2_1.xlsx', usecols=['ДОЛЖНОСТЬ', 'ЗАРПЛАТА'])
d = pd.read_excel(workDir+'\\data\\python_hw2_1.xlsx')
def sv_ot():
    df1 = df.pivot_table(values='ЗАРПЛАТА', columns='ДОЛЖНОСТЬ')
    my_file = open(workDir+"output/File3.txt", "w+")
    my_file.write(str(df1))
    my_file.close()
    return 'result in output'

def pr_ot():
    my_file = open(workDir+"output/File1.txt", "w+")
    my_file.write(str(d))
    my_file.close()
    return 'result in output'

def stat_ot():
    my_file = open(workDir+"output/File2.txt", "w+")
    u = pd.DataFrame(d)
    s = u.describe()
    for i in d:
        ss = u[i].value_counts()
        my_file.write(str(ss))
        ss = []
    my_file.write(str(s))
    my_file.close()
    return 'result in output'

def stolb():
    list1 = d['НОМ_СОТР'].tolist()
    list2 = d['ЗАРПЛАТА'].tolist()
    plt.bar(list1, list2)
    plt.savefig(workDir+'graphics/1.png')
    return 'result in graphics'

def hist():
    df.hist(bins=50, figsize=(15, 15))
    plt.savefig(workDir+'graphics/2.png')
    return 'result in graphics'

def cat():
    d.boxplot(column='НОМ_ОТД', by='ДОЛЖНОСТЬ')
    plt.savefig(workDir+'graphics/3.png')
    return 'result in graphics'

def bv():
    list1= d['ФАМ'].tolist()
    list2 = d['ЗАРПЛАТА'].tolist()
    list4 = d['НОМ_ОТД'].tolist()
    plt.scatter(list1, list2, list4)
    plt.savefig(workDir+'graphics/4.png')
    return 'result in graphics'


def ReadBase(dataBase, fName):
    """
    Считывает базу данных из файла fName и записывает в оперативную память базу данных в виде словаря словарей\n

    """
    try:
        f = open(fName, "rb")
    except:
        return
    data = pk.load(f)
    dataBase.clear()
    x = 0
    for key in data:
        dataBase[x] = data[key].copy()
        x += 1

    f.close()



def DelBaseElement(dataBase, surname):
    """
    Удаляет конкретного сотрудника из базы данных dataBase по фамилии surname\n

    """
    for base in dataBase:
        if dataBase[base]["Фамилия"] == surname:
            dataBase.pop(base)
            return
    return None


def ReIndexate(dataBase):
    """
    Выполняет переиндексацию словарей в базе данных dataBase\n

    """
    i = 0
    tempBase = {}
    for base in dataBase:
        tempBase[i] = dataBase[base].copy()
        tempBase[i]["Индекс"] = i
        i += 1
    dataBase.clear()
    for i in range(0, len(tempBase)):
        dataBase[i] = tempBase[i].copy()


def AddBaseElement(dataBase, surname, name, tel, no, nazv, nk, dolzn, ul, dom, sall):
    """
    Добавляет конкретного сотрудника из базы данных dataBase
    """
    data = {
        "Фамилия": surname,
        "Имя": name,
        "Телефон": int(tel),
        "Номер отдела": int(no),
        "Название отдела": nazv,
        "Номер корпуса": int(nk),
        "Должность": dolzn,
        "Улица": ul,
        "Дом": int(dom),
        "Зарплата": int(sall)
    }
    dataBase[len(dataBase)] = data


def ChangeBaseElement(dataBase, index, newsurname, newname, newtel, newno, newnazv, newnk, newdolzn, newul, newdom, newsall):
    """
    Изменяет конкретный элемент из базы данных dataBase c индексом index.

    """
    dataBase[int(index)] = {
        "Фамилия": newsurname,
        "Имя": newname,
        "Телефон": int(newtel),
        "Номер отдела": int(newno),
        "Название отдела": newnazv,
        "Номер корпуса": int(newnk),
        "Должность": newdolzn,
        "Улица": newul,
        "Дом": int(newdom),
        "Зарплата": int(newsall)
    }

def SaveBase(dataBase, f):
    """
    Сохраняет dataBase в файл

    """
    try:
        SaveFile = open(f, "wb")
    except:
        return

    pk.dump(dataBase, file=SaveFile)
    SaveFile.close()

def base2():
    file = pd.read_excel('./data/python_hw2_2.xlsx')
    return file

