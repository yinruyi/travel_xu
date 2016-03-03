#coding:utf-8
import os
import sys
import string
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')
abspath = os.getcwd()

class pretreatment():
    """预处理"""
    def __init__(self):
        pass
    def read_txt(self, txtPath, coding = 'utf-8'):
        import codecs
        f = codecs.open(txtPath,'r',coding).readlines()
        f[0] = f[0].replace(u"\ufeff",u"")
        dataset = []
        for line in f:
            line = line.replace("\r\n","")
            line = line.replace("\n","")
            dataset.append(line)
        return dataset

    def writeMatrix(self, dataset, Path, coding = "utf-8"):
        for i in xrange(len(dataset)):
            temp = dataset[i]
            temp = [str(temp[j]) for j in xrange(len(temp))]
            temp = ",".join(temp)
            dataset[i] = temp
        string = "\n".join(dataset)
        f = open(Path, "a+")
        line = f.write(string+"\n")
        f.close()

class methods():
    def trans_data(self, dataset, mainAttraction):
        #将数据集转变成一个景点二维表
        result = []
        for i in xrange(len(dataset)):
            result_temp = []
            temp = dataset[i].split()
            if len(temp) > 0:
                for j in xrange(len(temp)):
                    new_temp = temp[j].split("/")
                    if new_temp[0] in mainAttraction and new_temp[1] == "tttttttt":
                        result_temp.append(new_temp[0])
            result.append(result_temp)
        return result
    
    def moveAA(self, dataset):
        #消除list中相连两个相同的情况
        result = []
        for i in xrange(len(dataset)):
            result_temp = []
            temp = dataset[i]
            if len(temp) == 0:
                pass
            elif len(temp) == 1:
                result_temp = temp
            else:
                for j in xrange(len(temp)-1):
                    pass
    def fixAttractionFP(self, dataset):
        result = []
        for i in xrange(len(dataset)):
            resultTemp = []
            temp = dataset[i]
            if len(temp) == 0:
                pass
            elif len(temp) == 1:
                resultTemp = temp
            else:
                resultTemp.append(temp[0])
                for j in xrange(1,len(temp)):
                    if temp[j] == temp[j-1]:
                        pass
                    else:
                        resultTemp.append(temp[j])
            result.append(resultTemp)
        return result




    def attractionFP(self, dataset):
        #对景点挖掘频繁集
        resultSet = {}
        resultList = []
        for i in xrange(len(dataset)):
            temp = dataset[i]
            if len(resultList) == 0:
                resultSet[tuple(temp)] = 1
            else:
                flag = 0
                for j in xrange(len(resultList)):
                    if set(resultList[j]) == set(temp):
                        temp = resultList[j]
                        flag = 1
                if flag == 0 :
                    resultList.append(temp)
                    resultSet[tuple(temp)] = 1
                else:
                    resultSet[tuple(temp)] += 1
        return resultSet

    def recommandation(self, attractionList):
        kind = self.read_txt(abspath+"//data//kind.txt")
        #print kind
        kind = self.transData(kind)
        #print kind
        attractionSet = self.transAtrantionList(attractionList,kind)
        #print attractionList
        #print attractionSet
        totalPointTable = self.read_table(abspath+"//data//section.txt")#ABCDEF大景区路线的得分
        #print totalPointTable
        district = []#目标景区
        for k,v in attractionSet.items():
            district.append(k)
        rounteResult = []#最后路线推荐
        district_route = district#最后景区行走推荐
        if len(district) == 1:
            temp = attractionSet[district[0]]
            smallPointTable = self.read_table(abspath+"//data//"+str(district[0])+".txt")
            rounteResult = self.section_rec(temp, smallPointTable)
        else:
            #print "aa"
            #print district
            big_rounte = self.section_rec(district,totalPointTable)#景区路径推荐
            for i in xrange(len(big_rounte)):
                temp = attractionSet[big_rounte[i]]
                if len(temp) == 1:
                    rounteResult.append(temp[0])
                else:
                    smallPointTable = self.read_table(abspath+"//data//"+str(big_rounte[i])+".txt")
                    #print smallPointTable
                    small_rounte = self.section_rec(temp, smallPointTable)
                    #print small_rounte
                    rounteResult.extend(small_rounte)
        return rounteResult,district_route

            


    def read_table(self,path):
        resultSet = {}
        data = self.read_txt(path)
        for i in xrange(len(data)):
            temp = data[i].split(u",")
            resultSet[(temp[0],temp[1])] = float(temp[2])
        return resultSet

    def section_rec(self, attractionList, pointTable):
        #给定景区或者某个景区内景点进行路线推荐
        rountePointSet = {}
        point_list = []
        if len(attractionList) == 1:
            return attractionList
        else:
            #a = ["a","b","d","c"]
            #print self.Permutations(a)
            rounte = self.Permutations(attractionList)
            for i in xrange(len(rounte)):
                one_rounte = rounte[i]
                point = self.rountePoint(one_rounte,pointTable)
                point_list.append(point)
                rountePointSet[tuple(one_rounte)] = point
            point_max = max(point_list)
            for k,v in rountePointSet.items():
                if v == point_max:
                    return list(k)


    def rountePoint(self, rounte, pointTable):
        #对每条路线进行打分
        point = 0
        for i in xrange(len(rounte)-1):
            temp = (rounte[i],rounte[i+1])
            if pointTable.has_key(temp):
                point += pointTable[temp]
            else:
                point = point - 10000#惩罚
        return point


    def transData(self,data):
        result = []
        for i in xrange(len(data)):
            temp = data[i].split(u",")
            result.append(temp)
        return result

    def transAtrantionList(self,attractionList,kind):
        flag = "ABCDEF"
        attractionSet = {}
        for i in xrange(len(attractionList)):
            attraction  = attractionList[i]
            for j in xrange(len(kind)):
                if attraction in kind[j]:
                    section = flag[j]
            if section in attractionSet:
                temp = attractionSet[section]
                temp.append(attraction)
                attractionSet[section] = temp
            else:
                attractionSet[section] = [attraction]
        return attractionSet

    def Permutations(self,List):
        #实现List的全排列
        #thank to http://www.jb51.net/article/62374.htm
        if len(List) == 1:
            return [List]
        else:
            result = []
            for i in xrange(0,len(List[:])):
                bak = List[:]
                head = bak.pop(i)
                for j in self.Permutations(bak):
                    j.insert(0,head)
                    result.append(j)
            return result



class DataAnalysis(pretreatment, methods):
    def FP(self):
        mainAttraction = self.read_txt(abspath+"//data//mainAttraction.txt")
        data = self.read_txt(abspath+"//data//tongjiblog998.txt")
        #print mainAttraction
        data = self.trans_data(data, mainAttraction)
        print len(data),data[0]
        data = self.fixAttractionFP(data)
        #self.writeMatrix(data, "998data.txt")
        #attractionFP = self.attractionFP(data)
        ##print type(attractionFP)
        #candidate = []
        #print len(attractionFP)
        #for k,v in attractionFP.items():
        #    #print k,v
        #    #break
        #    if v!=1:
        #        candidate.append(k)
        #print candidate
        #for i in xrange(len(candidate)):
        #    temp = candidate[i]
        #    #print temp
        #    self.main(temp)
        #for i in xrange(9):
        #    self.main(data[i])
        self.main(list(set(data[8])))

    def main(self,attractionList=[]):
        #attractionList = [u"天安门",u"天坛",u"毛主席纪念堂",u"八达岭",u"故宫",u"北京大学",u"清华大学"]
        #attractionList = [u"北京大学",u"清华大学",u"颐和园",u"圆明园"]
        attractionList = [u"后海",u"西海",u"烟袋斜街",u"南锣鼓巷",u"前海",u"鸦儿胡同",u"恭王府",u"什刹海"]
        recommand_rounte,district_route = self.recommandation(attractionList)
        print recommand_rounte
        self.writeMatrix([recommand_rounte,district_route],"result.txt")

        


if __name__ == '__main__':
    DataAnalysis().main()
    #DataAnalysis().FP()