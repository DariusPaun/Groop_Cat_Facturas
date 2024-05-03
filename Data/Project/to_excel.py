import pandas as pd
import os
import numpy as np
from datetime import datetime
def excelCreat(data):

    # Modify data
    
    new_data={}
    for elem in data[:-1]:
        if(elem[1] in new_data):
            new_data[elem[1]].append(elem[0])
        else:
            new_data[elem[1]] = [elem[0]]
    print(new_data)
    sum=[0] * len(new_data)
    i=0
    print("22212")
    for key in new_data:
        new_key={}
        for value in new_data[key]:
            if value in new_key:
                new_key[value]=new_key[value]+1
            else:
                new_key[value] = 1
            sum[i]=sum[i]+value
        new_data[key] = new_key
        i=i+1
    print(sum)
    maxval=0
    for this in new_data:
        if(len(new_data[this])>maxval):
            maxval= len(new_data[this])
    maxval=maxval*2+1
    realy_new_data = [[0 for _ in range(0)] for _ in range(len(new_data))]
    i=0
    for cler in new_data:
        realy_new_data[i].append(cler)
        for incler in new_data[cler]:
            realy_new_data[i].append(new_data[cler][incler])
            realy_new_data[i].append(incler)
        i=i+1
    the_final_product=[[0 for _ in range(maxval+2)] for _ in range(len(new_data)+1)]
    for i in range(len(new_data)+1):
        for j in range(maxval+1):
            if(i==0):
                if(j==0):
                    the_final_product[i][j]='CC'
                elif(j%2==0):
                    the_final_product[i][j]="Precio"
                else:
                    the_final_product[i][j]="U"
            else:
                try:
                    the_final_product[i][j]=realy_new_data[i-1][j]
                except:
                    the_final_product[i][j] = 0
        the_final_product[i][maxval+1]=sum[i-1]
    the_final_product[0][maxval+1]='TOTAL'

    # Create a DataFrame
    df = pd.DataFrame(the_final_product)

    # Specify the directory path
    output_directory = 'output'

    # Print the absolute path of the output directory
    absolute_output_directory = os.path.abspath(output_directory)

    # Create the output directory if it doesn't exist
    os.makedirs(absolute_output_directory, exist_ok=True)

    # Get the current date and time
    m = datetime.now().strftime('%m')
    d = datetime.now().strftime('%d')
    y = datetime.now().strftime('%y')
    H = datetime.now().strftime('%H')
    M = datetime.now().strftime('%M')
    S = datetime.now().strftime('%S')

    # Create the Excel file name with the formatted date
    excel_file_name = f'PDF_to_EXCEL_{y}-{m}-{d}_{H}.{M}.{S}.xlsx'

    # Export the DataFrame to an Excel file
    df.to_excel(os.path.join(absolute_output_directory, excel_file_name), index=False)
