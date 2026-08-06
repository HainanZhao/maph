# Erdős–Szekeres SAT Generator

This repository contains a Python script that generates DIMACS CNF instances for experiments related to the planar Erdős–Szekeres problem using a SAT encoding. The output CNF can be solved with **Kissat** or any other SAT solver

## 1) Install Kissat

Clone and build Kissat:

```bash
git clone https://github.com/arminbiere/kissat
cd kissat
./configure
make
````

## 2) Install PySAT

Install the Python SAT toolkit used by the generator:

```bash
pip install python-sat
```

## 3) Generate CNF with the script

Run the generator and write a `.cnf` file:

```bash
python es_sat_gen.py --n 33 --k 7 --layers "5,5,5,5,5,5" --offsets "0,4,4,4,4,4" --out instance.cnf
```

### More examples

Generate another configuration:

```bash
python es_sat_gen.py --n 33 --k 7 --layers "4,4,4,4,4,4,4,4" --offsets "0,3,3,3,3,3,3,3" --out hull_4x8.cnf
```

Generate a CNF without hull constraints:

```bash
python es_sat_gen.py --n 17 --k 6 --no-hull --out base_17_6.cnf
```

Print clause/variable counts only (no file written):

```bash
python es_sat_gen.py --n 33 --k 7 --layers "5,5,5,5,5,5" --offsets "0,4,4,4,4,4" --count-only
```

## Solving with Kissat

Solve a generated CNF:

```bash
/path/to/kissat instance.cnf
```

Kissat will report `s UNSATISFIABLE` or `s SATISFIABLE` at the end of the run.
