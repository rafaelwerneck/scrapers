from datetime import datetime
import scrapy
import json
import string
from requests import get
from tpdb.BaseSceneScraper import BaseSceneScraper


class SiteLusterySpider(BaseSceneScraper):
    name = 'Lustery'

    start_urls = ['https://lustery.com']

    selector_map = {
        'external_id': r'',
        'pagination': 'https://lustery.com/api/videos?offset=%s&sort=latest',
    }

    custom_scraper_settings = {
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'AUTOTHROTTLE_ENABLED': True,
        'USE_PROXY': False,
        'COOKIES_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'DOWNLOADER_MIDDLEWARES': {
            # ~ 'tpdb.helpers.scrapy_flare.FlareMiddleware': 542,
            'tpdb.middlewares.TpdbSceneDownloaderMiddleware': 543,
            'tpdb.custommiddlewares.CustomProxyMiddleware': 350,
            # ~ 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # ~ 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            # ~ 'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
        },
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }
    }

    def start_requests(self):
        meta = {}
        meta['page'] = self.page
        meta['playwright'] = True

        start_url = 'https://lustery.com/'
        yield scrapy.Request(start_url, callback=self.start_requests2, meta=meta)

    def start_requests2(self, response):
        ip = get('https://api.ipify.org').content.decode('utf8')
        print('My public IP address is: {}'.format(ip))

        for link in self.start_urls:
            url=self.get_next_page_url(link, self.page)
            yield scrapy.Request(url=url, callback=self.parse, meta=response.meta)    

    def get_next_page_url(self, base, page):
        page = str((int(page) - 1) * 18)
        return self.format_url(base, self.get_selector_map('pagination') % page)

    def get_scenes(self, response):
        meta = response.meta
        json_text = response.xpath("//pre/text()").get()
        jsondata = json.loads(json_text)
        permalinks = jsondata['currentPagePermalinks']
        for permalink in permalinks:
            meta['id'] = permalink
            link = f"https://lustery.com/api/video/{permalink}"
            yield scrapy.Request(link, callback=self.parse_scene, meta=meta)

    def parse_scene(self, response):
        meta = response.meta
        json_text = response.xpath("//pre/text()").get()
        jsondata = json.loads(json_text)
        if "video" in jsondata and jsondata['video']:
            scene = jsondata['video']
            # resources = jsondata['resources']
            item = self.init_scene()

            item['title'] = self.cleanup_title(scene['title'])

            if "poster" in scene and scene['poster']:
                # ~ item['image'] = f"https://static.lustery.com/cdn-cgi/image/format=auto/{scene['poster']['staticPath']}"
                item['image'] = f"https://img.lustery.com/cache/image/resize/width=1600/{scene['poster']['staticPath']}"
                item['image_blob'] = self.get_image_blob_from_link(item['image'])

            item['date'] = datetime.utcfromtimestamp(scene['publishAt']).strftime('%Y-%m-%d')

            item['id'] = meta['id']
            if not scene['series']:
                item['url'] = f"https://lustery.com/video-preview/{meta['id']}"
            else:
                item['url'] = f"https://lustery.com/video/series/{meta['id']}"
            item['site'] = 'Lustery'
            item['tags'] = scene['tags']
            item['duration'] = scene['duration']
            item['parent'] = 'Lustery'
            item['network'] = 'Lustery'

            # for resource in resources:
            #     if "videoInfo" in resources[resource] and resources[resource]['videoInfo']:
            #         item['description'] = resources[resource]['videoInfo']['description']

            if "coupleName" in scene and scene['coupleName']:
                if "&" in scene['coupleName']:
                    coupleName = scene['coupleName'].split("&")
                else:
                    coupleName = [scene['coupleName']]
                for model in coupleName:
                    item['performers'].append(string.capwords(model.strip()))

            yield self.check_item(item, self.days)
