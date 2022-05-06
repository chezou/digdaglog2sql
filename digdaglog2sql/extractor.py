import re

from .td_op import extract_td_sql


def extract_sql(input: str, drop_cdp_db: bool = False):
    output = extract_td_sql(input, drop_cdp_db=drop_cdp_db)

    pat = re.compile(r"\d{4}-\d{2}-\d{2} .+")
    output = re.sub(pat, r"", output).strip()
    output = re.sub(r"\n+", r"\n", output)

    return output
