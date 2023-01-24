from argparse import ArgumentParser
from pathlib import Path
from typing import List

from callscript import modify_code


def main(args = None):
    parser = ArgumentParser(description="Extract Script into a Module using Comment Tags")
    parser.add_argument('script', help="Path to the script")

    args = parser.parse_args(args=args)

    code = Path(args.script).read_text()
    meta = modify_code(code=code)
    new_code = meta['code']
    print(new_code)


if __name__ == '__main__':
    main()
