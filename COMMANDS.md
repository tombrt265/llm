# `llm`

My Own LLM

**Usage**:

```console
$ llm [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `scrape`: Scrapes a URL and returns the content.
* `docs`: Documentation for this CLI.

## `llm scrape`

Scrapes a URL and returns the content.

**Usage**:

```console
$ llm scrape [OPTIONS] {url}
```

**Arguments**:

* `url`: [required]

**Options**:

* `--help`: Show this message and exit.

## `llm docs`

Documentation for this CLI.

**Usage**:

```console
$ llm docs [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `generate`: Generate Markdown docs for all commands.
* `show`: Show the docs rendered in the terminal.

### `llm docs generate`

Generate Markdown docs for all commands.

**Usage**:

```console
$ llm docs generate [OPTIONS]
```

**Options**:

* `-o, --output <path>`: Target file.  [default: COMMANDS.md]
* `--help`: Show this message and exit.

### `llm docs show`

Show the docs rendered in the terminal.

**Usage**:

```console
$ llm docs show [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
