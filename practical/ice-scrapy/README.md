# ice_scrapy
将原生的scrapy的模块替换成使用ice进行通信的模块，通过这个模块进行分布式通信。实现与scrapy_redis相同的功能。


# 方法
将spiders下的spider文件的继承方法改为继承genspider.Spider或者genspider.IceCrawlSpider。

