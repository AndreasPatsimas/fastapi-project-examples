import PyPDF2


PATH = "/home/andreas/PycharmProjects/fastApiProject/file_handling/uploaded_files/"


f = open(PATH + "ανδρεασ.pdf", "rb")
pdf_reader = PyPDF2.PdfFileReader(f)
print(pdf_reader.numPages)

page_one = pdf_reader.getPage(0)
print(page_one.extractText())
f.close()