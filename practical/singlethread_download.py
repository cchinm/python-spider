# -*- coding: utf-8 -*-

import requests

url = ""
cookies = ""
headers = {}

defalut_params = {

}

def response_from_url(url:str, headers:dict, method:str='GET', cookies:str=None,
                      proxies:str=None, data=None):
    method = method.upper()
    req = requests.session()
    try:
        if method == 'GET':
            response = req.request(method=method, url=url, proxies=proxies,
                                   headers=headers, cookies=cookies, stream=True)
        elif method == 'POST':
            response = req.request(method=method, url=url, proxies=proxies,
                                   headers=headers, cookies=cookies, data=data, stream=True)
        else:
            raise ValueError("NO SUCH METHOD ``%s``" % method)
        return response
    except Exception as e:
        print(e)
        req.close()




def download_file(filename:str, response:object, content_size:int):
    import sys, time
    total = float(len(response.content))
    count = 0
    with open(filename, "wb") as fp:
        for _ in response.iter_content(chunk_size=content_size):
            fp.write(_)
            count += len(_)/total*50
            fp.flush()
            sys.stdout.write("\r[%s%s] %d%%" % ('█' * int(count), ' ' * (50 -int(count)), count*2))
            sys.stdout.flush()
            time.sleep(.2)
    response.close()



if __name__ == '__main__':
    resp = response_from_url(url="https://blog.csdn.net/qq_35203425/article/details/80903769",
                             headers={})
    download_file(r"C:\Users\root\Downloads\test.txt",resp,1024)