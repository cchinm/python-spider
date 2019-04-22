# baidumap执行说明

执行说明
1. 执行model.py文件sql，建库。配置好mysql_url
2. 如果是第一次执行，则bdmap.py中的seekCityCode函数一定要执行。这是保存每个城市的bd_id
3. bdmap.py中的main函数可以帮助你爬取的相应关键词匹配的地点信息，包括经纬度(BD_09标准)，地区，地址，地点类别等。