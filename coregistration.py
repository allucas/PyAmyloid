import os
import glob
import subprocess
import argparse
import sys


parser = argparse.ArgumentParser(description="Register a PET image to MNI template using greedy.")
parser.add_argument("pet_path", help="Path to PET image file (nii or nii.gz)")
args = parser.parse_args()

pet_path = args.pet_path
if not os.path.exists(pet_path):
    print(f"[ERROR] PET file not found: {pet_path}")
    sys.exit(1)

# Define paths
pet_template = "./MNI/average_pet_template.nii.gz"
output_root = "./temp_greedy_registration_outputs"

greedy_path = "/mnt/sauce/littlab/tools/bin/greedy"  # Adjust this path if necessary

# Extract subject ID from filename
subject_id = os.path.basename(pet_path).split(".")[0]

# Define paths
subject_out_dir = output_root
os.makedirs(subject_out_dir, exist_ok=True)

mat_file = os.path.join(subject_out_dir, f"{subject_id}_to_template.mat")
warped_file = os.path.join(subject_out_dir, f"{subject_id}_MNI_greedy.nii.gz")

# Construct greedy registration command
register_cmd = [
    greedy_path,
    "-d", "3",
    "-a",
    "-i", pet_template, pet_path,
    "-ia-image-centers",
    "-dof", "12",
    "-n", "100x100x0x0",
    "-m", "NMI",
    "-o", mat_file
]

# Construct greedy apply transform command
apply_cmd = [
    greedy_path,
    "-d", "3",
    "-rf", pet_template,
    "-rm", pet_path, warped_file,
    "-r", mat_file
]

print(f"[INFO] Registering {subject_id} with greedy...")
try:
    subprocess.run(register_cmd, check=True)
    subprocess.run(apply_cmd, check=True)
    print(f"[DONE] Greedy registration complete for {subject_id}")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Greedy failed for {subject_id}: {e}")
