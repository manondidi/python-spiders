# -*- coding: utf-8 -*-
import datetime
import re

import scrapy
import logging

from items import VideoItem
import time


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili_spider'
    allowed_domains = ['bilibili.com', 'ibilibili.com']
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
            video_item = VideoItem()
            video_item["title"] = video.css('.title::text').extract_first()
            video_item['videoUrl'] = "https:" + video.css('.cover::attr(href)').extract_first()
            video_item['coverUrl'] = "https:" + video.css('.cover img::attr(src)').extract_first()
            video_item['videoDownUrl'] = ""
            video_item['author'] = author
            video_item['createTime'] = self.convert_time(video.css('.time::text').extract_first())
            # yield videoItem
            # yield scrapy.Request(videoItem['videoUrl'].replace('.bilibili.', '.ibilibili.'),
            #                      callback=self.parseDownloadUrl)

            yield scrapy.Request(video_item['videoUrl'].replace('.bilibili.', '.ibilibili.'),
                                 callback=lambda response, video_item=video_item: self.parse_downloadurl(response,
                                                                                                      video_item))

        self.total = 1
        if self.page < self.total:
            self.page += 1
            yield scrapy.Request('https://space.bilibili.com/' + self.uuid + '/video?page=' + str(self.page),
                                 callback=self.parse)

    def parse_downloadurl(self, response, video_item):
        download_url = response.xpath('//video/@src').get()
        video_item['videoDownUrl'] = download_url
        logging.info("downloadUrl:" + download_url)
        yield video_item

    @staticmethod
    def convert_time(timeStr):
        time_str = timeStr.replace("\n", "")
        time_str = time_str.replace(" ", "")
        today = time.localtime()
        if re.match('\d+-\d+-\d+', time_str):
            return time_str
        elif re.match('\d+-\d+', time_str):
            return time.strftime("%Y", today) + "-" + time_str
        elif time_str == '昨天':
            return str(BilibiliSpider.get_yesterday())
        else:
            return time.strftime("%Y-%m-%d", today)

    @staticmethod
    def get_yesterday():
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday
