import os
import sys

base = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(base, "scripts")
results_dir = os.path.join(base, "results")
visuals_dir = os.path.join(base, "visuals")
logs_dir = os.path.join(base, "logs")

os.makedirs(results_dir, exist_ok=True)
os.makedirs(visuals_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)

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

log_lines = []
log_lines.append("======================================================================")
log_lines.append("RUNNING COMPLETE CLINVAR VUS EDA PIPELINE")
log_lines.append("======================================================================\n")

for script_name in scripts:
    log_lines.append("======================================================================")
    log_lines.append(f"RUNNING: {script_name}")
    log_lines.append("======================================================================")
    
    script_path = os.path.join(scripts_dir, script_name)
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Capture print output
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    global_vars = {"__file__": script_path}
    try:
        exec(code, global_vars)
        output = sys.stdout.getvalue()
        log_lines.append(output)
    except Exception as e:
        log_lines.append(f"ERROR: {e}")
    finally:
        sys.stdout = old_stdout

log_lines.append("\n======================================================================")
log_lines.append("COMPLETE PIPELINE FINISHED")
log_lines.append("======================================================================")

log_content = "\n".join(log_lines)

log_file_path = os.path.join(logs_dir, "full_analysis.log")
with open(log_file_path, "w", encoding="utf-8") as f:
    f.write(log_content)

print(f"Pipeline executed synchronously. Full log saved to {log_file_path}")
