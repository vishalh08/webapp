import os
import requests
import sys

if len(sys.argv) < 2:
    raise SystemExit("Usage: python upload_reports.py <report-file>")

file_name = sys.argv[1]
scan_type = ''

if file_name == 'gitleaks.json':
    scan_type = 'Gitleaks Scan'
elif file_name == 'semgrep.json':
    scan_type = 'Semgrep JSON Report'
elif file_name == 'retire.json':
    scan_type = 'Retire.js Scan'
elif file_name == 'report_json.json':
    scan_type = 'ZAP Scan'
else:
    raise SystemExit(f"Unsupported report file: {file_name}")

if not os.path.exists(file_name):
    print(f"Report file not found, skipping upload: {file_name}")
    sys.exit(0)

url = os.getenv('DEFECTDOJO_IMPORT_URL', 'https://demo.defectdojo.org/api/v2/import-scan/')
token = os.getenv('DEFECTDOJO_API_TOKEN')
if not token:
    raise SystemExit('Missing DEFECTDOJO_API_TOKEN environment variable')

headers = {'Authorization': f'Token {token}'}

data = {
    'active': True,
    'verified': True,
    'scan_type': scan_type,
    'minimum_severity': 'Low',
}

engagement_id = os.getenv('DEFECTDOJO_ENGAGEMENT_ID')
if engagement_id:
    data['engagement'] = engagement_id

with open(file_name, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, headers=headers, data=data, files=files)

if response.status_code == 201:
    print('Scan results imported successfully')
else:
    raise SystemExit(f'Failed to import scan results: {response.status_code} {response.content}')
