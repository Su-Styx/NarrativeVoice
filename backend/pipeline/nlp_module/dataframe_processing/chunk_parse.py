# iterate through directory and then 

import json
from pathlib import Path
import pandas as pd

from private_directories import chunk_directory
# print('this ran')

directory=Path(chunk_directory) 

counter=0
collective_chunk_attrbutes={}

for file_path in directory.glob("*.json"):
    
    counter+=1
    
    chunk_attributes={}
    
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        # counter=0
        for i in data['validation']['accepted']:
            chunk_attributes[i['field']]=str(i['statement'])
        

        # print (counter)
    # print(chunk_attributes)

    # if counter==2:
    #     quit()
    collective_chunk_attrbutes['chunk'+str(counter)]=chunk_attributes
# print(collective_chunk_attrbutes)

print(collective_chunk_attrbutes['chunk1'])


# here are the fields we have so far:
# themes
# challenges
# experiences
# topics
# stated_links

