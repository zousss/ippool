from scrapy.spiders import CrawlSpider
from ippool.items import IppoolItem
import scrapy
import urllib
import socket
import time

class ipPoolSpider(CrawlSpider):
    name = "ippool"
    start_urls = ["http://www.xicidaili.com/nn"]
    base_url = 'http://www.xicidaili.com/nn/'

    def parse(self, response):
        print response.url
        for site in response.xpath('//*[@id="ip_list"]/tr')[1:]:
            ip = ''.join(site.xpath('td[2]/text()').extract())
            port = ''.join(site.xpath('td[3]/text()').extract())
            type = ''.join(site.xpath('td[6]/text()').extract())
            if self.detect_ip(type,ip,port):
                ippoolItem = IppoolItem()
                ippoolItem['ip'] = ip
                ippoolItem['port'] = port
                ippoolItem['addr'] = ''.join(site.xpath('td[4]/a/text()').extract())
                ippoolItem['type'] = type
                ippoolItem['record_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[0:10]
                yield ippoolItem
        for i in range(2,20):
            page_link = self.base_url+str(i)
            next_page = scrapy.Request(page_link,callback=self.parse)
            yield next_page

    def detect_ip(self,type,ip,port):
        url = 'http://ip.chinaz.com/getip.aspx'
        try:
            proxy_host =type.lower()+'://'+ip+':'+port
            socket.setdefaulttimeout(3)
            response = urllib.urlopen(url,proxies={"http":proxy_host})
            if response.getcode()!=200:
                return False
            else:
                print proxy_host,'success proxy',response.read().split(':')[1].split(',')[0]
                return True
        except Exception,e:
            print proxy_host,'bad proxy',e.message