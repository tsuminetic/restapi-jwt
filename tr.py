listOfNum = [int(x) if x.isdigit() else 0 for x in input().split(' ') ]
ypos=int((listOfNum[0]-1)/2)
xpos=int((listOfNum[1]-7)/2)
print(ypos)
x=3
count=0
for i in range(listOfNum[0]):
    para=''
    for j in range(listOfNum[1]):
        if i==ypos and j==xpos:
            para+='WELCOME'
        if j-7<=xpos and i==ypos and j>xpos:
            pass
        else:
            if j< ((listOfNum[1]-x)/2) or j>=(((listOfNum[1]-x)/2)+x):
                para+="-"
            elif not i==ypos:
                if count==0 or j>=(((listOfNum[1]-x)/2)+x-1):
                    para+="."
                    count+=1
                else:
                    para+='|'
                    count+=1
            else:
                para+="-"
    print(para)
    
    if i>=ypos:
        x-=12
    x+=6
    count=0
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # If you ever feel like your interest has shifted or if you're not feeling it anymore, could you let me know? I just want us to be open with each other.
    # I would rather deal with heartbreak than uncertainity.