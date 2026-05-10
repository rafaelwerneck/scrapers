import re
import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper

true = True
false = False


class SiteBrattyMILFSpider(BaseSceneScraper):
    name = "BrattyMILF"
    site = "Bratty MILF"
    parent = "Bratty MILF"
    network = "Nubiles"

    start_urls = [
        "https://brattymilf.com/",
    ]

    # -------------------------
    # Browser Cookies
    # -------------------------
    cookies = [
        {
            "domain": "brattymilf.com",
            "name": "user_viewport_setting",
            "path": "/",
            "value": "mobile",
        },
        {
            "domain": "brattymilf.com",
            "name": "18-plus-modal",
            "path": "/",
            "value": "hidden",
        },
        {
            "domain": ".brattymilf.com",
            "name": "click",
            "path": "/",
            "secure": True,
            "value": "lJWbtcmUa7VsnmTUltZlmcmayuBvmJ2YypqUrJeVlq5r4ZxxyZWX",
        },
    ]

    # -------------------------
    # Scraper Settings
    # -------------------------
    custom_scraper_settings = {

        # REQUIRED for scrapy-playwright
        "TWISTED_REACTOR":
            "twisted.internet.asyncioreactor.AsyncioSelectorReactor",

        "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,

        "RETRY_ENABLED": True,
        "RETRY_TIMES": 10,
        "RETRY_HTTP_CODES": [400, 403, 408, 500, 503, 504],
        "HANDLE_HTTPSTATUS_LIST": [400, 403, 408, 500, 503, 504],

        "DOWNLOAD_FAIL_ON_DATALOSS": True,
        "SPIDERMON_ENABLED": False,

        # Playwright handler
        "DOWNLOAD_HANDLERS": {
            "http":
                "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https":
                "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },

        # ✅ Keep UA consistent with Playwright Chromium
        "PLAYWRIGHT_CONTEXTS": {
            "default": {
                "user_agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/145.0.0.0 Safari/537.36"
                ),
                "viewport": {"width": 1920, "height": 1080},
                "locale": "en-US",
            }
        },

        # Extremely important stability flags on servers
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        },
    }

    # -------------------------
    # Selectors
    # -------------------------
    selector_map = {
        "title": "//h2/text()",
        "description": '//div[contains(@class,"collapse")]/p/text()',
        "date":
            '//span[contains(@class,"date")]/text()',
        "image": '//meta[@property="og:image"]/@content',
        "image_blob": '//meta[@property="og:image"]/@content',
        "performers":
            '//div[@class="content-pane-performers"]/a/text()',
        "tags": '//div[@class="categories"]/a/text()',
        "external_id": r"watch/(\d+)/",
        "trailer": "",
        "pagination": "/video/gallery/%s",
    }

    # -------------------------
    # Start Requests
    # -------------------------
    async def start(self):
        meta = {
            "page": self.page,
            "playwright": True,

            # ✅ inject cookies into browser
            "playwright_context_kwargs": {
                "storage_state": {
                    "cookies": self.cookies
                }
            },
        }

        for link in self.start_urls:
            yield scrapy.Request(
                url=self.get_next_page_url(link, self.page),
                callback=self.parse,
                meta=meta,
                headers=self.headers,
            )

    # -------------------------
    # Scene Listing
    # -------------------------
    def get_scenes(self, response):

        scenes = response.xpath(
            "//figcaption/div/span/a/@href"
        ).getall()

        for scene in scenes:
            if re.search(
                self.get_selector_map("external_id"),
                scene,
            ):
                yield scrapy.Request(
                    url=self.format_link(response, scene),
                    callback=self.parse_scene,
                    meta={"playwright": True},
                )

    # -------------------------
    # Pagination
    # -------------------------
    def get_next_page_url(self, base, page):
        page = str((int(page) - 1) * 12)
        return self.format_url(
            base,
            self.get_selector_map("pagination") % page,
        )