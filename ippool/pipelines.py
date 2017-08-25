# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ippool.items import IppoolItem
from scrapy.conf import settings
import pymysql

class IppoolPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode= True,
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == IppoolItem:
            try:
                sql = 'INSERT INTO ippool VALUES(%s,%s,%s,%s,%s)'
                param = (item['ip'],item['port'],item['addr'],item['type'],item['record_time'])
                self.cursor.execute(sql,param)
                self.connect.commit()
            except pymysql.Warning,w:
                print "Warning:%s" % str(w)
            except pymysql.Error, e:
                print "Error:%s" % str(e)
        return item
