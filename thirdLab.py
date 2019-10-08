#Arithmetic coding
import math,sys
from decimal import *
p=dict()#letter probs
firstIntervals=dict()
count=0

print("Write name of the file, please")
name=input()
print()
try:
    file=open(name,'r')
except FileNotFoundError:
    print("There is no such a file :0")
    sys.exit(0)
s=file.read()    
for c in s:
    if c.isalpha() or c.isdigit():
        sym=c.upper()
    elif c==" ":
        sym=" "
    else:
        sym="."
    p.setdefault(sym,0)#this function looks for sym in the dict, and if there is no such a thing, it adds this to dict with the 0
    firstIntervals.setdefault(sym,[0,1])
    p[sym]+=1
    count+=1

for x in p:
    p[x]=Decimal(p[x]/count)

#sortedP = list(p.items())
#sortedP.sort(key=lambda x: x[1],reverse=True)#in decsending order of probs
pointer=Decimal(0)
for x in firstIntervals:
    firstIntervals[x][0]=Decimal(pointer)
    firstIntervals[x][1]=Decimal(pointer+p[x])
    pointer=Decimal(pointer+p[x])

def aryth(l,r,symb):
    leng=Decimal(r-l)
    newl=Decimal(firstIntervals[symb][0]*leng+l)
    newr=Decimal(firstIntervals[symb][1]*leng+l)
    return newl,newr
left=0
right=1
for c in s:
    if c.isalpha() or c.isdigit():
        sym=c.upper()
    elif c==" ":
        sym=" "
    else:
        sym="."
    left,right=aryth(left,right,sym)

  
point=Decimal((left+right)/2)
tochn=Decimal(right-left)

from math import copysign, fabs, floor, isfinite, modf

def float_to_bin(f):
    if not isfinite(f):
        return repr(f)  # inf nan
    sign = '-' * (copysign(1.0, f) < 0)
    frac, fint = modf(fabs(f))  # split on fractional, integer parts
    n, d = frac.as_integer_ratio()  # frac = numerator / denominator
    assert d & (d - 1) == 0  # power of two
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length()-1}b}'
newfile=str(float_to_bin(point))

print(newfile)
try:
    koef=Decimal((-math.log2(right-left)/(len(s)*8))*100)
    print(koef,"%")
except:
    print("The interval is too small T_T")

newStr=""
num=point
def decode(l,r,num,newStr):
    #print()
    leng=Decimal(r-l)
    #print("NUM",num)
    for x in firstIntervals:
        #print("FOR",x,"INTERVAL IS",Decimal(firstIntervals[x][0]*leng+l),Decimal(firstIntervals[x][1]*leng+l))
        if Decimal(num)>=Decimal(firstIntervals[x][0]*leng+l) and Decimal(num)<Decimal(firstIntervals[x][1]*leng+l):
            newS=newStr+x
            l=Decimal(firstIntervals[x][0]*leng+l)
            r=Decimal(firstIntervals[x][1]*leng+l)
            #print("DECODED:",newS)
            #print("LEFT:",l)
            #print("RIGHT:",r)
            return l,r,newS
   
        
left=0
right=1
#print("TOCHN:",tochn)
while Decimal(right-left)>Decimal(tochn):
    #print("COMPARE WITH TOCHN:",right-left)
    left,right,newStr=decode(left,right,num,newStr)
print(newStr)
