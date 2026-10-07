import typer

from llm.data.dataset import load_tokens, save_merges, save_tokens
from llm.data.tokenize import generate_token_set

app = typer.Typer(
    help="Generate a token set from the stored dataset.",
    no_args_is_help=False,
    invoke_without_command=True,
)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    "Builds a BPE token set from the whole dataset and writes merges.json."
    if ctx.invoked_subcommand is not None:
        return

    typer.echo("Loading dataset ...")
    words: list[str] = load_tokens()
    if not words:
        typer.echo("No scraped data found in data/. Scrape some pages first.")
        raise typer.Exit(code=1)
    typer.echo(f"Loaded {len(words)} tokens from the dataset.")

    typer.echo("Generating token set ...")
    tokens, merges = generate_token_set(words)
    typer.echo(f"Built a vocabulary of {len(tokens)} tokens.")

    typer.echo("Writing merges to data/merges.json ...")
    merges_path = save_merges(merges)
    typer.echo(f"Saved merges to {merges_path}")

    typer.echo("Writing tokens to data/tokens.json ...")
    tokens_path = save_tokens(tokens)
    typer.echo(f"Saved tokens to {tokens_path}")
    typer.echo("Done!")
