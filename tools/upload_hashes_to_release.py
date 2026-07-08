"""Upload bsassets hashes/ as individual files to a GitHub release.

Flattens hashes/XX/YY/ZZZZ -> XXYYZZZZ (full hash name) and uploads
to a GitHub release via gh CLI. Designed for lesscache consumption.

Resumes automatically: skips files already present on the release.
Respects GitHub secondary rate limits with configurable delays.

Usage:
  python3 tools/upload_hashes_to_release.py [--batch-size N] [--delay S] [--dry-run]
"""

from __future__ import annotations

import os
import sys
import json
import time
import subprocess

HASHES_DIR = "hashes"
STAGING_DIR = "build/lesscache-staging"
RELEASE_TAG = "lesscache"
RELEASE_TITLE = "Lesscache Prebuilts"
RELEASE_NOTES = (
    "Individual hash files for lesscache consumption. Auto-generated."
)
DEFAULT_BATCH_SIZE = 25
DEFAULT_DELAY = 15


def _get_existing_assets(tag: str) -> set[str]:
    result = subprocess.run(
        ["gh", "release", "view", tag, "--json", "assets", "--jq",
         "[.assets[].name]"],
        check=True,
        capture_output=True,
        text=True,
    )
    return set(json.loads(result.stdout))


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    batch_size = DEFAULT_BATCH_SIZE
    delay = DEFAULT_DELAY
    for i, arg in enumerate(sys.argv):
        if arg == "--batch-size" and i + 1 < len(sys.argv):
            batch_size = int(sys.argv[i + 1])
        if arg == "--delay" and i + 1 < len(sys.argv):
            delay = int(sys.argv[i + 1])

    if not os.path.isdir(HASHES_DIR):
        print(f"ERROR: {HASHES_DIR} directory not found. "
              f"Run from bsassets repo root.")
        sys.exit(1)

    os.makedirs(STAGING_DIR, exist_ok=True)

    flat_files: list[str] = []
    for prefix in sorted(os.listdir(HASHES_DIR)):
        prefix_path = os.path.join(HASHES_DIR, prefix)
        if not os.path.isdir(prefix_path):
            continue
        for mid in sorted(os.listdir(prefix_path)):
            mid_path = os.path.join(prefix_path, mid)
            if not os.path.isdir(mid_path):
                continue
            for rest in sorted(os.listdir(mid_path)):
                src = os.path.join(mid_path, rest)
                if not os.path.isfile(src):
                    continue
                full_hash = f"{prefix}{mid}{rest}"
                dst = os.path.join(STAGING_DIR, full_hash)
                if not os.path.exists(dst):
                    os.link(src, dst)
                flat_files.append(dst)

    total = len(flat_files)
    print(f"Staged {total} hash files in {STAGING_DIR}.")

    if dry_run:
        print("DRY RUN: would upload to release "
              f"'{RELEASE_TAG}' in {batch_size}-file batches.")
        return

    print(f"Checking/creating GitHub release '{RELEASE_TAG}'...")
    result = subprocess.run(
        ["gh", "release", "view", RELEASE_TAG],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        print(f"Creating release '{RELEASE_TAG}'...")
        subprocess.run(
            [
                "gh", "release", "create", RELEASE_TAG,
                "--title", RELEASE_TITLE,
                "--notes", RELEASE_NOTES,
            ],
            check=True,
        )
        existing = set()
    else:
        print("Fetching existing assets on release...")
        existing = _get_existing_assets(RELEASE_TAG)
        print(f"  {len(existing)} assets already on release.")

    new_files = [
        f for f in flat_files
        if os.path.basename(f) not in existing
    ]
    skipped = total - len(new_files)
    if skipped:
        print(f"Skipping {skipped} already-uploaded files.")
    if not new_files:
        print("All files already uploaded. Nothing to do.")
        return

    batches = [
        new_files[i : i + batch_size]
        for i in range(0, len(new_files), batch_size)
    ]
    total_batches = len(batches)
    print(f"Uploading {len(new_files)} new files "
          f"in {total_batches} batches of {batch_size} "
          f"(delay={delay}s)...")

    for batch_num, batch in enumerate(batches, 1):
        print(f"  Batch {batch_num}/{total_batches} "
              f"({len(batch)} files)...", end=" ", flush=True)
        try:
            subprocess.run(
                ["gh", "release", "upload", RELEASE_TAG,
                 "--clobber"] + batch,
                check=True,
                capture_output=True,
            )
            print("OK")
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode() if e.stderr else ""
            if "secondary rate limit" in stderr.lower() or "403" in stderr:
                print(f"RATE LIMITED. Waiting {delay * 2}s...")
                time.sleep(delay * 2)
                print("  Retrying batch...", end=" ", flush=True)
                subprocess.run(
                    ["gh", "release", "upload", RELEASE_TAG,
                     "--clobber"] + batch,
                    check=True,
                )
                print("OK")
            else:
                raise

        if batch_num < total_batches:
            time.sleep(delay)

    print(f"Done! {len(new_files)} files uploaded "
          f"(skipped {skipped} existing).")


if __name__ == "__main__":
    main()
