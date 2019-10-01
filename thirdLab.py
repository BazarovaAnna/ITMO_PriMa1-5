#Arithmetic coding
import math,sys
count=0

print("Write name of the file, please")
name=input()
print()
try:
    file=open(name,'r')
except FileNotFoundError:
    print("There is no such a file :0")
    sys.exit(0)

