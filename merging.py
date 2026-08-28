"""Merge query-image features into an HLoc database feature file."""

import argparse
from pathlib import Path

import h5py


def merge_features(database: Path, query: Path) -> tuple[int, int]:
    copied = skipped = 0
    with h5py.File(database, "a") as database_file, h5py.File(query, "r") as query_file:
        for image_name in query_file:
            if image_name in database_file:
                skipped += 1
                continue
            query_file.copy(image_name, database_file)
            copied += 1
    return copied, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--query", type=Path, required=True)
    args = parser.parse_args()
    copied, skipped = merge_features(args.database, args.query)
    print(f"Merged {copied} feature groups; skipped {skipped} existing groups")


if __name__ == "__main__":
    main()
