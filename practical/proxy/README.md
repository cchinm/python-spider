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


## db.py 
配置保存的数据库，在这里你可以使用你任意喜欢的数据库。个人在这里使用redis作为数据库。
          
注意：在这里我定义了一个抽象基类DBbaseHandler, 当使用其他数据库时先继承此类。重写抽象类，这是为了后续维护的便利性。

## valid_celery.py



## crawler.py
加载config.py的参数， 实例celery对象




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