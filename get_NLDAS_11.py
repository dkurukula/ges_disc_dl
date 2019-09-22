
from pathlib import Path
import requests
import pandas as pd
from tqdm import tqdm, tqdm_pandas

DOWNLOAD_FOLDER = '11'
username = ''
password = '' 


DL_List_path = list(Path.cwd().joinpath('download_list',DOWNLOAD_FOLDER).glob('*inp.txt'))[0]
df = pd.read_csv(DL_List_path,sep='\t', skiprows=1,names = ['url'])


data_path = Path.cwd().joinpath('data')
data_path.mkdir(parents=True, exist_ok=True)
 
def dl_urls(df):
    with requests.Session() as session:
        url = str(df['url'])
        print(f'Attempting to download url: {url}')
        session.auth = (username, password)
        r1 = session.request('get', url)
        r = session.get(r1.url, auth=(username, password))
        print(f'status_code \n {r.status_code} \n\n') 
        print(f"headers['content-type'] \n {r.headers['content-type']} \n") 
        print(f'encoding \n {r.encoding} \n')
        if r.ok:
            print('Success \n')
            filename = dict(x.split('=') for x in url.split('&'))['LABEL']
            fullpath = data_path.joinpath(filename)
            with open(fullpath, 'wb') as f:
                f.write(r.content)
                print(f'Saved as: \n {fullpath}')
            #print(r.content) # Say

tqdm.pandas()
df.progress_apply(dl_urls, axis=1)

