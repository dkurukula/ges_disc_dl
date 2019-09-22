
from pathlib import Path
import requests
import pandas as pd
from tqdm import tqdm, tqdm_pandas

import logging
from threading import Thread
from queue import Queue
q = Queue(maxsize=0)
num_theads = 50



DOWNLOAD_FOLDER = '6'
username = ''
password = '' 

DL_List_path = list(Path.cwd().joinpath('download_list',DOWNLOAD_FOLDER).glob('*inp.txt'))[0]
df = pd.read_csv(DL_List_path,sep='\t', skiprows=1,names = ['urls'])


data_path = Path.cwd().joinpath('data')
data_path.mkdir(parents=True, exist_ok=True)

results = [{} for x in df.urls];

for i,url in enumerate((df.urls)):
    q.put((i,url))


def dl_url(q, results):
    while not q.empty():
        work = q.get()
        print(f'work ----- {work}')
        #try:
        with requests.Session() as session:
            url = work[1]
            print(f'Attempting to download url: {url}')
            session.auth = (username, password)
            r1 = session.request('get', url)
            r = session.get(r1.url, auth=(username, password))
            print(f'status_code \n {r.status_code} \n\n') 
            print(f"headers['content-type'] \n {r.headers['content-type']} \n") 
            print(f'encoding \n {r.encoding} \n')
            if r.ok:
                print('Success \n')
                results[work[0]] = 'Complete'
                filename = dict(x.split('=') for x in url.split('&'))['LABEL']
                fullpath = data_path.joinpath(filename)
                with open(fullpath, 'wb') as f:
                    f.write(r.content)
                    print(f'Saved as: \n {fullpath}')
    #except:
        #    print('could not get data...')
        q.task_done()
    return True

for i in range(num_theads):
    print(f'Starting thread {i}')
    worker = Thread(target = dl_url, args=(q, results))
    worker.setDaemon(True)
    worker.start()

q.join()
        



