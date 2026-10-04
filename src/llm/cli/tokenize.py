import json
import typer

from llm.data.tokenize import normalize, pre_tokenize, tokenize


app = typer.Typer(help="Tokenize a string of text.", no_args_is_help=True)


@app.command()
def main(text: str):
    "Tokenizes a string based on a token-merge-strategy."
    typer.echo("Read merges.json ...")
    with open("merges.json", encoding="utf-8") as f:
        merges = {(a, b): v for a, b, v in json.load(f)}

    typer.echo("Normalizing text ...")
    normalized_text: list[str] = normalize([text])
    words: list[str] = pre_tokenize(normalized_text)
    
    typer.echo("Tokenized text: ")
    tokenized_text: list[str] = tokenize(words, merges)
    typer.echo(tokenized_text)
