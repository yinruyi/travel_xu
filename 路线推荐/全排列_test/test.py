def Mideng(li):
  if(type(li)!=list):
    return 0
  if(len(li)==1):
    return [li]
  result=[]
  for i in range(0,len(li[:])):
    bak=li[:]
    head=bak.pop(i) #head of the recursive-produced value
    for j in Mideng(bak):
      j.insert(0,head)
      result.append(j)
  #print li[:]
  return result

def MM(n):
  if(type(n)!=int or n<2):
    return 0
  return Mideng(list(range(1,n)))

print MM(6)
List = list(range(1,5))
print List,List[:]
