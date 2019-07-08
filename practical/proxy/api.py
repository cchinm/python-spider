# author: Z.M Z
# 提取代理的api
# 调用方式 /api?sign='testtesttesttest'
# 请使用自己的加密方式

import sanic
from sanic import response
from practical.proxy.crawler import redis_conn
app = sanic.Sanic(__name__)

@app.route("/api", methods=['POST', 'GET'])
async def api(request):
    try:
        form = request.args
        signture = form['sign']
        # 判断是否符合规则
        if signture == 'testtesttesttest':
            t = redis_conn.zscan("http_proxy")
            return response.json(t)
        return response.redirect("https://www.baobeihuijia.com/index.aspx")
    except:
        return response.redirect("https://www.baobeihuijia.com/index.aspx")

@app.route("/")
def home(request):
    return response.redirect("https://www.baobeihuijia.com/index.aspx")

if __name__ == '__main__':
    app.run()