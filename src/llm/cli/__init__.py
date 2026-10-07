import typer 

from llm.cli import docs
from llm.cli import scrape
from llm.cli import test
from llm.cli import generate_tokens


app = typer.Typer(
    help="My Own LLM",
    no_args_is_help=True,
)

# app.command()(scrape)

app.add_typer(scrape.app, name="scrape")
app.add_typer(docs.app, name="docs")
app.add_typer(test.app, name="test")
app.add_typer(generate_tokens.app, name="generate-tokens")
