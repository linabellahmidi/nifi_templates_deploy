import requests

# NiFi URL and authentication token
nifi_url = "https://localhost:8443"  # Update with your NiFi URL
nifi_token = "your-nifi-token"  # Replace with your NiFi token

# Path to the NiFi template XML file
template_file_path = "path/to/template.xml"  # Update with the correct file path

# Step 1: Upload template XML
with open(template_file_path, 'rb') as f:
    template_data = f.read()

headers = {
    'Authorization': f'Bearer {nifi_token}'
}

response = requests.post(
    f'{nifi_url}/nifi-api/templates/upload',
    headers=headers,
    files={'template': ('template.xml', template_data)}
)

if response.status_code != 201:
    print("Failed to upload template XML:", response.text)
    exit()

template_id = response.json()['template']['id']

# Step 2: Import the uploaded template
response = requests.post(
    f'{nifi_url}/nifi-api/templates/import',
    headers=headers,
    json={'templateId': template_id}
)

if response.status_code != 201:
    print("Failed to import template:", response.text)
    exit()

imported_template_id = response.json()['template']['id']

# Step 3: Instantiate the imported template
response = requests.post(
    f'{nifi_url}/nifi-api/template-instance',
    headers=headers,
    json={'templateId': imported_template_id}
)

if response.status_code == 201:
    print("Template deployed successfully.")
else:
    print("Failed to deploy template:", response.text)
