import subprocess
import os
import sys

BASE = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

scripts = [

    "01_load_and_inventory.py",

    "02_quality_control.py",

    "03_binary_analysis.py",

    "04_alphamissense_analysis.py",

    "05_raw_score_analysis.py",

    "06_correlation_analysis.py",

    "07_allele_frequency.py",

    "08_concordance.py",

    "09_visualizations.py",

    "10_validation.py"

]

print("=" * 70)
print("RUNNING COMPLETE CLINVAR VUS EDA PIPELINE")
print("=" * 70)

for script in scripts:

    script_path = os.path.join(
        BASE,
        "scripts",
        script
    )

    print("\n")
    print("=" * 70)
    print(
        "RUNNING:",
        script
    )
    print("=" * 70)

    result = subprocess.run(
        [
            sys.executable,
            script_path
        ]
    )

    if result.returncode != 0:

        print(
            "\nERROR:",
            script
        )

        sys.exit(
            result.returncode
        )

print("\n")
print("=" * 70)
print("COMPLETE PIPELINE FINISHED")
print("=" * 70)
