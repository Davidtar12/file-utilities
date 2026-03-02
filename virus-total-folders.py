import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()


# Configuration
API_KEY = os.getenv('VIRUSTOTAL_API_KEY')
FOLDER_PATH = r"C:\Users\USERNAME\Downloads\victoria-hdd-ssd-5-37\Victoria537"  # Replace with your target folder path

# VirusTotal API endpoints
UPLOAD_URL = 'https://www.virustotal.com/vtapi/v2/file/scan'
REPORT_URL = 'https://www.virustotal.com/vtapi/v2/file/report'

# VirusTotal Free API rate limits
MAX_REQUESTS_PER_MINUTE = 4
SLEEP_BETWEEN_REQUESTS = 15  # Adjusted to prevent hitting API limits


def get_files_to_scan(folder_path):
    """Retrieve a list of all files in the folder (including subfolders)."""
    if not os.path.exists(folder_path):
        print(f"❌ Error: The folder path '{folder_path}' does not exist.")
        return []

    files = []
    print(f"📂 Scanning folder: {folder_path}")

    for root, _, filenames in os.walk(folder_path):
        print(f"📁 Checking directory: {root}")  # Debugging output
        for filename in filenames:
            full_path = os.path.join(root, filename)
            print(f"✅ Found file: {full_path}")  # Debugging output
            files.append(full_path)

    if not files:
        print("⚠️ No files found in the folder.")
    return files


def upload_file(file_path):
    """Upload a file to VirusTotal for scanning."""
    params = {'apikey': API_KEY}

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(UPLOAD_URL, files=files, params=params)

        if response.status_code == 204:
            print(f"⚠️ API limit reached. Pausing for 60 seconds...")
            time.sleep(60)
            return upload_file(file_path)  # Retry upload

        if response.status_code != 200:
            print(f"❌ Error: Failed to upload {file_path}. HTTP {response.status_code}")
            return None

        return response.json()

    except Exception as e:
        print(f"❌ Error uploading {file_path}: {e}")
        return None


def get_report(scan_id, max_retries=5, wait_time=30):
    """Retrieve the scan report for a given file hash, with retries."""
    params = {'apikey': API_KEY, 'resource': scan_id}

    for attempt in range(max_retries):
        response = requests.get(REPORT_URL, params=params)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 204:
            print(f"⚠️ Report not ready yet (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"❌ Error: Failed to retrieve report for scan ID {scan_id}. HTTP {response.status_code}")
            return None

    print(f"❌ Report for scan ID {scan_id} was not found after {max_retries} attempts.")
    return None


def scan_files(files):
    """Scan a list of files using VirusTotal, respecting rate limits."""
    request_count = 0

    for file_path in files:
        print(f"🚀 Uploading {file_path} to VirusTotal...")
        upload_result = upload_file(file_path)

        if not upload_result or 'scan_id' not in upload_result:
            print(f"⚠️ Failed to upload {file_path}. Skipping.")
            continue

        scan_id = upload_result['scan_id']
        print(f"📄 Scan ID received: {scan_id}")

        # Wait for the scan to complete
        print("⏳ Waiting 60 seconds for VirusTotal to process the scan...")
        time.sleep(60)

        # Retrieve the report
        report = get_report(scan_id)

        if not report or 'positives' not in report:
            print(f"⚠️ Failed to retrieve report for {file_path}. Skipping.")
            continue

        # Process the report
        positives = report.get('positives', 0)
        total = report.get('total', 0)
        permalink = report.get('permalink', 'N/A')

        print(f"🛡️ Results for {file_path}:")
        print(f"   🔍 Detected by {positives} out of {total} engines.")
        print(f"   🔗 Report: {permalink}\n")

        # Respect VirusTotal rate limits
        request_count += 1
        if request_count >= MAX_REQUESTS_PER_MINUTE:
            print(f"⏸️ Rate limit reached ({MAX_REQUESTS_PER_MINUTE} requests/min). Pausing for 60 seconds...")
            time.sleep(60)
            request_count = 0  # Reset counter


def main():
    files_to_scan = get_files_to_scan(FOLDER_PATH)

    if not files_to_scan:
        print("⚠️ No files found to scan.")
        return

    print(f"📊 Found {len(files_to_scan)} files to scan.")
    scan_files(files_to_scan)


if __name__ == "__main__":
    main()
