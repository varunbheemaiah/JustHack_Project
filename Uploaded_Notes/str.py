def CheckSub(Str,ChkStr):
    count = 0;
    Chk = 0
    StrLen = len(Str)
    ChkLen = len(ChkStr)
    for i in range(0,StrLen):
        for j in range(Chk,ChkLen):
            if(Str[i] == ChkStr[j]):
                Chk = j;
                count += 1
    if(count == StrLen):
        return True
    else:
        return False


BaseStr = input()
ChkStr = input()

length = len(BaseStr)
SubString = []
for i in range(length):
    for j in range(i,length):
        SubString.append(BaseStr[i:j + 1])
SubString.sort(key = len)
SubString.reverse()
for X in SubString:
    print(X)
    if(CheckSub(X,ChkStr)):
        print("Works")
        break
