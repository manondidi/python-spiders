# -*- coding: utf-8 -*-
import datetime
import re

import scrapy
import logging

from items import VideoItem
import time


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili_spider'
    allowed_domains = ['bilibili.com']
    page = 1
    uuid = '24738601'
    # uuid = '6265316'
    start_urls = ['https://space.bilibili.com/' + uuid + '/video?page=' + str(page)]
    total = 0

    def parse(self, response):
        videos = response.xpath('//div[@id="submit-video-list"]').css('.cube-list li')
        author = response.xpath('//span[@id = "h-name"]/text()').get()
        self.total = int(re.sub("\D", "", response.css('.be-pager-total::text').get()))
        for video in videos:
            videoItem = VideoItem()
            videoItem["title"] = video.css('.title::text').extract_first()
            videoItem['videoUrl'] = "https" + video.css('.cover::attr(href)').extract_first()
            videoItem['coverUrl'] = "https:" + video.css('.cover img::attr(src)').extract_first()
            videoItem['videoDownUrl'] = ""
            videoItem['author'] = author
            videoItem['createTime'] = self.convertTime(video.css('.time::text').extract_first())
            yield videoItem
        # self.total = 3
        if self.page < self.total:
            self.page += 1
            yield scrapy.Request('https://space.bilibili.com/' + self.uuid + '/video?page=' + str(self.page),
                                 callback=self.parse)

    @staticmethod
    def convertTime(timeStr):
        time_str = timeStr.replace("\n", "")
        time_str = time_str.replace(" ", "")
        today = time.localtime()
        logging.info("time_str:" + time_str)
        if re.match('\d+-\d+-\d+', time_str):
            return time_str
        elif re.match('\d+-\d+', time_str):
            return time.strftime("%Y", today) + "-" + time_str
        elif time_str == '昨天':
            return str(BilibiliSpider.getYesterday())
        else:
            return time.strftime("%Y-%m-%d", today)

    @staticmethod
    def getYesterday():
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday
