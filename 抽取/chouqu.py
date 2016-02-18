#import time

def readtxt(road):
    #读取文件
    data1 = open(road,'r',encoding= 'utf-8').readlines()
    new_data = []
    for i in data1:
        if i[-1] == '\n':#去掉回车符号
            i = i[0:-1]
        new_data.append(i)
    return new_data

def word_tag_fliter(data):
    #留下tag里面有的词性
    tag = readtxt('cixing.txt')
    #print(new_tag)
    for i in range(len(data)):
        temp = data[i].split()
        if len(temp) == 0:
            pass
        else:
            for j in range(len(temp)):
                h = temp[j].split('/')
                if len(h) == 2:
                    if h[1] not in tag:
                        temp[j] = ' '
        data[i] = ' '.join(temp)
    return data

def tab_flitter(data,num):
    #过滤空行
    new_data = []
    for i in range(len(data)):
        if len(data[i]) <= num:
            pass
        else:
            new_data.append(data[i])
    return new_data

def word_seq_find(seq):
    tag_break = ['wj','wt','ww']
    temp = seq.split()
    for i in range(len(temp)):
        hh = temp[i].split('/')
        if len(hh) == 2:
            if hh[1] in tag_break:
                temp[i] = ' ****** '
    seq = ' '.join(temp)
    return seq
#________________________________________________
def fix(fix_array,k):
    if len(fix_array) == 0:
            pass
    else:
        if k == 0:
            for i in range(len(fix_array)):
                fix_array[i].append(1)
        else:
            if len(fix_array) == 1:
                fix_array[0].append(1)
            else:
                for i in range(len(fix_array)):
                    if i == len(fix_array)-1:
                        fix_array[i].append(k)
                    else:
                        for j in range(i+1,len(fix_array)+1):
                            if j == len(fix_array):
                                fix_array[i].append(k)
                                #print(fix_array[i])
                                break
                            else:
                                if fix_array[i][0] != fix_array[j][0]:
                                    fix_array[i].append(fix_array[j][0])
                                    #print(fix_array[i])
                                    break
    return fix_array

                    
def drop(data):
    #去掉重复项
    new_data = []
    for i in range(len(data)):
        if data[i] not in data[i+1:]:
            new_data.append(data[i])
    return new_data

def fix2(data,k):
    arr = []
    arr2 = []
    for i in range(len(data)):
        arr.append(data[i][0])
        arr2.append(data[i][2])   
    #print(max(arr))
    for i in range(len(data)):
        if data[i][0] == min(arr):
            #print(type(data[i][0]))
            data[i][0] = 0
    for i in range(len(data)):
        if data[i][2] == max(arr2):
            #print('hh')
            data[i][2] = k
    return data
def fix3(data):
    if len(data) >= 2:
        data[len(data)-2][2] = data[len(data)-1][0]
        return data
    else:
        return data
       
#_______________________________________________    
def gety_seq(seq,city):
    temp = seq.split('******')
    #print(temp)
    temp = tab_flitter(temp, 2)
    fix_array = []
    result = {}
    #print(seq)
    for i in range(len(temp)):
        if 'zzzz' in temp[i]:
            #print(temp[i])
            new_temp = temp[i].split()
            #print(new_temp)
            for j in range(len(new_temp)):
                hh = new_temp[j].split('/')
                if len(hh) == 2:
                    if hh[1] =='zzzz':
                        a = [i,hh[0]]
                        fix_array.append(a)
    #[[0, '纽约'], [12, '纽约'], [16, '纽约'], [28, '纽约'], [47, '纽约'], [81, '纽约'], [87, '纽约']]
    #print(fix_array)
    #print(len(temp))
    fix_array = drop(fix_array)
    fix_array = fix(fix_array,len(temp))
    fix_array = fix2(fix_array,len(temp))
    #fix_array = fix3(fix_array)
    #print(fix_array)
    if len(fix_array) == 0:
        pass
    else:
        if len(fix_array) == 1:
            result[fix_array[0][1]] = temp
        else:
            for k in range(len(fix_array)):
                if k == 0:
                    result[fix_array[0][1]] = temp[fix_array[0][0]:fix_array[0][2]]###
                else:
                    if k == len(fix_array)-1:
                        getseq = temp[fix_array[k][0]:]
                        if fix_array[k][1] in result:
                            for item in range(len(getseq)):
                                result[fix_array[k][1]].append(getseq[item])
                        else:
                            result[fix_array[k][1]] = getseq
                    else:
                        getseq = temp[fix_array[k][0]:fix_array[k][2]]##
                        if fix_array[k][1] in result:
                            for item in range(len(getseq)):
                                result[fix_array[k][1]].append(getseq[item])
                        else:
                            result[fix_array[k][1]] = getseq
    #print(result)
    return result

def scence(data):
    #非热门景点标记成kkkkkk
    scence = readtxt('attraction.txt')#景点矩阵
    for i in range(len(data)):
        temp = data[i].split('******')
        if len(temp) > 0:
            for j in range(len(temp)):
                h = temp[j].split()
                if len(h) > 0:
                    for k in range(len(h)):
                        aa = h[k].split('/')
                        if len(aa) == 2:
                            if aa[1] == 'zzzz' and aa[0] not in scence:
                                h[k] = '/'.join([aa[0],'kkkkkk'])
                temp[j] = ' '.join(h)
        data[i] = ' ****** '.join(temp)
    return data

def getseqmian(data,city,rounte):
    data = word_tag_fliter(data)
    data = tab_flitter(data,8)
    #------------------------------------------------------
    #print(scence(data)[8])
    data = scence(data)
    #print(data[0])
    #-----------------------------------------------------
    k =[]
    write_file = open(rounte,'a',encoding= 'utf-8')
    for i in range(len(data)):
        #break
        seq = word_seq_find(data[i])
        #tem = seq.split('******')
        #if len(tem) == 1:
            #print(i+1)
        result = gety_seq(seq,city)
        #print(result)
        #print(city)
        if city not in result:
            #print(i+1)
            pass
        else:    
            a = ' ****** '.join(result[city])
            if a == '':
                print(i)
            k.append(a)
    #print(len(k))
    write_file=open(rounte,'w',encoding= 'utf-8')
    for i in range(len(k)):
        write_file.writelines(k[i])
        write_file.writelines('\n')
    write_file.close()
    return k

   
def ref(data,city):
    new_data = []
    for i in range(len(data)):
        if city in data[i]:
            new_data.append(data[i])
    return new_data
            
def maketuple(data):
    #将元组中每行删去重复的
    new_data = []
    for i in range(len(data)):
        temp = data[i].split()
        if len(temp) == 1:
            new_data.append(temp)
        else:
            if len(temp) > 1:
                new_temp = []
                for j in range(len(temp)):
                    if temp[j] not in new_temp:
                        new_temp.append(temp[j])
                new_data.append(new_temp)
    return new_data
                    
def beforecount(data):
    new_data = []
    for i in range(len(data)):
        temp = data[i]
        if len(temp) >= 1:
            for j in range(len(temp)):
                new_data.append(temp[j])
    for i in range(len(new_data)):
        temp = new_data[i].split('/')
        new_data[i] = temp[0]
    return new_data
        
def counts(data):
    dic = {}
    for i in range(len(data)):
        if data[i] in dic:
            dic[data[i]] += 1
        else:
            dic[data[i]] = 1
    return dic
    
  
if __name__=='__main__':
    data = open('data.txt','r',encoding= 'utf-8').readlines()
    data_org = word_tag_fliter(data)#删了词性的原始数据集
    dic_org = counts(beforecount(maketuple(data_org)))#原始数据集计数
    dic_org['******'] = 0
    #print(dic_org)
    city = readtxt('attraction.txt')
    for i in range(len(city)):
        rounte = str(city[i])+'.txt'
        #print(city[i])
        getseqmian(data,city[i],rounte)



    
    
    
    
