import math,sys
p=dict()#letter probs
codeSF=dict()#letter codes Shannon-Fano
count=0

print("Write name of the file, please")
name=input()
print()
try:
    file=open(name,'r')
except FileNotFoundError:
    print("There is no such a file :0")
    sys.exit(0)

for c in file.read():#here file.read is a string that contains all the symbols of the file
    if c.isalpha() or c.isdigit():
        sym=c.upper()
    elif c==" ":
        sym=" "
    else:
        sym="."
    p.setdefault(sym,0)#this function looks for sym in the dict, and if there is no such a thing, it adds this to dict with the 0
    codeSF.setdefault(sym,list())
    p[sym]+=1
    count+=1
    
for x in p:
    p[x]=p[x]/count
sortedP = list(p.items())
sortedP.sort(key=lambda x: x[1],reverse=True)#in decsending order of probs

#for x in sortedP:
#    print(x[0],":",f'{x[1]:.4f}')

def ShanFan(array):
    #2) первоначальный ансамбль кодируемых сигналов разбивают на две группы
        #таким образом, чтобы суммарные вероятности сообщений обеих групп
        #были по возможности равны;
    prob=0
    for x in array:
        prob += x[1]
    prob /=2
    #print(prob)
    arr1=list()
    pr=0
    i=0
    while pr<prob:
       pr+=array[i][1]
       arr1.append(array[i])
       #print(pr, array[i][0])

       i+=1
    #print()   
    arr2=array[i:]
    #3) первой группе присваивают символ 0, второй – символ 1; 
    for x in arr1:
        codeSF[x[0]].append(0)
    for x in arr2:
        codeSF[x[0]].append(1)
    #4) каждую из групп делят на две подгруппы так, чтобы их
        #суммарные вероятности были по возможности равны;
    #5) первым подгруппам каждой из групп вновь
        #присваивают 0, а вторым – 1, в результате получают вторые цифры кода;
    #6) каждую из четырех подгрупп вновь делят на
        #равные (с точки зрения суммарной вероятности) части
        #до тех пор, пока в каждой из них не останется одна буква.
    if len(arr1)>1:
        ShanFan(arr1)
    if len(arr2)>1:
        ShanFan(arr2)

#Shannon-Fano
ShanFan(sortedP)
print("Shannon-Fano")
for x in sortedP:
    print(x[0],":",f'{x[1]:.4f}',*codeSF[x[0]],len(codeSF[x[0]]))

file.close()

#Huffman
    
import heapq
from collections import Counter
from collections import namedtuple#модули для работы с минимальной кучей и словарь с поддержкой счетчика

class Node(namedtuple("Node",["left","right"])):#структура дерева
    def walk(self,code,acc):
        self.left.walk(code,acc+"0")
        self.right.walk(code,acc+"1")
    
class Leaf(namedtuple("Leaf",["char"])):#объявление класса для «листьев дерева», у них нет потомков, но есть значение символа
    def walk(self,code,acc):
        code[self.char]=acc or "0"

def Huff(s):#функция кодирования символов в коды Хаффмана
    h=[]
    for ch,freq in Counter(s).items():
        if ch.isalpha() or ch.isdigit():
            sym=ch.upper()
        elif ch==" ":
            sym=" "
        else:
            sym="."
        h.append((freq,len(h),Leaf(sym)))
    heapq.heapify(h)
    count = len(h)
    while len(h)>1:
        freq1, _count1, left = heapq.heappop(h)
        freq2, _count2, right = heapq.heappop(h)

        heapq.heappush(h,(freq1+freq2, count,Node(left,right)))

        count+=1
    code={}
    if h:
        [(_freq, _count, root)] =h
        root.walk(code,"")
    return code


file=open(name,'r')
s=file.read()
file.close

code=Huff(s)#letter codes for huffman
print("Huffman")
for x in sortedP:
    print(x[0],":",f'{x[1]:.4f}',code[x[0]])

