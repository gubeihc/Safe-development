import asyncio
import aiodns
import re
from loguru import  logger
import  argparse

parser = argparse.ArgumentParser("aws-cname 解析-顾北")
parser.add_argument("-url", '--target', help='输入目标', metavar='')
parser.add_argument("-f", '--file', help='批量目标', metavar='')
parser.add_argument("-t", '--time', help='dns超时时间', metavar='', default=1)
parser.add_argument("-s", '--save', help='保存', metavar='', default="result.txt")
args = parser.parse_args()
result=[]
async def get_dns(name):
    domain_list=set()
    try:
        with open(name,'r')as f:
            data=f.read().splitlines()
            for domain in data:
                if not re.findall(
                        r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
                        domain):
                    if domain.startswith(('http://', 'https://')):
                        key = domain.split('//')[1]
                        domain_list.add(key)
                    else:
                        domain_list.add(domain)
        return domain_list
    except  Exception as e:
        print(e)
async def query(name):
    #dns 查询
    resolver = aiodns.DNSResolver(timeout=args.time,nameservers=['114.114.114.114',"1.1.1.1","8.8.8.8"])
    try:
        host = await resolver.query(name,'CNAME')
        aws_cname = re.findall(".*.amazonaws.com",host.cname)
        if aws_cname:
            logger.info(f" {name}   [*]  {host.cname}")
            log ={
                name:host.cname
            }
            result.append(log)
    except Exception as e:
        pass
async def save(domain_list):
    with  open(args.save,'a') as f:
        for domain in domain_list:
            f.write(str(domain) +'\n')
    logger.info(f"结果保存到{args.save}")
async def main():
    domains=await get_dns(args.file)
    data= [asyncio.create_task(query(domain)) for domain in domains]
    await  asyncio.wait(data)
    await  save(result)
async def start():
    if args.target and args.file:
        print('请不要单个目标 和文件一起执行')
    elif args.target:
        logger.info("解析开始，如果没回显示就代表没解析到aws cname")
        await  query(args.target)
    elif args.file:
        logger.info("解析开始，如果没回显示就代表没解析到aws cname")
        await main()
    elif  not args.target  and not args.file:
        print("请输入目标哦")

if __name__ == '__main__':
    asyncio.run(start())