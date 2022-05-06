# digdaglog2sql

## Install

```sh
pip install --user digdaglog2sql
```

or,

```sh
$ python -m venv .venv
$ source .venv/bin/activate
(.venv)$ pip install digdaglog2sql
```

## Usage

```sh
$ digdaglog2sql --help
Usage: digdaglog2sql [OPTIONS]

Options:
  --input FILENAME               Option is mutually exclusive with session_id,
                                 site.
  --session-id INTEGER           Session ID of workflow. Option is mutually
                                 exclusive with input.
  --site [us|jp|eu01|ap02|ap03]  Option is mutually exclusive with input.
  --output FILENAME              [required]
  --drop-cdp-db                  If true, drop cdp_audience_xxx DB name.
  --help                         Show this message and exit.
```

You can use log file on local environment.

```sh
digdaglog2sql --input workflow-log.txt --output output.sql
```

Or, you can use Session ID of Treasure Workflow.

```sh
digdaglog2sql --session-id 12345 --site us --output output.sql
```
