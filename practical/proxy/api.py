# author: Z.M Z
# 提取代理的api
# 调用方式 /api?sign='testtesttesttest'
# 请使用自己的加密方式

import sanic
from sanic import response
from crawler import redis_conn
app = sanic.Sanic(__name__)

@app.route("/api", methods=['POST', 'GET'])
async def api(request):
    try:
        form = request.args
        signture = form['sign']

        t = redis_conn.all("http_proxy")[:10]
        return response.json(t)
        # return response.redirect("https://www.baobeihuijia.com/index.aspx")
    except:
        return response.redirect("https://www.baobeihuijia.com/index.aspx")

@app.route("/")
def home(request):
    return response.redirect("https://www.baobeihuijia.com/index.aspx")


import pickle
if __name__ == '__main__':
    app.run()