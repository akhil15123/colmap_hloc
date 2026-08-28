"""Match HLoc features using paths supplied on the command line."""

import argparse
from pathlib import Path

from hloc.match_features import confs, match_from_paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairs", type=Path, required=True)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--matches", type=Path, required=True)
    parser.add_argument("--method", choices=sorted(confs), default="aliked+lightglue")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    match_from_paths(
        confs[args.method],
        args.pairs,
        args.matches,
        args.features,
        args.features,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
