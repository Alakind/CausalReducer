# Causal Reducer

A command-line tool for **causal analysis** of a labeled transition system (LTS), which describes the state space of a Rebeca actor model. This tool takes a state space description as input and optionally enables a shortened display mode for simplified state space.

Learn more about Rebeca: [https://rebeca-lang.org/](https://rebeca-lang.org/)

## Features

- Reads a statespace description from a file in `.statespace` format.
- Optional "shortened mode" to simplify the statespace for readability.
- CLI-based — easy to integrate into scripts or analysis pipelines.

## Usage

```bash
python main.py [-h] [--short SHORT] -i INPUT_FILE
```

## Options

- -i INPUT_FILE, --input INPUT_FILE — Path to the input .statespace file (required).

- --short SHORT — Enable shortened mode (e.g., true, 1, etc.) (optional).

- -h, --help — Show help message and exit.

## Example

```bash
python3 main.py -i examples/Batteries.statespace
```

```bash
python3 main.py -i examples/GlassBottle.statespace --short
```

## Requirements

- Python 3.6+

- Standard Library only (no external dependencies).
