# partition-functions-as-dirac-measures

Compute partition functions as Dirac measures (Rust) and visualize them (Python). Outputs are split by partition number `n` under `output/n{n}/`.

## Prerequisites

- Rust
- Python 3.12
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Usage

**One command** (compute + visualize for a given `n`):

```bash
./run.sh 12
```

Omit the argument for default `n = 12`.

**Or run steps separately:**

**Compute** (generates `output/n12/partitions_measures.json`):

```bash
cargo run -- 12
```

Omit the argument to use the default `n = 12`.

**Visualize** (reads the JSON and writes charts into the same directory):

```bash
uv run python scripts/run_visualization.py --n 12
```

Charts saved under `output/n12/`:

- `chart_individual_measure.png`
- `chart_heatmap_partitions.png`
- `chart_aggregate_measure.png`
- `chart_haar_first_difference.png`
- `chart_heatmap_log_scaled.png`

To use a custom JSON path instead of `--n`:

```bash
uv run python scripts/run_visualization.py --input path/to/partitions_measures.json
```

Add `--show` to also display plots interactively.

**Convenience:** `uv run main.py` runs visualization with default `n = 12`.

## Layout

- `input/` — optional config or sample inputs (not gitignored). Example: `input/sample_n12.json` shows the expected JSON format.
- `output/` — generated data and charts, one subfolder per partition number (e.g. `output/n12/`). Gitignored.
