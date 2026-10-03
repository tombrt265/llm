import typer


app = typer.Typer()


@app.command()
def main():
    print("Hello from llm!")


if __name__ == "__main__":
    app()
