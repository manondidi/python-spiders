# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BilibiliSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class UserAgentMiddleware(object):
#     def __init__(self):
#         self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
#
#     def process_request(self, request, spider):
#         request.headers['USER_AGENT'] = self.user_agent


class CookieMiddleware(object):
    def __init__(self):
        self.cookie = "LIVE_BUVID=AUTO9615542641675756; stardustvideo=1; CURRENT_FNVAL=16; fts=1554972978; sid=bt825k8g; _uuid=95E234BB-537C-515B-BD01-6331027FA30B20325infoc; UM_distinctid=16a48a4d0c2ff-0df2e74d275006-36697e04-13c680-16a48a4d0c32fb; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1555997744; rpdid=|(JYYu~~JY~Y0J'ullY|~|Yk~; CURRENT_QUALITY=80; finger=1e7fd4f8; im_notify_type_317494753=0; DedeUserID=317494753; DedeUserID__ckMd5=5f10400728746233; SESSDATA=57a654e7%2C1561194311%2Ce48ade51; bili_jct=2d29eb554ca1be97662a985ecd7b4f7e; buvid3=8FC78551-210B-4C63-8E7D-B4BC224EB9FD40781infoc; bp_t_offset_317494753=264036108118042828; _dfcaptcha=f868a0c3c3ee72294fbc94916761d315; CNZZDATA2724999=cnzz_eid%3D1507791915-1555995996-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1560330459"

    def process_request(self, request, spider):
        request.headers['Cookie'] = self.cookie


class SeleniumMiddleware(object):
    def __init__(self):
        self.browser = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.browser, 5000)

    def __del__(self):
        self.browser.quit()

    def process_request(self, request, spider):
        if request.url.find('https://space.bilibili.com') != -1:
            self.browser.get(request.url)
            video_cell = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#submit-video-list>.clearfix.cube-list>li')))
            html = self.browser.page_source
            return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')
