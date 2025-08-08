# ------------------------------------------
# SYSTEM SETUP
# ------------------------------------------
sudo apt update && sudo apt install -y \
  git cmake build-essential ninja-build \
  libboost-all-dev libeigen3-dev libflann-dev libglew-dev \
  qtbase5-dev libqt5opengl5-dev libcgal-dev libfreeimage-dev \
  libgoogle-glog-dev libgflags-dev libsqlite3-dev \
  python3 python3-pip python3-dev python3-venv

# ------------------------------------------
# INSTALL COLMAP FROM SOURCE
# ------------------------------------------
cd ~
git clone https://github.com/colmap/colmap.git
cd colmap
mkdir build && cd build
cmake .. -GNinja
ninja
sudo ninja install
colmap help

# ------------------------------------------
# INSTALL HLOC
# ------------------------------------------
cd ~
git clone https://github.com/cvg/Hierarchical-Localization.git
cd Hierarchical-Localization
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install lightglue kornia pycolmap

# ------------------------------------------
# SETUP WORKSPACE & COPY DATA
# ------------------------------------------
cd ~
mkdir -p hloc_project/dataset/images      # ← your reference images go here
mkdir -p hloc_project/dataset/queries     # ← your query images go here
mkdir -p hloc_project/dataset/hloc

cd ~/Hierarchical-Localization
source venv/bin/activate

# ------------------------------------------
# HLOC PIPELINE: FEATURE EXTRACTION (REFERENCE)
# ------------------------------------------
python -m hloc.extract_features \
  --image_dir ~/hloc_project/dataset/images \
  --features_path ~/hloc_project/dataset/hloc/features.h5 \
  --method superpoint_aachen

# ------------------------------------------
# IMAGE PAIRING (EXHAUSTIVE)
# ------------------------------------------
python -m hloc.pairs_from_exhaustive \
  ~/hloc_project/dataset/images \
  ~/hloc_project/dataset/hloc/pairs.txt

# ------------------------------------------
# MATCHING FEATURES
# ------------------------------------------
python -m hloc.match_features \
  --pairs_path ~/hloc_project/dataset/hloc/pairs.txt \
  --features_path ~/hloc_project/dataset/hloc/features.h5 \
  --matches_path ~/hloc_project/dataset/hloc/matches.h5 \
  --method superglue

# ------------------------------------------
# TRIANGULATE (SPARSE SfM MODEL)
# ------------------------------------------
python -m hloc.triangulation \
  --image_dir ~/hloc_project/dataset/images \
  --sfm_dir ~/hloc_project/dataset/hloc/sfm \
  --pairs ~/hloc_project/dataset/hloc/pairs.txt \
  --features ~/hloc_project/dataset/hloc/features.h5 \
  --matches ~/hloc_project/dataset/hloc/matches.h5

# ------------------------------------------
# LOCALIZATION PAIRS (QUERY → DB IMAGES)
# ------------------------------------------
python -m hloc.pairs_from_retrieval \
  --query_dir ~/hloc_project/dataset/queries \
  --db_dir ~/hloc_project/dataset/images \
  --output_path ~/hloc_project/dataset/hloc/query_pairs.txt \
  --method netvlad

# ------------------------------------------
# FEATURE EXTRACTION (QUERY IMAGES)
# ------------------------------------------
python -m hloc.extract_features \
  --image_dir ~/hloc_project/dataset/queries \
  --features_path ~/hloc_project/dataset/hloc/query_features.h5 \
  --method superpoint_aachen

# ------------------------------------------
# MATCH QUERY → DB
# ------------------------------------------
python -m hloc.match_features \
  --pairs_path ~/hloc_project/dataset/hloc/query_pairs.txt \
  --features_path ~/hloc_project/dataset/hloc/query_features.h5 \
  --matches_path ~/hloc_project/dataset/hloc/query_matches.h5 \
  --method superglue

# ------------------------------------------
# LOCALIZE (GET 6DOF POSES)
# ------------------------------------------
python -m hloc.localize_sfm \
  --sfm_dir ~/hloc_project/dataset/hloc/sfm \
  --pairs_path ~/hloc_project/dataset/hloc/query_pairs.txt \
  --features_path ~/hloc_project/dataset/hloc/query_features.h5 \
  --matches_path ~/hloc_project/dataset/hloc/query_matches.h5 \
  --output_path ~/hloc_project/dataset/hloc/poses.txt

# ------------------------------------------
# DENSE RECONSTRUCTION → POINT CLOUD & MESH
# ------------------------------------------

# UNDISTORT IMAGES
colmap image_undistorter \
  --image_path ~/hloc_project/dataset/images \
  --input_path ~/hloc_project/dataset/hloc/sfm \
  --output_path ~/hloc_project/dataset/dense \
  --output_type COLMAP

# PATCH-MATCH STEREO (depth maps)
colmap patch_match_stereo \
  --workspace_path ~/hloc_project/dataset/dense \
  --workspace_format COLMAP \
  --PatchMatchStereo.geom_consistency true

# FUSE DEPTH MAPS (generate dense point cloud)
colmap stereo_fusion \
  --workspace_path ~/hloc_project/dataset/dense \
  --workspace_format COLMAP \
  --input_type geometric \
  --output_path ~/hloc_project/dataset/dense/fused.ply

# ------------------------------------------
# ✅ DONE
# ------------------------------------------

echo "✅ Pipeline complete!"
echo "📌 6DoF poses → ~/hloc_project/dataset/hloc/poses.txt"
echo "📌 Dense point cloud → ~/hloc_project/dataset/dense/fused.ply"
