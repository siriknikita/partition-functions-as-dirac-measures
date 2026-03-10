#!/usr/bin/env bash
# Run computation (Rust) then visualization (Python) for partition number n.
# Usage: ./run.sh [n]
# Example: ./run.sh 12

set -e
n="${1:-12}"
cd "$(dirname "$0")"
cargo run -- "$n"
uv run python scripts/run_visualization.py --n "$n"
