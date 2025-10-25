from __future__ import annotations

import argparse
import sys
from typing import List

import httpx

from confradar.extraction.date_extract import extract_dates_from_text


def _read_stdin() -> str:
    return sys.stdin.read()


def cmd_parse(args: argparse.Namespace) -> int:
    text = args.text if args.text is not None else _read_stdin()
    dates = extract_dates_from_text(text)
    for d in dates:
        print(d.isoformat())
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    url = args.url
    with httpx.Client(timeout=15) as client:
        resp = client.get(url)
        resp.raise_for_status()
        text = resp.text
    dates = extract_dates_from_text(text)
    for d in dates:
        print(d.isoformat())
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="confradar", description="ConfRadar CLI")
    sub = p.add_subparsers(dest="command", required=True)

    p_parse = sub.add_parser("parse", help="Parse dates from provided text or stdin")
    p_parse.add_argument("--text", type=str, default=None, help="Text to parse; defaults to stdin")
    p_parse.set_defaults(func=cmd_parse)

    p_fetch = sub.add_parser("fetch", help="Fetch a URL and parse date-like values")
    p_fetch.add_argument("url", type=str, help="URL to fetch")
    p_fetch.set_defaults(func=cmd_fetch)

    return p


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    return ns.func(ns)


if __name__ == "__main__":
    raise SystemExit(main())
