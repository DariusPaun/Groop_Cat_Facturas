from functions import get_providers2,price_chasis,trans_number
def pdf_ex2(reader):
    nr_pages=len(reader.pages)
    final_list=[]
    sum=-1

    # getting a specific page from the pdf file 
    for kk in range(nr_pages):
    
        page1 = reader.pages[kk] 
        text1 = page1.extract_text() 
        if(text1 == "00"):
            ###print(f"No Detalles pag1 {kk}")
            priceAndChasis=[[-1,-1,kk+1]]
        else:
            providers=get_providers2(text1)
            if(kk==0):
                del providers[0]
            priceAndChasis = [[0] * 3 for _ in range(len(providers)+1)]
            i = 0
            for provider in providers :
                PC=price_chasis(provider)
                priceAndChasis[i]=PC
                priceAndChasis[i][2]=kk+1
                i=i+1
        # extracting text second page from pages 
        if(kk != nr_pages-1):
            page2 = reader.pages[kk+1]
            text2 = page2.extract_text() 
            #text2 = page_format(text2)
            if(text2 == "00"):
                ###print(f"No Detalles  page {kk+2}")
                priceAndChasis2=[[-1,-1,kk]]
            else:
                
                providers2=get_providers2(text2)
                priceAndChasis2 = [[0] * 3 for _ in range(len(providers2)+1)]
                i = 0
                for provider in providers2 :
                    priceAndChasis2[i]=price_chasis(provider)
                    i=i+1
        else:
            priceAndChasis2 =[[-1,-1]]

        #rest of the code merge
        if(priceAndChasis[0][0]==-1):
            del priceAndChasis[0]
        n1=len(priceAndChasis)-1
        n2=len(priceAndChasis2)-1
        del priceAndChasis[n1]
        del priceAndChasis2[n2]
        if(kk != nr_pages-1):
            if((priceAndChasis[n1-1][0]==-1 and priceAndChasis[n1-1][1]!=-1) or (priceAndChasis[n1-1][1]==-1 and priceAndChasis[n1-1][0]!=-1)):
                if((priceAndChasis2[0][0]==-1 and priceAndChasis2[0][1]!=-1) or (priceAndChasis2[0][1]==-1 and priceAndChasis2[0][0]!=-1)):
                    if(priceAndChasis[n1-1][0]==-1 and priceAndChasis[n1-1][1]!=-1):
                        priceAndChasis[n1-1][0]=priceAndChasis2[0][0]
                    else:
                        priceAndChasis[n1-1][1]=priceAndChasis2[0][1]
        lung=len(priceAndChasis)
        ###print(f"Page {kk+1}-> {priceAndChasis}")
        for prc in priceAndChasis:
            if(prc[0]!=-1):
                final_list.append(prc)
    #total sum 
    pag = reader.pages[nr_pages-2]
    text_pag=pag.extract_text()
    parts = text_pag.split("Suma excl. I.V.A",1)
    if(len(parts)==1):
        pag = reader.pages[nr_pages-1]
        text_pag=pag.extract_text()
        parts = text_pag.split("Suma excl. I.V.A",1)
    else:
        parturi=parts[1].split()
        for i in range(len(parturi)-1):
            if parturi[i+1]=="EUR" :
                sum=parturi[i]
                break
                
    e1=str(final_list[len(final_list)-1][0])
    e2=str(sum)
    if e1==e2:
        del final_list[len(final_list)-1]
    sum0=0.0
    sum=trans_number(sum)
    for el in final_list:
        el[0]=trans_number(el[0])
        sum0=sum0+el[0]
    if(abs(sum0-sum)<0.1):
        final_list.append(["Good",f"Calculated->{sum0}",f"Found it->{sum}"])
    else:
        final_list.append(["Bad",f"Calculated({sum0})",f"Found it({sum})"])
    i=1
    for elem in final_list[:-1]:
        elem[2]= f"{i} / {elem[2]}"
        i+=1
    return final_list


