#!/usr/bin/env python

from collections.abc import Sequence
from pathlib import Path
import re
import sys

ENVIRONMENT = "production"
if len(sys.argv) > 1:
    ENVIRONMENT = sys.argv[1]

print(f"ENVIRONMENT: {ENVIRONMENT}")

BASE_DIR = Path(__file__).parent.resolve()
PRODUCTION_DOTENVS_DIR = BASE_DIR / ".envs" / f".{ENVIRONMENT}"
PRODUCTION_DOTENV_FILES = [
    PRODUCTION_DOTENVS_DIR / ".django",
    PRODUCTION_DOTENVS_DIR / ".oracle",
]
DOTENV_FILE = BASE_DIR / ".env"


def merge(
    output_file: Path,
    files_to_merge: Sequence[Path],
) -> None:
    merged_content = ""
    for merge_file in files_to_merge:
        if merge_file.exists():
            merged_content += merge_file.read_text().strip()
            merged_content += "\n# CUSTOM LOCAL VARIABLES\n"
    if output_file.exists():
        for ouput_line in output_file.open("r"):
            m = re.match(r"^(\w+)=([^\n]+)", ouput_line)
            if m:
                var_name = r"^#?\s*" + m.group(1) + r"=[^\n]+"
                (merged_content, has_changed) = re.subn(var_name, ouput_line, merged_content, flags=re.MULTILINE)
                if has_changed == 0:
                    merged_content += ouput_line

    output_file.write_text(merged_content)

if __name__ == "__main__":
    merge(DOTENV_FILE, PRODUCTION_DOTENV_FILES)
