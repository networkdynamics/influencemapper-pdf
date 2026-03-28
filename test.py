#%%
from urllib import response
import requests
from bs4 import BeautifulSoup
from main import _clean_empty_and_duplicate_authors_from_grobid_parse, extract_disclosure_from_tei_xml, extract_paper_metadata_from_grobid_xml, process_pdf
from main import extract_paper_metadata_from_grobid_xml
#%%
response = requests.get("http://localhost:8070/api/isalive")
print(response.status_code, response.text)
#%%
GROBID_URL = os.getenv("GROBID_URL", "http://localhost:8070/api/processFulltextDocument")
HEADERS = {"Accept": "application/xml", "consolidateCitations": "1", "consolidateFunders": "1"}


pdf_path = 'pdfs/lutfiyya-et-al-2008-disparities-in-adult-african-american-women-s-knowledge-of-heart-attack-and-stroke-symptomatology.pdf'
with open(pdf_path, "rb") as pdf_file:
    response = requests.post(GROBID_URL, files={"input": pdf_file}, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "xml")
        metadata = extract_paper_metadata_from_grobid_xml(soup.fileDesc)
        # clean metadata authors (remove dupes etc)
        metadata['authors'] = _clean_empty_and_duplicate_authors_from_grobid_parse(metadata['authors'])
        back_matter, found = extract_disclosure_from_tei_xml(soup)
        disclosure = ' '.join(back_matter)
        metadata['disclosure'] = disclosure
# response = process_pdf(pdf_path)
#%%
xml_path = 'pdfs/lutfiyya-et-al-2008-disparities-in-adult-african-american-women-s-knowledge-of-heart-attack-and-stroke-symptomatology.pdf.tei.xml'
xml_str = open(xml_path).read()
soup = BeautifulSoup(xml_str, "xml")
metadata = extract_paper_metadata_from_grobid_xml(soup.fileDesc)
# clean metadata authors (remove dupes etc)
metadata['authors'] = _clean_empty_and_duplicate_authors_from_grobid_parse(metadata['authors'])
back_matter, found = extract_disclosure_from_tei_xml(soup)
disclosure = ' '.join(back_matter)
metadata['disclosure'] = disclosure
#%%
authors = metadata.get('authors', [])
disclosure = metadata.get('disclosure', '')
rows = []
for author in authors:
    first_name = author['first']
    middle_names = ' '.join(author['middle'])
    last_name = author['last']
    full_name = f"{first_name} {middle_names} {last_name}".strip()
    affiliation = author.get('affiliation', {})
    affiliation_name = ''
    if len(affiliation) > 0:
        lab = affiliation.get('laboratory', '')
        institution = affiliation.get('institution', '')
        country = affiliation.get('location', {}).get('country', '')
        affiliation_name = f"{lab}, {institution}, {country}".strip(', ')
    rows.append({
        'Title': metadata['title'],
        'Author Name': full_name.strip(),
        'Affiliation': affiliation_name,
        'Email': author.get('email', ''),
        'Disclosure Statement': disclosure
    })