#keywords extractor
from tkinter import filedialog
import extractpdf01

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text2text-generation", model="ilsilfverskiold/tech-keywords-extractor")



def interact():
    file = filedialog.askopenfilename()
    extractpdf01.details_pdf(file)
    abstract = extractpdf01.get_abstract(file)
    kw = pipe(abstract)
    print(kw)

interact()