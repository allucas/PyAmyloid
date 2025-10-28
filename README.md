# PyAmyloid
**PyAmyloid** is a lightweight Python toolkit for computing Centiloid-scale [18]F-florbetapir amyloid PET values from NIfTI images. It automates registration to MNI space and regional quantification using predefined reference and target regions obtained from the Global Alzheimer's Association Interactive Network (GAAIN) dataset (https://www.gaain.org/centiloid-project).

---

## Installation

### Clone this repository
```bash
git clone https://github.com/allucas/PyAmyloid.git
cd PyAmyloid
```

### Create a Conda environment

You’ll need Conda installed. Then run:

```bash
conda create -n pyamyloid python=3.10
conda activate pyamyloid
pip install -r requirements.txt
```

### Download the 18F-Florbetapir Template 

We have a pre-computed 18F-florbetapir template in MNI space computed from the GAAIN dataset.

Download the template [here](https://drive.google.com/file/d/1FxdcuMSAwM91dJM5-xXvE4z1mxCdjdl5/view?usp=sharing), and move it to the `MNI` directory within the repository.

### Install Greedy

PyAmyloid uses the Greedy registration tool for image coregistration.

#### You can install Greedy via ITK-SNAP (recommended):

- Download and install ITK-SNAP: https://www.itksnap.org/pmwiki/pmwiki.php?n=Downloads.SNAP4

- Run Help->Install Command-Line Tools from the ITK-SNAP main menu.

To verify installation:

```bash
greedy -version
```

If this prints a version (e.g., Greedy v0.6.1), you’re all set!

Alternatively, you can change line 21 in `coregistration.py` to the path to `Greedy` 

### Input Requirements

Your input must be a 3D amyloid PET image in NIfTI (.nii or .nii.gz) format.

If your data are in DICOM format, convert them using `dcm2niix`:

```bash
dcm2niix -z y -f amyloid_pet -o . /path/to/dicom_folder/
```

This will produce `amyloid_pet.nii.gz`, which can be used directly with PyAmyloid.

## Usage

### Basic command

```bash
python run_pyamyloid.py amyloid_pet.nii.gz
```

This will:

- Register your PET image to MNI space using Greedy

- Extract regional uptake values

- Normalize to the cerebellar reference region

- Output a file named `centiloid_results.csv` in the current directory

### Custom output file

```bash
python run_pyamyloid.py amyloid_pet.nii.gz my_output.csv
```

## Output

A CSV file (default: `centiloid_results.csv`) containing Centiloid-normalized SUVRs per region.

## Directory Structure

`MNI/average_pet_template.nii.gz` – Standard PET template in MNI space computed from GAAIN data

`MNI/reference_region/` – Cerebellar mask(s) for normalization from AVID ROIs

`MNI/target_regions/` – Cortical target regions for SUVR computation from AVID ROIs

`temp_greedy_registration_outputs/` – Intermediate registration outputs (auto-generated)
