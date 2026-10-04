import json
import typer

from llm.data.scrape import scrape_wikipedia, scrape_pdf
from llm.data.tokenize import normalize, pre_tokenize, generate_token_set 

app = typer.Typer(help="Scraping different parts of the web.", no_args_is_help=True)


@app.command()
def wikipedia(url):
    "Scrapes a wikipedia.org/wiki/ sub-url and returns the parsed content."
    
    content: str = scrape_wikipedia(url)
    typer.echo(content)


@app.command()
def pdf(url):
    "Parses a pdf file from the web and returns its content."
    typer.echo("Scraping pdf content ...")
    content: str = scrape_pdf(url)

    typer.echo("Normalizing content ...")
    normalized_content: list[str] = normalize(content.split("\n"))
    words: list[str] = pre_tokenize(normalized_content)
    
    typer.echo("Generating token set ...")
    tokens, merges = generate_token_set(words)
    typer.echo(tokens)

    typer.echo("Write merges to merges.json ...")
    with open("merges.json", "w", encoding="utf-8") as f:
        json.dump([[k[0], k[1], v] for k, v in merges.items()], f, ensure_ascii=False, indent=2)
    typer.echo("Done!")
