import typer

from llm.data.scrape import scrape_wikipedia, scrape_pdf
from llm.data.tokenize import normalize, pre_tokenize
from llm.data.dataset import is_scraped, save_page

app = typer.Typer(help="Scraping different parts of the web.", no_args_is_help=True)


def _scrape_and_store(url: str, source: str, content: str) -> None:
    "Normalize, pre-tokenize and persist a scraped page as a token list."
    typer.echo("Normalizing content ...")
    normalized_content: list[str] = normalize(content.split("\n"))
    tokens: list[str] = pre_tokenize(normalized_content)

    typer.echo("Storing tokens ...")
    page_path = save_page(url, source, tokens)
    typer.echo(f"Saved {len(tokens)} tokens to {page_path}")
    typer.echo("Done!")


@app.command()
def wikipedia(url: str):
    "Scrapes a wikipedia.org/wiki/ sub-url and stores the parsed content."
    if is_scraped(url):
        typer.echo(f"URL already scraped, skipping: {url}")
        raise typer.Exit()

    typer.echo("Scraping wikipedia content ...")
    content: str = scrape_wikipedia(url)
    _scrape_and_store(url, "wikipedia", content)


@app.command()
def pdf(url: str):
    "Parses a pdf file from the web and stores its content."
    if is_scraped(url):
        typer.echo(f"URL already scraped, skipping: {url}")
        raise typer.Exit()

    typer.echo("Scraping pdf content ...")
    content: str = scrape_pdf(url)
    _scrape_and_store(url, "pdf", content)
