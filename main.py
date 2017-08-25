import os
import time

while 1:
    for h in range(24):
        cur_time = time.localtime(time.time())
        if h == cur_time.tm_hour and cur_time.tm_min == 15 and cur_time.tm_sec == 0:
            print "***current time is %s,spider start!***" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            os.system('scrapy crawl ippool')
            print "***current time is %s,spider waiting!***" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            time.sleep(3500)