# author: Z.M Z

BROKER_URL = 'redis://127.0.0.1:6379/0'                 # 使用Redis作为消息代理
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'      # 把任务结果存在了Redis

CELERY_TIMEZONE='Asia/Shanghai'                         # 指定时区，默认是 UTC

CELERY_TASK_SERIALIZER = 'pickle'                       # 任务序列化和反序列化使用pickle方案
CELERY_RESULT_SERIALIZER = 'json'                       # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_TASK_RESULT_EXPIRES = 60 * 60                # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
CELERY_ACCEPT_CONTENT = ['json','pickle']               # 指定接受的内容类型

CELERY_IMPORTS = (                                  # 指定导入的任务模块

    'valid_celery', # 阻塞时调用函数文件
)


# 定时任务
from datetime import timedelta
from celery.schedules import crontab


# schedules
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

