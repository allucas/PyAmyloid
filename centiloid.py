import os
import numpy as np
import nibabel as nib
import pandas as pd
import argparse
import sys

parser = argparse.ArgumentParser(description="Register a PET image to MNI template using greedy.")
parser.add_argument("pet_path", help="Path to PET image file (nii or nii.gz)")
parser.add_argument(
    "--results",
    default="./centiloid_results.csv",
    help="Path to output CSV file for centiloid results (default: ./centiloid_results.csv)"
)
args = parser.parse_args()

pet_path = args.pet_path
if not os.path.exists(pet_path):
    print(f"[ERROR] PET file not found: {pet_path}")
    sys.exit(1)

# Output path for results
results_file = args.results

# Extract subject ID from filename
subject_id = os.path.basename(pet_path).split(".")[0]


# Define paths
output_root = "./temp_greedy_registration_outputs"
target_regions_path = "./MNI/target_regions"
reference_regions_path = "./MNI/reference_region"

# Subjects
subjects = [subject_id]

# ROIs
target_regions_names = [f for f in os.listdir(target_regions_path) if f.endswith('MNI.nii.gz')]

for subject in subjects:
    pet_file = os.path.join(output_root, f"{subject}_MNI_greedy.nii.gz")
    if not os.path.exists(pet_file):
        print(f"PET file not found for subject {subject}: {pet_file}")
        continue

    # Load PET image
    pet_data = nib.load(pet_file).get_fdata()

    # Load reference region
    ref_file = os.path.join('./MNI/reference_region/cere_all_MNI.nii.gz')
    if not os.path.exists(ref_file):
        print(f"Reference file not found for subject {subject}: {ref_file}")
        continue

    ref_data = nib.load(ref_file).get_fdata()
    mean_ref = pet_data[ref_data > 0].mean()

    # Average across all target regions
    target_means = []
    for target_name in target_regions_names:
        target_file = os.path.join(target_regions_path, target_name)
        target_data = nib.load(target_file).get_fdata()
        mean_val = pet_data[target_data > 0].mean()
        target_means.append(mean_val)

    # Compute SUVR and centiloid
    mean_target = np.mean(target_means)
    suvr = mean_target / mean_ref if mean_ref != 0 else np.nan
    centiloid = 175 * suvr - 182 if mean_ref != 0 else np.nan
    print(f'Subject: {subject}, SUVR: {suvr}, Centiloid: {centiloid}')

    # Append results to CSV
    df = pd.DataFrame([[subject, suvr, centiloid]], columns=["Subject", "SUVR", "Centiloid"])
    if os.path.exists(results_file):
        df_existing = pd.read_csv(results_file)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(results_file, index=False)
    print(f"[DONE] Centiloid calculation complete for {subject}, results saved to {results_file}")
 

