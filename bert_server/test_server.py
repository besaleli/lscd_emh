import requests
import json

URL = 'http://bd5f-34-143-194-120.ngrok.io/'
response = requests.post(f'{URL}/get_embeddings', json={'instances': ['hello my name is raz'], 
                                                                  'parameters': {}})

if response.ok:
    print(json.loads(response.text))
else:
    print(f"[{response.status_code}] {response.text}")
