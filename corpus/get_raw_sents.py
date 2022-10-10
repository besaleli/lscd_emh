import json
import lxml
import glob
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
import os

STREET_ADS_PATH = 'corpora/ephemera/street_ads/TEI/*.xml'
BYP_PATH = 'corpora/projectbenyehuda/TEI/by-decades-accurate/*/*.xml'
TODIR = 'corpus/corpus_files'

os.system(f'mkdir -p {TODIR}')

# get street ads
def parse(filename: str, filetype: str, writer_id: int):
    with open(filename, 'r') as f:
        raw_doc = f.read()
        
    document = BeautifulSoup(raw_doc, 'lxml')
    
    data = dict()
    data['name'] = filename.split('/')[-1][:-4]
    data['year'] = int(document.find('date').attrs['when'][:4])
    
    if filetype == 'ephemera':
        raw_sents = map(lambda i: i.text.strip(), document.find_all('p'))
    elif filetype == 'byp':
        raw_sents = filter(lambda i: bool(i), 
                           map(lambda i: i.strip(),
                               document.find('text').text.split('\n')))
    else:
        raw_sents = None
        assert filetype in ['ephemera', 'byp']
        
    data['raw_sents'] = list(raw_sents)
        
    with open(f"{TODIR}/{filetype}_{writer_id}.json", 'w') as f:
        json.dump(data, f)
        f.close()

print('parsing street ads...')
for i, fname in tqdm(enumerate(glob.glob(STREET_ADS_PATH))):
    parse(fname, 'ephemera', i)

print('parsing byp...')
for i, fname in tqdm(enumerate(glob.glob(BYP_PATH))):
    parse(fname, 'byp', i)
    
# sanity check
for i in json.load(open(f"{TODIR}/byp_0.json", 'r'))['raw_sents']:
    print(i)
