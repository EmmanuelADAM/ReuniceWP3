######################################################v##
## interaction with the abstract of a research article
## the article must have a part begining with "Abstract"
## E.A.

from tkinter import filedialog
import extractpdf01

from transformers import pipeline
#pipe = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")
pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")


#file = "C:/Users/emmanuel adam/Documents/biblio/jadex.pdf"


def interact():
    file = filedialog.askopenfilename()
    extractpdf01.details_pdf(file)
    abstract = extractpdf01.get_abstract(file)
    ok = True
    while ok:
        print("what is your question :")
        question = input()
        output = pipe({"context": abstract, "question": question })
        score = output["score"]
        answer = output["answer"]
        print(f"rep ({score:.2f}/1) -> {answer}")
        print("another question ? (y/n)")
        rep = input()
        ok = (rep == "y")
