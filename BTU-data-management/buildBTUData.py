#import for the waiting
from tqdm import tqdm
#import for web requests
import requests
#import for csv
import pandas as pd

#data obtained from BTU 
#details = 'Dokument-ID	Dokumenttyp	Verfasser/Autoren	Herausgeber	Haupttitel	Abstract	Auflage	Verlagsort	Verlag	Erscheinungsjahr	Seitenzahl	Schriftenreihe Titel	Schriftenreihe Bandzahl	ISBN	Quelle der Hochschulschrift	Konferenzname	Quelle:Titel	Quelle:Jahrgang	Quelle:Heftnummer	Quelle:Erste Seite	Quelle:Letzte Seite	URN	DOI	Abteilungen'
#data to obtain from  DOI 
doi_keys = ["title","author","subject", "reference"]
#data to store in a csv file
csv_data = [['title', 'keyword', 'abstract', 'field', 'authors', 'date', 'doi', 'references','id']]

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



#details = 'Dokument-ID	Dokumenttyp	Verfasser/Autoren	Herausgeber	Haupttitel	Abstract	Auflage	Verlagsort	Verlag	Erscheinungsjahr	Seitenzahl	Schriftenreihe Titel	Schriftenreihe Bandzahl	ISBN	Quelle der Hochschulschrift	Konferenzname	Quelle:Titel	Quelle:Jahrgang	Quelle:Heftnummer	Quelle:Erste Seite	Quelle:Letzte Seite	URN	DOI	Abteilungen'
#details = 'ID du document Type de document Auteur(s) Editeur Titre principal Édition du résumé Lieu de publication Éditeur Année de publication Numéro Nombre de publications Série Titre Série Nombre de publications ISBN Source de la thèse Nom de la conférence Source :Titre Source :Année Source :Numéro d'émission Source :Première page Source :Dernière page URN DOI Départements'
csv_data = [['title', 'keyword', 'abstract', 'field', 'authors', 'date', 'doi', 'references','id','type']]
def save_pdf(filename):    
    df = pd.read_csv(filename, sep='\t', encoding='ISO-8859-1')
    len = df.shape[0]
    csv_content = []
    for i in tqdm(range(0,len)):
        publi = {}
        row = df.iloc[i]
        publi['title'] = row['Haupttitel'] if row['Haupttitel'] != '' else ""
        publi['keyword'] = ""
        publi['abstract'] = row['Abstract'] if row['Abstract'] != '' else ""
        publi['field'] =  ""
        publi['authors'] = row['Verfasser/Autoren'] if row['Verfasser/Autoren'] != '' else ""
        publi['date'] = row['Erscheinungsjahr'] if row['Erscheinungsjahr'] != '' else ""        
        publi['doi'] = ""
        publi['references'] = ""
        if "DOI" in row:
            references = ""
            publi['doi'] = row['DOI']
            doi_values = add_data_doi(publi['doi']) if type(publi['doi']) == str and publi['doi'] != "" else {}
            if 'subject' in doi_values: publi['field'] = ",".join(doi_values['subject']) if type(doi_values['subject']) == list else doi_values['subject']
            if 'reference' in doi_values: 
                refs = doi_values['reference']
                for ref in refs:
                    if 'DOI' in ref:
                        references = references + ref['DOI'] + ", "
                publi['references'] = references
        publi['id'] = row['Dokument-ID'] if row['Dokument-ID'] != '' else ""
        publi['type'] = row['Dokumenttyp'] if row['Dokumenttyp'] != '' else ""
        csv_content.append(publi)
    df = pd.DataFrame(csv_content)
    df.to_csv(filename.replace(".csv", "-new.csv"), index=False,  encoding="utf-8")

    
for i in range(2,6):
    filename = f"C:/Users/emmanuel adam/Documents/python/nlp/reunice/export ({i}).csv"
    save_pdf(filename)



# for i in range(0, 14):
#     details_articles = get_data(i*2000, 2000)
#     csv_content = build_csv(details_articles)
#     save_pdf(f"outputHAL{i*2000}-{(i+1)*2000}.csv", csv_content)
