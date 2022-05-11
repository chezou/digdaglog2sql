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

Input log by file:
  --input FILENAME               Input file name of a workflow log. Use - for
                                 STDIN.

Download log by Session ID:
  --session-id INTEGER           Session ID of the target workflow.
  --site [us|jp|eu01|ap02|ap03]  Treasure Workflow site name.  [default: us]
  --endpoint TEXT                Digdag server endpoint.
  --http                         Enforce to use http schema.

Output:
  --output FILENAME              Output file name. Use - for STDOUT.  [required]

Other options:
  --drop-cdp-db                  If true, drop cdp_audience_xxx DB name.
  --help                         Show this message and exit.

Constraints:
  {--input, --session-id}  exactly 1 required
  {--site, --endpoint}     exactly 1 required if --session-id is set
  {--site, --http}         mutually exclusive
```

You can use log file on local environment.

```sh
digdaglog2sql --input workflow-log.txt --output output.sql
```

Or, you can use Session ID of Treasure Workflow.

```sh
digdaglog2sql --session-id 12345 --site us --output output.sql
```

Ensure set `TD_API_KEY` into environment variable.

## Note

As of May 5 2022, if you want to use sqllineage for Trino and Hive logs from Treasure Data,
recommend to install sqlparse and sqllineage as the following:

```sh
pip install git+https://github.com/chezou/sqlparse.git@trino#egg=sqlparse==0.4.3.dev0
pip install git+https://github.com/chezou/sqllineage.git@trino#egg=sqllineage==1.3.4
```

You have to ensure to have node environment for sqllineage installation from source.
