import ssl
import requests

nifi_url="https://localhost:8443/nifi-api/access/token"
username = "lbellahmidi"
password = 123456780000
data={
    "username" : username ,
    "password" : password
    }

header = {
    "Content-Type" : "application/x-www-form-urlencoded"
}

response = requests.post(nifi_url,data=data,headers=header,verify=ssl.CERT_NONE)

if response.status_code == 201:
        token = response.text
        print(token)
else:
        print("Failed to get token:", response.text)
