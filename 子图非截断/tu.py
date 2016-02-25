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
    def makeMatrix(self, dataset):
    	for i in xrange(len(dataset)):
    		pass

class Methods():
	def getAttraction(self, dataset):
		attractionList = []
		attraction = []
		for i in xrange(len(dataset)):
			attraction_temp = []
			temp = dataset[i]
			temp = temp.split()
			#print temp
			if len(temp) > 0:
				#print "hh"
				for j in xrange(len(temp)):
					item = temp[j]
					item = item.split(u"/")
					if len(item) == 2 and item[1] == "tttttttt":
						attraction_temp.append(item[0])
						#print attraction_temp
			attraction_temp = list(set(attraction_temp))
			attractionList.append(attraction_temp)
			attraction.extend(attraction_temp)
		attractionSet = self.count(attraction)#景点名对应出现次数的set
		attractionList = self.clearAttraction(attractionList)#景点名二维list
		#print len(attractionSet)
		candidateConnection = self.calculateMC(attraction, attractionSet)#候选连接集
		#print candidateConnection[0:10]
		Connection = {}
		for i in xrange(len(candidateConnection)):
			temp = candidateConnection[i]
			#print temp[0],temp[1]
			num = 0#关系出现的次数
			for j in xrange(len(attractionList)):
				if temp[0] in attractionList[j] and temp[1] in attractionList[j]:
					num += 1
			#print num
			if num >= 10:
				mc = num*1.0/min(attractionSet[temp[0]],attractionSet[temp[1]])
				if mc >= 0.5:
					Connection[temp] = [num,mc,attractionSet[temp[0]],attractionSet[temp[1]]]	
		return Connection

	def calculateMC(self, attraction, attractionSet):
		attraction = list(set(attraction))
		candidateConnection = []
		for i in xrange(len(attraction)-1):
			for j in xrange(i+1,len(attraction)):
				if attractionSet[attraction[i]] >= 10 and attractionSet[attraction[j]] >= 10:
					candidateConnection.append((attraction[i],attraction[j]))
		return candidateConnection

	def up_supportAttraction(self, dataset, support = 10):
		dataset = self.count(dataset)
		pass

	def clearAttraction(self, dataset):
		attractionResult = []
		for i in xrange(len(dataset)):
			if len(dataset[i]) > 1:
				attractionResult.append(dataset[i])
		return attractionResult

	def joinResult(self, dataset):
		#为了归类[(1,2),(2,3),(3,4),(5,6)] -> [[1,2,3,4],[5,6]]
		dataset = [list(i) for i in dataset]
		def joinSingle(dataset):
			for i in xrange(len(dataset)-1):
				for j in xrange(i+1,len(dataset)):
					#print (i,j)
					if len(set(dataset[i]) & set(dataset[j])) != 0:
						dataset[i] = list((set(dataset[i]) | set(dataset[j])))
						dataset[j] = []
			return dataset
		dataset = joinSingle(dataset)
		while [] in dataset:
			new_dataset = []
			for i in xrange(len(dataset)):
				if dataset[i] != []:
					new_dataset.append(dataset[i])
			dataset = joinSingle(new_dataset)
		return dataset

	def findSmallAtraction(self, one_kindResult, other_kindResult, connection):
		#print "aa"
		candidateConnection = []
		for k,v in connection.items():
			if k[0] in other_kindResult and k[1] in other_kindResult:
				pass
			else:
				if v[1] >= 0.8:
					temp = [k[0],k[1],v[0],v[1],v[2],v[3]]
					candidateConnection.append(temp)
		kindConnection = []
		#print candidateConnection[0]
		tempList = ["a"]
		while tempList != []:
			one_kindResult_org = one_kindResult
			for i in xrange(len(candidateConnection)):
				temp = candidateConnection[i]
				if temp[0] in one_kindResult or temp[1] in one_kindResult:
					one_kindResult.extend([temp[0],temp[1]])
			one_kindResult = list(set(one_kindResult))
			tempList = list(set(one_kindResult)-set(one_kindResult_org))
		#print one_kindResult,len(one_kindResult)
		for i in xrange(len(candidateConnection)):
			temp = candidateConnection[i]
			if temp[0] in one_kindResult and temp[1] in one_kindResult:
				kindConnection.append(temp)
		return kindConnection









class treatment():
	def count(self, dataset):
		resultSet = {}
		for i in xrange(len(dataset)):
			if dataset[i] in resultSet:
				resultSet[dataset[i]] += 1
			else:
				resultSet[dataset[i]] = 1
		return resultSet



class DataAnalysis(pretreatment, Methods, treatment):
	pass

def mcpart():
	#通过mc=0.5找到TOP39之间的连接关系
	data = DataAnalysis().read_txt(abspath+"//data//data.txt")
	mainAttraction = DataAnalysis().read_txt(abspath+"//data//mainAttraction.txt")
	connection = DataAnalysis().getAttraction(data)
	print len(connection)
	result = []
	for k,v in connection.items():
		if k[0] in mainAttraction and k[1] in mainAttraction:
			temp = [k[0],k[1],v[0],v[1]]
			result.append(temp)
	print len(result)
	DataAnalysis().writeMatrix(result, "test.txt")

def findkind():
	#将top39景点归类然后寻找每类下小景点
	data = DataAnalysis().read_txt(abspath+"//data//data.txt")
	mainAttraction = DataAnalysis().read_txt(abspath+"//data//mainAttraction.txt")
	connection = DataAnalysis().getAttraction(data)#满足阈值的所有景点的两两关系
	#print len(connection)
	result = []
	for k,v in connection.items():
		if k[0] in mainAttraction and k[1] in mainAttraction:
			result.append(k)
	#print result#TOP39景点两两关系
	kindResult = DataAnalysis().joinResult(result)
	kindResult.append([u"八达岭"])#已经对TOP39景点分好类
	#print kindResult,len(kindResult)
	one_kindResult = kindResult[0]
	other_kindResult = list(set(mainAttraction)-set(one_kindResult))
	print other_kindResult
	kindconnection = DataAnalysis().findSmallAtraction(one_kindResult,other_kindResult,connection)
	print kindconnection
	DataAnalysis().writeMatrix(kindconnection, "0_kind.txt")



if __name__=='__main__':
	#mcpart()
	findkind()
	

