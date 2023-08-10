import pickle
import pandas
from library import datab


def base1():
    fields = []
    file = pandas.read_excel("C:/Users/advor/work/data/python_hw2_2.xlsx", sheet_name='Лист1')
    for col in file:
        fields.append(col)
    surname = file['Фамилия'].tolist()
    w1 = []
    y = 0
    for i in surname:
        globals()[i] = []
        for j in fields:
            r = file[j].values[y]
            globals()[str(i)].append(r)
        w1.append(globals()[str(i)])
        y += 1


# Создаем списко словарей
    w2 = [dict(zip(fields, x)) for x in w1]
# Создаем словарь словарей
    w3 = dict(zip(surname, w2))
    return w3

pickle.DEFAULT_PROTOCOL
data1 = base1()
selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)
# открываем файл для записи
output = open('GDS.pic', 'wb')
pickle.dump(data1, output)
# список запишем по протоколу 4
pickle.dump(selfref_list, output, 4)
# закрываем файл
output.close()
