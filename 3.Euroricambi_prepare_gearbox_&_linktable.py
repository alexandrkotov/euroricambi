#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Подготовка заготовок gearbox, linktable и списка ссылок для комментирования в каждом kit наборе 
http://www.euroricambi.com

Использован Python 3.2.5 (32 bit)
pip установлен через get-pip.py
Selenium установлен через pip install -U selenium
'''
import os
from os import listdir
import time
import urllib.request
import re
from datetime import datetime

#============== функции ====================================================
#функция возвращает количество схем по одной модели (разные модификации)
def count_num_in_one_kit(dirKit, kitFolderName):
    
    dirKitFolder = dirKit + "\\" + kitFolderName#fid[0]
    num_in_kit = 0

    gr1 = os.path.getsize(dirKitFolder + "\\gruppo1.png")
    if gr1 > 210:
        num_in_kit = num_in_kit + 1
    gr2 = os.path.getsize(dirKitFolder + "\\gruppo2.png")
    if gr2 > 210:
        num_in_kit = num_in_kit + 1
    gr3 = os.path.getsize(dirKitFolder + "\\gruppo3.png")
    if gr3 > 210:
        num_in_kit = num_in_kit + 1
    gr4 = os.path.getsize(dirKitFolder + "\\gruppo4.png")
    if gr4 > 210:
        num_in_kit = num_in_kit + 1
    gr5 = os.path.getsize(dirKitFolder + "\\gruppo5.png")
    if gr5 > 210:
        num_in_kit = num_in_kit + 1
    gr6 = os.path.getsize(dirKitFolder + "\\gruppo6.png")
    if gr6 > 210:
        num_in_kit = num_in_kit + 1
    gr7 = os.path.getsize(dirKitFolder + "\\gruppo7.png")
    if gr7 > 210:
        num_in_kit = num_in_kit + 1
    gr8 = os.path.getsize(dirKitFolder + "\\gruppo8.png")
    if gr8 > 210:
        num_in_kit = num_in_kit + 1
    gr9 = os.path.getsize(dirKitFolder + "\\gruppo9.png")
    if gr9 > 210:
        num_in_kit = num_in_kit + 1
    gr10 = os.path.getsize(dirKitFolder + "\\gruppo10.png")
    if gr10 > 210:
        num_in_kit = num_in_kit + 1
    gr11 = os.path.getsize(dirKitFolder + "\\gruppo11.png")
    if gr11 > 210:
        num_in_kit = num_in_kit + 1
    gr12 = os.path.getsize(dirKitFolder + "\\gruppo12.png")
    if gr12 > 210:
        num_in_kit = num_in_kit + 1

    #print("В наборе {} схемы".format(str(num_in_kit)))
    
    #print("gruppo1 {} байт".format(gr1))
    #print("gruppo2 {} байт".format(gr2))
    #print("gruppo3 {} байт".format(gr3))
    #print("gruppo4 {} байт".format(gr4))
    #print("gruppo5 {} байт".format(gr5))
    #print("gruppo6 {} байт".format(gr6))
    #print("gruppo7 {} байт".format(gr7))
    #print("gruppo8 {} байт".format(gr8))
    #print("gruppo9 {} байт".format(gr9))
    #print("gruppo10 {} байт".format(gr10))
    #print("gruppo11 {} байт".format(gr11))
    #print("gruppo12 {} байт".format(gr12))

    return num_in_kit


#функция определения имен всех kit наборов внутри папки kit
def get_kit_folders_name(info, file):
    #
    dib = "./kit"
    q = listdir(dib)
    fid = []
    inqq = ""
    outqq = ""
    kitfolders = 0
    if file == True:
        f = open('kit.csv', 'w')
    for a in q:
        inqq = a#str(a[:8]).strip()
        if inqq != outqq:
            fid.append(inqq)
            if file == True:
                f.write(inqq+'\n')
            outqq = inqq
            kitfolders = kitfolders + 1
    if file == True:
        f.close()
    if info == True:
        print("Определено {} наборов внутри папки kit".format(str(kitfolders)))
    fid.sort()
    return fid

#функция распределения сквозных номеров по наборам
def allocate_numbers_for_kits(fid):

    #fid = get_kit_folders_name("print")
    all_count = 0
    dirKit = os.path.join(r'kit')
    dic_kit_num = {}

    for i in range(len(fid)):
        arr_num = []
        kitFolderName = fid[i]
        cur_count = count_num_in_one_kit(dirKit, kitFolderName)

        for j in range(1, cur_count+1):
            cur_num = all_count + j
            arr_num.append(cur_num)

        dic_kit_num[kitFolderName] = arr_num
        all_count = all_count + cur_count
        #if cur_count == 12:
        #    print(kitFolderName)
        #print("{}: {}-{}".format(kitFolderName,str(all_count),str(cur_count)))
      
    print("Сквозные номера {} распределены по наборам, словарь dic_kit_num сформирован".format(str(all_count)))
    #print(dic_kit_num)
    return dic_kit_num

#функция возвращает словарь названий модификаций модели
def get_gruppo_name(table):
    
    dic_gruppo = {}
    ft1=open(table,'r')
    for line in ft1:
        #row_count = row_count + 1
        l = line.split(";")
        if l[8].strip() == "*" and l[9].strip() not in dic_gruppo.values():
            dic_gruppo[1] = l[9].strip()
        if l[10].strip() == "*" and l[11].strip() not in dic_gruppo.values():
            dic_gruppo[2] = l[11].strip()
        if l[12].strip() == "*" and l[13].strip() not in dic_gruppo.values():
            dic_gruppo[3] = l[13].strip()
        if l[14].strip() == "*" and l[15].strip() not in dic_gruppo.values():
            dic_gruppo[4] = l[15].strip()
        if l[16].strip() == "*" and l[17].strip() not in dic_gruppo.values():
            dic_gruppo[5] = l[17].strip()
        if l[18].strip() == "*" and l[19].strip() not in dic_gruppo.values():
            dic_gruppo[6] = l[19].strip()
        if l[20].strip() == "*" and l[21].strip() not in dic_gruppo.values():
            dic_gruppo[7] = l[21].strip()
        if l[22].strip() == "*" and l[23].strip() not in dic_gruppo.values():
            dic_gruppo[8] = l[23].strip()
        if l[24].strip() == "*" and l[25].strip() not in dic_gruppo.values():
            dic_gruppo[9] = l[25].strip()
        if l[26].strip() == "*" and l[27].strip() not in dic_gruppo.values():
            dic_gruppo[10] = l[27].strip()
        if l[28].strip() == "*" and l[29].strip() not in dic_gruppo.values():
            dic_gruppo[11] = l[29].strip()
        if l[30].strip() == "*" and l[31].strip() not in dic_gruppo.values():
            dic_gruppo[12] = l[31].strip()
    ft1.close()
    return dic_gruppo

#функция возвращает количество строк в table
def get_row_count(table):
    #
    row_count = 0
    ft2=open(table,'r')
    for line in ft2:
        row_count = row_count + 1    
    ft2.close()
    return row_count

#функция формирования pre_linktable
def make_pre_linktable(kitFolderName, dic_kit_num):

    dirKit = os.path.join(r'kit')
    dirKitFolder = dirKit + "\\" + kitFolderName
    #print("dirKitFolder = {}".format(dirKitFolder))

    table = dirKitFolder + "\\table.csv"
    pre_gearbox = dirKitFolder + "\\pre_gearbox.csv"
    pre_linktable = dirKitFolder + "\\pre_linktable.csv"


    arr_num = []
    arr_num = dic_kit_num[kitFolderName]
    block_count = len(arr_num)

    #читаем table, находим количество строк и названия модификаций модели
    dic_gruppo = {}
    row_count_block = 0
    row_count_block = get_row_count(table)    
    dic_gruppo = get_gruppo_name(table)
    #print(dic_gruppo)
    #формируем блоки модификаций и собираем в плоскую таблицу (разворачиваем)
    res_str = ""
    col = 0
    for b in range(1,block_count+1):
        #print(b)   
        ft=open(table,'r')
        for line in ft:
            l = line.split(";")#fig            ourno            partno    adtscod description      notes            qty              tp
            pref = str(b)+";"+l[0].strip()+";"+l[1].strip()+";"+l[2].strip()+";;"+l[3].strip()+";"+l[5].strip()+";"+l[6].strip()+";"+l[7].strip()
            if l[b+7+col].strip() == "*":
                res_str = res_str + pref + "\n"#";" + l[b+7+col].strip()+"\n"
        ft.close()
        col = col + 1
    #print(res_str)

    f=open(pre_linktable,'w')
    f.write(res_str)
    f.close()
    print("{} сформирован".format(pre_linktable))

#функция формирует pre_disable_href.csv
def make_pre_disable_href(kitFolderName, dic_kit_num):

    block_count = len(dic_kit_num[kitFolderName])
    #print("Блоков {}".format(block_count))
    dirKit = os.path.join(r'kit')
    dirKitFolder = dirKit + "\\" + kitFolderName

    pre_disable_href = dirKitFolder + "\\pre_disable_href.csv"
    pre_linktable = dirKitFolder + "\\pre_linktable.csv"
    #максимальная fig
    max_fig = 0
    f=open(pre_linktable,'r')
    for line in f:
        l = line.split(";")
        fig = int(l[1].strip())
        if fig > max_fig:
            max_fig = fig
    f.close()
    #print("max_fig = {}".format(str(max_fig)))

    hrefMax = []
    for x in range(1, max_fig + 1):
        hrefMax.append(x)

    #print(str(hrefMax))
    cur_num = 0
    prev_fig = 0
    #идея - сгенерировать максимальный массив от 1 до max_fig
    #собрать 12-ть массивов
    #вычесть из копии максимального массива каждый массив

    href1 = []
    href2 = []
    href3 = []
    href4 = []
    href5 = []
    href6 = []
    href7 = []
    href8 = []
    href9 = []
    href10 = []
    href11 = []
    href12 = []

    f=open(pre_linktable,'r')
    for line in f:
        l = line.split(";")
        num = int(l[0].strip())
        fig = int(l[1].strip())
        if num == 1:
            href1.append(fig)
        if num == 2:
            href2.append(fig)
        if num == 3:
            href3.append(fig)
        if num == 4:
            href4.append(fig)
        if num == 5:
            href5.append(fig)
        if num == 6:
            href6.append(fig)
        if num == 7:
            href7.append(fig)
        if num == 8:
            href8.append(fig)
        if num == 9:
            href9.append(fig)
        if num == 10:
            href10.append(fig)
        if num == 11:
            href11.append(fig)
        if num == 12:
            href12.append(fig)
    f.close()

    d1 = list(set(hrefMax)-set(href1))
    d1.sort()
    d2 = list(set(hrefMax)-set(href2))
    d2.sort()
    d3 = list(set(hrefMax)-set(href3))
    d3.sort()
    d4 = list(set(hrefMax)-set(href4))
    d4.sort()
    d5 = list(set(hrefMax)-set(href5))
    d5.sort()
    d6 = list(set(hrefMax)-set(href6))
    d6.sort()
    d7 = list(set(hrefMax)-set(href7))
    d7.sort()
    d8 = list(set(hrefMax)-set(href8))
    d8.sort()
    d9 = list(set(hrefMax)-set(href9))
    d9.sort()
    d10 = list(set(hrefMax)-set(href10))
    d10.sort()
    d11 = list(set(hrefMax)-set(href11))
    d11.sort()
    d12 = list(set(hrefMax)-set(href11))
    d12.sort()
    #print(str(d1))
    #print(str(d2))
    #print(str(d3))
    #print(str(d4))
    #print(str(d5))
    #print(str(d6))
    #print(str(d7))
    #print(str(d8))
    #print(str(d9))
    #print(str(d10))
    #print(str(d11))
    #print(str(d12))

    res_str = ""
    for j in range(1,block_count+1):
        #
        #print(j)
        if j == 1:
            res_str = res_str + str(j)+";"+str(d1).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 2:
            res_str = res_str + str(j)+";"+str(d2).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 3:
            res_str = res_str + str(j)+";"+str(d3).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 4:
            res_str = res_str + str(j)+";"+str(d4).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 5:
            res_str = res_str + str(j)+";"+str(d5).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 6:
            res_str = res_str + str(j)+";"+str(d6).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 7:
            res_str = res_str + str(j)+";"+str(d7).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 8:
            res_str = res_str + str(j)+";"+str(d8).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 9:
            res_str = res_str + str(j)+";"+str(d9).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 10:
            res_str = res_str + str(j)+";"+str(d10).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 11:
            res_str = res_str + str(j)+";"+str(d11).replace("[","").replace("]","").replace(" ","")+"\n"
        if j == 12:
            res_str = res_str + str(j)+";"+str(d12).replace("[","").replace("]","").replace(" ","")+"\n"
    #print(res_str)
    fh=open(pre_disable_href,'w')
    fh.write(res_str)
    fh.close()
    print("{} сформирован".format(pre_disable_href))

#функция формирует pre_gearbox.csv
def make_pre_gearbox_with_notes(kitFolderName):

    #задача - сформировать pre_gearbox
    # num - пока не сквозной
    # omegacode - пока пусто
    # brandname = brandname
    # series = model_name
    # specification = gruppo_name[X]
    # gearboxgroup = family_name
    # sourcedir - пробел
    # exceltool - пусто
    # notes - всё из файла notes.txt

    dirKit = os.path.join(r'kit')
    dirKitFolder = dirKit + "\\" + kitFolderName
    table = dirKitFolder + "\\table.csv"
    pre_gearbox = dirKitFolder + "\\pre_gearbox.csv"
    notes = ""
    notes_file = dirKitFolder + "\\notes.txt"
    notes_file_fix = dirKitFolder + "\\notes_fix.txt"
    #фиксим CR переносы в notes
    notes_b = bytearray()
    fnfix=open(notes_file_fix,'wb')
    fn=open(notes_file,'r')
    for line in fn:
        new = line.replace(";",",").strip()
        new_b = bytearray(new.encode('utf-8'))
        new_b.append(0x20)
        new_b.append(0x20)
        new_b.append(0x0A)
        #здесь надо к notes_b добавить new_b
        notes_b.extend(new_b)
    try:
        notes_b.pop()#удаляем последний LF
        print("Notes - вычищен от CR")
    except:
        print("Notes пустой")
    fnfix.write(notes_b)
    fnfix.close()
    fn.close()
    
    #при построчном чтении из файла, windows добавляет CR, поэтому
    #строку до и после note преобразовать в массивы байтов
    #собрать общий массив байтов (массив до + note + массив после)и в режиме wb записать в pre_gearbox.csv
    count_block = count_num_in_one_kit(dirKit, kitFolderName)
    #print("Блоков {}".format(count_block))
    gruppo_name = get_gruppo_name(table)
    #print(str(gruppo_name))

    res_str_pref = ""
    res_str_post = ""
    gearbox_b = bytearray()
    for i in range(1,count_block+1):
        num_block = i
        gruppo = gruppo_name[i]
        #print("num_block={}, gruppo={}".format(str(i),gruppo))               
        res_str_pref = str(num_block)+";;"+brandname+";"+model_name+";"+gruppo+";"+family_name+"; ;;"
        res_str_post = "\r\n"

        gearbox_b.extend(res_str_pref.encode('utf-8'))
        gearbox_b.extend(notes_b)
        gearbox_b.extend(res_str_post.encode('utf-8'))

    fg=open(pre_gearbox,'wb')
    fg.write(gearbox_b)
    fg.close()
    print("{} сформирован".format(pre_gearbox))


#функция формирует pre_gearbox.csv без Notes
def make_pre_gearbox(kitFolderName):

    #задача - сформировать pre_gearbox
    # num - пока не сквозной
    # omegacode - пока пусто
    # brandname = brandname
    # series = model_name
    # specification = gruppo_name[X]
    # gearboxgroup = family_name
    # sourcedir - пробел
    # exceltool - пусто
    # notes - НЕ ДОБАВЛЯЕМ!!!!

    dirKit = os.path.join(r'kit')
    dirKitFolder = dirKit + "\\" + kitFolderName
    table = dirKitFolder + "\\table.csv"
    pre_gearbox = dirKitFolder + "\\pre_gearbox.csv"
    notes = ""

    count_block = count_num_in_one_kit(dirKit, kitFolderName)
    #print("Блоков {}".format(count_block))
    gruppo_name = get_gruppo_name(table)
    #print(str(gruppo_name))

    res_str = ""

    for i in range(1,count_block+1):
        num_block = i
        try:
            gruppo = gruppo_name[i]
            #print("num_block={}, gruppo={}".format(str(i),gruppo))               
            res_str = res_str + str(num_block)+";;"+brandname+";"+model_name+";"+gruppo+";"+family_name+"; ;;\n"
        except:
            print("Дублирование gruppo в table.csv в наборе {}".format(kitFolderName))
            quit()


    fg=open(pre_gearbox,'w')
    fg.write(res_str)
    fg.close()
    print("{} сформирован".format(pre_gearbox))







#===================================================================================
tStart = time.time()

fid = get_kit_folders_name(True,False)#вывод на экран, вывод в файл
dic_kit_num = allocate_numbers_for_kits(fid)

print("---")

brandname = "DAF"
#в цикле считываем аргументы
f=open(os.path.join(r'models_link.csv'))
fid_index = 0
for line in f:
    l = line.split(";")
    family_name = l[1].strip()
    model_name = l[2].strip()
    kitFolderName = fid[fid_index]
    fid_index = fid_index + 1
    #print("brandname={}, family_name={}, model_name={}, kitFolderName={}".format(brandname,family_name, model_name,kitFolderName))
    print("\n{}, {}, {}, {}".format(kitFolderName,brandname,family_name, model_name))
    make_pre_linktable(kitFolderName, dic_kit_num)
    make_pre_disable_href(kitFolderName, dic_kit_num)
    make_pre_gearbox(kitFolderName)



#задачи для 4-го скрипта:
# - собрать общий gearbox (сквозные номера), строки через массив байт
# - собрать общий linktable (сквозные номера)
# - кросс на товары адтс
# - сформировать base64 и jpg
# - пустую базу скопировать под нужным именем
# - в базу загрузить gerabox, linktable и infobase

print("\nВремя выполнения: %f сек." % (time.time()-tStart))
