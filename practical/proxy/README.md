[TOC]


# 前期准备:

    python3  编译环境
    celery   任务框架，异步式处理框架
    supervisor 启动模块（非必须），用户守护celery进程
    ubuntu 系统环境（任意系统也可以，建议是linux系统。如果不用supervisor也可以用windows）
    redis 保存数据库/消息队列
    
# 目的
爬取免费公开代理ip，并定时筛选有效代理保存。并通过封装接口进行获取代理池中的代理。

# 文件目录

创建以下目录文件

- proxy
    - `__init__.py`
    - config.py
    - crawl_proxy.py
    - crawler.py
    - db.py
    - valid_celery.py
    - api.py


## `__init__.py`

模块声明文件，空

## config.py
配置celery调度的参数

    # author: Z.M Z

    BROKER_URL = 'redis://127.0.0.1:6379/0'                 # 使用Redis作为消息代理
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'      # 把任务结果存在了Redis
    
    CELERY_TIMEZONE='Asia/Shanghai'                         # 指定时区，默认是 UTC
    
    CELERY_TASK_SERIALIZER = 'pickle'                       # 任务序列化和反序列化使用pickle方案
    CELERY_RESULT_SERIALIZER = 'json'                       # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
    CELERY_TASK_RESULT_EXPIRES = 60 * 60                # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显。这里表示一个小时
    CELERY_ACCEPT_CONTENT = ['json','pickle']               # 指定接受的内容类型
    
    CELERY_IMPORTS = (                                  # 指定导入的任务模块
    
        'valid_celery', # 阻塞时调用函数文件
    )
    
    
    # 定时任务
    from datetime import timedelta
    from celery.schedules import crontab
    
    
    # schedules 如果开启定时任务以下配置才会使用
    CELERYBEAT_SCHEDULE = {
    
      'valid_proxy:per10mins':{
           'task':'valid_celery.clean_proxy',
           'schedule':timedelta(minutes=10), # 每隔10min检查代理有效
           'args':()
       },
      # 'crawl_proxy:per10mins':{
      #      'task':'valid_celery.common_crawl',
      #      'schedule':timedelta(minutes=5), # 每隔5min检查代理有效
      #      'args':()
      #  }
    
    }

## db.py 
配置保存的数据库，在这里你可以使用你任意喜欢的数据库。个人在这里使用redis作为数据库。

    # author: Z.M Z

    import abc
    import redis
    import time
    
    class DBbaseHandler:
    
        @abc.abstractmethod
        def delete(self, key, name):
            pass
    
        @abc.abstractmethod
        def deletemany(self, name, *key):
            pass
    
        @abc.abstractmethod
        def add(self, value, key, name):
            pass
    
    
        def addmany(self, name, *kvs):
            for k, v in kvs:
                self.add(v, k, name)
    
        @abc.abstractmethod
        def all(self, name):
            pass
    
        @abc.abstractmethod
        def has(self, key, name):
            pass
    
    
    class RedisHandler(DBbaseHandler):
    
        def __init__(self, url='redis://127.0.0.1:6379/0', name=None):
            self.__conn = redis.Redis().from_url(url=url)
            self.name = name
    
        def delete(self, key, name):
            name = self.name or name
            return self.__conn.execute_command("ZREM", name, key)
    
        def deletemany(self, name, *key):
            name = self.name or name
            return self.__conn.execute_command("ZREM", name, *key)
    
        def add(self, value, key, name):
            return self.__conn.execute_command("ZADD", name, value, key)
    
        def all(self, name):
            return self.__conn.zscan(name)
    
        def has(self, key, name):
            return self.__conn.zscore(name, key) is not None
            
注意：在这里我定义了一个抽象基类DBbaseHandler, 当使用其他数据库时先继承此类。重写抽象类，这是为了后续维护的便利性。

## valid_celery.py

    # author: Z.M Z

    from crawler import cele
    
    import requests
    import lxml.html
    from crawler import redis_conn
    import time
    import traceback
    
    HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
               # "Cookie":'_ga=GA1.2.914577764.1561213321; OUTFOX_SEARCH_USER_ID_NCOO=834227477.8411206; OUTFOX_SEARCH_USER_ID="2076912312@10.168.11.11"; JSESSIONID=aaatO8n_MFD71fbGNnZUw; ___rl__test__cookies=1562080308876',
    }
    
    
    
    def crawl_proxy(rules):
        """
        爬取xicidaili的免费代理IP
        
        :param rules: 
        :return: 
        """
        url = rules['url']
        host = rules['host']
        port = rules['port']
        req = requests.get(url, headers=HEADERS)
        resp = lxml.html.fromstring(req.text)
        host_text = resp.xpath(host)
        port_text = resp.xpath(port)
        for i in range(len(host_text)):
            valid_proxy.delay(host_text[i], port_text[i])
    
    
    @cele.task
    def common_crawl():
        """
        将爬取操作封装成celery的任务进行调用，使用定时操作。可以启动此任务
        :return: 
        """
        for i in range(1, 3):
            rules = {
                'url': 'https://www.xicidaili.com/wt/%d' % i,
                'host': '//*[@id="ip_list"]//tr/td[2]/text()',
                'port': '//*[@id="ip_list"]//tr/td[3]/text()'
            }
            crawl_proxy(rules)
    
    @cele.task
    def valid_proxy(host, port):
        """
        验证ip是否有效，如果有效插入数据库，否则在数据库删除此记录
        :param host: 
        :param port: 
        :return: 
        """
        http_proxy = 'http://{}:{}'.format(host, port)
        count = 1
        while count <= 3:
            try:
                timeout = 3 * count
                req = requests.get(url="http://120.79.19.42/post/celery",
                                   headers=HEADERS,
                                   proxies={'http':http_proxy},
                                   timeout=timeout)
                print(req.status_code, http_proxy)
                if req.status_code == 200:
                    redis_conn.add(name="http_proxy",
                                   key='{}:{}'.format(host, port),
                                   value=int(time.time()))
                break
            except:
                print('500', http_proxy)
            count += 1
        else:
            redis_conn.delete(name="http_proxy", key='{}:{}'.format(host, port))
    
    
    @cele.task
    def clean_proxy():
        """
        从数据库加载代理ip数据，进行验证。如果失败则删除此条数据
        :return: 
        """
        try:
            ip_set = redis_conn.all(name="http_proxy")[1]
            for http_proxy, score in ip_set:
                host, port = http_proxy.decode("utf8").split(":")
                valid_proxy.delay(host, port)
        except:
            traceback.print_exc()


## crawler.py
加载config.py的参数， 实例celery对象

    from celery import Celery
    from proxy import db
    
    cele = Celery(__name__)
    cele.config_from_object("config")
    
    redis_conn = db.RedisHandler()


## crawl_proxy.py
在这里我没有使用celery的定时方法，采取的是while循环进行重复采集。

## api.py
这里我使用sanic起服务端。具体模块使用参看官网文档


# 项目环境以及脚本启动

在supervisor.conf 同级目录下创建proxy.conf 内容如下

    [program:proxy]
    command=celery -A crawler worker -P eventlet -c 20 --loglevel info
    directory=/home/zzm/api/proxy
    process_name=%(process_num)02d
    autostart=true
    autorestart=true
    startsecs=1
    startretries=20
    redirect_stderr=true
    user=common
    stdout_logfile=/opt/module/supervisor/logs/proxy.log
    stderr_logfile=/opt/module/supervisor/logs/proxy.err.log
    
    几个重要的参数说明
    [program:proxy] 必须要唯一，当然你也可以更改名字成[program:hahah],只要唯一就可以
    command 执行脚本的命令，在这里我执行启动celery的命令
    directory 你的项目路径
    user 启动用户，不建议使用root用户进行启动
    
    
-------------------
    启动方法
    $ supervisorctl reload # 重载配置
    cd 到你的项目路径下
    启动crawl_proxy.py脚本 后台挂起
    $ nohup python3 crawl_proxy.py > /dev/null & 
    
    $ supervisorctl status # 查看你的进程是否RUNNING中，这里的进程名字是proxy， 
    
    $ tailf /opt/module/supervisor/logs/proxy.log # 查看启动日志