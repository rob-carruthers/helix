#!/usr/bin/env python3
import argparse
import re
import sys


def is_valid_sql_query(input_string: str) -> bool:
    if "select" not in input_string.lower() or "from" not in input_string.lower():
        return False
    return True


def build_query_call(query_string: str, db: str, as_polars: bool):
    base_query = f'df = query_to_df("{db}", query'
    if as_polars:
        base_query += ", as_polars=True"

    sql_vars: list[str] = re.findall(r":[a-zA-Z0-9_]+\b", query_string, flags=re.M)
    for sql_var in sql_vars:
        base_query += f", {sql_var[1:]}={sql_var[1:]}"
    base_query += ")"
    return base_query


def main(input_string: str, db: str, as_polars: bool) -> None:
    if input_string[:3] == '"""':
        prepend = input_string[:3]
    elif input_string[:1] == '"':
        prepend = input_string[:1]
    else:
        prepend = ""

    if input_string[-3:] == '"""':
        append = input_string[-3:]
    elif input_string[-1] == '"':
        append = input_string[-1:]
    else:
        append = ""

    if prepend:
        input_string = input_string.lstrip(prepend)
    if append:
        input_string = input_string.rstrip(append)

    query_call = build_query_call(input_string, db, as_polars)
    output = prepend + input_string + append + "\n" + query_call

    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("-d", "--db")
    _ = parser.add_argument("-o", "--as-polars", action="store_true")
    args = parser.parse_args()
    assert isinstance(args.db, str)  # pyright: ignore [reportAny]
    assert isinstance(args.as_polars, bool)  # pyright: ignore [reportAny]

    input_string = "".join(sys.stdin)
    if not is_valid_sql_query(input_string):
        print(input_string)

    main(input_string=input_string, db=args.db, as_polars=args.as_polars)
