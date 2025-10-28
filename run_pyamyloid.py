import argparse
import os
import shutil
import subprocess
import sys
import time

#!/usr/bin/env python3

def main():
    t0 = time.perf_counter()

    parser = argparse.ArgumentParser(description="Run coregistration then centiloid on a NIfTI file")
    parser.add_argument("nifti", help="path to input NIfTI (.nii or .nii.gz)")
    parser.add_argument(
        "--coreg", "-c",
        default=os.path.join(os.path.dirname(__file__), "coregistration.py"),
        help="coregistration script to call (default: ./coregistration.py next to this file)"
    )
    parser.add_argument(
        "--centiloid",
        default=os.path.join(os.path.dirname(__file__), "centiloid.py"),
        help="centiloid script to call (default: ./centiloid.py next to this file)"
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="python interpreter to use for running the scripts (default: current interpreter)"
    )
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="extra arguments to forward to the coregistration script (prefix with -- if needed)"
    )
    args = parser.parse_args()

    if not os.path.isfile(args.nifti):
        print(f"Error: nifti file not found: {args.nifti}", file=sys.stderr)
        sys.exit(2)

    def resolve_script(path):
        if os.path.isfile(path):
            return path
        found = shutil.which(path)
        if found:
            return found
        print(f"Error: script not found: {path}", file=sys.stderr)
        sys.exit(2)

    coreg_path = resolve_script(args.coreg)
    cent_path = resolve_script(args.centiloid)

    # Run coregistration (takes the nifti file as input)
    coreg_cmd = [args.python, coreg_path, args.nifti] + args.extra
    try:
        ret = subprocess.run(coreg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Coregistration script failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except OSError as e:
        print(f"Failed to run coregistration command: {e}", file=sys.stderr)
        sys.exit(1)

    # Run centiloid (no inputs)
    cent_cmd = [args.python, cent_path, args.nifti]
    try:
        ret = subprocess.run(cent_cmd, check=True)
        t1 = time.perf_counter()
        elapsed = t1 - t0
        print(f"[INFO] Total processing time: {elapsed:.2f} seconds")
        sys.exit(ret.returncode)

    except subprocess.CalledProcessError as e:
        print(f"Centiloid script failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except OSError as e:
        print(f"Failed to run centiloid command: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
    
