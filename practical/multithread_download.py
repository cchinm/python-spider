import sys
import requests
import threadpool
from threadpool import ThreadPool


from practical.singlethread_download import response_from_url


defaults_params = {
    'thread_pool_size':5
}
workers = ThreadPool(defaults_params['thread_pool_size'])
fsize = 0
fcount = 0


def download_handler(start:int, end:int, url:str, headers:dict, filename:str) -> object():
    global fcount
    headers['Range'] = 'bytes=%d-%d' % (start, end)
    # print(headers)
    response = response_from_url(url=url, headers=headers)
    with open(filename, 'r+b') as fp:
        fp.seek(start)
        fp.write(response.content)
        fcount = fcount + end - start
        sys.stdout.write("\rTotal: %d  Now: %d" % (fsize, fcount))
        sys.stdout.flush()






def multi_download_file(filename:str, url:str):
    global fsize
    head = requests.head(url)
    file_size = int(head.headers.get('Content-Length', 0))
    fsize = file_size
    if file_size > 0:
        fp = open(filename, "wb")
        fp.truncate(file_size)
        fp.close()
        single_part = file_size// 16
        thread_list = []
        for i in range(16):
            start = single_part*i
            if i == 15:
                end = file_size
            else:
                end = start + single_part
            thread_list.append((None, {"start":start,
                                "end":end,
                                "url":url,
                                "headers":{},
                                "filename":filename}))
        reqs = threadpool.makeRequests(download_handler, thread_list)
        [workers.putRequest(req) for req in reqs]
        workers.wait()


