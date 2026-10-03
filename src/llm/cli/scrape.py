import typer

from llm.data.scrape import scrape_url


def scrape(url):
    "Scrapes a URL and returns the content."
    
    content: str = scrape_url(url)
    typer.echo(content)
