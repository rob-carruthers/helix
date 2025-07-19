#!/usr/bin/env python3
from pathlib import Path
import sys

# Dummy constant here for easy patching
# (Used when handling tricky Windows UNC paths, manual override)
REPLACE_IN_PATH = {
    "foo": "foo",
}


def helix_relative_path() -> str:
    input_stdin: list[str] = []
    for line in sys.stdin:
        input_stdin.append(line.rstrip())
    assert len(input_stdin) == 1

    input_relative = input_stdin[0]

    # Convienience if input string happens to include quotes
    if input_relative[0] in ("'\""):
        prepend = input_relative[0]
    else:
        prepend = ""
    if input_relative[-1] in ("'\""):
        append = input_relative[-1]
    else:
        append = ""

    # Now remove quotes for finding a valid path
    input_relative = input_relative.replace("'", "").replace('"', "")

    input_path_relative = Path(input_relative)

    # Return feedback if file does not exist
    if not input_path_relative.exists():
        return prepend + "!!" + input_relative + "!!" + append

    input_path_absolute = input_path_relative.resolve()
    input_path_absolute = str(input_path_absolute)

    for old, new in REPLACE_IN_PATH.items():
        input_path_absolute = input_path_absolute.replace(old, new)

    return prepend + input_path_absolute + append


if __name__ == "__main__":
    output = helix_relative_path()
    print(output)
