# singlethread-download单线程文件下载

执行说明:

    response_from_url(url:str, headers:dict, method:str='GET', cookies:str=None,
                      proxies:str=None, data=None)
    download_file(filename:str, response:object, content_size:int)
# multithread-download多线程文件下载

执行说明:

    multi_download_file(filename:str, url:str)
    
# parsefont 猫眼字体解析工具
# ice-scrapy 基于使用ice进行网络通信的scrapy