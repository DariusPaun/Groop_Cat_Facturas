import json

def nr_Pages(page):
    parts=page.split("Pagina")
    if(len(parts)!=2):
        print("ERROR PAGE")
    else:
        the_parts=parts[1].split("/")
        the_part=the_parts[1].split()
        return int(the_part[0])

def is_chassis_number(elem):
    
    with open('Data\Project\Data_Base.json', 'r') as file:
        full_data = json.load(file)
        chassisNumber = full_data["set2"]
    try:
        val=chassisNumber[elem]
    except KeyError:
        val = -1
    return val
def is_mercancia_number(strin):
    
    with open('Data\Project\Data_Base.json', 'r') as file:
        full_data=json.load(file)
        mercancia = full_data["set1"]

    for key in mercancia.keys():
        if key in strin:
            return mercancia[key]
    return -1
def trans_number(stri):
    if stri == -1:
        return 0
    value=0.0
    [n1,n2]=stri.split(",")
    values=n1.split(".")
    ord=len(values)
    for i in range(ord):
        j=ord-i-1
        value=value + int(values[i]) * (1000**j)
    n2=n2[:2]
    return value+float(f"0.{n2}")
def get_providers2(page):
    provider=page.split("Alquiler :")
    return provider
def get_providers1(page):
    provider=page.split("mercancia : ")
    return provider

def price_chasis(provider):
    prcChasis = [-1,-1,0]
    elem = provider.split()
    size=len(elem)
    for i in range(size-1):
        if elem[i+1] == "EUR" and prcChasis[0] == -1:
            prcChasis[0]=elem[i]
            break
    value=-1
    for i in range(size):
        value=is_chassis_number(elem[i])
        if value!=-1:
            break
        else:
            value=-1
    prcChasis[1]=value
    return prcChasis
def price_mercancia(provider):
    prcChasis = [-1,-1,0]
    elem = provider.split()
    size = len(elem)
    for i in range(size-1):
        if elem[i+1] == "EUR" and prcChasis[0] == -1:
            prcChasis[0]=elem[i]
            break
    strin = (provider.split("EUR"))[0]
    prcChasis[1] = is_mercancia_number(strin)
    return prcChasis

def check_veracity(data):
    print(data)
    leng=len(data)
    sumCalc=0
    sum=data[leng-1][2]
    for i in range(leng-1):
        
        a=data[i][0]
        b=data[i][1]
        a=str(a)
        b=str(b)
        try:
            fl1=float(a)
        except:
            print(f"1 - 1  ({a}--{b})")
            return -1
        
        decimal=a.split(".")
        if(len(decimal)==1):
            a=int(decimal[0])
        elif(int(decimal[1])==0):
            a=int(decimal[0])
        elif(int(decimal[1])>0 and int(decimal[1])<9):
            a=int(decimal[0])+0.1*int(decimal[1])
        elif(int(decimal[1])>9 and int(decimal[1])<100):
            a=int(decimal[0])+0.01*int(decimal[1])
        else:
            print("2 - 1")
            return -1
        data[i][0]=a
        sumCalc+=float(a)
    print(data[leng-1][1])
    sum=float(data[leng-1][2].split(">")[1])
    print(f"-<<{sum} {sumCalc}")
    print(data)
    if abs(sum-sumCalc)>0.005:
        return -2
    return data


            



