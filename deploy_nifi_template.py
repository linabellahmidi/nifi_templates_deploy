import requests
import json
import os

# NiFi cluster details
nifi_url = os.environ.get("NIFI_URL")
nifi_token = os.environ.get("NIFI_TOKEN")

# Directory containing NiFi templates
template_dir = os.environ.get("TEMPLATE_DIR")

# Function to deploy a NiFi template
def deploy_template(template_file):
    with open(template_file, 'rb') as f:
        template_data = f.read()

    headers = {
        'Authorization': f'Bearer {nifi_token}'
    }

    data = {
        'template': (os.path.basename(template_file), template_data)
    }

    response = requests.post(f'{nifi_url}/nifi-api/process-groups/root/templates/upload', headers=headers, files=data)

    if response.status_code == 201:
        template_id = response.json()['template']['id']
        response = requests.post(f'{nifi_url}/nifi-api/process-groups/root/template-instance', headers=headers, json={'templateId': template_id})

        if response.status_code == 201:
            print(f"Template {template_file} deployed successfully.")
        else:
            print(f"Failed to deploy template {template_file}: {response.text}")
    else:
        print(f"Failed to upload template {template_file}: {response.text}")

# Deploy templates
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith(".xml"):
            template_file = os.path.join(root, file)
            deploy_template(template_file)
