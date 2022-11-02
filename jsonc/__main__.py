import argparse
import json
import sys

from . import load


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("f", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("--allow-trailing-comma", action="store_true")

    args = parser.parse_args()

    print(json.dumps(load(args.f, allow_trailing_comma=args.allow_trailing_comma)))


if __name__ == "__main__":  # pragma: no cover
    main()
