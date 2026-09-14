#!/usr/bin/env python3
"""Align the SolarsplitWorkspace package pins on SolarsplitWeb/Package.resolved.

Xcode keeps one Package.resolved for the whole workspace, in
SolarsplitWorkspace.xcworkspace/xcshareddata/swiftpm/, and never re-syncs it
when the backend bumps a pin: a `main` branch or a version range stays
satisfied by the old revision, so nothing triggers a new resolution. The
backend then fails to compile inside package APIs, as on 14.09.2026 with
HelvetAI (WhatsAppTransports.swift) and HelvetBexioPackage
(BexioBillingExecutionProvider.swift), 28 pins behind that day.

This script copies the backend's state for every package identity present in
both files, leaves the packages only the iOS project uses untouched, keeps a
dated backup of the workspace file next to it, and prints what changed. It is
idempotent and silent when nothing differs, so the post-merge, post-checkout
and post-rewrite hooks of the SolarsplitWeb clone run it on every pull and
branch switch.

    python3 align-workspace-pins.py            align, print the changes
    python3 align-workspace-pins.py --check    change nothing, exit 1 on drift
    python3 align-workspace-pins.py --dry-run  print the changes, write nothing

Exit codes: 0 aligned or nothing to do, 1 drift found with --check,
2 a resolved file is missing or unreadable.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


def code_root() -> Path:
    """`~/solarsplit-dev/code`, derived from this file so a moved clone still works."""
    here = Path(__file__).resolve()
    candidate = here.parents[2] if len(here.parents) > 2 else None
    if candidate and (candidate / "SolarsplitWeb").is_dir():
        return candidate
    return Path.home() / "solarsplit-dev" / "code"


ROOT = code_root()
BACKEND_RESOLVED = ROOT / "SolarsplitWeb" / "Package.resolved"
WORKSPACE_RESOLVED = (
    ROOT / "SolarsplitWorkspace.xcworkspace" / "xcshareddata" / "swiftpm" / "Package.resolved"
)


def describe(state: dict) -> str:
    version = state.get("version") or state.get("branch") or "?"
    return f"{version} {state.get('revision', '')[:9]}"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str]) -> int:
    check = "--check" in argv
    dry_run = "--dry-run" in argv

    if not WORKSPACE_RESOLVED.is_file():
        # No workspace on this machine, nothing to align, hooks stay silent.
        if check:
            print(f"no workspace resolved file at {WORKSPACE_RESOLVED}")
            return 2
        return 0
    if not BACKEND_RESOLVED.is_file():
        print(f"no backend resolved file at {BACKEND_RESOLVED}", file=sys.stderr)
        return 2

    try:
        workspace = load(WORKSPACE_RESOLVED)
        backend = load(BACKEND_RESOLVED)
    except (OSError, ValueError) as error:
        print(f"cannot read a resolved file: {error}", file=sys.stderr)
        return 2

    backend_pins = {pin["identity"]: pin for pin in backend.get("pins", [])}
    changes: list[tuple[str, str, str]] = []
    for pin in workspace.get("pins", []):
        target = backend_pins.get(pin["identity"])
        if target is None or target["state"] == pin["state"]:
            continue
        changes.append((pin["identity"], describe(pin["state"]), describe(target["state"])))
        pin["state"] = dict(target["state"])

    if not changes:
        if check:
            print("workspace pins already aligned on the backend")
        return 0

    width = max(len(identity) for identity, _, _ in changes)
    header = "workspace pins behind the backend:" if check or dry_run else "workspace pins aligned on the backend:"
    print(f"{header} {len(changes)}")
    for identity, before, after in changes:
        print(f"  {identity.ljust(width)}  {before} -> {after}")

    if check:
        return 1
    if dry_run:
        return 0

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = WORKSPACE_RESOLVED.with_name(f"{WORKSPACE_RESOLVED.name}.bak-{stamp}")
    shutil.copy2(WORKSPACE_RESOLVED, backup)
    with WORKSPACE_RESOLVED.open("w", encoding="utf-8") as handle:
        # Same layout as Xcode writes: two-space indent, spaces around the colon.
        json.dump(workspace, handle, indent=2, separators=(",", " : "))
        handle.write("\n")
    print(f"  previous file kept as {backup.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
