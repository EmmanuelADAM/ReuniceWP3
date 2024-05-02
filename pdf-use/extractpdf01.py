from PyPDF2 import PdfReader

#file="C:/Users/emmanuel adam/Documents/biblio/jadex.pdf"
file="C:/Users/emmanuel adam/Documents/biblio/Reactive control of overall power consumption.pdf"

def details_pdf(file):
    print(file)
    reader = PdfReader(file)
    nb_pages = len(reader.pages)   
    print("nb pages : ", nb_pages)
    # All of the following could be None!
    meta = reader.metadata
    if(meta.title):print("title : ", meta.title)
    if(meta.author):print("author : ", meta.author)
    if(meta.subject):print("subject : ", meta.subject)
    if(meta.creator):print("creator : ", meta.creator)
    if(meta.producer):print("producer : ", meta.producer)


def clean_page(page):
    """ remove the header and footer of the page """
    parts = []
    def visitor_body(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 50 and y < 720:
            parts.append(text)
    page.extract_text(visitor_text=visitor_body)
    text_body = "".join(parts)
    return (text_body)


def get_all(file):
    """ get the abstract of the pdf """
    reader = PdfReader(file)
    nb_pages = len(reader.pages)   
    txt = []
    for i in range(0, nb_pages):
        text = clean_page(reader.pages[i])
        for line in text.splitlines():
            txt.append(line)
        txt.append(clean_page(reader.pages[i]))
    total = " ".join(txt)
    return total


def get_abstract(file): 
    """ get the abstract of a search article in pdf """
    reader = PdfReader(file)
    text = clean_page(reader.pages[0])
    txt = []
    start = False
    for line in text.splitlines():
        pos = line.find("Abstract")
        if(pos==-1):pos = line.find("abstract")
        if(pos==-1):pos = line.find("A B S T R A C T")
        if(pos>-1):
            start = True
            line = line[pos+8:]
        if(start):
            pos = line.find("Introduction")
            if(pos>-1): break
            txt.append(line)
    abstract = " ".join(txt)
    return abstract
