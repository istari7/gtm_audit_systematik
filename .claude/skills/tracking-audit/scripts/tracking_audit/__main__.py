"""CLI: python -m tracking_audit <command> [brands...]

  run      capture + parse + report for each brand (default command)
  capture  Playwright visit with consent accept + reload; saves containers + network
  parse    decode containers + analyse network -> outputs/<brand>/audit.json
  report   render outputs/<brand>/README.md from audit.json (keeps Analyst Notes)
  index    rebuild outputs/AUDIT_INDEX.md (summary table of all brand folders; README.md is the static how-to)
  fetch    fetch a container by ID directly:  fetch GTM-XXXX --brand <slug>
  resolve  mark a flagged capture as manually verified:  resolve <slug> --note "MCP re-capture, OneTrust accepted"
  ingest   build raw/ files from a Playwright MCP session (bot-wall fallback):
           ingest <url> --brand <slug> --requests reqs.txt [--consent "OneTrust button"] [--snapshot snap.json]

Brands are URLs ("bychari.com"), "slug=url", or a .txt file (one per line).
With no brands, brands.txt in the current directory is used. Output goes to outputs/<slug>/ (see --out).
"""

import argparse
import asyncio
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from .brands import load_brands
from .container import analyze, container_id_from, extract_data
from .findings import build_findings
from .network import analyze_network
from .reconstruct import reconstruct
from .best_practices import evaluate
from .platforms import evaluate_platforms
from .analyst_checks import build_checklist
from .report import render, render_index

INDEX_FILE = "AUDIT_INDEX.md"  # generated brand table; the root README.md is hand-written docs


def brand_name(capture: dict, slug: str) -> str:
    snaps = capture.get("snapshots") or {}
    for key in ("reload", "initial"):
        s = snaps.get(key) or {}
        if s.get("site_name"):
            return s["site_name"].strip()
    title = (snaps.get("reload") or snaps.get("initial") or {}).get("title") or ""
    parts = [p.strip() for p in re.split(r"\s[|–—-]\s", title) if p.strip()]
    if parts:
        short = min(parts, key=len)
        if len(short) <= 40:
            return short
    return slug.title()


def best_practice_findings(bp: dict, prefix: str = "GTM") -> list[dict]:
    out = []
    for cid, res in bp.items():
        for c in res["checks"]:
            if c["status"] not in ("fail", "warn") or c["check"] == "Universal Analytics removed":
                continue
            sev = ("P1" if c["status"] == "fail" and c["impact"] == "High" else
                   "P2" if c["status"] == "fail" or c["impact"] == "High" else "P3")
            out.append({"severity": sev, "area": f"{prefix} · {c['area']}", "title": ("Not met: " if c["status"] == "fail" else "Needs attention: ")
                        + (f"{c['check']} — {cid}" if prefix == "GTM" else f"{c['area']} — {c['check']}"),
                        "detail": c["evidence"] + (f" Why it matters: {c['why']}" if c.get("why") else ""),
                        "recommendation": c["recommendation"] or "Review.", "source": "best_practice"})
    return out


def parse_brand(root: Path, slug: str, url: str) -> dict:
    bdir = root / slug
    capture = json.loads((bdir / "raw" / "capture.json").read_text(encoding="utf-8"))
    requests = json.loads((bdir / "raw" / "network.json").read_text(encoding="utf-8"))
    html_path = bdir / "raw" / "page.html"
    html = html_path.read_text(encoding="utf-8") if html_path.exists() else ""

    cmeta = {c["id"]: c for c in capture.get("containers", [])}
    containers, datas = [], {}
    for jf in sorted(p for p in (bdir / "containers").glob("*.json") if not p.name.endswith(".export.json")):
        data = json.loads(jf.read_text(encoding="utf-8"))
        cid = jf.stem
        datas[cid] = data
        m = cmeta.get(cid, {})
        containers.append(analyze(data, cid, {k: m.get(k) for k in ("url", "phase", "first_party_loader", "size_kb")}))
        if cid.startswith("GTM-"):
            export = reconstruct(data, cid)
            (bdir / "containers" / f"{cid}.export.json").write_text(json.dumps(export, indent=1, ensure_ascii=False),
                                                                  encoding="utf-8")
            containers[-1]["reconstruction"] = export["reconstruction"]
    containers.sort(key=lambda c: (c["kind"] != "gtm", c["id"]))

    net = analyze_network(requests, capture, html)
    url = capture.get("url") or url
    audit = {
        "brand": {"slug": slug, "url": url, "name": brand_name(capture, slug), "final_url": capture.get("final_url"),
                  "platform": net["platform"], "audit_date": date.today().isoformat()},
        "capture": {k: v for k, v in capture.items() if k not in ("snapshots", "containers")},
        "network": net,
        "containers": containers,
    }
    audit["findings"] = build_findings(audit)
    audit["best_practices"] = evaluate(audit, datas)
    audit["findings"] += best_practice_findings(audit["best_practices"])
    ini_path = bdir / "raw" / "initiators.json"
    initiators = json.loads(ini_path.read_text(encoding="utf-8")) if ini_path.exists() else []
    audit["platforms"] = evaluate_platforms(audit, requests, initiators, html)
    audit["findings"] += best_practice_findings({k: v for k, v in audit["platforms"].items() if not k.startswith("_")},
                                                prefix="Tracking")
    order = {"P1": 0, "P2": 1, "P3": 2}
    audit["findings"].sort(key=lambda f: order[f["severity"]])
    audit["analyst_checklist"] = build_checklist(audit)
    (bdir / "audit.json").write_text(json.dumps(audit, indent=1, ensure_ascii=False, default=list), encoding="utf-8")
    p1 = sum(f["severity"] == "P1" for f in audit["findings"])
    print(f"[{slug}] parsed: {len(containers)} container(s), {net['totals']['vendors']} vendors, "
          f"{len(audit['findings'])} findings ({p1} P1)")
    return audit


def report_brand(root: Path, slug: str):
    bdir = root / slug
    audit = json.loads((bdir / "audit.json").read_text(encoding="utf-8"))
    readme = bdir / "README.md"
    prev = readme.read_text(encoding="utf-8") if readme.exists() else None
    readme.write_text(render(audit, prev), encoding="utf-8")
    print(f"[{slug}] report -> {readme}")


def fetch_container(root: Path, cid: str, slug: str):
    """Download a container by ID (GTM-… via gtm.js, G-/AW-/GT-/DC- via gtag/js). A 404 means the ID is
    referenced on the site but not published - recorded so it surfaces as a finding."""
    path = "gtm.js" if cid.startswith("GTM-") else "gtag/js"
    req = urllib.request.Request(f"https://www.googletagmanager.com/{path}?id={cid}", headers={"User-Agent": "Mozilla/5.0"})
    cap_path = root / slug / "raw" / "capture.json"
    cap = json.loads(cap_path.read_text(encoding="utf-8")) if cap_path.exists() else {}
    try:
        body = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        print(f"[{slug}] {cid}: HTTP {e.code} - container is not published")
        if cap_path.exists():
            cap["unpublished_containers"] = sorted(set(cap.get("unpublished_containers", [])) | {cid})
            cap_path.write_text(json.dumps(cap, indent=1, ensure_ascii=False), encoding="utf-8")
        return
    data = extract_data(body)
    if not data:
        print(f"[{slug}] {cid}: no container JSON in response")
        return
    cdir = root / slug / "containers"
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / f"{cid}.js").write_text(body, encoding="utf-8")
    (cdir / f"{cid}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    if cap_path.exists():
        cap.setdefault("containers", [])
        cap["containers"] = [c for c in cap["containers"] if c["id"] != cid] + [{
            "id": cid, "url": req.full_url, "phase": "direct_fetch",
            "first_party_loader": False, "size_kb": round(len(body.encode()) / 1024, 1)}]
        cap_path.write_text(json.dumps(cap, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"[{slug}] {cid} saved ({round(len(body) / 1024)} KB)")


MCP_LINE = re.compile(r"\[(GET|POST|PUT|HEAD|OPTIONS)\]\s+(\S+)(?:\s+=>\s+\[(\d+)\])?", re.I)


def ingest_mcp(root: Path, slug: str, url: str, requests_file: Path, consent: str | None, snapshot_file: Path | None):
    """Build raw/ files from a Playwright MCP session (browser_network_requests output saved to a file).
    Lines before a line containing '--- reload ---' are tagged 'initial', the rest 'reload'."""
    bdir = root / slug / "raw"
    bdir.mkdir(parents=True, exist_ok=True)
    phase, reqs = "initial", []
    for line in requests_file.read_text(encoding="utf-8").splitlines():
        if "--- reload ---" in line:
            phase = "reload"
            continue
        m = MCP_LINE.search(line)
        if m:
            reqs.append({"phase": phase, "url": m.group(2), "method": m.group(1).upper(), "type": "other",
                         "status": int(m.group(3)) if m.group(3) else None, "failure": None, "post": None, "frame": None})
    snaps = json.loads(snapshot_file.read_text(encoding="utf-8")) if snapshot_file else {}
    cap_path = bdir / "capture.json"
    cap = json.loads(cap_path.read_text(encoding="utf-8")) if cap_path.exists() else {}
    cap.update({"slug": slug, "url": url, "final_url": url, "method": "playwright-mcp",
                "consent": {"accepted": bool(consent), "method": "manual (MCP)" if consent else None, "detail": consent},
                "snapshots": {"reload": snaps} if snaps else cap.get("snapshots", {}), "request_count": len(reqs)})
    cap.setdefault("containers", [])
    (bdir / "network.json").write_text(json.dumps(reqs, indent=1), encoding="utf-8")
    cap_path.write_text(json.dumps(cap, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"[{slug}] ingested {len(reqs)} MCP requests")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="tracking_audit", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", default="run", choices=["run", "capture", "parse", "report", "index", "fetch", "ingest", "resolve"])
    ap.add_argument("brands", nargs="*")
    ap.add_argument("--out", default="outputs", help="output root; each brand gets <out>/<slug>/ (default: outputs)")
    ap.add_argument("--brand", help="slug for `fetch` / `ingest`")
    ap.add_argument("--requests", help="`ingest`: file with browser_network_requests output")
    ap.add_argument("--consent", help="`ingest`: how consent was accepted")
    ap.add_argument("--note", help="`resolve`: how the review flag was verified / fixed")
    ap.add_argument("--snapshot", help="`ingest`: JSON from the page snapshot script")
    ap.add_argument("--headless", action="store_true", help="headless browser (more likely to be bot-blocked)")
    ap.add_argument("--no-pdp", action="store_true", help="skip product page + add-to-cart")
    ap.add_argument("--dwell", type=int, default=5000, help="ms to wait after each load (default 5000)")
    ap.add_argument("--fresh", action="store_true",
                    help="clear these brands' cookies/storage in the persistent profile for a true first visit")
    ap.add_argument("--profile", help="persistent browser profile dir (default: ./.browser-profile)")
    ap.add_argument("--parallel", type=int, default=3, help="brands captured concurrently (default 3)")
    a = ap.parse_args(argv)
    root = Path(a.out).resolve()
    root.mkdir(parents=True, exist_ok=True)

    if a.command == "fetch":
        for cid in a.brands:
            fetch_container(root, cid, a.brand or sys.exit("--brand required"))
        return
    if a.command == "resolve":
        for slug in a.brands:
            cp = root / slug / "raw" / "capture.json"
            cap = json.loads(cp.read_text(encoding="utf-8"))
            cap["review_resolved"] = a.note or "verified manually"
            cp.write_text(json.dumps(cap, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"[{slug}] review resolved: {cap['review_resolved']}")
        return
    if a.command == "ingest":
        if not (a.brand and a.requests and a.brands):
            sys.exit("ingest needs <url> --brand <slug> --requests <file>")
        ingest_mcp(root, a.brand, a.brands[0], Path(a.requests), a.consent, Path(a.snapshot) if a.snapshot else None)
        return
    if a.command == "index":
        (root / INDEX_FILE).write_text(render_index(root), encoding="utf-8")
        print(f"index -> {root / INDEX_FILE}")
        return

    brands = load_brands(a.brands, Path("brands.txt"))
    if not brands:
        # parse/report may also be given bare slugs of existing folders
        sys.exit("no brands given and no brands.txt found")

    if a.command in ("run", "capture"):
        from .capture import capture_all
        asyncio.run(capture_all(brands, root, headless=a.headless, dwell_ms=a.dwell, pdp=not a.no_pdp,
                                parallel=a.parallel, fresh=a.fresh, profile=Path(a.profile) if a.profile else None))
    if a.command in ("run", "parse"):
        for slug, url in brands:
            try:
                parse_brand(root, slug, url)
            except FileNotFoundError as e:
                print(f"[{slug}] skipped parse: {e}")
    if a.command in ("run", "report"):
        for slug, _ in brands:
            if (root / slug / "audit.json").exists():
                report_brand(root, slug)
    if a.command == "run":
        (root / INDEX_FILE).write_text(render_index(root), encoding="utf-8")
        print(f"index -> {root / INDEX_FILE}")


if __name__ == "__main__":
    main()
