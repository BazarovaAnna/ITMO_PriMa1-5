import math
##encoding
print("input number in bin to encode")
toCode=list(input())
infL=len(toCode)
for i in range(infL):
    toCode[i]=int(toCode[i])
code=list()
po=1
j=0
i=0
while j<infL:
    if i+1==po:
        po*=2
        code.append(0)
    else:
        code.append(toCode[j])
        j+=1
    i+=1

L=len(code)
numR=int(math.log2(L+1))
sums=[0]*numR
for i in range(len(sums)):
    s=0
    j=2**i-1
    #print(j)
    while j<len(code):
        for l in range(2**i):
            s^=code[j]
            #print("xor",j)
            j+=1
            if not(j<len(code)):
                break
        j+=2**i
    #print("s:",s)
    sums[i]=s
for i in range(numR):
    if sums[i]==1:
        code[2**i-1]=1
encode=""
for i in range(len(code)):
    encode=encode+str(code[i])
print("The coding result:",encode)

##decoding
print("input number in bin to decode")
code=list(input())

print("Let's decode")
for i in range(len(code)):
    code[i]=int(code[i])
L=len(code)
numR=int(math.log2(L+1))
print("Number of checking bytes:",numR)
print("Number of informational bytes:",L-numR)
print("Counting control sums")
sums=[0]*numR
for i in range(len(sums)):
    s=0
    j=2**i-1
    #print(j)
    while j<len(code):
        for l in range(2**i):
            s^=code[j]
            #print("xor",j)
            j+=1
            if not(j<len(code)):
                break
        j+=2**i
    #print("s:",s)
    sums[i]=s

check=""
for i in range(len(sums)):
    print(f"Conrtol sum {i} is {sums[i]}")
    check=check+str(sums[i])

index=int(check[::-1],base=2)
if(index!=0):
    print(f"There is a mistake in {index} bit")
    index-=1
    if(code[index]==0):
        code[index]=1
    else:
        code[index]=0
    print("Correct message:")
    for x in code:
        print(x,end="")
    print()
else:
    print("The message was correct")
print("Now lets take the message out of there")
decode=""
po=1
for i in range(len(code)):
    if i+1==po:
        po*=2
    else:
        decode=decode+str(code[i])
print(decode)
print("This is a number:",int(decode,base=2))
