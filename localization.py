import argparse
from pathlib import Path

from hloc.localize_sfm import main as localize


def run_localization() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref-sfm", type=Path, required=True)
    parser.add_argument("--query-list", type=Path, required=True)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--matches", type=Path, required=True)
    parser.add_argument("--pairs", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()

    localize(
        reference_sfm=args.ref_sfm,
        queries=[args.query_list],
        features=args.features,
        matches=args.matches,
        retrieval=args.pairs,
        results=args.results,
    )

if __name__ == "__main__":
    run_localization()
