import os
import sys
import subprocess
from pathlib import Path

# Set the minimum coverage threshold (80%)
MIN_COVERAGE = 80

# Get the current working directory
project_dir = Path(__file__).resolve().parent

# Create the "push_reports" directory if it doesn't exist
push_reports_dir = project_dir / "push_reports"
push_reports_dir.mkdir(parents=True, exist_ok=True)

# Run PyTest with coverage
try:
    result = subprocess.run(
        ["pytest", "--cov", "--cov-report=xml", "--cov-report=html"],
        cwd=project_dir,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
except subprocess.CalledProcessError as e:
    print(e.stderr.decode())
    sys.exit(1)

# Parse the coverage XML report
coverage_xml_path = project_dir / "coverage.xml"
coverage_data = {}
with open(coverage_xml_path, "r") as xml_file:
    for line in xml_file:
        if line.startswith("<coverage"):
            coverage_data["lines"] = int(
                line.split("lines-covered=\"")[1].split("\"")[0])
            coverage_data["lines_total"] = int(
                line.split("lines-valid=\"")[1].split("\"")[0])

# Calculate the coverage percentage
coverage_percentage = (coverage_data["lines"] / coverage_data[
    "lines_total"]) * 100

# Check if the coverage threshold is met
if coverage_percentage < MIN_COVERAGE:
    print(
        f"Coverage ({coverage_percentage:.2f}%) is below the minimum threshold"
        f" ({MIN_COVERAGE}%).")
    sys.exit(1)

# Copy the coverage report to the "push_reports" directory
coverage_html_path = project_dir / "htmlcov" / "index.html"
coverage_html_report_path = push_reports_dir / "coverage_report.html"
coverage_html_report_path.parent.mkdir(parents=True, exist_ok=True)
os.replace(coverage_html_path, coverage_html_report_path)

print(f"Coverage report saved to: {coverage_html_report_path}")
print(
    f"Coverage ({coverage_percentage:.2f}%) meets the minimum threshold "
    f"({MIN_COVERAGE}%).")
