# -*-coding:utf-8 -*-
"""
提供两个requests请求会话池
"""
import asyncio

import aiohttp
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

# from functools import lru_cache

DEFAULT_TIMEOUT = 30
ASYNC_TIMEOUT = aiohttp.ClientTimeout(total=5, connect=None, sock_connect=None, sock_read=None)
SESSION_DEFAULT_NUM_POOLS = 10
SESSION_DEFAULT_POOL_MAXSIZE = 15
DEFAULT_POOLBLOCK = False
RETRY = Retry(
    total=10,
    read=5,
    connect=24,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 503, 504, 520, 524),
    allowed_methods=('HEAD', 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE')
)


# @lru_cache(maxsize=128, typed=False) # 缓存
def gen_retry_session(session=None):
    """自定义连接会话池大小, 支持http 与 https, 支持自定义重连"""
    session = session or requests.Session()
    adapter = HTTPAdapter(
        max_retries=RETRY,  # 失败重试的次数
        pool_connections=SESSION_DEFAULT_NUM_POOLS,  # 连接池的数量
        pool_maxsize=SESSION_DEFAULT_POOL_MAXSIZE,  # 连接池的最大数量
        pool_block=DEFAULT_POOLBLOCK  # 是否超过连接池最大数量进行阻塞
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


# @lru_cache(maxsize=128, typed=False) # 缓存
def gen_default_session():
    return requests.Session()


class AsyncSession:

    @staticmethod
    async def async_get(url, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False, headers=headers, timeout=ASYNC_TIMEOUT) as r:
                print(url, r.status)
                await r.read()

    @staticmethod
    async def async_post(url, json=None, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json, ssl=False, headers=headers, timeout=ASYNC_TIMEOUT) as r:
                # print(url, r.status)
                await r.read()


request_session = gen_default_session()
custom_session = gen_retry_session()

if __name__ == '__main__':
    """异步调用示例"""
    url_1 = "https://baidu.com"
    url_2 = "https://163.com"
    li = [url_1, url_2]


    async def main(url_list: list):
        task_list = [asyncio.create_task(AsyncSession.async_get(url)) for url in url_list]
        await asyncio.gather(*task_list)

        # t1 = asyncio.create_task(AsyncSession.async_get(url_1))
        # t2 = asyncio.create_task(AsyncSession.async_get(url_2))
        # await asyncio.gather(*[t1, t2])


    asyncio.run(main(li))
