import scrapy
import re
import dateparser
import base64
import requests
from tpdb.BaseSceneScraper import BaseSceneScraper
true = True
false = False


    # This scraper is just to fill in historical scenes from Data18 that don't exist on the "actual" sites
    # any longer.  Obviously data isn't being added, so it's just a one-time scrape for each site


class Data18Spider(BaseSceneScraper):
    name = 'Data182022'

    cookies = [{"domain":".data18.com","expirationDate":1770850491.532554,"hostOnly":false,"httpOnly":true,"name":"data_user","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"UNK-en-1"},{"domain":".data18.com","expirationDate":1770850491.532577,"hostOnly":false,"httpOnly":true,"name":"data_user_functions","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0"},{"domain":".data18.com","hostOnly":false,"httpOnly":true,"name":"data_user_navigation","path":"/","sameSite":"unspecified","secure":true,"session":true,"storeId":"0","value":"1"},{"domain":".data18.com","expirationDate":1767564353.740662,"hostOnly":false,"httpOnly":true,"name":"data_user_captcha","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"1"},{"domain":".data18.com","hostOnly":false,"httpOnly":true,"name":"data_user_nav_custom","path":"/","sameSite":"unspecified","secure":true,"session":true,"storeId":"0","value":"t%3D3%26b%3D1%26html%3Dagw-entertainment"},{"domain":".data18.com","hostOnly":false,"httpOnly":true,"name":"last_media","path":"/","sameSite":"unspecified","secure":true,"session":true,"storeId":"0","value":"scene-1172732"}]

    start_urls = [

        #### Scraped 2022-07-09
        # ~ ['http://www.data18.com', 'https://www.data18.com/sys/page.php?t=3&b=2&o=0&html=haze-her&html2=&total=57&doquery=1&cache=0&spage=%s&dopage=1', 'Haze Her', 'Haze Her', 'Bang Bros', 'https://www.data18.com/studios/haze-her/scenes'],
        # ['http://www.data18.com', 'https://www.data18.com/sys/page.php?t=3&b=1&o=0&html=pornpros_disgraced-18&html2=&total=&doquery=1&spage=%s&dopage=1', 'Disgraced 18', 'Disgraced 18', 'PornPros', 'https://www.data18.com/studios/college-rules/scenes'],
        ['http://www.data18.com', 'https://www.data18.com/sys/page.php?t=3&b=1&o=0&html=agw-entertainment&html2=&total=166&doquery=1&spage=%s&dopage=1', 'AGW Entertainment', 'Angela White', 'Angela White', 'https://www.data18.com/studios/agw-entertainment'],
    ]

    selector_map = {
        'title': '//h1//text()',
        'description': '//b[contains(text(), "Story")]/..//text()',
        'date': '//b[contains(text(), "Release date")]/following-sibling::a/b/text()',
        'date_formats': ['%B %d, %Y'],
        'image': '//img[@id="playpriimage"]/@src',
        'performers': '//a[contains(@href, "/name/") and contains(@class, "bold gen")]/text()',
        'tags': '//b[contains(text(), "Categories")]/following-sibling::a[contains(@href, "tags")]/text()',
        'external_id': r'/(\d+)$',
        'trailer': '//video/source/@src',
    }

    custom_scraper_settings = {
        # 'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'AUTOTHROTTLE_ENABLED': True,
        'USE_PROXY': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        # 'HANDLE_HTTPSTATUS_LIST': [404],
        'DOWNLOADER_MIDDLEWARES': {
            # 'tpdb.helpers.scrapy_flare.FlareMiddleware': 542,
            'tpdb.middlewares.TpdbSceneDownloaderMiddleware': 543,
            'tpdb.custommiddlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
        },
        # 'DOWNLOAD_HANDLERS': {
        #     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        #     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        # },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62',
    }

    def start_requests(self):

        for link in self.start_urls:
            meta = {}
            meta['page'] = self.page
            meta['pagination'] = link[1]
            meta['site'] = link[2]
            meta['parent'] = link[3]
            meta['network'] = link[4]
            # meta['playwright'] = True
            yield scrapy.Request(url=self.get_next_page_url(link[0], self.page, link[1]),
                                 callback=self.parse,
                                 meta=meta,
                                 headers={'Referer': link[5]},
                                 cookies=self.cookies)

    def parse(self, response, **kwargs):
        scenes = self.get_scenes(response)
        count = 0
        for scene in scenes:
            count += 1
            yield scene

        if count:
            if 'page' in response.meta and response.meta['page'] < self.limit_pages:
                meta = response.meta
                meta['page'] = meta['page'] + 1
                print('NEXT PAGE: ' + str(meta['page']))
                yield scrapy.Request(url=self.get_next_page_url(response.url, meta['page'], meta['pagination']),
                                     callback=self.parse,
                                     meta=meta,
                                     headers=self.headers,
                                     cookies=self.cookies)

    def get_next_page_url(self, base, page, pagination):
        return self.format_url(base, pagination % page)

    def get_scenes(self, response):
        meta = response.meta
        scenes = response.xpath('//div[contains(@style, "margin-top")]/div/a[contains(@href, "scenes")]/@href').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                url = self.format_link(response, scene)
                yield scrapy.Request(url, callback=self.parse_scene, meta=meta)

    def get_title(self, response):
        title = super().get_title(response)
        title = title.replace("- ", "")
        return title

    def get_description(self, response):
        description = super().get_description(response)
        description = description.replace("Story - ", "")
        return description

    def get_image(self, response):
        image = super().get_image(response)
        if not image or image in response.url:
            return ""
        return image
    
    def get_date(self, response):
        date = super().get_date(response)
        if not date:
            scenedate = response.xpath('//b[contains(text(), "Release date")]/following-sibling::text()')
            if scenedate:
                scenedate = scenedate.get().strip()
                scenedate = re.search(r'(\w+, \d{4})', scenedate)
                if scenedate:
                    scenedate = scenedate.group(1)
                    scenedate = scenedate.replace(", ", " 1, ")
                    date = dateparser.parse(scenedate.strip()).strftime('%Y-%m-%d')
        return date