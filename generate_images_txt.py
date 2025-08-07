# generate_images_txt.py

from pathlib import Path

query_image_dir = Path("/Users/akhilb/Downloads/rgbd_dataset_freiburg3_long_office_household/query/images")
output_file = Path("/Users/akhilb/Downloads/rgbd_dataset_freiburg3_long_office_household/query/images.txt")

camera_model = "PINHOLE"
width, height = 640, 480
fx = fy = 525.0
cx, cy = 319.5, 239.5

with open(output_file, 'w') as f:
    for img_path in sorted(query_image_dir.glob("*.png")):
        f.write(f"{camera_model} {width} {height} {fx} {fy} {cx} {cy} {img_path.name}\n")

print(f"✅ Written to: {output_file}")
