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

* `scrape`: Scraping different parts of the web.
* `docs`: Documentation for this CLI.
* `test`: Commands for testing parts of the pipeline.
* `generate-tokens`: Generate a token set from the stored dataset.

## `llm scrape`

Scraping different parts of the web.

**Usage**:

```console
$ llm scrape [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `wikipedia`: Scrapes a wikipedia.org/wiki/ sub-url and...
* `pdf`: Parses a pdf file from the web and stores...

### `llm scrape wikipedia`

Scrapes a wikipedia.org/wiki/ sub-url and stores the parsed content.

**Usage**:

```console
$ llm scrape wikipedia [OPTIONS] {url}
```

**Arguments**:

* `url`: [required]

**Options**:

* `--help`: Show this message and exit.

### `llm scrape pdf`

Parses a pdf file from the web and stores its content.

**Usage**:

```console
$ llm scrape pdf [OPTIONS] {url}
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

## `llm test`

Commands for testing parts of the pipeline.

**Usage**:

```console
$ llm test [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `tokenize`: Tokenizes a string based on a...

### `llm test tokenize`

Tokenizes a string based on a token-merge-strategy.

**Usage**:

```console
$ llm test tokenize [OPTIONS] {text}
```

**Arguments**:

* `text`: [required]

**Options**:

* `--help`: Show this message and exit.

## `llm generate-tokens`

Generate a token set from the stored dataset.

**Usage**:

```console
$ llm generate-tokens [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.
