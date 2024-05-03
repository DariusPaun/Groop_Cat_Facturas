from functions import get_providers1, trans_number, price_mercancia, nr_Pages


def pdf_ex1(reader):
    nr_pages = nr_Pages(reader.pages[1].extract_text())
    final_list = []
    sum = -1
    skip = False
    # getting a specific page from the pdf file
    for kk in range(nr_pages):
        page1 = reader.pages[kk]
        text1 = page1.extract_text()
        if text1 == "00":
            priceAndChasis = [[-1, -1, kk + 1]]
        else:
            providers = get_providers1(text1)
            if kk == 0:
                del providers[0]
            priceAndChasis = [[0] * 3 for _ in range(len(providers))]
            i = 0
            for provider in providers:
                priceAndChasis[i] = price_mercancia(provider)
                priceAndChasis[i][0] = trans_number(priceAndChasis[i][0])
                priceAndChasis[i][2] = kk + 1
                i = i + 1
            if priceAndChasis[0][0] == 0:
                del priceAndChasis[0]

        if skip:
            del priceAndChasis[0]
            aaaa = 2
        skip = False
        # second page
        if kk + 1 != nr_pages and priceAndChasis[len(priceAndChasis) - 1][0] == 0:
            page2 = reader.pages[kk + 1]
            text2 = page2.extract_text()
            if text1 == "00":
                priceAndChasis_2 = [-1, -1, kk + 2]
            else:
                providers = get_providers1(text2)
                priceAndChasis_2 = price_mercancia(providers[0])
                priceAndChasis_2[0] = trans_number(priceAndChasis_2[0])
                priceAndChasis_2[2] = kk + 2
                priceAndChasis_2[0] = max(
                    priceAndChasis_2[0], priceAndChasis[len(priceAndChasis) - 1][0]
                )
                priceAndChasis_2[1] = max(
                    priceAndChasis_2[1], priceAndChasis[len(priceAndChasis) - 1][1]
                )
                del priceAndChasis[len(priceAndChasis) - 1]
                priceAndChasis.append(priceAndChasis_2)
                skip = True

        for prc in priceAndChasis:
            if prc[0] != -1:
                final_list.append(prc)
    # total sum
    pag = reader.pages[nr_pages - 1]
    text_pag = pag.extract_text()
    parts = text_pag.split("Suma excl. I.V.A", 1)
    if len(parts) == 1:
        pag = reader.pages[nr_pages]
        text_pag = pag.extract_text()
        parts = text_pag.split("Suma excl. I.V.A", 1)
    else:
        parturi = parts[1].split()
        for i in range(len(parturi) - 1):
            if parturi[i + 1] == "EUR":
                sum = parturi[i]
                break
    sum = trans_number(sum)
    if abs(sum - final_list[len(final_list) - 1][0]) < 0.1:
        del final_list[len(final_list) - 1]

    sum0 = 0.0
    for el in final_list:
        sum0 = sum0 + el[0]
    if abs(sum0 - sum) < 0.1:
        final_list.append(["Good",f"Calculated->{sum0}",f"Found it->{sum}"])
    else:
        print(abs(sum0 - sum))
        final_list.append(["Bad",f"Calculated->{sum0}",f"Found it->{sum}"])
    i=1
    for elem in final_list[:-1]:
        elem[2]= f"{i} / {elem[2]}"
        i+=1
    return final_list
