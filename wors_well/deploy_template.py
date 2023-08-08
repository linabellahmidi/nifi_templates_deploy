import requests
import xml.etree.ElementTree as ET


nifi_url = "https://localhost:8443"
nifi_token = "eyJraWQiOiIzMTE2NzdmYS04OTYyLTQ0ZDEtODE0MS05Yjg5NmFmZGQ1MzAiLCJhbGciOiJQUzUxMiJ9.eyJzdWIiOiI4ZjU3NTY4ZC1iZWM5LTQwMGYtOTMxOC05N2ViZDMzMDQwZGUiLCJhdWQiOiJTaW5nbGVVc2VyTG9naW5JZGVudGl0eVByb3ZpZGVyIiwibmJmIjoxNjkxNDg3MTAwLCJpc3MiOiJTaW5nbGVVc2VyTG9naW5JZGVudGl0eVByb3ZpZGVyIiwiZ3JvdXBzIjpbXSwicHJlZmVycmVkX3VzZXJuYW1lIjoiOGY1NzU2OGQtYmVjOS00MDBmLTkzMTgtOTdlYmQzMzA0MGRlIiwiZXhwIjoxNjkxNTE1OTAwLCJpYXQiOjE2OTE0ODcxMDAsImp0aSI6ImYzMWFiMTUyLTRkYjEtNDFhMy1iZjg3LWI3Y2VhZWQ1OGRhZSJ9.bQ3kppfdSia6Iw5A_Rq4WXh63GJReltqU2bQCovxZWMRaau3P3wUbm6TtaqpCk6VJuOsKCz3GByBNHDFkP0i0yJAwRbdAXNeuB06fXN0E2gKCkIXX6Gcjk3LU4d6I1zGoEtbiFDN_srF5yYQDEe4W2ovrMLUe95E7H1TyszGSUw6wYdUWXuizGUjEdUae3NH2HSp79Cn7XwqsNpEMqdR4N6Gukm8TIGglvMvRRc_qVas5CUhdY35168HHUoUHmKqkXfrLpKGggySb7OPJ-qhmVyO5SSpXI3YyhqLfepmNtb3fUBkwe4Va78_fOD_JMEw_Rjd01FR9a3IMbraWU0YCi2cKw2KYSMsiN5cXTXHeqw7BktVCuZ2CjSyuf5NzlgDN12uTjhqweK_YpRlwJHk5Bf9R5PstJyyIegIRYnGqMysVcIM8yU1AxZiCqfPF5TtzJZ_DFY0SDm-FBinK2jKeoxHLGxVojg8TOzruQ-1e9BcEXdLIuFqh1XSky_SBsb4FoqqGnYr7RJIy8Vc0lOq9-fh_ARgnstbX_RgYnclzVX4kgPba3PsR8YHkShAjxetYEw0yejeIo4dXC9JFc2hh4XGjWKjanL8Ft7rdLcoyLYoJLjnJSt6m7medMcWMSiatOOZFhO9aiNftHLjmjZu4gIKTuzXdvZ2nkcH9zjcACo"

template_file_path = "templates/CsvToJSON.xml"

# Step 1: Upload template XML
with open(template_file_path, 'rb') as f:
    template_data = f.read()

print('file opened')
#print(template_data)
headers = {
    'Authorization': f'Bearer {nifi_token}'
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
    'Authorization': f'Bearer {nifi_token}',
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
