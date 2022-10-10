import json
import requests
import glob
from tqdm.auto import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--server', help='Server URL')
parser.add_argument('-c', '--corpus', help='Corpus Directory')

args = parser.parse_args()

CORPUS_DIR = f'{args.corpus}/*.json'

SERVER_URL = args.server

class EncoderError(Exception):
    pass

def batcher(lst: list, n: int = 5):
    return (lst[i:i + n] for i in range(0, len(lst), n))

def encode_sents(sents: list):
    response = requests.post(f"{SERVER_URL}/get_embeddings", json={'instances': sents, 
                                                                   'parameters': {}})
    
    if response.ok:
        return json.loads(response.text)['predictions']
    else:
        raise EncoderError('Server failed!!!')

for filename in tqdm(glob.glob(CORPUS_DIR)):
    document = json.load(open(filename, 'r'))
    document['sentences'] = []
    
    for batch in batcher(document['raw_sents'], n=250):
        encoded_sents = encode_sents(batch)
        
        f_embeddings = [{'sentence': s, 
                         'tokens': t} for s, t in zip(batch, 
                                                      encoded_sents)]
        
        document['sentences'] += f_embeddings
        
    with open(filename, 'w') as f:
        json.dump(document, f)
        f.close()
    
