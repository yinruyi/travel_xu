#coding:utf-8
'''
import numpy as np

a = np.array(
                [[  2,  7,  1, 2],
                [ 35,  9,  1, 2],
                [ 22, 12,  4, 2]]
             )
print a
a1 = a[:,::-1].T
print a1
a2 = np.lexsort(a1)
print a2
a3 = a[a2]

print a3
'''
import numpy as np
from numpy import * 
import pprint 
a = np.array(
                [[  2,  77,  1, 2],
                [ 35,  9,  1, 2],
                [ 22, 12,  4, 2]]
             )
'''
print '排序前：'
pprint.pprint(a)

a1 = a.T
print a1
a2 = a1[array([0,1,2,1])]  #2列换到最后列（因为转置，此时应该说2行换最后行）
print a2
a3 = np.lexsort(a2)
a4 = a[a3]

print '排序后：'
pprint.pprint(a4)
'''

def npRank(dataset, k):
	#对于第k列升序排序
	k = [k for i in xrange(len(dataset[0]))]
	#print k
	temp = dataset.T[array(k)]
	#print temp
	temp = np.lexsort(temp)
	#print temp
	print dataset
	dataset = dataset[temp]
	print dataset

npRank(a,0)