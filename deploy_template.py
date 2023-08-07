import requests

# NiFi URL and authentication token
nifi_url = "https://localhost:8443"  # Update with your NiFi URL
nifi_token = "eyJraWQiOiIzODA2MDc5Zi01MmZmLTRkNDMtOWQzNS1jZmI1NGVhNjQ3MWYiLCJhbGciOiJQUzUxMiJ9.eyJzdWIiOiIwYzNlNGUyMS03YWIxLTQwOGMtYjBlOS1jMjZhODNmZWI4ZWMiLCJhdWQiOiJTaW5nbGVVc2VyTG9naW5JZGVudGl0eVByb3ZpZGVyIiwibmJmIjoxNjkxNDQ0OTQ3LCJpc3MiOiJTaW5nbGVVc2VyTG9naW5JZGVudGl0eVByb3ZpZGVyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiMGMzZTRlMjEtN2FiMS00MDhjLWIwZTktYzI2YTgzZmViOGVjIiwiZXhwIjoxNjkxNDczNzQ3LCJpYXQiOjE2OTE0NDQ5NDcsImp0aSI6ImY1MzU5YTcwLTI1YjEtNGZhMi1hNWYyLWU1OThkZmNkMGZkYiJ9.iOi9N5JCh-XfPNaxFkev8C7UJqAocNq-psTvGa_hajXt88n6DkOZwbK-F9omZIx3AK0vV-mpNNAZ0NbrWcMcLjyjZPnENr_I29p0f_3kJIkpjWKkw7zIr1Z_pkiFHrGvpuOVuiLB1BEExguOsARfN7hbCqabkrMe5lA9ymH0YLrLfP2Sf1jEZVfJX7HrnwJb5XEFp5C7jjykBiBhnkSWj_J2kNEBtWtFpw1kDEyCqBJnYg4KKshWusuZDafXxtkYPUi8bXW_H9Zik9YJu5CxosqT2hgywGFYtQCFaLXXbp_hwulAgo2FSARnvfWANdmgh-0qI-V-5l_HM1y8iIniAf44rV7qjUfqWHwsLXdhvZFk_8m-ZUbQzyL6GACZsdQgG9feRMcVruYucC5yFUijojE4zX8O4WS-CYfgtBAnC9XIG8WS8-Jw9ZfhjbtpNpPGAQgUlnYq-sqPg9LJA0pU5JMh135UYajdQnTX3wQ4tYENU3tcWpl1sKBlrdOKqB5e8KtwBMYvmghaa9A_k-nAEROFgpWHbG2q6w71bJ_Ak_YLOeDdPzBkkkmuxW-rdqfcAqlDH4yzouPOQWuAGLgNo5JZvyWUh1c8TeSFUB-NbycY9w6s1d65dgiTowOE1huiTFjDsdKsW_A_a9wAJHhQ_pmZ3X3vJNn_cu3BDAM7qYI"  # Replace with your NiFi token

# Path to the NiFi template XML file
template_file_path = "/nifi_templates/CsvToJSON.xml"

# Step 1: Upload template XML
with open(template_file_path, 'rb') as f:
    template_data = f.read()

headers = {
    'Authorization': f'Bearer {nifi_token}'
}

response = requests.post(
    f'{nifi_url}/nifi-api/process-groups/root/templates/upload', 
    headers=headers,
    files={'template': ('template.xml', template_data)}
)

print('first req sent')

if response.status_code != 201:
    print("Failed to upload template XML:", response.text)
    exit()

template_id = response.json()['template']['id']

# Step 2: Import the uploaded template
response = requests.post(
    f'{nifi_url}/nifi-api/process-groups/root/templates/import',
    headers=headers,
    json={'templateId': template_id}
)

if response.status_code != 201:
    print("Failed to import template:", response.text)
    exit()

print('second req sent')
imported_template_id = response.json()['template']['id']

# Step 3: Instantiate the imported template
response = requests.post(
    f'{nifi_url}/nifi-api/process-groups/root/template-instance',
    headers=headers,
    json={'templateId': imported_template_id}
)

print('third req sent')
if response.status_code == 201:
    print("Template deployed successfully.")
else:
    print("Failed to deploy template:", response.text)
