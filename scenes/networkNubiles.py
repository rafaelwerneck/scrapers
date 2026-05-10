import re
import json
import hashlib
import requests
from requests import get
from datetime import date, timedelta, datetime
import dateparser
import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper
true = True
false = False


class NubilesSpider(BaseSceneScraper):
    name = 'Nubiles'
    network = 'nubiles'

    # Must match the UA that Scrapy actually sends (forced by TpdbSceneDownloaderMiddleware).
    # Server binds the PoW-verified session to this UA — mismatch → 429.
    USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 '
                  'Edg/107.0.1418.62')

    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Ch-Ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
    }

    custom_scraper_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'DOWNLOADER_MIDDLEWARES': {
            'tpdb.middlewares.TpdbSceneDownloaderMiddleware': 543,
            # Disabled — sends Scrapy requests through a different IP than
            # get_verified_cookies() used to solve the PoW, invalidating the session.
            # 'tpdb.custommiddlewares.CustomProxyMiddleware': 350,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        },
    }

    cookies = [{
                "hostOnly": true,
                "httpOnly": false,
                "name": "18-plus-modal",
                "path": "/",
                "sameSite": "unspecified",
                "secure": false,
                "session": false,
                "storeId": "0",
                "value": "hidden"
            }
        ]

    start_urls = [
        "https://anilos.com",
        "https://badteenspunished.com",
        "https://bountyhunterporn.com",
        "https://brattysis.com",
        "https://cheatingsis.com",
        "https://cumswappingsis.com",
        "https://daddyslilangel.com",
        "https://datingmystepson.com",
        "https://deeplush.com",
        "https://detentiongirls.com",
        "https://doublepies.com",
        "https://driverxxx.com",
        "https://familyswap.xxx",
        "https://hotcrazymess.com",
        "https://momlover.com",
        "https://momsteachsex.com",
        "https://myfamilypies.com",
        "https://nfbusty.com",
        "https://nubilefilms.com",
        "https://nubiles-casting.com",
        "https://nubiles-porn.com",
        "https://nubiles.net",
        "https://nubileset.com",
        "https://nubilesunscripted.com",
        "https://petitehdporn.com",
        "https://petiteballerinasfucked.com",
        "https://princesscum.com",
        "https://realitysis.com",
        "https://stepsiblingscaught.com",
        "https://teacherfucksteens.com",
        "https://thatsitcomshow.com",
        "https://thepovgod.com",
    ]

    selector_map = {
        'title': '//*[contains(@class, "content-pane-title")]/h2/text()',
        'description': '//div[contains(@class, "content-pane-description")]/p/text()',
        'date': '//span[@class="date"]/text()',
        'image': '//video/@poster|//img[@class="fake-video-player-cover"]/@src',
        'performers': '//a[@class="content-pane-performer model"]/text()',
        'tags': '//*[@class="categories"]//a/text()',
        'external_id': '(\\d+)',
        'trailer': '//div[contains(@class,"video-container")]//source[contains(@src, ".mp4") and contains(@src,"1280")]/@src|//div[contains(@class,"video-container")]//source[contains(@src, ".mp4") and contains(@src,"960")]/@src|//div[contains(@class,"video-container")]//source[contains(@src, ".mp4") and contains(@src,"640")]/@src|//meta[@property="og:video"]/@content',
        'pagination': '/video/gallery/%s'
    }

    async def start(self):
        ip = get('https://api.ipify.org').content.decode('utf8')
        print('My public IP address is: {}'.format(ip))

        for link in self.start_urls:
            verified_cookies = self.get_verified_cookies(link)
            if verified_cookies is None:
                self.logger.error(f"Could not solve PoW captcha for {link}, skipping")
                continue

            cookies = {'18-plus-modal': 'hidden'}
            cookies.update(verified_cookies)

            meta = {'page': self.page}
            yield scrapy.Request(
                url=self.get_next_page_url(link, self.page),
                callback=self.parse,
                meta=meta,
                headers=self.headers,
                cookies=cookies,
            )

    @staticmethod
    def _solve_pow(challenge, difficulty):
        """Find a nonce such that SHA-256(challenge + ':' + nonce) has `difficulty` leading zero bits."""
        target = 1 << (256 - difficulty)
        nonce = 0
        while True:
            h = hashlib.sha256(f"{challenge}:{nonce}".encode()).digest()
            if int.from_bytes(h, 'big') < target:
                return nonce
            nonce += 1

    def get_verified_cookies(self, base_url):
        """Solve the homegrown PoW captcha and return a dict of verified session cookies.

        Returns None on failure. Returns an empty dict if the site doesn't actually
        present the captcha (already accessible).
        """
        base = base_url.rstrip('/')
        gallery_url = base + '/video/gallery'

        session = requests.Session()
        session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        })

        try:
            r = session.get(gallery_url, timeout=15)
        except requests.RequestException as e:
            self.logger.warning(f"get_verified_cookies: GET {gallery_url} failed: {e}")
            return None

        if r.status_code == 429:
            self.logger.warning(f"get_verified_cookies: rate-limited on {gallery_url}")
            return None

        m = re.search(r"var\s+turnstileConfig\s*=\s*(\{.*?\});", r.text)
        if not m:
            return dict(session.cookies)

        try:
            config = json.loads(m.group(1))
            nonce = self._solve_pow(config['challenge'], config['difficulty'])
        except Exception as e:
            self.logger.warning(f"get_verified_cookies: PoW solve failed for {base}: {e}")
            return None

        verify_url = base + '/turnstile/verify'
        payload = {
            'nonce': str(nonce),
            'timestamp': config['timestamp'],
            'difficulty': config['difficulty'],
            'environmentChecks': {
                'screenWidth': 1920,
                'screenHeight': 1080,
                'hasCanvas': True,
                'hasWebGL': True,
                'colorDepth': 24,
                'timezoneOffset': 300,
                'languages': 'en-US,en',
                'platform': 'Win32',
                'cookieEnabled': True,
            },
            'returnTo': config['returnTo'],
        }

        try:
            vr = session.post(
                verify_url,
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'Referer': gallery_url,
                    'Origin': base,
                },
                timeout=15,
            )
        except requests.RequestException as e:
            self.logger.warning(f"get_verified_cookies: POST {verify_url} failed: {e}")
            return None

        if vr.status_code != 200:
            self.logger.warning(f"get_verified_cookies: verify POST returned {vr.status_code} for {base}")
            return None

        try:
            result = vr.json()
        except ValueError:
            self.logger.warning(f"get_verified_cookies: non-JSON verify response for {base}")
            return None

        if not result.get('success'):
            self.logger.warning(f"get_verified_cookies: verify failed for {base}: {result}")
            return None

        self.logger.info(f"get_verified_cookies: solved PoW for {base} (nonce={nonce})")
        return dict(session.cookies)

    def get_scenes(self, response):
        # print(response.text)
        scenes = response.xpath('//figcaption')
        for scene in scenes:
            link = scene.xpath('./div/span/a/@href').get()
            if re.search(r'video/watch', link) is not None:
                scenedate = scene.xpath('.//span[@class="date"]/text()').get()
                meta = {
                    'title': scene.xpath('./div/span/a/text()').get().strip(),
                    'date': dateparser.parse(scenedate, date_formats=['%b %d, %Y']).strftime('%Y-%m-%d'),
                }
                if "brattysis" in response.url:
                    meta['site'] = "Bratty Sis"
                    meta['parent'] = "Bratty Sis"
                if "cheatingsis" in response.url:
                    meta['site'] = "Cheating Sis"
                    meta['parent'] = "Cheating Sis"
                if "cumswappingsis" in response.url:
                    meta['site'] = "Cum Swapping Sis"
                    meta['parent'] = "Cum Swapping Sis"
                elif "anilos" in response.url:
                    meta['site'] = "Anilos"
                    meta['parent'] = "Anilos"
                elif "deeplush" in response.url:
                    meta['site'] = "Deep Lush"
                    meta['parent'] = "Deep Lush"
                elif "doublepies" in response.url:
                    meta['site'] = "Double Pies"
                    meta['parent'] = "Momlover"
                elif "hotcrazymess" in response.url:
                    meta['site'] = "Hot Crazy Mess"
                    meta['parent'] = "Hot Crazy Mess"
                elif "nfbusty" in response.url:
                    meta['site'] = "NF Busty"
                    meta['parent'] = "NF Busty"
                elif "nubiles.net" in response.url:
                    meta['site'] = "Nubiles"
                    meta['parent'] = "Nubiles"
                elif "thepovgod" in response.url:
                    meta['site'] = "The POV God"
                    meta['parent'] = "The POV God"
                if 'site' not in meta or not meta['site']:
                    meta['site'] = scene.xpath('.//a[@class="site-link"]/text()').get()
                    meta['parent'] = scene.xpath('.//a[@class="site-link"]/text()').get()
                url=self.format_link(response, link)
                if self.check_item(meta, self.days):
                    yield scrapy.Request(url,callback=self.parse_scene, meta=meta)

    def get_next_page_url(self, base, page):
        if "nubiles.net" in base and page == 1:
            return "https://nubiles.net/video/gallery"
        if "doublepies.com" in base and page == 1:
            return "https://doublepies.com/video/gallery"
        page = ((page - 1) * 12)
        return self.format_url(base, self.get_selector_map('pagination') % page)

    def get_description(self, response):
        if 'description' not in self.get_selector_map():
            return ''
        descriptionxpath = self.process_xpath(response, self.get_selector_map('description'))
        description = ''
        if descriptionxpath:
            descriptionxpath = descriptionxpath.getall()
            for descrow in descriptionxpath:
                descrow = descrow.replace("\n", "").replace("\r", "").replace("\t", "").strip()
                if descrow:
                    description = description + descrow

        if not description or (description and not description.strip()):
            description = response.xpath('//div[@class="col-12 content-pane-column"]/div//text()[not(contains(., "Show More")) and not(contains(., "Show Less"))]')
            description = description.getall()
            if description:
                description = " ".join(description)
        if description:
            return description.replace('Description:', '').strip()
        return ""

    def get_trailer(self, response, path=None):
        if 'trailer' in self.get_selector_map():
            trailer = self.get_element(response, 'trailer', 're_trailer')
            if type(trailer) is list:
                trailer = trailer[-1]
            if trailer:
                if path:
                    return self.format_url(path, trailer)
                else:
                    return self.format_link(response, trailer)

        return ''
    
    def get_performers(self, response):
        perf_list = response.xpath('//a[@class="content-pane-performer model"]')
        performers = []
        if perf_list:
            for performer in perf_list:
                perf_name = performer.xpath('./text()').get()
                perf_url = performer.xpath('./@href').get()
                perf_id = re.search(r'profile/(\d+)/', perf_url)
                if perf_id:
                    perf_id = perf_id.group(1)

                if " " not in perf_name and perf_id:
                    perf_name = perf_name + " " + perf_id
                performers.append(perf_name.strip())
        return performers