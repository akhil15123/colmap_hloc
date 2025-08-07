from pathlib import Path
from hloc.localize_sfm import main as localize
import argparse

def run_localization():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ref_sfm', type=str, required=True)
    parser.add_argument('--query_list', type=str, required=True)
    parser.add_argument('--features', type=str, required=True)
    parser.add_argument('--matches', type=str, required=True)
    parser.add_argument('--pairs', type=str, required=True)
    parser.add_argument('--results', type=str, required=True)
    args = parser.parse_args()

    localize(
        reference_sfm=Path(args.ref_sfm),
        queries=[Path(args.query_list)],  # ← FIXED: wrap in list
        features=Path(args.features),
        matches=Path(args.matches),
        retrieval=Path(args.pairs),
        results=Path(args.results),
    )

if __name__ == "__main__":
    run_localization()
