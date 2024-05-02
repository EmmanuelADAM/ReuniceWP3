#import for the waiting
from tqdm import tqdm
#import for web requests
import requests
#import for csv
import pandas as pd

#data to obtain from HAL 
details = 'title_s,authFullName_s,keyword_s,conferenceTitle_s,doiId_s,journalTitle_s,proceedings_s,bookTitle_s,abstract_s,submittedDateY_i,anrProjectAcronym_s,collIsParentOfColl_fs'
#data to obtain from  DOI 
doi_keys = ["title","author","subject", "reference"]
#data to store in a csv file
csv_data = [['title', 'keyword', 'abstract', 'field', 'authors', 'date', 'doi', 'references']]

def get_details(articles):
    """keep only the non empty details for each articles"""
    true_details = []
    for idx, article in enumerate(articles, start=1):
        dict_details = {}
        tab_details = details.split(',')
        for d in tab_details:
            value = article.get(d, '')
            if value != '':
                dict_details[d] = value
    #            print(f"{d} : {dict_details[d]}")
        true_details.append(dict_details)
    return true_details

def get_data(start:int, nb:int):
    """ return the data in JSON format from the query """
    req = f"http://api.archives-ouvertes.fr/search/uphf/?q=*:*&start={start}&rows={nb}&sort=submittedDateY_i desc&fl="+details
    response = requests.get(req)
    if response.status_code == 200: 
        data = response.json()
        articles = data["response"]["docs"]
        true_details = get_details(articles)
        return true_details

def add_data_doi(doi):
    """return an extract of the DOI data"""
    doi_info = {}
    if doi[-1] == '.': doi = doi[:-1]
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
#    print(response)
    # check if success
    if response.status_code == 200:
        # extract  JSON data 
        data = response.json()
        data = data["message"]
        for key in doi_keys:
            if key in data:
                doi_info[key] = data[key]
    return doi_info

def build_csv(true_details):
    """build the csv data from the detail of each articles"""
    csv_content = []
    csv_content.append(csv_data[0])
    #start a csv file
    for article in tqdm(true_details):
        title = ""
        keyword = ""
        abstract = ""
        field  = ""
        authors = ""
        date = ""
        doi = ""
        doi = article.get('doiId_s', '')
        references = ""    
        if(doi!=""):
            doi_values = add_data_doi(doi)
            #get the field "subject" if exists  
            if 'subject' in doi_values: field = doi_values['subject']
            if 'reference' in doi_values: 
                refs = doi_values['reference']
                for ref in refs:
                    if 'DOI' in ref:
                        references = references + ref['DOI'] + ", "
        if 'title_s' in article: title = article['title_s']
        if 'keyword_s' in article: keyword = article['keyword_s']
        if 'abstract' in article: abstract = article['abstract_s']
        if 'authFullName_s' in article: authors = article['authFullName_s']
        if 'submittedDateY_i' in article: date = article['submittedDateY_i']
        row = [",".join(title), ",".join(keyword), ",".join(abstract), ",".join(field), ",".join(authors), date, doi, references]
        csv_content.append(row)
    return csv_content

def save_pdf(filename, csv_data):
    df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
    df.to_csv(filename, index=False,  encoding="utf-8")


#The data has been retrieved manually and stored in outputHAL0-2000.csv, outputHAL2000-4000.csv, ...
#this code open each file to build the csv file in the format defined in introduction

# for i in range(0, 14):
#     details_articles = get_data(i*2000, 2000)
#     csv_content = build_csv(details_articles)
#     save_pdf(f"outputHAL{i*2000}-{(i+1)*2000}.csv", csv_content)
