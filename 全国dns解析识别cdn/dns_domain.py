import asyncio
import aiodns
import argparse
from prettytable import PrettyTable


class GetDns(object):

    def parsers(self):
        parser = argparse.ArgumentParser(description='全国dns解析-识别CDN')
        parser.add_argument("-url", '--target', help='输入目标', metavar='')
        parser.add_argument("-f", '--file', help='批量目标', metavar='')
        parser.add_argument("-t", '--time', help='dns超时时间', metavar='', default=0.1)

        args = parser.parse_args()

        return args

    def __init__(self):
        self.start = self.parsers()
        self.dns = {
            '1.2.4.8': 'CNNIC SDNS',
            '108.168.255.118': '上海电信 DNS',
            '112.124.47.27': 'oneDNS',
            '114.114.114.114': '114 DNS',
            '114.114.115.115': '114 DNS',
            '114.215.126.16': 'oneDNS',
            '115.29.189.118': '杭州电信',
            '116.228.111.118': '上海电信 DNS',
            '118.244.224.124': '北方联通',
            '119.29.29.29': '腾讯 DNS',
            '119.6.6.6': '四川联通 DNS',
            '124.161.87.155': '四川联通 DNS',
            '178.79.131.110': 'V2EX DNS',
            '180.153.225.136': '上海电信',
            '180.76.76.76': '百度 DuDNS',
            '199.91.73.222': 'V2EX DNS',
            '202.101.172.35': '浙江电信 DNS',
            '202.101.224.69': '江西电信 DNS',
            '202.101.226.68': '江西电信 DNS',
            '202.102.128.68': '山东联通 DNS',
            '202.102.134.68': '山东联通 DNS',
            '202.102.152.3': '山东联通 DNS',
            '202.102.154.3': '山东联通 DNS',
            '202.102.224.68': '河南联通 DNS',
            '202.102.227.68': '河南联通 DNS',
            '202.103.0.68': '湖北电信 DNS',
            '202.103.224.68': '广西电信 DNS',
            '202.103.225.68': '广西电信 DNS',
            '202.103.24.68': '湖北电信 DNS',
            '202.106.0.20': '北京联通 DNS',
            '202.106.195.68': '北京联通 DNS',
            '202.106.196.115': '北京联通 DNS',
            '202.106.46.151': '北京联通 DNS',
            '202.96.128.166': '广东电信 DNS',
            '202.96.128.68': '广东电信 DNS',
            '202.96.128.86': '广东电信 DNS',
            '202.96.134.33': '广东电信 DNS',
            '202.96.209.133': '上海电信 DNS',
            '202.96.209.5': '上海电信 DNS',
            '202.97.224.68': '黑龙江联通',
            '202.97.224.69': '黑龙江联通',
            '202.98.0.68': '吉林联通 DNS',
            '202.98.192.67': '贵州电信 DNS',
            '202.98.198.167': '贵州电信 DNS',
            '202.98.5.68': '吉林联通 DNS',
            '202.99.104.68': '天津联通 DNS',
            '202.99.160.68': '河北联通 DNS',
            '202.99.166.4': '河北联通 DNS',
            '202.99.192.66': '山西联通 DNS',
            '202.99.192.68': '山西联通 DNS',
            '202.99.224.68': '内蒙古联通',
            '202.99.224.8': '内蒙古联通',
            '202.99.96.68': '天津联通 DNS',
            '203.195.182.150': '广东电信',
            '208.67.220.220': 'OpenDNS',
            '208.67.222.222': 'OpenDNS',
            '210.21.196.6': '广东联通 DNS',
            '210.22.70.3': '上海联通 DNS',
            '210.22.84.3': '上海联通 DNS',
            '218.2.135.1': '江苏电信 DNS',
            '218.2.2.2': '江苏电信 DNS',
            '218.30.19.40': '陕西电信 DNS',
            '218.4.4.4': '江苏电信 DNS',
            '218.6.200.139': '四川电信 DNS',
            '219.146.0.130': '山东电信 DNS',
            '219.146.0.132': '天津电信 DNS',
            '219.147.198.230': '黑龙江电信',
            '219.147.198.242': '黑龙江电信',
            '219.148.162.31': '内蒙古电信',
            '219.150.32.132': '山东电信 DNS',
            '221.11.1.67': '陕西联通 DNS',
            '221.11.1.68': '陕西联通 DNS',
            '221.12.1.227': '浙江联通 DNS',
            '221.12.33.227': '浙江联通 DNS',
            '221.5.203.98': '重庆联通 DNS',
            '221.5.88.88': '广东联通 DNS',
            '221.6.4.66': '江苏联通 DNS',
            '221.6.4.67': '江苏联通 DNS',
            '221.7.92.98': '重庆联通 DNS',
            '222.172.200.68': '云南电信 DNS',
            '222.246.129.80': '湖南电信 DNS',
            '222.74.39.50': '内蒙古电信',
            '222.85.85.85': '河南电信 DNS',
            '222.88.88.88': '河南电信 DNS',
            '223.5.5.5': '阿里 AliDNS',
            '223.6.6.6': '阿里 AliDNS',
            '4.2.2.1': '微软 DNS',
            '4.2.2.2': '微软 DNS',
            '42.120.21.30': 'OpenerDNS',
            '59.51.78.211': '湖南电信 DNS',
            '60.191.244.5': '浙江电信 DNS',
            '61.134.1.4': '陕西电信 DNS',
            '61.139.2.69': '四川电信 DNS',
            '61.147.37.1': '江苏电信 DNS',
            '61.153.177.196': '浙江电信 DNS',
            '61.153.81.75': '浙江电信 DNS',
            '61.166.150.123': '云南电信 DNS',
            '61.178.0.93': '甘肃电信 DNS',
            '8.8.4.4': 'Google DNS',
            '8.8.8.8': 'Google DNS',
            '202.100.64.68': '甘肃电信 DNS',
        }
        self.Dns_to_ip = []
        self.Dns_name = []
        self.DNS_ip = []
        self.key = ''

    async def Table(self):
        x = PrettyTable()
        x.field_names = ["目标域名", "全国dns", "dns服务器IP", "解析IP"]
        for dns, dns_ip, ip in zip(self.Dns_name, self.DNS_ip, self.Dns_to_ip):
            x.add_row([self.key, dns, dns_ip, ip])
        print(x)
        self.Dns_to_ip = []
        self.Dns_name = []
        self.DNS_ip = []

    async def query(self, name, ip):
        resolver = aiodns.DNSResolver(timeout=int(self.start.time), nameservers=[ip])
        dns = self.dns.get(ip)
        try:
            host = await resolver.query(name, 'A')
            if len(host) > 1:
                for ips in host:
                    self.Dns_to_ip.append(ips.host)
                    self.Dns_name.append(dns)
                    self.DNS_ip.append(ip)
            else:
                self.Dns_to_ip.append(host[0].host)
                self.Dns_name.append(dns)
                self.DNS_ip.append(ip)
        except Exception as e:
            pass

    async def file_read(self, name):
        if name:
            with open(name, 'r') as f:
                data = f.read().splitlines()
                return data
        else:
            print('请输入文件名称')

    async def main(self):
        if self.start.target and self.start.file:
            print('请不要单个目标 和文件一起执行')
        elif self.start.target:
            print(f'            {self.start.target} 任务进行')

            data = [asyncio.create_task(self.query(self.start.target, ip)) for ip in self.dns.keys()]
            self.key = self.start.target
            await  asyncio.wait(data)
            await  self.Table()
        elif self.start.file:
            urls = await self.file_read(self.start.file)
            for domain in urls:
                print(f'            {domain} 任务进行')
                tasks = [asyncio.create_task(self.query(domain, ip)) for ip in self.dns.keys()]
                self.key = domain
                await asyncio.wait(tasks)
                await  self.Table()


if __name__ == '__main__':
    data = GetDns()
    asyncio.run(data.main())
