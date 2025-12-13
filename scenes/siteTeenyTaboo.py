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

    # ~ cookies = [{"name": "warn", "value": "true"}]
    cookies = [{"domain":"teenytaboo.com","hostOnly":true,"httpOnly":false,"name":"PHPSESSID","path":"/","sameSite":"lax","secure":true,"session":true,"storeId":"0","value":"0htiftg2inhvda6js3gkt6b93o"},{"domain":"teenytaboo.com","expirationDate":1767716489,"hostOnly":true,"httpOnly":false,"name":"warn","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"true"},{"domain":"teenytaboo.com","hostOnly":true,"httpOnly":true,"name":"e1n3md44JfuLO8Ar","path":"/","sameSite":"lax","secure":true,"session":true,"storeId":"0","value":"AQAAMqGLg3EZO6N13I0lsy8Ju7yWjuPZ8J6z7s9tL63FyqnzqDVpAAAAAADgAQDpqbkVY2H11WMHqvEPfWx6fQEA7-3JFxl0hs0Q_rhKiVdymA_jC5_pVUTe3EKnIK7fqCxqw8-9gtWhsmcmM526HVjwz0N99t3muDltocMVP9sSE7T_ANBKUKhukBb6DDWWF3cIASBG94Bywba-gP0i_uxyMrp5kau8sEOmD77qdHHvDoz6O-6FCrswPL9FE80GbPpHuiPL1JQCkNPrpzlTmnIRcB8T4ueYgBOeLHx6BRXrfpbwe_W1p1B8U1dDuOu3Xx8o_337jd_aASXszI5i4QosbmIkjUQvt6_tsU4VvI2J9y3KDoAn1Mh7rKDUcJ3o72Pgw6wM5K3UORUg5HYaRwKjUvX_IE98T4-XMuyHvjyn_Ea9GLp2Gb3Z-uJtpZTEKZPZvp0C1aTdIB2eKfIopkmTT8aSMV-5xnvCP9zXIRS7L_YtNdG_zPSkWbN_7Yv8nTAytZIkMIPb12-aRAIZLKc896zugKuF1r10QMsyqOhcfB-YPHRpmmcfl3byqutdT7h20p7Jhq_lSB"}]

    selector_map = {
        'title': '//h1[contains(@class, "customhcolor")]/text()',
        'description': '//h2[contains(@class, "customhcolor")]/p/text()',
        'date': '//span[@class="date"]/text()',
        'date_formats': ['%B %d %Y'],
        'image': '//center/img/@src',
        'image_blob': True,
        'performers': '//h3[contains(@class, "customhcolor")]/a/text()',
        'tags': '',
        'trailer': '',
        'external_id': r'video/(.*?)/',
        'pagination': '/page%s'
    }

    custom_scraper_settings = {
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        # ~ 'AUTOTHROTTLE_ENABLED': True,
        # ~ 'AUTOTHROTTLE_START_DELAY': 1,
        # ~ 'AUTOTHROTTLE_MAX_DELAY': 120,
        'CONCURRENT_REQUESTS': 1,
        # 'DOWNLOAD_DELAY': 60,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
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
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 300,
            'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 301,
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 100,
        }
    }

    def start_requests(self):
        meta = {}
        meta['page'] = self.page
        meta['playwright'] = True

        for link in self.start_urls:
            yield scrapy.Request(url=self.get_next_page_url(link, self.page), callback=self.parse, meta=meta)

    def get_scenes(self, response):
        scenes = response.xpath('//div[contains(@class,"videoimg_wrapper")]/a/@href').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                url=self.format_link(response, scene)
                yield scrapy.Request(url, callback=self.parse_scene)

    def get_title(self, response):
        title = super().get_title(response)
        return string.capwords(title.replace("-", " "))

    def get_tags(self, response):
        tags = response.xpath('//h4[contains(@class, "customhcolor")]/text()')
        if tags:
            tags = tags.get().split(",")
            return list(map(lambda x: string.capwords(x.strip()), tags))
        return []
