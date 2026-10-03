from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.markdown import Markdown
from typer.cli import get_docs_for_click

app = typer.Typer(help="Documentation for this CLI.", no_args_is_help=True)


def _build_docs(ctx: typer.Context) -> str:
    root = ctx.find_root()
    docs = get_docs_for_click(obj=root.command, ctx=root, name="llm")
    return docs.strip() + "\n"


@app.command()
def generate(
    ctx: typer.Context,
    output: Annotated[
        Path, typer.Option("--output", "-o", help="Target file.")
    ] = Path("COMMANDS.md"),
):
    """Generate Markdown docs for all commands."""
    output.write_text(_build_docs(ctx), encoding="utf-8")
    typer.echo(f"Docs written to {output}")


@app.command()
def show(ctx: typer.Context):
    """Show the docs rendered in the terminal."""
    Console().print(Markdown(_build_docs(ctx)))
