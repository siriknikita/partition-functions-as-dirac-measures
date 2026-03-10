#!/usr/bin/env python3
"""
Visualization script for partition measures.
Reads JSON produced by the Rust binary and saves charts to the same directory.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def load_data(json_path: Path) -> tuple[int, list, np.ndarray, np.ndarray]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    n = data["n"]
    records = data["partitions"]
    aggregate = np.array(data["aggregate_measure"], dtype=float)
    if "aggregate_first_difference" in data:
        aggregate_first_difference = np.array(
            data["aggregate_first_difference"], dtype=float
        )
    else:
        aggregate_first_difference = np.diff(aggregate, prepend=0)
    return n, records, aggregate, aggregate_first_difference


def run_visualization(json_path: Path, out_dir: Path, show: bool) -> None:
    n, records, aggregate, aggregate_first_difference = load_data(json_path)
    measure_matrix = np.array([r["measure"] for r in records], dtype=float)
    x = np.arange(1, n + 1)

    example_index = min(12, len(records) - 1)
    example_partition = records[example_index]["partition"]
    example_measure = np.array(records[example_index]["measure"], dtype=float)

    def save_figure(filename: str) -> None:
        out_path = out_dir / filename
        plt.savefig(out_path, dpi=180)
        if show:
            plt.show()
        plt.close()
        print(f"Saved {out_path}")

    # 1. Individual measure
    plt.figure(figsize=(10, 5))
    plt.stem(x, example_measure)
    plt.xlabel("Part size k")
    plt.ylabel("Multiplicity m_k")
    plt.title(f"Measure of one partition: {example_partition}")
    plt.tight_layout()
    save_figure("chart_individual_measure.png")

    # 2. Heatmap of all partitions
    plt.figure(figsize=(10, 8))
    plt.imshow(measure_matrix, aspect="auto", origin="lower")
    plt.colorbar(label="Multiplicity")
    plt.xlabel("Part size k")
    plt.ylabel("Partition index")
    plt.xticks(ticks=np.arange(n), labels=np.arange(1, n + 1))
    plt.title(f"Stacked partition measures for n = {n}")
    plt.tight_layout()
    save_figure("chart_heatmap_partitions.png")

    # 3. Aggregate measure
    plt.figure(figsize=(10, 5))
    plt.bar(x, aggregate)
    plt.xlabel("Part size k")
    plt.ylabel("Total multiplicity across all partitions")
    plt.title(f"Aggregate measure M_n for n = {n}")
    plt.tight_layout()
    save_figure("chart_aggregate_measure.png")

    # 4. Haar-like first difference
    plt.figure(figsize=(10, 5))
    plt.stem(x, aggregate_first_difference)
    plt.xlabel("Part size k")
    plt.ylabel("First difference")
    plt.title(f"Haar-like first-difference of aggregate measure for n = {n}")
    plt.tight_layout()
    save_figure("chart_haar_first_difference.png")

    # 5. Log-scaled heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(np.log1p(measure_matrix), aspect="auto", origin="lower")
    plt.colorbar(label="log(1 + multiplicity)")
    plt.xlabel("Part size k")
    plt.ylabel("Partition index")
    plt.xticks(ticks=np.arange(n), labels=np.arange(1, n + 1))
    plt.title(f"log-scaled stacked measures for n = {n}")
    plt.tight_layout()
    save_figure("chart_heatmap_log_scaled.png")

    # 6. 3D surface of stacked partition measures
    X = np.arange(1, n + 1)
    Y = np.arange(1, measure_matrix.shape[0] + 1)
    XX, YY = np.meshgrid(X, Y)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(
        XX, YY, np.log1p(measure_matrix),
        rstride=1, cstride=1, linewidth=0, antialiased=True,
    )
    ax.set_xlabel("Part size k")
    ax.set_ylabel("Partition index")
    ax.set_zlabel("log(1+multiplicity)")
    ax.set_title(f"3D surface of stacked partition measures for n={n}")
    fig.tight_layout()
    save_figure("chart_surface_3d.png")

    # 7. 3D ridge surface of aggregate measure
    X = np.arange(1, n + 1)
    Y_ridge = np.arange(0, 2)
    XX_ridge, YY_ridge = np.meshgrid(X, Y_ridge)
    ZZ = np.vstack([aggregate, aggregate])
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(
        XX_ridge, YY_ridge, ZZ,
        rstride=1, cstride=1, linewidth=0, antialiased=True,
    )
    ax.set_xlabel("Part size k")
    ax.set_ylabel("Thickness axis")
    ax.set_zlabel("Total multiplicity")
    ax.set_title(f"3D ridge surface of the aggregate measure for n={n}")
    fig.tight_layout()
    save_figure("chart_aggregate_ridge_3d.png")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate partition measure charts from JSON produced by the Rust binary."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--n",
        type=int,
        metavar="N",
        help="Partition number; reads output/n{N}/partitions_measures.json",
    )
    group.add_argument(
        "--input",
        type=Path,
        metavar="PATH",
        help="Path to partitions_measures.json; charts saved in the same directory",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Also display plots interactively",
    )
    args = parser.parse_args()

    if args.n is not None:
        json_path = Path(f"output/n{args.n}/partitions_measures.json")
        if not json_path.exists():
            print(f"Error: {json_path} not found. Run: cargo run -- {args.n}", file=sys.stderr)
            return 1
        out_dir = json_path.parent
    else:
        json_path = args.input
        if not json_path.is_file():
            print(f"Error: not a file: {json_path}", file=sys.stderr)
            return 1
        out_dir = json_path.parent

    run_visualization(json_path, out_dir, args.show)
    return 0


if __name__ == "__main__":
    sys.exit(main())
