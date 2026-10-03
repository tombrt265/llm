import typer

from llm.data.scrape import scrape_wikipedia, scrape_pdf


app = typer.Typer(help="Scraping different parts of the web.", no_args_is_help=True)


@app.command()
def wikipedia(url):
    "Scrapes a wikipedia.org/wiki/ sub-url and returns the parsed content."
    
    content: str = scrape_wikipedia(url)
    typer.echo(content)


@app.command()
def pdf(url):
    "Parses a pdf file from the web and returns its content."

    content: str = scrape_pdf(url)
    typer.echo(content)
