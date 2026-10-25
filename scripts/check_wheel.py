#!/usr/bin/env python3
"""Install one built wheel into a temporary uv environment and smoke-test it."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

EXTRAS = ("base", "httpx", "playwright", "all")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path, help="path to a built .whl file")
    parser.add_argument("--extra", choices=EXTRAS, required=True)
    args = parser.parse_args()

    wheel = args.wheel.resolve()
    if not wheel.is_file() or wheel.suffix != ".whl":
        parser.error(f"wheel does not exist or is not a .whl file: {wheel}")

    uv = os.environ.get("UV", "uv")
    smoke_script = Path(__file__).with_name("smoke_installed.py").resolve()
    with TemporaryDirectory(prefix="extract-emails-wheel-") as directory:
        environment = Path(directory) / "venv"
        workdir = Path(directory) / "work"
        workdir.mkdir()
        subprocess.run(
            [uv, "venv", "--python", sys.executable, str(environment)],
            check=True,
            cwd=workdir,
        )
        python = environment / (
            "Scripts/python.exe" if os.name == "nt" else "bin/python"
        )
        extras = f"[{args.extra}]" if args.extra != "base" else ""
        package_requirement = f"extract-emails{extras} @ {wheel.as_uri()}"
        subprocess.run(
            [uv, "pip", "install", "--python", str(python), package_requirement],
            check=True,
            cwd=workdir,
        )
        subprocess.run(
            [str(python), str(smoke_script), "--extra", args.extra],
            check=True,
            cwd=workdir,
        )


if __name__ == "__main__":
    main()
