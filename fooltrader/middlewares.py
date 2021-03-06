# -*- coding: utf-8 -*-

import logging

from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpErrorMiddleware, HttpError

from fooltrader.proxy import get_checked_proxy

logger = logging.getLogger(__name__)


# spider middleware
class FoolErrorMiddleware(HttpErrorMiddleware):
    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, HttpError):
            if response.status == 456:
                # response.meta['fool_blocked'] = True
                # return None
                raise CloseSpider('catch forbidden,close for a while')


# downloader middleware
class ForbiddenHandleMiddleware(object):
    forbidden_codes = (456, 403)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_proxy', False):
            return response
        if response.status in self.forbidden_codes:
            # 新浪财经
            if 'sina.com' in request.url:
                proxy_df = get_checked_proxy()
                request.meta['proxy'] = proxy_df.at[random.choice(proxy_df.index), 'url']
                return request
        return response


import random


class RandomProxy(object):
    def process_request(self, request, spider):
        proxy_df = get_checked_proxy()
        request.meta['proxy'] = proxy_df.df.at[random.choice(proxy_df.index), 'url']
