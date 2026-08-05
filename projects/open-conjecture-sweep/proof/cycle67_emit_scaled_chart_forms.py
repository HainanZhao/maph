#!/usr/bin/env python3
"""Emit six-times-scaled integer function-value forms for C67 charts."""

import argparse
import csv
from pathlib import Path

from cycle67_equality_blowup import charts, scale
from cycle67_equality_blowup_orbit import actual_values


def main():
    p=argparse.ArgumentParser();p.add_argument("output",type=Path);a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("w",newline="",encoding="utf-8") as handle:
        w=csv.writer(handle,delimiter="\t",lineterminator="\n");w.writerow(("chart","value","x","y","r","h","coefficient"))
        for name,(family,zforms) in charts().items():
            for value,form in enumerate(actual_values(family,zforms)):
                for exponent,coefficient in sorted(scale(form,6).items()):
                    assert coefficient.denominator==1
                    w.writerow((name,value,*exponent,coefficient.numerator))
    return 0


if __name__=="__main__":raise SystemExit(main())
