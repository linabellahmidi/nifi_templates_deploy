import requests
import xml.etree.ElementTree as ET


nifi_url = "http://localhost:8080"
username = ""
password = ""

#If https
if nifi_url.startswith('https'):
    # Request headers
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    # Request data
    data = {
        "username": username,
        "password": password
    }

    # Send the request to get the token
    response = requests.post(nifi_url,
                            headers=headers,
                            data=data,
                            verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        token = response.text
    else:
        print("Failed to get token:", response.text)

template_file_path = "templates/CsvToJSON.xml"

# Upload template XML
with open(template_file_path, 'rb') as f:
    template_data = f.read()

print('file opened')
#Auth required only for https
headers = {
    #'Authorization': f'Bearer {nifi_token}'
}

response = requests.post(
    f'{nifi_url}/nifi-api/process-groups/root/templates/upload', 
    headers=headers,
    files={'template': ('template.xml', template_data)},
    verify=False
)

print('first req sent')

if response.status_code != 201:
    print("Failed to upload template XML:", response.text)
    exit()

template_id = ET.fromstring(response.text).find('.//template/id').text
print('Here is the template id: '+ template_id)


#Step 2: Instanciate template

headers = {
    #'Authorization': f'Bearer {nifi_token}',
    'Content-Type': 'application/json'
}

response = requests.post(
    f'{nifi_url}/nifi-api/process-groups/root/template-instance',
    headers=headers,
    json={'templateId': template_id,
        "originX": 0.0,
        "originY": 0.0,
        "disconnectedNodeAcknowledged": True},
    verify=False
)

print('second req sent')
if response.status_code == 201:
    print("Template instantiated successfully.")
else:
    print("Failed to instantiate template:", response.text)

try:
    instance_id = ET.fromstring(response.text).find('.//template/id').text
    print('Here is the template id: '+ instance_id)
except Exception as e:
    print('Exception occured: ',e)
