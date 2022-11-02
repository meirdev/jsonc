import json
import sys
import unittest.mock
from pathlib import Path

from jsonc.__main__ import main

BASE_DIR = Path(__file__).resolve().parent


def test_main(capsys):
    with unittest.mock.patch.object(
        sys, "argv", ["", str(BASE_DIR / "test_file.jsonc"), "--allow-trailing-comma"]
    ):
        main()
        captured = capsys.readouterr()
        json.loads(captured.out)
