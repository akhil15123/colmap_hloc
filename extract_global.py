import argparse
from pathlib import Path
from hloc import extract_features

# Use OpenIBL config
conf = extract_features.confs['openibl']

parser = argparse.ArgumentParser()
parser.add_argument('--images', required=True, help='Path to image directory')
parser.add_argument('--output', required=True, help='Path to output .h5 file')
args = parser.parse_args()

# Run extraction
extract_features.main(Path(args.images), Path(args.output), conf)
