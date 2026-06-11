#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API_ENDPOINT = "https://en.wikipedia.org/w/api.php"


class PageNotFoundError(Exception):
    pass


def build_api_url(article_title: str, limit: int = 30) -> str:
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": article_title,
        "rvprop": "timestamp|user",
        "rvlimit": str(limit),
        "redirects": "1",
    }
    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"{API_ENDPOINT}?{query_string}"


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; Python script)"},
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def parse_api_response(data: dict[str, Any]) -> tuple[str | None, list[tuple[str, str]]]:
    query = data.get("query", {})
    redirects = query.get("redirects")
    redirect_target = None
    if redirects:
        redirect_target = str(redirects[-1].get("to", ""))

    pages = query.get("pages", {})
    if not pages:
        raise PageNotFoundError("No Wikipedia page for the specified article.")

    page = next(iter(pages.values()))
    if page.get("missing") is not None or page.get("invalid") is not None:
        raise PageNotFoundError("No Wikipedia page for the specified article.")

    revisions = page.get("revisions", [])
    changes: list[tuple[str, str]] = []
    for revision in revisions:
        timestamp = revision.get("timestamp")
        user = revision.get("user")
        if timestamp is not None and user is not None:
            changes.append((timestamp, user))

    changes.sort(key=lambda item: item[0], reverse=True)
    return redirect_target, changes


def format_redirect_message(redirect_target: str) -> str:
    return f"Redirected to {redirect_target}"


def format_change_line(timestamp: str, user: str) -> str:
    return f"{timestamp} {user}"


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print("Please provide a Wikipedia article name.", file=sys.stderr)
        return 1

    article_title = " ".join(argv[1:]).strip()
    if not article_title:
        print("Please provide a Wikipedia article name.", file=sys.stderr)
        return 1

    try:
        api_url = build_api_url(article_title)
        data = fetch_json(api_url)
        redirect_target, changes = parse_api_response(data)
    except PageNotFoundError as error:
        print(error, file=sys.stderr)
        return 2
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as error:
        print(f"Network error: {error}", file=sys.stderr)
        return 3

    if redirect_target:
        print(format_redirect_message(redirect_target))

    for timestamp, user in changes:
        print(format_change_line(timestamp, user))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
