from pathlib import Path
from hloc.match_features import match_from_paths, confs

def main():
    # Define the dataset/query directory
    query_dir = Path("/Users/akhilb/Downloads/rgbd_dataset_freiburg3_long_office_household/query")

    # Define paths
    pairs_path = query_dir / "pairs-query_strict.txt"
    features_path = query_dir / "feats-aliked-lightglue.h5"
    matches_path = query_dir / "matches-aliked-lightglue.h5"

    # Run matching using ALIKED + LightGlue
    match_from_paths(
        confs['aliked+lightglue'],
        pairs_path,
        matches_path,
        features_path,
        features_path,  # both query and reference features
        overwrite=True
    )

if __name__ == "__main__":
    main()
