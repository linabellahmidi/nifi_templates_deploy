from pathlib import Path
import random
from datetime import datetime

current_date = datetime.now().date()
formatted_date = current_date.strftime('%d-%m-%Y')
directory_path = Path('./templates')
print(formatted_date)

#Retrieve templates to be deployed
for file in directory_path.iterdir():
    if file.is_file():
        template_file_path = file
        source_path=Path(f'./{template_file_path}')
        destination_path = Path(f'./templates_deployed/{formatted_date}')
        destination_path.mkdir(parents=True, exist_ok=True)
        new_file_path = destination_path / source_path.name
        source_path.rename(new_file_path)

