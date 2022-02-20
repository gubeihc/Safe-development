import aiohttp
import asyncio
from lxml import etree
import brotli
import re 
import  json
async def get_aizhan(ip):
    headers = {

        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Cookie": "_csrf=16b2bd859ee90099c4b304fb48f127a82363545940d3c1a86f3a729adf901441a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22CyYa11H_U-MQ6B01kG-vUmT7vdGHRVGQ%22%3B%7D; Hm_lvt_b37205f3f69d03924c5447d020c09192=1645349732; Hm_lpvt_b37205f3f69d03924c5447d020c09192=1645349737",
        "Referer": "https://dns.aizhan.com/",
    }
    url = f'https://dns.aizhan.com/{ip}/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    print(f'当前请求{resp.url}')
                    html = await resp.text()
                    next_list = await parser_aizhan(html)
                    tasks = []
                    for url in next_list:
                        tasks.append(asyncio.create_task(get_aizhan_list(url)))
                    await  asyncio.wait(tasks)
                    # data = [asyncio.create_task(await get_aizhan_list(url) for url in next_list)]
                    # await  asyncio.wait(data)
                else:
                    print(resp.status, resp.url)
    except  Exception as e:
        print(e)


async def get_aizhan_list(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "_csrf=16b2bd859ee90099c4b304fb48f127a82363545940d3c1a86f3a729adf901441a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22CyYa11H_U-MQ6B01kG-vUmT7vdGHRVGQ%22%3B%7D; Hm_lvt_b37205f3f69d03924c5447d020c09192=1645349732; Hm_lpvt_b37205f3f69d03924c5447d020c09192=1645349737",
        "Host": "dns.aizhan.com",
        "Referer": "https://dns.aizhan.com/",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    print(f'当前请求{resp.url}')
                    html = await resp.text()
                    await parser_aizhan(html)
    except  Exception as e:
        print(e)


async def parser_aizhan(text):
    html = etree.HTML(text)
    # 获取 反查询到的url列表
    href_list = html.xpath('//table/tbody/tr/td[@class="domain"]/a/@href')
    # 获取所有下一页链接
    next_list = html.xpath('//div[@class="pager"]/ul/li/a/@href')
    url_href = set()
    for url in next_list:
        if url.startswith('https://dns.aizhan.com/'):
            url_href.add(url)
    await  save(href_list)
    return url_href


async def save(urls):
    with  open('url_result.txt', 'a') as f:
        for url in urls:
            # f.write(url +'\n')
            print(url, '反查询到的域名')


async def get_bugscaner(ip):
    try:
        url=f'http://dns.bugscaner.com/{ip}.html'
        headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "Hm_lvt_28854d93a1a7808d166385b06bf6d551=1645347424",
    "Host": "dns.bugscaner.com",
    "Proxy-Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,headers=headers) as resp:
                if resp.status == 200:
                    print(f'当前请求{resp.url}')
                    text = await resp.text()
                    html = etree.HTML(text)
                    url_list=html.xpath('//div[@class="col-md-12"]/table/tbody/tr/td/a[@rel="nofollow"]/@href')
                    await save(url_list)
                    next_list = ['http://dns.bugscaner.com' + url for url in html.xpath('//div[@class="col-md-12"]/nav/ul/li/a/@href') if url.startswith('/')]
                    # print(next_list)
                    tasks = [asyncio.create_task(get_bugscaner_list(url)) for url in next_list]
                    await asyncio.wait(tasks)
    except  Exception as e:
        print(e)

async def get_bugscaner_list(url):
    try:
        headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "Hm_lvt_28854d93a1a7808d166385b06bf6d551=1645347424",
    "Host": "dns.bugscaner.com",
    "Proxy-Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,headers=headers) as resp:
                if resp.status == 200:
                    print(f'当前请求{resp.url}')
                    text = await resp.text()
                    html = etree.HTML(text)
                    url_list=html.xpath('//div[@class="col-md-12"]/table/tbody/tr/td/a[@rel="nofollow"]/@href')
                    await save(url_list)
    except  Exception as e:
        print(e)

async def get_vieinfo(ip):
    url=f'https://viewdns.info/reverseip/?host={ip}&t=1'
    headers={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "__utmz=126298514.1645347506.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _fbp=fb.1.1645347506404.1534356357; __gads=ID=9b0a30eb383f0ba9-220a3aa7b2d000b3:T=1645347506:RT=1645347506:S=ALNI_MbUqQ4TeqAFqnaQCdnsFg7gFNqcSw; PHPSESSID=usqpe7k5v5vo3aiutsgsbovn60; __utma=126298514.382184739.1645347506.1645347506.1645352387.2; __utmc=126298514; __utmt=1; __utmb=126298514.1.10.1645352387",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,headers=headers) as resp:
                if resp.status == 200:
                    text = await  resp.text()
                    html=etree.HTML(text)
                    #这里有个坑 浏览器自动补全html 内容 自己获取的源码跟浏览器不一致
                    url_list = html.xpath('//table[@border="1"]/tr/td[1]/text()')
                    await  save(url_list[1:])
    except  Exception as e:
        print(e)
async def get_ip138(ip):
    url=f'https://site.ip138.com/{ip}'
    headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "Hm_lvt_d39191a0b09bb1eb023933edaa468cd5=1645347558,1645353021; Hm_lpvt_d39191a0b09bb1eb023933edaa468cd5=1645353025",
    "Host": "site.ip138.com",
    "Referer": f"https://site.ip138.com/{ip}/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}
    async with aiohttp.ClientSession() as session:
        async with session.get(url,headers=headers) as resp:
            if resp.status == 200:
                text=await resp.text()
                html = etree.HTML(text)
                url_list = html.xpath('//ul[@id="list"]/li/a[@target="_blank"]/text()')
                #这里要注意没获取到token 会出现索引异常
                token=re.findall("var _TOKEN = '(.*?)';",text)[0]
                await save(url_list)
                await ip138_list(ip,token)

async def ip138_list(ip,token):
    i=1
    while 1:
        try:
            i = i+1
            url = f'https://site.ip138.com/index/querybyip/?ip={ip}&page={i}&token={token}'
            headers={
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "Hm_lvt_d39191a0b09bb1eb023933edaa468cd5=1645347558,1645353021; Hm_lpvt_d39191a0b09bb1eb023933edaa468cd5=1645353508; international=2",
    "Host": "site.ip138.com",
    "Referer": f"https://site.ip138.com/{ip}/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}
            print(url)
            async with  aiohttp.ClientSession() as session:
                async with session.get(url,headers=headers) as resp:
                    if resp.status == 200:
                        text =json.loads(await resp.text())
                        data=[url['domain']  for url in text['data']]
                        await save(data)
        except  Exception as e:
            break
async def main(ip):
    start =[
        get_ip138(ip),get_vieinfo(ip),get_bugscaner(ip),get_aizhan(ip)
    ]
    await asyncio.wait(start)

if __name__ == '__main__':
    #图形化下次录屏写
    asyncio.run(main('220.181.38.251'))