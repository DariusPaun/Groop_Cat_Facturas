from PyPDF2 import PdfReader
from pdf_extractor_1 import pdf_ex1
from pdf_extractor_2 import pdf_ex2
def get_pdf(path):
    reader = PdfReader(path)
    return reader

def type_PDF(reader):
    text = ""
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        text += page.extract_text()
    if "Cantidad UM" in text:
        return 2 #type 2
    return 1 #type 1
def main(path):
    reader=get_pdf(path)
    typePDF=type_PDF(reader)
    if typePDF == 2:
        final_list = pdf_ex2(reader)
    else:
        final_list = pdf_ex1(reader)
    return final_list