#!/usr/bin/env python3
"""Move legacy root conjecture trees into projects/open-conjecture-sweep.

The command is a dry run unless ``--execute`` is supplied.  By default it
refuses to move anything while the bounded covering experiment is live.  The
explicit relay mode pauses that run, performs same-filesystem renames, leaves
a temporary compatibility symlink, and resumes it.  Every destination is
checked before the first mutation, tracked files use ``git mv``, and
untracked/ignored research outputs are preserved.
"""

from __future__ import annotations

import argparse
import os
import signal
import shutil
import subprocess
import time
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
PROJECT = REPOSITORY / "projects" / "open-conjecture-sweep"
SOURCE_TREES = ("discovery", "experiments", "paper", "proof")
ACTIVE_MARKERS = (
    b"cover_23_6_2_bounded_experiment.py",
    b"cover-23-6-2-wave4-20260807",
)


def tracked_paths() -> set[Path]:
    command = ["git", "ls-files", "-z", "--", *SOURCE_TREES]
    result = subprocess.run(
        command,
        cwd=REPOSITORY,
        check=True,
        stdout=subprocess.PIPE,
    )
    return {
        REPOSITORY / item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    }


def source_files() -> list[Path]:
    files: list[Path] = []
    for tree_name in SOURCE_TREES:
        tree = REPOSITORY / tree_name
        if not tree.is_dir():
            raise SystemExit(f"missing source tree: {tree}")
        for path in tree.rglob("*"):
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            if path.is_file() or path.is_symlink():
                files.append(path)
    return sorted(files)


def active_covering_processes() -> list[tuple[int, str]]:
    active: list[tuple[int, str]] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit() or int(entry.name) == os.getpid():
            continue
        try:
            command = (entry / "cmdline").read_bytes()
        except (FileNotFoundError, PermissionError):
            continue
        if any(marker in command for marker in ACTIVE_MARKERS):
            rendered = command.replace(b"\0", b" ").decode(errors="replace")
            active.append((int(entry.name), rendered))
    return sorted(active)


def pause_processes(processes: list[tuple[int, str]]) -> list[int]:
    paused: list[int] = []
    for pid, _ in processes:
        try:
            os.kill(pid, signal.SIGSTOP)
        except ProcessLookupError:
            continue
        paused.append(pid)

    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline:
        states: dict[int, str] = {}
        for pid in paused:
            try:
                status = Path(f"/proc/{pid}/status").read_text(encoding="utf-8")
            except FileNotFoundError:
                continue
            state_line = next(line for line in status.splitlines() if line.startswith("State:"))
            states[pid] = state_line.split()[1]
        if all(state in {"T", "t"} for state in states.values()):
            return paused
        time.sleep(0.05)
    raise SystemExit(f"could not pause every live covering process: {states}")


def resume_processes(pids: list[int]) -> None:
    for pid in reversed(pids):
        try:
            os.kill(pid, signal.SIGCONT)
        except ProcessLookupError:
            pass


def destination(path: Path) -> Path:
    return PROJECT / path.relative_to(REPOSITORY)


def remove_empty_sources() -> None:
    for tree_name in SOURCE_TREES:
        tree = REPOSITORY / tree_name
        for cache in sorted(tree.rglob("__pycache__"), reverse=True):
            shutil.rmtree(cache)
        for directory in sorted(
            (path for path in tree.rglob("*") if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            directory.rmdir()
        tree.rmdir()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="perform the checked migration (default: report only)",
    )
    parser.add_argument(
        "--relay-active-covering",
        action="store_true",
        help=(
            "pause a live covering run during the move and leave a temporary "
            "root discovery symlink for its frozen paths"
        ),
    )
    args = parser.parse_args()

    files = source_files()
    tracked = tracked_paths()
    collisions = [(path, destination(path)) for path in files if destination(path).exists()]
    missing_tracked = sorted(tracked.difference(files))
    if collisions:
        for source, target in collisions:
            print(f"COLLISION {source.relative_to(REPOSITORY)} -> {target.relative_to(REPOSITORY)}")
        raise SystemExit("destination collisions block migration")
    if missing_tracked:
        for path in missing_tracked:
            print(f"MISSING_TRACKED {path.relative_to(REPOSITORY)}")
        raise SystemExit("tracked-file inventory is incomplete")

    total_bytes = sum(path.lstat().st_size for path in files)
    print(
        f"REHOME_PREFLIGHT_PASS files={len(files)} tracked={len(tracked)} "
        f"untracked_or_ignored={len(files) - len(tracked)} bytes={total_bytes}"
    )
    if not args.execute:
        print("DRY_RUN: pass --execute after the covering solver is terminal")
        return

    active = active_covering_processes()
    if active and not args.relay_active_covering:
        for pid, command in active:
            print(f"ACTIVE_PROCESS pid={pid} command={command}")
        raise SystemExit("live covering processes block migration")

    paused: list[int] = []
    try:
        if active:
            paused = pause_processes(active)
            print("ACTIVE_RELAY_PAUSED pids=" + ",".join(map(str, paused)))

        for path in files:
            target = destination(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            if path in tracked:
                subprocess.run(
                    ["git", "mv", "--", str(path), str(target)],
                    cwd=REPOSITORY,
                    check=True,
                )
            else:
                path.replace(target)

        remove_empty_sources()
        if active:
            (REPOSITORY / "discovery").symlink_to(
                Path("projects/open-conjecture-sweep/discovery"),
                target_is_directory=True,
            )
            print("ACTIVE_RELAY_LINK discovery -> projects/open-conjecture-sweep/discovery")
    finally:
        resume_processes(paused)

    print(
        f"REHOME_EXECUTION_PASS files={len(files)} tracked={len(tracked)} "
        f"bytes={total_bytes} destination={PROJECT.relative_to(REPOSITORY)}"
    )


if __name__ == "__main__":
    main()
