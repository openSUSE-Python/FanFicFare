# -*- coding: utf-8 -*-

# Copyright 2022 FanFicFare team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import absolute_import
import logging
logger = logging.getLogger(__name__)

from .. import exceptions

from .base_fetcher import FetcherResponse
from .decorators import FetcherDecorator
from .log import make_log

class BrowserCacheDecorator(FetcherDecorator):
    def __init__(self,cache):
        super(BrowserCacheDecorator,self).__init__()
        self.cache = cache

    def fetcher_do_request(self,
                           fetcher,
                           chainfn,
                           method,
                           url,
                           parameters=None,
                           referer=None,
                           usecache=True):
        # logger.debug("BrowserCacheDecorator fetcher_do_request")
        if usecache:
            d = self.cache.get_data(url)
            logger.debug(make_log('BrowserCache',method,url,d is not None))
            if d:
                return FetcherResponse(d,redirecturl=url,fromcache=True)
        ## make use_browser_cache true/false/only?
        if fetcher.getConfig("use_browser_cache_only"):
            raise exceptions.HTTPErrorFFF(
                url,
                428, # 404 & 410 trip StoryDoesNotExist
                     # 428 ('Precondition Required') gets the
                     # error_msg through to the user.
                "Page not found or expired in Browser Cache (see FFF setting browser_cache_age_limit)",# error_msg
                None # data
                )
        return chainfn(
            method,
            url,
            parameters=parameters,
            referer=referer,
            usecache=usecache)

