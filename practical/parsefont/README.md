# parsefont 猫眼字体解析工具

    # 实例对象
    from parsefont.analysis import MaoyanFont
    
    p = MaoyanFont()
    
    # 调用本地woff文件，与基准文件进行校对
    file = '本地woff文件路径'
    result = p.load(file)
    print(result)
    >>> {'uniE631': 6, 'uniE659': 0, 'uniE715': 9, 'uniE923': 7, 'uniF024': 8, 'uniF255': 4, 'uniF467': 3, 'uniF4E8': 2, 'uniF533': 5, 'uniF7A7': 1}

    # 下载线上内容，与基准文件进行校对
    from base64 import b64decode
    s = '网页base64编码内容'
    s = b64decode(s) 
  
    result = p.loads(s)
    print(result)
    >>> {'uniE188': 7, 'uniE7CA': 8, 'uniE7F2': 0, 'uniE8E6': 2, 'uniE8F1': 1, 'uniEB56': 3, 'uniECDF': 5, 'uniED63': 9, 'uniF1FA': 4, 'uniF8A6': 6}
    
    # 获取网页源编码
    p.uni_to_raw()
    >>> {'&#e188;': 7, '&#e7ca;': 8, '&#e7f2;': 0, '&#e8e6;': 2, '&#e8f1;': 1, '&#eb56;': 3, '&#ecdf;': 5, '&#ed63;': 9, '&#f1fa;': 4, '&#f8a6;': 6}
    # 将字符码转变为十进制
    p.uni_to_int()
    >>> {57736: 7, 59338: 8, 59378: 0, 59622: 2, 59633: 1, 60246: 3, 60639: 5, 60771: 9, 61946: 4, 63654: 6}