#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Сборка общих gearbox и linktable, создание base64, загрузка в пустую БД SQLite3 
http://www.euroricambi.com

Время выполнения: 700.718618 сек.

настройки внизу скрипта

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
import shutil
import sqlite3
import base64

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
    
    #при построчном чтении из файла, винда добавляет CR, поэтому
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

#функции текущего скрипта===========================================================

def get_cross_dic(filename):

    cross_dic = {}
    brand=filename.split("_")[1][:-4]
    f=open(os.path.join(filename))
    qq = 0
    for line in f:
        qq = qq +1
        l=line.split(";")
        art=l[0].strip()
        adts=l[1].strip()
        rus=l[2].replace(";","").strip()
        #print("Строка {}".format(str(qq)))
        brand=l[3].strip()
        val=adts+";"+rus+";"+brand
        cross_dic[art]=val
    f.close()
    #print(cross_dic_Euroricambi['95531091'])
    print("Словарь {} кросс-номеров {} - сформирован".format(len(cross_dic.keys()),brand))
    return cross_dic



def compile_linktable():
    
    dirKit = os.path.join(r'kit')
    linktable = os.path.join(r'linktable_no_cross.csv')
    pl=open(linktable,'w')
    pl.close()

    #в цикле считываем аргументы
    f=open(os.path.join(r'models_link.csv'))
    fid_index = 0
    all_row = 0
    for line in f:
        l = line.split(";")
        family_name = l[1].strip()
        model_name = l[2].strip()
        kitFolderName = fid[fid_index]
        dirKitFolder = dirKit + "\\" + kitFolderName
        pre_gearbox = dirKitFolder + "\\pre_gearbox.csv"
        pre_disable_href = dirKitFolder + "\\pre_disable_href.csv"
        pre_linktable = dirKitFolder + "\\pre_linktable.csv"
    
        fid_index = fid_index + 1
        #print("{}, {}, {}, {}, {}".format(kitFolderName,brandname,family_name, model_name, dic_kit_num[kitFolderName]))

        #сквозные номера по набору
        block_nums = dic_kit_num[kitFolderName]
        append_num = block_nums[0]-1
        #print("\nДобавить {}".format(append_num))

        #читаем текущий linktable и в первой колонке к номеру добавляем append_num
        #и собираем общий linktable
        res_str = ""
        pf=open(pre_linktable,'r')
        for pline in pf:
            pl=pline.split(";")
        
            pnum = int(pl[0].strip())+append_num
            pfig = pl[1].strip()
            pourno = pl[2].strip()
            ppartno = pl[3].strip()
            padts = ""
            pdescription = pl[5].strip()
            pnotes = pl[6].strip()
            pqty = pl[7].strip()
            ptp = pl[8].strip()

            res_str = res_str + str(pnum)+";"+pfig+";"+pourno+";"+ppartno+";;"+pdescription+";"+pnotes+";"+pqty+";"+ptp+"\n"
            all_row = all_row + 1
        pf.close()
        pl=open(linktable,'a')
        pl.write(res_str)
        pl.close()
    print("Общий linktable_no_cross.csv собран, всего строк {}".format(str(all_row)))

def cross_linktable():

    linktable_no_cross = os.path.join(r'linktable_no_cross.csv')
    linktable_eng = os.path.join(r'linktable_eng.csv')
    linktable_rus = os.path.join(r'linktable_rus.csv')
    print("Обработка {}".format(linktable_no_cross))
    res_str_eng = ""
    res_str_rus = ""

    count_row = 0
    f=open(linktable_no_cross,'r')
    for line in f:

        count_row = count_row + 1
        if count_row%1000 == 0:
            print("Обработано {} тысяч строк {}".format(str(count_row//1000),linktable_no_cross))
        l=line.split(";")

        num = l[0].strip()
        fig = l[1].strip()
        ourno = l[2].strip()
        partno = l[3].strip()
        adts = ""
        description_rus = ""
        try:
            row_dic = cross_dic_Euroricambi[ourno].split(";")
            adts = row_dic[0].strip()
            description_rus = row_dic[1].strip()
        except:
            try:
                row_dic = cross_dic_ZF[partno].split(";")
                adts = row_dic[0].strip()
                description_rus = row_dic[1].strip()
            except:
                adts = ""
                description_rus = ""
        description = l[5].strip()
        notes = l[6].strip()
        qty = l[7].strip()
        tp = l[8].strip()
        res_str_eng = res_str_eng + num+";"+fig+";"+ourno+";"+partno+";"+adts+";"+description+";"+notes+";"+qty+";"+tp+"\n"
        if description_rus != "":
            res_str_rus = res_str_rus + num+";"+fig+";"+ourno+";"+partno+";"+adts+";"+description_rus+";"+notes+";"+qty+";"+tp+"\n"
        else:
            res_str_rus = res_str_rus + num+";"+fig+";"+ourno+";"+partno+";"+adts+";"+description+";"+notes+";"+qty+";"+tp+"\n"
    f.close()
    print("Всего обработано {} строк {}".format(str(count_row),linktable_no_cross))

    print("Запись файлов eng и rus")
    f=open(linktable_eng,'w')
    f.write(res_str_eng)
    f.close()
    print("{} собран".format(linktable_eng))

    f=open(linktable_rus,'w')
    f.write(res_str_rus)
    f.close()
    print("{} собран".format(linktable_rus))

    
#вычистить функцию от мусора!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def compile_gearbox(pref):

    dirKit = os.path.join(r'kit')
    #gearbox = os.path.join(r'gearbox.csv')
    gearbox_s = os.path.join(r'gearbox_separator.csv')

    #pg=open(gearbox,'wb')
    #pg.close()

    pgs=open(gearbox_s,'w')
    pgs.close()
    
    #в цикле считываем аргументы
    f=open(os.path.join(r'models_link.csv'))
    fid_index = 0
    all_row = 0
    for line in f:
        l = line.split(";")
        family_name = l[1].strip()
        model_name = l[2].strip()
        kitFolderName = fid[fid_index]
        dirKitFolder = dirKit + "\\" + kitFolderName
        pre_gearbox = dirKitFolder + "\\pre_gearbox.csv"
        notes_file = dirKitFolder + "\\notes.txt"
        #фиксим CR переносы в notes
        notes_b = bytearray()
        notes_s = ""
        fn=open(notes_file,'r')
        for line in fn:
            new = line.replace(";",",").strip()
            if notes_s == "":
                notes_s = notes_s +  new
            else:
                notes_s = notes_s + "sep@r@t0r" + new
            new_b = bytearray(new.encode('utf-8'))
            new_b.append(0x20)
            new_b.append(0x20)
            new_b.append(0x0A)
            notes_b.extend(new_b)
        fn.close()
        try:
            notes_b.pop()#удаляем последний LF
            #print("Notes - вычищен от CR")
        except:
            #print("Notes пустой")
            pass
        fid_index = fid_index + 1

        #сквозные номера по набору
        block_nums = dic_kit_num[kitFolderName]
        append_num = block_nums[0]-1
        #print("\nДобавить {}".format(append_num))
        #print("{}, {}, {}, {}, {}".format(kitFolderName,brandname,family_name, model_name, dic_kit_num[kitFolderName]))

        #читаем текущий gearbox, в первой колонке к номеру добавляем append_num
        #и собираем общий gearbox
        res_str_pref = ""
        res_str_post = ""
        res_str = ""
        gearbox_b = bytearray()
        pg=open(pre_gearbox,'r')
        for pline in pg:
            pl=pline.split(";")
            num = int(pl[0].strip()) + append_num
            omegacode = pref+str((10000 + num))[1:]
            brandname = pl[2].strip()
            series = pl[3].strip()
            specification = pl[4].strip()
            gearboxgroup = pl[5].strip()
            sourcedir = " "
            exceltool = ""
            #notes = pl[8].strip()#тут проблема, винда добавит CR
            #print("num={}, omegacode={}, brandname={}, series={}, specification={}, gearboxgroup={}".format(num,omegacode,brandname,series,specification,gearboxgroup))

            res_str_pref = str(num)+";"+omegacode+";"+brandname+";"+series+";"+specification+";"+gearboxgroup+"; ;;"
            res_str_post = "\r\n"
            res_str = res_str + res_str_pref+notes_s+"\n"
        
            gearbox_b.extend(res_str_pref.encode('utf-8'))
            gearbox_b.append(0x20)
            gearbox_b.append(0x20)
            gearbox_b.extend(notes_b)
            gearbox_b.extend(res_str_post.encode('utf-8'))
        pg.close()
        #pg=open(gearbox,'ab')
        #pg.write(gearbox_b)
        #pg.close()

        pgs=open(gearbox_s,'a')
        pgs.write(res_str)
        pgs.close()
    print("{} собран".format(gearbox_s))

#функция конвертации картинки в base64
def convert(image, dib):
    f=open(dib+"/"+image+".jpg", "rb")
    data = f.read()
    f.close()
    string = base64.b64encode(data)

    f=open(dib+"/"+image+"xBASE64.html", "w")

    f.write('<img src="data:image/jpg;base64,')
    f.close()
    f=open(dib+"/"+image+"xBASE64.html", "ab")

    f.write(string)
    f.close()
    f=open(dib+"/"+image+"xBASE64.html", "a")
    f.write('" style="position: absolute; top: 0px; left: 0px;">\n')
    f.close()
    #терерь открыть старый файл и со второй строки дописать в новый
    f=open(dib+"/"+image+".html", "r")
    body = f.readlines()
    f.close()

    f=open(dib+"/"+image+"xBASE64.html", "a")
    for l in body[1:]:
        f.write(l)
    f.close()


def prepare_infobase(pref):

    reg_ex_row = re.compile(r'div id="anonymous_element_\d+" class="ClassUnSelected" ([A-Za-z0-9-=\":;_>< ]*)')
    reg_ex_num = re.compile(r'>([0-9]+)<')
    dirKit = os.path.join(r'kit')
    #создаем директорию 
    infobase = os.path.join(r'infobase')
    if not os.path.exists(infobase):  
        os.makedirs(infobase)

    for k in range(len(fid)):#(1):#
        kitFolderName = fid[k]
        dirKitFolder = dirKit + "\\" + kitFolderName
    
        tavola9 = dirKitFolder + "\\tavola9.jpg"
        tavola_print = dirKitFolder + "\\tavola_print.jpg"
        raw_map = dirKitFolder + "\\raw_map.txt"
        pre_disable_href = dirKitFolder + "\\pre_disable_href.csv"

        f=open(raw_map,'r')
        ss=f.readlines()
        f.close()
        s=ss[3]
        #print(s)
        #словарь комментариев ссылок
        dic_disable_href={}
        fd=open(pre_disable_href,'r')
    
        for lined in fd:
            ld=lined.split(";")
            cur_row=int(ld[0].strip())
            linksForDisable=ld[1].strip()
            arrLincs = linksForDisable.split(",")
            dic_disable_href[cur_row]=arrLincs
        fd.close()
        #print(dic_disable_href)      
        nums = dic_kit_num[kitFolderName]
        #print(nums)
        for j in range(len(nums)):

            arrLincs = dic_disable_href[j+1]
            #print(arrLincs)
            divlist = []
            linknum=[]
        
            fileName = infobase+"\\"+pref+str((10000 + nums[j]))[1:]
            print("\n{} -> {}".format(kitFolderName,fileName))
            shutil.copy(tavola9, fileName+'.jpg')
            shutil.copy(tavola_print, fileName+'rep.jpg')

            f2 = open(fileName+'.html', 'w')
            f2.write('<img src="'+fileName+'.jpg" style="position: absolute; top: 0px; left: 0px;">\n')
        
            divlist = reg_ex_row.findall(s)
            #print(divlist)
            for i in divlist:
                qq = i.replace('6pt','12pt').replace('7pt','12pt').replace('8pt','12pt').replace('9pt','12pt').replace('10pt','12pt').replace('11pt','12pt')
                #print(qq)
                linknum = reg_ex_num.findall(qq)
                if int(linknum[0]) > 9:
                    qq2 = '<a href="#'+linknum[0]+'" '+qq+'/a>\n'
                else:
                    qq2 = '<a href="#0'+linknum[0]+'" '+qq+'/a>\n'

                if linknum[0] in arrLincs:
                    qq2 = "<!--\n"+qq2+"-->\n"
                f2.write(qq2)
            if linksForDisable != "":
                print("Сформировано {} ссылок, из них {} закоментировано".format(len(divlist),len(arrLincs)))
            else:
                print("Сформировано {} ссылок".format(len(divlist)))
            print("Созданы файлы:")
            print("  таблица ссылок               {}.html".format(fileName))
            print("  картинка большая для подбора {}.jpg".format(fileName))
            print("  картинка малая для печати    {}.jpg".format(fileName))
            f2.close()
    #добавляем base64
    #dib = "./infobase"
    dib = os.path.join(r'infobase')
    q = listdir(dib)
    fid2 = []
    inqq = ""
    outqq = ""
    for a in q:
        inqq = str(a[:8]).strip()
        if inqq != outqq:
            fid2.append(inqq)
            outqq = inqq
    for img in fid2:
        convert(img,dib)
        print("{} -> base64".format(img))
    print("Создано {} html файлов со встроенными изображениями".format(len(fid2)))

#функция вставки одной строки в таблицу infobase
def insert_infobase(gb, cursor):
    
    dib = os.path.join(r'infobase')
    num = int(gb[4:])
    html64_path = dib+"/"+gb+"xBASE64.html"
    jpgrep_path = dib+"/"+gb+"rep.jpg"

    f = open(html64_path, 'rb')
    html64_bin = f.read()
    f.close()

    f = open(jpgrep_path, 'rb')
    jpgrep_bin = f.read()
    f.close()
    cursor.execute("INSERT INTO infobase (num,html,jpg) VALUES (?,?,?)", (num, sqlite3.Binary(html64_bin),sqlite3.Binary(jpgrep_bin),))
           

#функция вставки всех строк из gearbox.csv  в таблицу gearbox
def insert_gearbox(cursor, conn):

    gearbox_s = os.path.join("gearbox_separator.csv")
    fg=open(gearbox_s,'r')
    row = 0
    for line in fg:
        l=line.split(";")
        num = l[0].strip()#int(l[0].strip())
        omegacode = l[1].strip()
        brandname = l[2].strip()
        series = l[3].strip()
        specification = l[4].strip()
        gearboxgroup = l[5].strip()
        sourcedir = " "
        exceltool = " "
        #notes = l[8].strip()#"test"#l[8].strip().replace("sep@r@t0r","\n")
        notes = l[8].strip().replace("sep@r@t0r","\n")
        #print(notes)
        cursor.execute("INSERT INTO gearbox (num,omegacode,brandname,series,specification,gearboxgroup,sourcedir,exceltool,notes) VALUES (?,?,?,?,?,?,?,?,?)", (num, omegacode, brandname, series, specification, gearboxgroup, sourcedir, exceltool, notes,))
        row = row + 1
        #conn.commit()
        #print("{} - Ok".format(omegacode))
    #
    conn.commit()
    fg.close()
    print("В таблицу gearbox добавлено {} записей".format(str(row)))
    
#функция вставки всех строк из linktable.csv  в таблицу linktable
def insert_linktable(linktable_filename, cursor, conn):

    linktable = os.path.join(linktable_filename)
    fl=open(linktable,'r')
    row = 0
    for line in fl:
        l=line.split(";")
        num = l[0].strip()
        fig = l[1].strip()
        ourno = l[2].strip()
        partno = l[3].strip()
        adtscod = l[4].strip()
        description = l[5].strip()
        notes = l[6].strip()
        qty = l[7].strip()
        tp = l[8].strip()
        #print(num)
        cursor.execute("INSERT INTO linktable (num,fig,ourno,partno,adtscod,description,notes,qty,tp) VALUES (?,?,?,?,?,?,?,?,?)", (num, fig, ourno, partno, adtscod, description, notes, qty, tp,))
        row = row + 1
        #conn.commit()
        #print("{} - Ok".format(omegacode))
    #
    conn.commit()
    fl.close()
    print("В таблицу linktable добавлено {} записей из {}".format(str(row), linktable_filename))

#обертка для всех вставок в БД
def insert_SQL3(dbname):
    
    db_blank = os.path.join("no_password_blank.sch")
    db_eng = os.path.join(dbname+"_ENG.sch")
    db_rus = os.path.join(dbname+"_RUS.sch")

    shutil.copy(db_blank, db_eng)

    #dib = "./infobase"
    dib = os.path.join(r'infobase')
    #print(dib)
    q = listdir(dib)
    #print(q)
    fid3 = []
    inqq = ""
    outqq = ""

    for a in q:
        inqq = str(a[:8]).strip()
        if inqq != outqq:
            fid3.append(inqq)
            outqq = inqq
        
    if not os.path.exists(db_eng):
        print("База данных не обнаружена")

    conn = sqlite3.connect(db_eng)
    cursor = conn.cursor()
    j = 0
    for i in fid3:
        insert_infobase(i,cursor)
        j = j + 1
    conn.commit()
    print("В таблицу infobase добавлено {} записей".format(str(j)))

    insert_gearbox(cursor, conn)
    conn.close()

    shutil.copy(db_eng, db_rus)
    print("{} скопирована в {}".format(db_eng, db_rus))

    conn = sqlite3.connect(db_eng)
    cursor = conn.cursor()
    print("ENG")
    insert_linktable("linktable_eng.csv", cursor, conn)
    conn.close()

    conn = sqlite3.connect(db_rus)
    cursor = conn.cursor()
    print("RUS")
    insert_linktable("linktable_rus.csv", cursor, conn)
    conn.close()

#функция возвращает максимальный номер схемы в текущем наборе
def max_num(dic_kit_num):

    max_num = 0
    all_nums = list(dic_kit_num.values())

    for i in range(len(all_nums)):
        cur_nums = all_nums[i]    
        for j in range(len(cur_nums)):
            cn = int(cur_nums[j])
            if cn > max_num:
                max_num = cn
    return str(max_num)

#===================================================================================
tStart = time.time()

fid = get_kit_folders_name(True,False)#вывод на экран, вывод в файл
dic_kit_num = allocate_numbers_for_kits(fid)

brandname = "DAF"
pref="AXDF"
dbname="no_password_DAF_AXLE_"+(max_num(dic_kit_num))+"_NOTES"

print("---")
cross_dic_Euroricambi = get_cross_dic("cross_Euroricambi.csv")
cross_dic_ZF = get_cross_dic("cross_DAF.csv")#("cross_ZF.csv")
print("---")
compile_linktable()
cross_linktable()
compile_gearbox(pref)
prepare_infobase(pref)
insert_SQL3(dbname)

print("\nВремя выполнения: %f сек." % (time.time()-tStart))
