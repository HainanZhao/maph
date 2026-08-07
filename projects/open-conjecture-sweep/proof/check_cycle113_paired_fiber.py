#!/usr/bin/env python3
"""Exact signed-triangle C113 check, including endpoint-fiber terms."""
import json

Q = 7
N = 2 * Q
PAIRS = [(x, y) for x in range(Q) for y in range(x + 1, Q)]
FREE = [(x, y) for x, y in PAIRS if x != 0]


def signs(mask):
    h = [[1] * Q for _ in range(Q)]
    for x in range(Q): h[x][x] = 0
    for bit, (x, y) in enumerate(FREE):
        h[x][y] = h[y][x] = 1 if (mask >> bit) & 1 else -1
    return h


def triangle_counts(h, x, y):
    plus = sum(h[x][y] * h[x][z] * h[y][z] == 1
               for z in range(Q) if z not in (x, y))
    return plus, Q - 2 - plus


def direct_caps(h):
    # The Seidel row-sum has forced all seven internal fiber edges red.
    a = [[False] * N for _ in range(N)]
    for x in range(Q): a[2*x][2*x+1] = a[2*x+1][2*x] = True
    for x, y in PAIRS:
        for ex in (0, 1):
            for ey in (0, 1):
                red = (1 if ex == ey else -1) == h[x][y]
                a[2*x+ex][2*y+ey] = a[2*y+ey][2*x+ex] = red
    degrees = [sum(row) for row in a]
    red = blue = 0
    for u in range(N):
        for v in range(u + 1, N):
            common = sum(a[u][w] == a[u][v] and a[v][w] == a[u][v]
                         for w in range(N) if w not in (u, v))
            if a[u][v]: red = max(red, common)
            else: blue = max(blue, common)
    return degrees, red, blue


def main():
    formula_disagreements = []
    hits = []
    profiles = {}
    for mask in range(1 << len(FREE)):
        h = signs(mask)
        red = blue = 0
        for x, y in PAIRS:
            plus, minus = triangle_counts(h, x, y)
            # A red book is witnessed only on a red edge, and a blue book
            # only on a blue edge.  The endpoint terms occur in the opposite
            # colour on a cross edge, so they are recorded in the proof but
            # do not enter these two asymmetric book maxima.
            # Every fiber pair contains both a red and a blue matching edge;
            # h_xy only chooses which matching has which colour.
            red, blue = max(red, plus), max(blue, minus)
        degrees, direct_red, direct_blue = direct_caps(h)
        if degrees != [Q] * N or (red, blue) != (direct_red, direct_blue):
            formula_disagreements.append(mask)
        profiles[(red, blue)] = profiles.get((red, blue), 0) + 1
        if red <= 2 and blue <= 3:
            hits.append(mask)
    payload = {
        'status': 'PASS' if not formula_disagreements and not hits else 'FAIL',
        'normalized_sign_states': 1 << len(FREE),
        'normalized_q7_logical_states': (1 << len(FREE)) * (1 << Q),
        'degree_rejected_logical_states': (1 << len(FREE)) * ((1 << Q) - 1),
        'balanced_states_directly_checked': 1 << len(FREE),
        'formula_disagreements': formula_disagreements,
        'hits': hits,
        'profiles': [[list(k), v] for k, v in sorted(profiles.items())],
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == '__main__': main()
