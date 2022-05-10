import re


def upper_repl(match, op):
    return f"{op.upper()} {match.group(1).upper()} {match.group(2)};"


def extract_td_sql(input: str, drop_cdp_db: bool = False):
    pat = re.compile(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+ \+\d{4} \[INFO\]"
        r" \([\w\S]+?\) [\w\.]+?\$TdOperator:.+?:\n(.*?)"
        r"(?=(?:;?\n+\d{4}-\d{2}-\d{2})|(?:\Z))",
        re.DOTALL,
    )
    pat2 = re.compile(
        r"\d{4}-\d{2}-\d{2} .+?\[INFO\].+?"
        r"\$TdDdlOperator: Renaming TD table (.+)\.(.+) -> (.+)"
    )
    pat3 = re.compile(
        r"\d{4}-\d{2}-\d{2} .+?\[INFO\].+?\$TdDdlOperator: "
        r"Deleting TD (database|table) (.+)"
    )
    pat4 = re.compile(
        r"\d{4}-\d{2}-\d{2} .+?\[INFO\].+?\$TdDdlOperator: "
        r"Creating TD (database|table) (.+)"
    )

    data = re.sub(pat, r"\1\n;", input)
    data = re.sub(pat2, r"ALTER TABLE \1.\2 RENAME TO \1.\3;", data)
    data = re.sub(pat3, lambda match: upper_repl(match, "DROP"), data)
    data = re.sub(pat4, lambda match: upper_repl(match, "CREATE"), data)
    data = data.replace(";;", ";")

    if drop_cdp_db:
        data = re.sub(r"\"?cdp_audience_\d+?\"?\.", "", data)

    return data
