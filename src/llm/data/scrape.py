import io
import requests

from bs4 import BeautifulSoup
from pypdf import PdfReader


headers = {
    'User-Agent': 'Toms User Agent'
}


def _parse_html(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser") 
    
    content = []
    for section in soup.find_all("section", attrs={"data-mw-section-id": True}):
        text = "\n".join(kind.get_text().strip() for kind in section.find_all(recursive=False) if kind.name != "section")
        content.append(text)
    
    return "\n".join(content)

def scrape_wikipedia(url: str):
    response = requests.get(url, headers=headers)
    html_content: str = response.text

    content: str = _parse_html(html_content)
    return(content)


def scrape_pdf(url: str):
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    reader = PdfReader(io.BytesIO(response.content))

    content = []
    for page in reader.pages:
        text = page.extract_text()
        content.append(text)
    return "\n".join(content)
