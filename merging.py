import h5py
from pathlib import Path

db_feat_path = '/Users/akhilb/Downloads/rgbd_dataset_freiburg3_long_office_household/feats-aliked-lightglue.h5'
query_feat_path = '/Users/akhilb/Downloads/rgbd_dataset_freiburg3_long_office_household/query/feats-aliked-lightglue.h5'

with h5py.File(db_feat_path, 'a') as f_db, h5py.File(query_feat_path, 'r') as f_query:
    for image_name in f_query:
        if image_name in f_db:
            print(f"Skipping existing image: {image_name}")
            continue
        f_query.copy(image_name, f_db)
print("✅ Query features merged into database feature file.")
