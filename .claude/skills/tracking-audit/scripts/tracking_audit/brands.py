"""Brand list parsing: URL normalisation and folder slugs."""

import re
from pathlib import Path
from urllib.parse import urlparse

# Second-level labels that are not the brand (e.g. foo.co.uk, foo.com.au).
_GENERIC_SLD = {"co", "com", "org", "net", "gov", "edu", "ac"}


def normalize_url(raw: str) -> str:
    raw = raw.strip()
    if not re.match(r"^https?://", raw, re.I):
        raw = "https://" + raw
    return raw


def slug_for(url: str) -> str:
    """bychari.com -> bychari, www.explorescientific.ca -> explorescientific."""
    host = urlparse(url).hostname or url
    labels = [l for l in host.lower().split(".") if l and l != "www"]
    if len(labels) >= 3 and labels[-2] in _GENERIC_SLD:
        labels = labels[:-2]
    elif len(labels) >= 2:
        labels = labels[:-1]
    return re.sub(r"[^a-z0-9]+", "", labels[-1]) if labels else "site"


def parse_brand(entry: str) -> tuple[str, str]:
    """Accepts 'url' or 'slug=url'. Returns (slug, url)."""
    entry = entry.strip()
    if "=" in entry and not entry.lower().startswith("http"):
        slug, url = entry.split("=", 1)
        return slug.strip().lower(), normalize_url(url)
    url = normalize_url(entry)
    return slug_for(url), url


def load_brands(args: list[str], brands_file: Path | None) -> list[tuple[str, str]]:
    entries: list[str] = []
    for a in args:
        p = Path(a)
        if p.suffix in {".txt", ".md"} and p.exists():
            brands_file = p
        else:
            entries.append(a)
    if not entries and brands_file and brands_file.exists():
        for line in brands_file.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip().strip("-* ").strip()
            if line:
                entries.append(line)
    seen, out = set(), []
    for e in entries:
        slug, url = parse_brand(e)
        if slug not in seen:
            seen.add(slug)
            out.append((slug, url))
    return out
