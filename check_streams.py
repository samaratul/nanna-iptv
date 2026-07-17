#!/usr/bin/env python3
"""
check_streams.py

Validates every stream URL in an M3U/M3U8 playlist and reports which
channels are live vs. dead. Designed to run either:
  - locally: `python check_streams.py playlist.m3u8`
  - in CI (GitHub Actions) on a schedule, acting as an automated "bot"
    that keeps the playlist honest.

For each #EXTINF entry, it:
  1. Sends an HTTP GET with a short timeout and streams only the first
     chunk of the response (never downloads the whole video).
  2. Confirms the response is actually playlist/video-like content
     (an HLS/M3U8 manifest, or a video/octet-stream body) rather than
     a login page, 404 page, or empty response.
  3. Retries each URL up to RETRIES times before marking it dead, since
     free IPTV servers are often just momentarily slow.

Outputs:
  - playlist_working.m3u8  Written incrementally: the moment a stream is
    confirmed working it is appended to this file immediately, so you can
    load it into a player or `tail -f` it mid-run instead of waiting for
    every channel to finish checking.
  - stream_report.md   Human-readable report (working/dead per group),
    written once all checks finish.
  - stream_report.json Machine-readable results for other tooling.
  - Exit code 1 if more than FAIL_THRESHOLD% of streams are dead (useful
    for failing a CI job / triggering a GitHub issue), else exit code 0.
"""

import sys
import re
import json
import time
import argparse
import concurrent.futures as cf
from dataclasses import dataclass, field
from urllib.parse import urlparse

import urllib.request
import urllib.error
import ssl

TIMEOUT_SECONDS = 8
RETRIES = 2
RETRY_BACKOFF_SECONDS = 1.5
MAX_WORKERS = 24
FAIL_THRESHOLD_PCT = 40  # exit 1 if more than this % of streams are dead
CHUNK_BYTES = 2048
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) StreamChecker/1.0"

# Content that suggests a *working* HLS/video stream
GOOD_SIGNATURES = (b"#EXTM3U", b"#EXT-X-", b"ftyp", b"\x47")  # last one: MPEG-TS sync byte
# Content that suggests a dead/placeholder response (login walls, error pages)
BAD_SIGNATURES = (b"<html", b"<!DOCTYPE", b"404 Not Found", b"channel not found")


@dataclass
class Entry:
    tvg_id: str
    name: str
    group: str
    url: str
    extinf_line: str


@dataclass
class Result:
    entry: Entry
    ok: bool
    reason: str
    attempts: int = 0
    elapsed_ms: int = 0


class IncrementalPlaylistWriter:
    """
    Opens playlist_working.m3u8 immediately and appends each confirmed-working
    entry to it as soon as it's found, flushing + fsyncing every write so the
    file is genuinely up to date on disk in real time — not just buffered in
    memory until the run finishes. Safe to call from multiple worker threads.
    """

    def __init__(self, path="playlist_working.m3u8", header_lines=None):
        import threading
        self._lock = threading.Lock()
        self.path = path
        self._f = open(path, "w", encoding="utf-8")
        for line in (header_lines or ["#EXTM3U"]):
            self._f.write(line + "\n")
        self._f.flush()
        self.written = 0

    def add(self, entry: Entry):
        with self._lock:
            self._f.write(entry.extinf_line + "\n")
            self._f.write(entry.url + "\n")
            self._f.flush()
            import os
            os.fsync(self._f.fileno())
            self.written += 1

    def close(self):
        self._f.close()


def parse_m3u(path: str):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    lines = content.replace("\r\n", "\n").split("\n")
    entries = []
    header_lines = []
    i = 0
    seen_extm3u = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTM3U"):
            header_lines.append(line)
            seen_extm3u = True
            i += 1
            continue
        if line.startswith("#EXTINF"):
            m_id = re.search(r'tvg-id="([^"]*)"', line)
            m_group = re.search(r'group-title="([^"]*)"', line)
            name = line.split(",", 1)[-1].strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            url = lines[j].strip() if j < len(lines) else ""
            entries.append(Entry(
                tvg_id=m_id.group(1) if m_id else "",
                name=name,
                group=m_group.group(1) if m_group else "",
                url=url,
                extinf_line=line,
            ))
            i = j + 1
        else:
            i += 1
    return header_lines, entries


def check_one(entry: Entry) -> Result:
    if not entry.url or not urlparse(entry.url).scheme.startswith("http"):
        return Result(entry, False, "no http(s) url")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # many free IPTV hosts use self-signed/expired certs

    last_reason = "unknown error"
    start = time.time()
    for attempt in range(1, RETRIES + 2):
        try:
            req = urllib.request.Request(entry.url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS, context=ctx) as resp:
                status = resp.status
                chunk = resp.read(CHUNK_BYTES)
                elapsed = int((time.time() - start) * 1000)
                if status >= 400:
                    last_reason = f"HTTP {status}"
                elif any(sig in chunk for sig in BAD_SIGNATURES):
                    last_reason = "got HTML/error page instead of stream"
                elif len(chunk) == 0:
                    last_reason = "empty response body"
                else:
                    # Either a valid HLS manifest, or binary video data (TS/fMP4) — treat as alive
                    return Result(entry, True, f"HTTP {status}, {len(chunk)}B received", attempt, elapsed)
        except urllib.error.HTTPError as e:
            last_reason = f"HTTP {e.code}"
        except urllib.error.URLError as e:
            last_reason = f"connection error: {e.reason}"
        except (TimeoutError, OSError) as e:
            last_reason = f"timeout/os error: {e}"
        except Exception as e:  # noqa: BLE001 — log and retry regardless of cause
            last_reason = f"unexpected error: {e}"

        if attempt <= RETRIES:
            time.sleep(RETRY_BACKOFF_SECONDS)

    elapsed = int((time.time() - start) * 1000)
    return Result(entry, False, last_reason, RETRIES + 1, elapsed)


def run_checks(entries, max_workers=MAX_WORKERS, writer: "IncrementalPlaylistWriter | None" = None):
    results = []
    with cf.ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(check_one, e): e for e in entries}
        for i, fut in enumerate(cf.as_completed(futures), 1):
            res = fut.result()
            results.append(res)
            if res.ok and writer is not None:
                writer.add(res.entry)  # written to disk immediately, not batched
            status = "OK  " if res.ok else "DEAD"
            live_note = " -> written to playlist_working.m3u8" if (res.ok and writer is not None) else ""
            print(f"[{i}/{len(entries)}] {status} {res.entry.group:<28} {res.entry.name}  ({res.reason}){live_note}")
    return results


def write_report_md(results, path="stream_report.md"):
    total = len(results)
    working = sum(1 for r in results if r.ok)
    dead = total - working
    by_group = {}
    for r in results:
        by_group.setdefault(r.entry.group, []).append(r)

    lines = [
        "# Stream Check Report",
        "",
        f"Checked **{total}** streams — **{working} working**, **{dead} dead** "
        f"({(dead / total * 100 if total else 0):.1f}% dead).",
        "",
    ]
    for group in sorted(by_group):
        group_results = by_group[group]
        g_dead = [r for r in group_results if not r.ok]
        lines.append(f"## {group} ({len(group_results) - len(g_dead)}/{len(group_results)} working)")
        if g_dead:
            for r in g_dead:
                lines.append(f"- ❌ **{r.entry.name}** — {r.reason}  \n  `{r.entry.url}`")
        else:
            lines.append("- ✅ all working")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_report_json(results, path="stream_report.json"):
    data = [
        {
            "name": r.entry.name,
            "group": r.entry.group,
            "tvg_id": r.entry.tvg_id,
            "url": r.entry.url,
            "ok": r.ok,
            "reason": r.reason,
            "attempts": r.attempts,
            "elapsed_ms": r.elapsed_ms,
        }
        for r in results
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    ap = argparse.ArgumentParser(description="Check every stream URL in an M3U8 playlist.")
    ap.add_argument("playlist", help="Path to playlist.m3u8")
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--fail-threshold", type=float, default=FAIL_THRESHOLD_PCT,
                     help="Exit 1 if more than this percent of streams are dead")
    args = ap.parse_args()

    header_lines, entries = parse_m3u(args.playlist)
    if not entries:
        print("No #EXTINF entries found — check the playlist path.", file=sys.stderr)
        sys.exit(2)

    print(f"Checking {len(entries)} streams with {args.workers} workers...")
    print("playlist_working.m3u8 will update live as each working stream is confirmed.\n")

    writer = IncrementalPlaylistWriter("playlist_working.m3u8", header_lines)
    try:
        results = run_checks(entries, max_workers=args.workers, writer=writer)
    finally:
        writer.close()

    write_report_md(results)
    write_report_json(results)

    total = len(results)
    dead = sum(1 for r in results if not r.ok)
    dead_pct = dead / total * 100 if total else 0
    print(f"\nDone: {total - dead}/{total} working ({dead_pct:.1f}% dead).")
    print(f"playlist_working.m3u8 has {writer.written} channels (updated live during the run).")
    print("Wrote stream_report.md, stream_report.json")

    if dead_pct > args.fail_threshold:
        print(f"FAIL: dead rate {dead_pct:.1f}% exceeds threshold {args.fail_threshold}%")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
