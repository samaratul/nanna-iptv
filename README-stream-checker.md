# IPTV Stream Checker

Checks every URL in `playlist.m3u8` and reports which channels are actually
live right now. No external dependencies — pure Python standard library.

## Run it locally

```bash
python3 check_streams.py playlist.m3u8
```

This prints live progress to the terminal and writes three files:

- **`playlist_working.m3u8`** — updates **live, the instant each channel is
  confirmed working** — not batched at the end. The file is created (with
  just the `#EXTM3U` header) the moment the run starts, and every working
  channel is appended and flushed to disk as soon as it's found. You can
  point a player at this file, or `tail -f playlist_working.m3u8`, and
  watch it fill in while the check is still running — no need to wait for
  all channels to finish.
- **`stream_report.md`** — readable report, grouped by `Language - Category`,
  listing which channels are dead and why (timeout, HTTP 404, connection
  refused, etc.). Written once the full run completes.
- **`stream_report.json`** — same data as JSON, for scripting/dashboards.
  Also written once the full run completes.

Useful flags:

```bash
python3 check_streams.py playlist.m3u8 --workers 40 --fail-threshold 25
```

- `--workers` — how many streams to check in parallel (default 24)
- `--fail-threshold` — exit code 1 if more than this % of streams are dead
  (default 40), useful for CI

## Run it automatically as a GitHub "bot"

1. Create a repo (or use an existing one) and add:
   - `playlist.m3u8` (your playlist)
   - `check_streams.py` (this script, at the repo root)
   - `.github/workflows/check-streams.yml` (rename `check-streams.yml`
     from this bundle and place it at that exact path)
2. Push to GitHub.
3. Under the **Actions** tab, the workflow will run automatically every
   6 hours (edit the `cron` line in the workflow to change that), and you
   can also trigger it manually with **Run workflow**.
4. Each run commits a fresh `stream_report.md`, `stream_report.json`, and
   `playlist_working.m3u8` back to the repo.
5. If more than 40% of streams are dead, it automatically opens (or
   updates) a GitHub Issue tagged `stream-check` summarizing what's down —
   so you find out without checking manually.

## Notes

- Free IPTV streams flake in and out — a channel marked dead on one run
  might come back on the next. The retry logic (2 retries, 1.5s backoff)
  filters out most transient blips, but persistent failures usually mean
  the source really is down or the URL changed.
- The checker only downloads the first ~2KB of each stream to confirm it's
  real video/HLS content — it never downloads full video, so bandwidth use
  is minimal even for hundreds of channels.
- Some servers block requests without a browser-like `User-Agent` or from
  cloud IP ranges (GitHub Actions runners included) — a channel that works
  fine in your player but shows dead here may be geo/IP-restricted rather
  than actually offline.
