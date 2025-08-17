# Causal Reducer

A command-line tool for **causal analysis** of a labeled transition system (LTS), which describes the state space of a Rebeca actor model. This tool takes a state space description as input and optionally enables a shortened display mode for simplified state space.

Learn more about Rebeca: [https://rebeca-lang.org/](https://rebeca-lang.org/)

## Features

- Reads a statespace description from a file in `.statespace` format.
- Optional "shortened mode" to simplify the state space for readability.
- CLI-based — easy to integrate into scripts or analysis pipelines.

## Usage

```bash
python main.py [-h] [--short] -i INPUT_FILE
```

## Options

- -i INPUT_FILE, --input INPUT_FILE — Path to the input .statespace file (required).

- --short — Enable shortened mode (optional).

- --visualise — Visualises the reduced state space using graphviz (optional).

- --time — Logs the time spent on different stages of execution (optional).

- -h, --help — Show help message and exit.

## Example

```bash
python3 main.py -i examples/Batteries.statespace
```

```bash
python3 main.py -i examples/GlassBottle.statespace --short --visualise --time
```

## Usage with Rebeca models

In order to analyze a model, described in [Afra](https://rebeca-lang.org/alltools/Afra), follow the steps:

- Create a new Afra project and select `Export state space` from the configuration menu.

- Define the model.

- Specify hazardous properties in `.property` file in section property->define. Use `haz` prefix. For example:

```bash
property {
	define{
		isOn1 = battery1.isOn;
		isOn2 = battery2.isOn;
		isOn3 = battery3.isOn;

		hazAllBatteriesOff = !battery1.isOn && !battery2.isOn && !battery3.isOn;
	}
}
```

Any properties with `haz` prefix will be treated as hazardous during causal analysis.

- Run the model checker.

- Use the generated `.statespace` file as input for the Causal Reducer.

## Requirements

- Python 3.6+

- Graphviz library.

```bash
pip install graphviz
```
