import random
import ssl
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime





GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
nifi_url="https://localhost:8443"
username = "lbellahmidi"
password = 123456780000
data={
    "username" : username ,
    "password" : password
    }

header = {
    "Content-Type" : "application/x-www-form-urlencoded"
}

response = requests.post( f'{nifi_url}/nifi-api/access/token',data=data,headers=header,verify=ssl.CERT_NONE)

if response.status_code == 201:
        nifi_token = response.text
        print("Token succefully retrieved!")
else:
        print("Failed to get token:", response.text)

#Retrieve templates to be deployed
directory_path = Path('./templates')
current_date = datetime.now().date()
formatted_date = current_date.strftime('%d-%m-%Y')

for file in directory_path.iterdir():
    if file.is_file():
        template_file_path = file
        source_path=Path(f'./{template_file_path}')
        destination_path = Path(f'./templates_deployed/{formatted_date}')



        #Step 1:  Upload template XML
        with open(template_file_path, 'rb') as f:
            template_data = f.read()

        print(GREEN +'file opened'+ RESET)
        #Auth required only for https
        headers = {
            'Authorization': f'Bearer {nifi_token}'
        }

        response = requests.post(
            f'{nifi_url}/nifi-api/process-groups/root/templates/upload', 
            headers=headers,
            files={'template': ('template.xml', template_data)},
            verify=False
        )

        print(GREEN +'first req sent'+ RESET)

        if response.status_code != 201:
            print(RED +"Failed to upload template XML:"+ RESET, response.text)
            continue

        template_id = ET.fromstring(response.text).find('.//template/id').text
        print('Here is the template id: '+ template_id)




        #Step 2: Instanciate template

        headers = {
            'Authorization': f'Bearer {nifi_token}',
            'Content-Type': 'application/json'
        }

        originX=round(random.uniform(0,10),1)
        originY=round(random.uniform(0,10),1)

        response = requests.post(
            f'{nifi_url}/nifi-api/process-groups/root/template-instance',
            headers=headers,
            json={'templateId': template_id,
                "originX": originX,
                "originY": originY,
                "disconnectedNodeAcknowledged": True},
            verify=False
        )

        print(GREEN +'second req sent'+ RESET)

        if response.status_code == 201:
            print(GREEN +"Template instantiated successfully."+ RESET)
            destination_path.mkdir(parents=True, exist_ok=True)
            new_file_path = destination_path / source_path.name
            source_path.rename(new_file_path)
        else:
            print(RED +"Failed to instantiate template:"+ RESET, response.text)

        try:
            instance_id = ET.fromstring(response.text).find('.//template/id').text
            print('Here is the template id: '+ instance_id)
        except Exception as e:
            print(RED +'Exception occured: '+ RESET,e)
        
        print(GREEN +'File uploaded and istanciated succesfully'+ RESET)
