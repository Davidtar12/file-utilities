import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()


# Configuration
API_KEY = os.getenv('VIRUSTOTAL_API_KEY')
# Path to the ZIP file to scan
TARGET_FILE = r"C:\Users\USERNAME\Downloads\HDDLLFsetup.4.50.exe"

# VirusTotal API endpoints
UPLOAD_URL = 'https://www.virustotal.com/vtapi/v2/file/scan'
REPORT_URL = 'https://www.virustotal.com/vtapi/v2/file/report'

def upload_file(file_path):
    """Upload a file to VirusTotal for scanning."""
    params = {'apikey': API_KEY}
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(UPLOAD_URL, files=files, params=params)
    return response.json()

def get_report(resource):
    """Retrieve the scan report for a given file hash or scan_id."""
    params = {'apikey': API_KEY, 'resource': resource}
    response = requests.get(REPORT_URL, params=params)
    return response.json()

def scan_file(file_path):
    """Scan a single file using VirusTotal."""
    print(f"Uploading {file_path} to VirusTotal...")
    upload_result = upload_file(file_path)

    if 'error' in upload_result:
        print(f"Error uploading {file_path}: {upload_result['error']}")
        return

    # VirusTotal may return a scan_id and/or the file hash (resource)
    # Typically, it's better to use the file's hash provided in the response.
    resource = upload_result.get('resource', None)
    if not resource:
        print(f"No resource identifier received for {file_path}. Skipping.")
        return

    # Wait for the scan to complete
    time.sleep(15)  # Adjust based on VirusTotal's response time

    # Retrieve the report
    report = get_report(resource)

    if 'error' in report:
        print(f"Error retrieving report for {file_path}: {report['error']}")
        return

    # Process the report
    positives = report.get('positives', 0)
    total = report.get('total', 0)
    permalink = report.get('permalink', 'N/A')
    print(f"Results for {file_path}:")
    print(f"  Detected by {positives} out of {total} engines.")
    print(f"  Report: {permalink}\n")

    # Respect the rate limit
    time.sleep(15)  # Adjust based on the rate limit

def main():
    # Since we're scanning a single file (the zip file), call scan_file directly.
    if not os.path.isfile(TARGET_FILE):
        print("The specified file does not exist.")
        return

    scan_file(TARGET_FILE)

if __name__ == "__main__":
    main()
