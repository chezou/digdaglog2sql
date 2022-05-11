import os
import typing

import click
import cloup
import tdworkflow
from cloup import constraint, option, option_group
from cloup.constraints import If, RequireAtLeast, RequireExactly, mutually_exclusive

from .extractor import extract_sql


class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + f" Option is mutually exclusive with {', '.join(self.not_required_if)}."
        ).strip()
        super(Mutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        f"Illegal usage: '{self.name}' is mutually exclusive with "
                        f"{mutex_opt}."
                    )
                else:
                    self.prompt = None
        return super(Mutex, self).handle_parse_result(ctx, opts, args)


@cloup.command(show_constraints=True)
@option_group(
    "Input log by file",
    option(
        "--input",
        help="Input file name of a workflow log. Use - for STDIN.",
        type=click.File("r"),
    ),
)
@option_group(
    "Download log by Session ID",
    option("--session-id", help="Session ID of the target workflow.", type=int),
    option(
        "--site",
        type=click.Choice(["us", "jp", "eu01", "ap02", "ap03"]),
        help="Treasure Workflow site name.",
        default="us",
        show_default=True,
    ),
    option(
        "--endpoint",
        type=str,
        help="Digdag server endpoint.",
    ),
    option(
        "--http",
        help="Enforce to use http schema.",
        is_flag=True,
        default=False,
    ),
)
@option_group(
    "Output",
    option(
        "--output",
        help="Output file name. Use - for STDOUT.",
        type=click.File("wt"),
        required=True,
    ),
)
@option("--drop-cdp-db", help="If true, drop cdp_audience_xxx DB name. ", is_flag=True)
@constraint(RequireExactly(1), ["input", "session_id"])
@constraint(If("session_id", then=RequireExactly(1)), ["site", "endpoint"])
@constraint(mutually_exclusive, ["site", "http"])
def run(
    input: typing.IO,
    output: typing.IO,
    session_id: int,
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

            tdwf_opts["site"] = site
            tdwf_opts["apikey"] = apikey

        client = tdworkflow.client.Client(**tdwf_opts)
        attempt = client.session_attempts(session=session_id)[0]
        log = "".join(client.logs(attempt=attempt))

    sql = extract_sql(log, drop_cdp_db=drop_cdp_db)
    output.write(sql)


if __file__ == "__main__":
    run()
