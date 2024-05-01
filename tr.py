listOfNum = [int(x) if x.isdigit() else 0 for x in input().split(' ') ]
ypos=int((listOfNum[0]-1)/2)
xpos=int((listOfNum[1]-7)/2)
print(ypos, xpos)


x=3
for i in range(listOfNum[0]):
    para=''
    for j in range(listOfNum[1]):
        if i==ypos and j==xpos:
            para+='WELCOME'
        if j-7<=xpos and i==ypos and j>xpos:
            pass
        else:
            if j<(listOfNum[1]-x)/2 and j>((listOfNum[1]-x)/2)+3):
                para+='|'
            else:
                para+='-'
    print(para)
    x+=6