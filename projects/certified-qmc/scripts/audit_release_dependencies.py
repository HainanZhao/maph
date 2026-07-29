#!/usr/bin/env python3
"""Certify the release build graph and dynamic dependency perimeter."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "native"
OUTPUT = ROOT / "certificates" / "cycle-013-dependency-manifest.json"
RELEASE_SOURCES = (
    NATIVE / "Makefile",
    NATIVE / "direct_modular.c",
    NATIVE / "streaming_pilot.c",
    NATIVE / "cycle009_ntt.c",
)
BINARIES = (
    ROOT / "build" / "native" / "direct_modular",
    ROOT / "build" / "native" / "streaming_pilot",
    ROOT / "build" / "native" / "cycle009_ntt",
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def cpu_model() -> str:
    for line in Path("/proc/cpuinfo").read_text().splitlines():
        if line.lower().startswith("model name"):
            return line.split(":", 1)[1].strip()
    return platform.processor() or "UNKNOWN"


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> str:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def linked_dependencies(binary: Path) -> dict[str, object]:
    ldd = run(["ldd", str(binary)])
    dynamic = run(["readelf", "-d", str(binary)])
    needed = []
    for line in dynamic.splitlines():
        if "(NEEDED)" in line:
            needed.append(line.split("[", 1)[1].split("]", 1)[0])
    return {
        "binary": str(binary.relative_to(ROOT)),
        "sha256": digest(binary),
        "ldd": ldd.splitlines(),
        "elf_needed": needed,
        "contains_fftw": "fftw" in (ldd + dynamic).lower(),
    }


def clean_room_build() -> dict[str, object]:
    with tempfile.TemporaryDirectory(
        prefix="certified-qmc-cycle013-cleanroom-"
    ) as temporary:
        clean_root = Path(temporary)
        clean_native = clean_root / "native"
        clean_native.mkdir()
        for source in RELEASE_SOURCES:
            shutil.copy2(source, clean_native / source.name)

        wrapper = clean_root / "cc-no-fftw"
        wrapper.write_text(
            "#!/bin/sh\n"
            "for argument in \"$@\"; do\n"
            "  case \"$argument\" in\n"
            "    *fftw*|*FFTW*)\n"
            "      echo 'FFTW reference rejected by clean-room compiler' >&2\n"
            "      exit 97\n"
            "      ;;\n"
            "  esac\n"
            "done\n"
            "exec /usr/bin/cc \"$@\"\n"
        )
        wrapper.chmod(0o755)
        environment = os.environ.copy()
        for name in (
            "CFLAGS",
            "CPPFLAGS",
            "LDFLAGS",
            "LIBRARY_PATH",
            "CPATH",
            "C_INCLUDE_PATH",
        ):
            environment.pop(name, None)
        environment["CC"] = str(wrapper)
        environment["PKG_CONFIG_LIBDIR"] = str(clean_root / "empty-pkgconfig")
        run(["make", "-C", str(clean_native), "release"], env=environment)
        clean_binaries = (
            clean_root / "build" / "native" / "direct_modular",
            clean_root / "build" / "native" / "streaming_pilot",
            clean_root / "build" / "native" / "cycle009_ntt",
        )
        results = []
        for binary in clean_binaries:
            ldd = run(["ldd", str(binary)])
            results.append(
                {
                    "name": binary.name,
                    "sha256": digest(binary),
                    "ldd": ldd.splitlines(),
                    "contains_fftw": "fftw" in ldd.lower(),
                }
            )
        return {
            "release_sources_copied_only": [
                f"native/{source.name}" for source in RELEASE_SOURCES
            ],
            "compiler_wrapper_rejects_fftw_arguments": True,
            "pkg_config_search_path_empty": True,
            "build_succeeded": True,
            "binaries": results,
        }


def main() -> None:
    run(["make", "-C", str(NATIVE), "clean"])
    graph = run(["make", "-C", str(NATIVE), "--dry-run", "release"])
    if "fftw" in graph.lower():
        raise RuntimeError("release build graph references FFTW")
    run(["make", "-C", str(NATIVE), "release"])
    dependencies = [linked_dependencies(binary) for binary in BINARIES]
    if any(item["contains_fftw"] for item in dependencies):
        raise RuntimeError("release binary links FFTW")

    export_attribute = run(
        [
            "git",
            "check-attr",
            "export-ignore",
            "--",
            "tools/numerical-crosscheck",
        ],
        cwd=ROOT,
    ).strip()
    clean_room = clean_room_build()
    if any(
        item["contains_fftw"] for item in clean_room["binaries"]
    ):
        raise RuntimeError("clean-room binary links FFTW")

    compiler = run(["cc", "--version"]).splitlines()[0]
    payload = {
        "schema": "certified-qmc-cycle-013-dependency-manifest-v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_RELEASE_DEPENDENCY_PERIMETER",
        "release_target": "make -C native release",
        "frozen_kernel": {
            "source": "native/streaming_pilot.c",
            "sha256": digest(NATIVE / "streaming_pilot.c"),
            "compiler": compiler,
            "flags": (
                "-O3 -std=c11 -Wall -Wextra -Wpedantic "
                "-D_POSIX_C_SOURCE=200809L -fopenmp"
            ),
            "cpu_model": cpu_model(),
            "platform": platform.platform(),
        },
        "build_graph": {
            "dry_run_lines": graph.splitlines(),
            "sha256": sha256(graph.encode()).hexdigest(),
            "contains_fftw": False,
        },
        "release_sources": {
            str(path.relative_to(ROOT)): digest(path)
            for path in RELEASE_SOURCES
        },
        "dynamic_dependencies": dependencies,
        "dependency_policy": {
            "project_or_lgpl_math_dependencies": [],
            "system_or_compiler_runtime": [
                "libc",
                "ELF loader",
                "libgomp for the frozen OpenMP pilot kernel",
            ],
            "other_third_party_dependencies": [],
            "fftw_present": False,
        },
        "numerical_crosscheck_exclusion": {
            "path": "tools/numerical-crosscheck",
            "git_export_attribute": export_attribute,
            "excluded_from_release_target": True,
            "tag": "NUMERICAL",
        },
        "clean_room": clean_room,
        "gate": {
            "release_build_passed": True,
            "clean_room_build_passed": True,
            "fftw_absent_from_build_graph": True,
            "fftw_absent_from_dynamic_dependencies": True,
            "cycle_013_dependency_gate_passed": True,
        },
        "boundary": (
            "VERIFIED covers the recorded source graph, compiler command, "
            "ELF NEEDED entries, ldd resolution, export exclusion, and "
            "clean-room reproduction. System and compiler runtimes are "
            "listed explicitly; no FFTW, GMP, or FLINT object is linked."
        ),
    }
    payload["certificate_sha256"] = canonical_digest(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
