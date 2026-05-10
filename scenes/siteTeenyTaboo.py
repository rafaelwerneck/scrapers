import re
import string
import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper
true = True
false = False


class SieTeenyTabooSpider(BaseSceneScraper):
    name = 'TeenyTaboo'
    network = 'Teeny Taboo'
    parent = 'Teeny Taboo'
    site = 'Teeny Taboo'

    start_urls = [
        'https://www.teenytaboo.com',
    ]

    cookies = [{
            "domain": "www.teenytaboo.com",
            "hostOnly": true,
            "httpOnly": false,
            "name": "age_check",
            "path": "/",
            "sameSite": "unspecified",
            "secure": false,
            "session": false,
            "storeId": "0",
            "value": "true"
        }
    ]


    selector_map = {
        'title': '//h1[@class="video-title"]/text()',
        'description': '//div[@class="video-info"]/following-sibling::div[contains(@style, "white")]/p//text()',
        'date': '//div[@class="video-info"]//p[contains(text(), "Added")]/text()',
        're_date': r'(\w{3,4}\s+?\d{1,2}, \d{4})',
        'date_formats': ['%b %d, %Y'],
        'image': '//div[@id="video-player-section"]//img/@src',
        'image_blob': True,
        'duration': '//div[@class="video-info"]//p[contains(text(), "Length")]/text()',
        're_duration': r'((?:\d{1,2}\:)?\d{2}\:\d{2})',
        'performers': '//div[@class="model-tags"]/a[contains(@href, "/model/")]/text()',
        'tags': '//div[@class="model-tags"]/a[contains(@href, "/search/")]/text()',
        'trailer': '',
        'external_id': r'video/(.*?)/',
        'pagination': '/page%s/'
    }

    custom_scraper_settings = {
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        #'CONCURRENT_REQUESTS_PER_IP': 1,
        'SPIDERMON_ENABLED': False,
        'DOWNLOAD_FAIL_ON_DATALOSS': True,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 408, 307, 403],
        'HANDLE_HTTPSTATUS_LIST': [500, 503, 504, 400, 408, 307, 403],
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    async def start(self):
        meta = {}
        meta['page'] = self.page
        meta['playwright'] = True

        for link in self.start_urls:
            yield scrapy.Request(url=self.get_next_page_url(link, self.page), callback=self.parse, meta=meta, cookies=self.cookies)

    def get_scenes(self, response):
        scenes = response.xpath('//div[@class="lv-info"]/h3/a/@href|//div[contains(@class,"video-thumb")]/a/@href').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                url=self.format_link(response, scene)
                yield scrapy.Request(url, callback=self.parse_scene, dont_filter=True, meta=response.meta)
