#!/bin/python3
import subprocess
from pathlib import Path
import configparser
import argparse
import os
import sys
import shlex

CONFIG = "/usr/local/etc/zipy-backup.conf"

OPT_MAP = {"recurse": "r", "quiet": "q", "store_only": "0", "encrypt": "e"}


class Zipper:
    def __init__(self, dest: Path, src: Path, **kwargs):
        self.dest = dest
        self.src = src
        self.options = [OPT_MAP[opt] for opt in kwargs if kwargs[opt]]
        self.password = ""

    def encrypt(self, password: str):
        self.password = password
        self.options.append("e")

    @property
    def option_string(self) -> str:
        opts = "".join(self.options)
        return ("-" + opts) if opts else ""

    def __str__(self):
        return f"zip {self.option_string} {self.dest} ." + (
            f" -P {self.password}" if self.password else ""
        )

    @property
    def subprocess_list(self):
        return shlex.split(str(self))


class ZipperFactory:
    def __init__(self, dest: str):
        self.__recurse = True
        self.__quiet = True
        self.__store_only = True
        self.__dest = Path(dest).expanduser()

    def set_recurse(self, opt: bool):
        self.__recurse = opt
        return self

    def set_quiet(self, opt: bool):
        self.__quiet = opt
        return self

    def set_store_only(self, opt: bool):
        self.__store_only = opt
        return self

    def new(self, filename: str, source: str) -> Zipper:
        filename = filename if filename.endswith(".zip") else filename + ".zip"
        source = Path(source).expanduser()
        return Zipper(
            self.__dest.joinpath(filename),
            source,
            recurse=self.__recurse,
            quiet=self.__quiet,
            store_only=self.__store_only,
        )


def backup(sections, destination, quiet=False):
    zf = ZipperFactory(destination)

    for sect in sections:
        if "SOURCE" not in sect:
            if not quiet:
                print("Error: no source directory given, skipping", sys.stderr)
            continue
        zipper = zf.new(sect.name, sect["SOURCE"])
        if "PASSWORD" in sect:
            zipper.encrypt(sect["PASSWORD"])
        if not quiet:
            print(f"executing {zipper}")
        subprocess.run(zipper.subprocess_list, cwd=zipper.src)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", "-q", help="suppress all output", action="store_true", default=False)
    args = parser.parse_args()

    if not os.path.exists(CONFIG):
        if not args.quiet:
            print(f"{CONFIG}: No such file.", file=sys.stderr)
        sys.exit(1)
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG)
    except Exception as e:
        if not args.quiet:
            print(f"Bad config: {str(e)}", file=sys.stderr)
        sys.exit(1)

    sections = [config[section] for section in config.sections()]
    destination = config["DEFAULT"].get("DESTINATION", "~")
    backup(sections, destination, quiet=args.quiet)


if __name__ == "__main__":
    main()
