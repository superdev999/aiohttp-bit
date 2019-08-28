import os
import logging
import yaml
import weakref
from aiohttp import web, BasicAuth, ClientSession, WSMsgType, WSCloseCode
import asyncio
import uvloop
import json

from logger import init_logger


async def api_handler(request):
    print("api_handler")
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def on_shutdown(app):
    print("on_shutdown")
    for ws in set(app['websockets']):
        await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')


class BitcoinRpcClient(object):
    def __init__(self, app=None):
        self.logger = init_logger('test.aiohttp.bitcoin.rpcclient', log_level=logging.DEBUG, propagate=False)

        self.app = app
        config = app['config']
        customer_records = config.get('customer_records')[0]
        login = customer_records.get('bitcoin_rpc_username')
        password = customer_records.get('bitcoin_rpc_password')
        self.url = "http://{0}".format(customer_records.get('bitcoin_rpc_address'))
        self.auth = BasicAuth(login=login, password=password)

    async def getnewaddress(self):
        print("bitcoin_rpc_client getnewaddress")
        try:
            async with ClientSession(auth=self.auth) as session:
                async with session.post(self.url,
                                        data=json.dumps({"jsonrpc":"2.0","method":"getnewaddress","params":[]}),
                                        timeout=30) as resp:
                    return await resp.read()
        except Exception as err:
            self.logger.error(err)

    async def getnetworkinfo(self):
        print("bitcoin_rpc_client getnetworkinfo")
        try:
            async with ClientSession(auth=self.auth) as session:
                async with session.post(self.url,
                                        data=json.dumps({"jsonrpc":"2.0","method":"getnetworkinfo","params":[]}),
                                        timeout=30) as resp:
                    return await resp.json()
        except Exception as err:
            self.logger.error(err)

    async def getwalletinfo(self):
        print("bitcoin_rpc_client getwalletinfo")
        try:
            async with ClientSession(auth=self.auth) as session:
                async with session.post(self.url,
                                        data=json.dumps({"jsonrpc":"2.0","method":"getwalletinfo","params":[]}),
                                        timeout=30) as resp:
                    return await resp.json()
        except Exception as err:
            self.logger.error(err)


async def bitcoin_rpc_getnetworkinfo(app):
    rpc = BitcoinRpcClient(app)
    try:
        while True:
            getnetworkinfo = await rpc.getnetworkinfo()
            getnetworkinfo = getnetworkinfo.get('result')
            getnetworkinfo = {"network": getnetworkinfo}
            getnetworkinfo = json.dumps(getnetworkinfo)
            await app['queue'].put(getnetworkinfo)
            await app['queue'].put(getnetworkinfo)
            await asyncio.sleep(20)
    except asyncio.CancelledError:
        print("bitcoin_rpc_getnetworkinfo CancelledError")
    finally:
        print("bitcoin_rpc_getnetworkinfo finally")


async def bitcoin_rpc_getwalletinfo(app):
    rpc = BitcoinRpcClient(app)
    try:
        while True:
            getwalletinfo = await rpc.getwalletinfo()
            wallet = getwalletinfo.get('result')
            wallet = {"wallet": wallet}
            wallet = json.dumps(wallet)
            await app['queue'].put(wallet)
            await asyncio.sleep(20)
    except asyncio.CancelledError:
        print("bitcoin_rpc_getwalletinfo CancelledError")
    finally:
        print("bitcoin_rpc_getwalletinfo finally")


async def queue_sender(app):
    while True:
        item = await app['queue'].get()
        if item is None:
            app['queue'].task_done()
        else:
            for ws in set(app['websockets']):
                await ws.send_str(item)

async def start_background_tasks(app):
    app['bitcoin_rpc_getwalletinfo'] = asyncio.create_task(bitcoin_rpc_getwalletinfo(app))
    app['bitcoin_rpc_getnetworkinfo'] = asyncio.create_task(bitcoin_rpc_getnetworkinfo(app))
    app['queue_sender'] = asyncio.create_task(queue_sender(app))


async def cleanup_background_tasks(app):
    app['bitcoin_rpc_getwalletinfo'].cancel()
    await app['bitcoin_rpc_getwalletinfo']
    app['bitcoin_rpc_getnetworkinfo'].cancel()
    await app['bitcoin_rpc_getnetworkinfo']
    app['queue_sender'].cancel()
    await app['queue_sender']


class WebSocket(web.View):
    async def get(self):
        self.logger = init_logger('test.aiohttp.bitcoin.ws', log_level=logging.DEBUG, propagate=False)
        self.logger.debug("get WebSocket")
        self.status = True

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].add(ws)

        while self.status:
            msg = await ws.receive()
            if msg.type == WSMsgType.close:
                self.logger.debug('Close ws')
                await ws.close()
                self.status = False
                break
            elif msg.type == 1:
                self.logger.debug('send str')
                self.logger.debug(msg)
                await ws.send_str(msg.data)
            elif msg.type == WSMsgType.error:
                self.logger.debug('ws connection closed with exception %s' % ws.exception())
                break

        self.request.app['websockets'].remove(ws)
        self.logger.debug('websocket connection closed')

        return ws


async def index_handle(request):
    static_index = os.path.join(os.getcwd(), 'static', 'index.html')
    return web.FileResponse(static_index)


def main():
    logger = init_logger('test.aiohttp.bitcoin', log_level=logging.DEBUG, propagate=False)
    logger.info("start test aiohttp server.")

    profile_file = os.path.join(os.getcwd(), 'config.yml')
    with open(profile_file) as stream:
        config = yaml.load(stream)
    static_path = os.path.join(os.getcwd(), 'static')

    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    app = web.Application()
    app.router.add_get('/', index_handle)
    app.router.add_static('/css', os.path.join(static_path, "css"))
    app.router.add_static('/js', os.path.join(static_path, "js"))
    app.router.add_static('/fonts', os.path.join(static_path, "fonts"))
    app.router.add_static('/statics', os.path.join(static_path, "statics"))
    app.router.add_route('GET', '/api', api_handler)
    app.router.add_route('GET', '/ws', WebSocket, name='chat')

    app['websockets'] = weakref.WeakSet()
    app['queue'] = asyncio.Queue()
    app['config'] = config

    app.on_shutdown.append(on_shutdown)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app)


if __name__ == "__main__":
    main()
