import xml.etree.ElementTree as ET

response = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><templateEntity><template><description></description><groupId>d1d4eb3c-0189-1000-7a21-1da216861c68</groupId><id>bb6d983d-0e97-44f3-92fa-07158d117f41</id><name>CsvToJSON</name><timestamp>08/07/2023 22:46:34 UTC</timestamp><uri>https://localhost:8443/nifi-api/templates/bb6d983d-0e97-44f3-92fa-07158d117f41</uri></template></templateEntity>'

id = ET.fromstring(response).find('.//template/id').text
print(id)
