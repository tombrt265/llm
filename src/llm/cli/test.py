import typer

from llm.data.tokenize import normalize, pre_tokenize, tokenize
from llm.data.dataset import load_merges


app = typer.Typer(help="Commands for testing parts of the pipeline.", no_args_is_help=True)


@app.command(name="tokenize")
def tokenize_text(text: str):
    "Tokenizes a string based on a token-merge-strategy."
    typer.echo("Read merges.json ...")
    merges = load_merges()

    typer.echo("Normalizing text ...")
    normalized_text: list[str] = normalize([text])
    words: list[str] = pre_tokenize(normalized_text)

    typer.echo("Tokenized text: ")
    tokenized_text: list[str] = tokenize(words, merges)
    typer.echo(tokenized_text)
