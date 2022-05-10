import os
import typing

import click
import tdworkflow

from .extractor import extract_sql


class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + "Option is mutually exclusive with "
            + ", ".join(self.not_required_if)
            + "."
        ).strip()
        super(Mutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        f"Illegal usage: '{str(self.name)}' is mutually exclusive with "
                        + str(mutex_opt)
                        + "."
                    )
                else:
                    self.prompt = None
        return super(Mutex, self).handle_parse_result(ctx, opts, args)


@click.command()
@click.option(
    "--input",
    type=click.File("r"),
    prompt=True,
    cls=Mutex,
    not_required_if=["session_id", "site", "endpoint", "http"],
)
@click.option(
    "--session-id",
    type=int,
    help="Session ID of workflow. ",
    cls=Mutex,
    not_required_if=["input"],
)
@click.option(
    "--site",
    type=click.Choice(["us", "jp", "eu01", "ap02", "ap03"]),
    default="us",
    cls=Mutex,
    not_required_if=["input", "endpoint", "http"],
)
@click.option("--output", type=click.File("wt"), required=True)
@click.option(
    "--drop-cdp-db", help="If true, drop cdp_audience_xxx DB name. ", is_flag=True
)
@click.option(
    "--endpoint",
    type=str,
    help="Digdag server endpoint.",
    cls=Mutex,
    not_required_if=["site", "input"],
)
@click.option(
    "--http",
    help="Use http schema.",
    is_flag=True,
    default=False,
    cls=Mutex,
    not_required_if=["input", "side"],
)
def run(
    input: typing.IO,
    output: typing.IO,
    session_id: str,
    site: str,
    drop_cdp_db: bool,
    endpoint: str,
    http: bool,
):

    log = ""
    if input:
        log = input.read()
    elif session_id:
        tdwf_opts = {}
        if endpoint:
            tdwf_opts["endpoint"] = endpoint
            if http:
                tdwf_opts["schema"] = "http"
        else:
            apikey = os.getenv("TD_API_KEY")
            if not apikey:
                raise ValueError("TD_API_KEY should be set in environment variable.")
            if not site:
                raise ValueError("site option should be set.")

            tdwf_opts["site"] = site
            tdwf_opts["apikey"] = apikey

        client = tdworkflow.client.Client(**tdwf_opts)
        attempt = client.session_attempts(session=session_id)[0]
        log = "".join(client.logs(attempt=attempt))

    sql = extract_sql(log, drop_cdp_db=drop_cdp_db)
    output.write(sql)


if __file__ == "__main__":
    run()
