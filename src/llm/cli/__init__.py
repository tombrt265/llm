import typer 

from llm.cli import docs
from llm.cli import scrape
from llm.cli import tokenize


app = typer.Typer(
    help="My Own LLM",
    no_args_is_help=True,
)

# app.command()(scrape)

app.add_typer(scrape.app, name="scrape")
app.add_typer(docs.app, name="docs")
app.add_typer(tokenize.app, name="tokenize")
