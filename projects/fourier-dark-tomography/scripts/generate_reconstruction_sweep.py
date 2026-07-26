#!/usr/bin/env python3
"""Generate the vector validation figure using only the standard library."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from simulate_f4_reconstruction import linearity_radius_scan, monte_carlo


def pdf_text(x: float, y: float, value: str, size: float = 8) -> str:
    escaped = value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return f"BT /F1 {size:g} Tf {x:.2f} {y:.2f} Td ({escaped}) Tj ET"


def pdf_vertical_text(
    x: float, y: float, value: str, size: float = 8
) -> str:
    escaped = value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return (
        f"BT /F1 {size:g} Tf 0 1 -1 0 {x:.2f} {y:.2f} Tm "
        f"({escaped}) Tj ET"
    )


def circle(x: float, y: float, radius: float = 2.2) -> str:
    kappa = 0.5522847498 * radius
    return (
        f"{x + radius:.2f} {y:.2f} m "
        f"{x + radius:.2f} {y + kappa:.2f} "
        f"{x + kappa:.2f} {y + radius:.2f} "
        f"{x:.2f} {y + radius:.2f} c "
        f"{x - kappa:.2f} {y + radius:.2f} "
        f"{x - radius:.2f} {y + kappa:.2f} "
        f"{x - radius:.2f} {y:.2f} c "
        f"{x - radius:.2f} {y - kappa:.2f} "
        f"{x - kappa:.2f} {y - radius:.2f} "
        f"{x:.2f} {y - radius:.2f} c "
        f"{x + kappa:.2f} {y - radius:.2f} "
        f"{x + radius:.2f} {y - kappa:.2f} "
        f"{x + radius:.2f} {y:.2f} c f"
    )


def polyline(points: list[tuple[float, float]]) -> str:
    first, *rest = points
    return " ".join(
        [f"{first[0]:.2f} {first[1]:.2f} m"]
        + [f"{x:.2f} {y:.2f} l" for x, y in rest]
        + ["S"]
    )


def polygon(points: list[tuple[float, float]]) -> str:
    first, *rest = points
    return " ".join(
        [f"{first[0]:.2f} {first[1]:.2f} m"]
        + [f"{x:.2f} {y:.2f} l" for x, y in rest]
        + ["h f"]
    )


def map_log(
    value: float, low: float, high: float, start: float, extent: float
) -> float:
    return start + extent * (
        (math.log10(value) - math.log10(low))
        / (math.log10(high) - math.log10(low))
    )


def make_content(
    trial_rows: list[tuple[int, float, float]],
    bias_rows: list[tuple[float, float, float]],
) -> str:
    commands = ["1 J 1 j", "0 0 0 RG", "0 0 0 rg"]
    panels = (
        (42.0, 39.0, 180.0, 126.0),
        (278.0, 39.0, 180.0, 126.0),
    )
    for x, y, width, height in panels:
        commands.append(
            f"0.7 w {x:.2f} {y:.2f} m {x:.2f} {y+height:.2f} l "
            f"{x+width:.2f} {y:.2f} m {x:.2f} {y:.2f} l S"
        )

    lx, ly, lw, lh = panels[0]
    left_x = lambda value: map_log(value, 2.5e5, 4e6, lx, lw)
    left_y = lambda value: map_log(value, 1.7e-3, 9e-3, ly, lh)
    predicted = [(left_x(n), left_y(pred)) for n, pred, _ in trial_rows]
    empirical = [(left_x(n), left_y(emp)) for n, _, emp in trial_rows]
    commands += [
        "0.15 0.35 0.75 RG 1.2 w",
        polyline(predicted),
        "0.80 0.20 0.12 rg",
        *[circle(x, y) for x, y in empirical],
        "0 0 0 RG 0 0 0 rg",
        pdf_text(95, 181, "finite-shot scaling", 9),
        pdf_text(105, 18, "total trials N", 8),
        pdf_vertical_text(12, 84, "vector RMSE", 8),
    ]
    for value, label in (
        (2.5e5, "2.5e5"),
        (1e6, "1e6"),
        (4e6, "4e6"),
    ):
        x = left_x(value)
        commands += [
            f"0.4 w {x:.2f} {ly:.2f} m {x:.2f} {ly-3:.2f} l S",
            pdf_text(x - 10, ly - 13, label, 6.5),
        ]
    for value, label in ((0.002, ".002"), (0.004, ".004"), (0.008, ".008")):
        y = left_y(value)
        commands += [
            f"0.4 w {lx:.2f} {y:.2f} m {lx-3:.2f} {y:.2f} l S",
            pdf_text(lx - 28, y - 2, label, 6.5),
        ]
    commands += [
        "0.15 0.35 0.75 RG 1.2 w",
        f"145 176 m 161 176 l S",
        "0 0 0 RG",
        pdf_text(165, 173, "covariance", 6.5),
        "0.80 0.20 0.12 rg",
        circle(149, 166, 2.0),
        "0 0 0 rg",
        pdf_text(165, 163, "Monte Carlo", 6.5),
    ]

    rx, ry, rw, rh = panels[1]
    right_x = lambda value: map_log(value, 1e-4, 3e-2, rx, rw)
    right_y = lambda value: map_log(value, 1e-4, 4e-1, ry, rh)
    median = [(right_x(radius), right_y(med)) for radius, med, _ in bias_rows]
    maximum = [(right_x(radius), right_y(high)) for radius, _, high in bias_rows]
    band = maximum + list(reversed(median))
    commands += [
        "0.83 0.88 0.97 rg",
        polygon(band),
        "0.15 0.35 0.75 RG 1.2 w",
        polyline(median),
        polyline(maximum),
        "0 0 0 RG 0 0 0 rg",
        pdf_text(327, 181, "local-inversion bias", 9),
        pdf_text(331, 18, "error-vector norm", 8),
        pdf_vertical_text(248, 84, "relative bias", 8),
    ]
    for value, label in ((1e-4, "1e-4"), (1e-3, "1e-3"), (1e-2, "1e-2")):
        x = right_x(value)
        commands += [
            f"0.4 w {x:.2f} {ry:.2f} m {x:.2f} {ry-3:.2f} l S",
            pdf_text(x - 9, ry - 13, label, 6.5),
        ]
    for value, label in ((1e-3, "1e-3"), (1e-2, "1e-2"), (1e-1, "1e-1")):
        y = right_y(value)
        commands += [
            f"0.4 w {rx:.2f} {y:.2f} m {rx-3:.2f} {y:.2f} l S",
            pdf_text(rx - 28, y - 2, label, 6.5),
        ]
    commands += [
        "0.83 0.88 0.97 rg",
        "385 171 13 7 re f",
        "0 0 0 rg",
        pdf_text(402, 171, "median--maximum", 6.5),
    ]
    return "\n".join(commands) + "\n"


def write_pdf(path: Path, content: str) -> None:
    stream = content.encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 500 200] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
        + stream
        + b"endstream",
    ]
    # The second-line marker tells transfer and version-control tools that
    # this is a binary PDF even though the vector drawing stream is ASCII.
    document = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(document))
        document.extend(f"{index} 0 obj\n".encode("ascii"))
        document.extend(obj)
        document.extend(b"\nendobj\n")
    xref = len(document)
    document.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
    document.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        document.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    document.extend(
        (
            f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n"
        ).encode("ascii")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(document)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repetitions", type=int, default=1500)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("paper/figures/reconstruction_sweep.pdf"),
    )
    args = parser.parse_args()
    trial_rows = []
    for index, trials in enumerate((250_000, 500_000, 1_000_000, 2_000_000, 4_000_000)):
        result = monte_carlo(
            epsilon=0.05,
            total_trials=trials,
            background=1e-5,
            error_norm=0.002,
            repetitions=args.repetitions,
            seed=810 + index,
        )
        trial_rows.append(
            (trials, result["predicted_rmse"], result["empirical_rmse"])
        )
    bias_rows = linearity_radius_scan(
        0.05,
        radii=(1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2),
        directions=128,
        seed=701,
    )
    write_pdf(args.output, make_content(trial_rows, bias_rows))
    print("N predicted_RMSE empirical_RMSE")
    for row in trial_rows:
        print(f"{row[0]} {row[1]:.8g} {row[2]:.8g}")
    print("radius median_relative_bias maximum_relative_bias")
    for row in bias_rows:
        print(f"{row[0]:.8g} {row[1]:.8g} {row[2]:.8g}")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
