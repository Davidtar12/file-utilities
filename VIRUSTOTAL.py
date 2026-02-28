import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()


# Configuration
API_KEY = os.getenv('VIRUSTOTAL_API_KEY')
FOLDER_PATH = r"C:\Users\david\Downloads\victoria-hdd-ssd-5-37\Victoria537"  # Replace with your target folder path
FILE_EXTENSIONS = ['.epub', '.txt']  # File extensions to scan

# VirusTotal API endpoints
UPLOAD_URL = 'https://www.virustotal.com/vtapi/v2/file/scan'
REPORT_URL = 'https://www.virustotal.com/vtapi/v2/file/report'


def get_files_to_scan(folder_path, extensions):
    """Retrieve a list of files with specified extensions from the folder."""
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))
    return files


def upload_file(file_path):
    """Upload a file to VirusTotal for scanning."""
    params = {'apikey': API_KEY}
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(UPLOAD_URL, files=files, params=params)
    return response.json()


def get_report(file_hash):
    """Retrieve the scan report for a given file hash."""
    params = {'apikey': API_KEY, 'resource': file_hash}
    response = requests.get(REPORT_URL, params=params)
    return response.json()


def scan_files(files):
    """Scan a list of files using VirusTotal."""
    for file_path in files:
        print(f"Uploading {file_path} to VirusTotal...")
        upload_result = upload_file(file_path)

        if 'error' in upload_result:
            print(f"Error uploading {file_path}: {upload_result['error']}")
            continue

        scan_id = upload_result.get('scan_id', None)
        if not scan_id:
            print(f"No scan ID received for {file_path}. Skipping.")
            continue

        # Wait for the scan to complete
        time.sleep(15)  # Adjust based on VirusTotal's response time

        # Retrieve the report
        report = get_report(upload_result['scan_id'])

        if 'error' in report:
            print(f"Error retrieving report for {file_path}: {report['error']}")
            continue

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
    files_to_scan = get_files_to_scan(FOLDER_PATH, FILE_EXTENSIONS)
    if not files_to_scan:
        print("No files found with the specified extensions.")
        return

    print(f"Found {len(files_to_scan)} files to scan.")
    scan_files(files_to_scan)


if __name__ == "__main__":
    main()
