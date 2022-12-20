import PyPDF2

class ReadDocument:
    def ReadingFromPDF(self,filename, firstPage, lastPage):
        pdfFile = open(filename, "rb")
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        pdf = ""
        firstPage = int(firstPage)
        lastPage = int(lastPage)
        for i in range(firstPage - 1, lastPage):
            page = pdfReader.getPage(i)
            pdf += page.extractText()
        pdfFile.close()
        return pdf