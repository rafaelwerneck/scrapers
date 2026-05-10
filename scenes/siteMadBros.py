import json
import string
from typing import Optional
import pycountry
import scrapy

from tpdb.BaseSceneScraper import BaseSceneScraper


class SiteMadBrosSpider(BaseSceneScraper):
    name = 'MadBros'
    site = 'MadBros'
    parent = 'MadBros'
    network = 'MadBros'

    allowed_domains = [
        "api.madbrosx.com",
        "madbrosx.com",
        "iframe.mediadelivery.net",
    ]

    start_urls = [
        'https://api.madbrosx.com'
    ]

    selector_map = {
        'type': 'Scene',
        'external_id': r'.*/(.*?)/$',
        'pagination': '/user/assets/videos/search?limit=12&offset=%s&sortBy=newest',
    }

    def get_next_page_url(self, base, page):
        page = str((int(page) - 1) * 12)
        return self.format_url(base, self.get_selector_map('pagination') % page)

    def get_scenes(self, response):
        jsondata = json.loads(response.text)
        jsondata = jsondata['data']['data']

        for scene in jsondata:
            item = self.init_scene()
            item['title'] = string.capwords(scene['title'].strip())
            item['description'] = scene['description'].strip()
            item['date'] = self.parse_date(scene['createdAt']).isoformat()
            item['id'] = scene['_id']
            item['url'] = f"https://madbrosx.com/video/{scene['slug']}/"

            # ---- fallback image (used only if iframe fails) ----
            fallback_image = None
            if scene.get('thumbnailNsfw') and scene['thumbnailNsfw'].get('url'):
                fallback_image = self.format_link(
                    response,
                    scene['thumbnailNsfw']['url']
                ).replace(" ", "%20")

            item['image'] = fallback_image
            item['image_blob'] = self.get_image_blob_from_link(item['image']) if item['image'] else None

            item['tags'] = []
            for tag in (scene.get('categories') or []):
                item['tags'].append(tag['name'])

            item['performers'] = []
            if scene.get('performers'):
                item['performers'], item['performers_data'] = self.parse_model(scene['performers'])

            if scene.get('duration'):
                item['duration'] = scene['duration']

            item['site'] = "MadBros"
            item['parent'] = "MadBros"
            item['network'] = "MadBros"
            item['type'] = 'Scene'

            # ---- iframe request using bunnyTeaserId ----
            bunny_id = scene.get("bunnyTeaserId")
            if bunny_id:
                iframe_url = f"https://iframe.mediadelivery.net/embed/271231/{bunny_id}"

                yield scrapy.Request(
                    url=iframe_url,
                    callback=self.parse_iframe_image,
                    errback=self.iframe_errback,
                    meta={"item": item},
                    dont_filter=True,
                    headers={
                        "User-Agent": "Mozilla/5.0",
                        "Referer": item["url"],
                    }
                )
            else:
                # no iframe available → yield item as-is
                yield self.check_item(item, self.days)

    def parse_iframe_image(self, response):
        item = response.meta["item"]

        og_image = response.xpath(
            '//meta[@property="og:image"]/@content'
        ).get()

        if og_image:
            item['image'] = og_image

        yield self.check_item(item, self.days)

    def iframe_errback(self, failure):
        request = failure.request
        item = request.meta["item"]

        self.logger.debug(
            f"iframe fetch failed: {failure.value} url={request.url}"
        )

        yield self.check_item(item, self.days)

    def parse_model(self, scene_performers):
        performers = []
        performers_data = []

        for performer in scene_performers:
            performers.append(performer['name'])

            perf = {
                "name": performer['name'],
                "image": performer['avatar'],
                "gender": "Female",
                "site": "MadBros",
                "extra": {
                    "birthplace": self.get_country(performer['country']),
                    "gender": "Female"
                },
                "url": f"https://madbrosx.com/model/{performer['_id']}",
            }

            performers_data.append(perf)

        return performers, performers_data

    def get_country(self, code: str) -> Optional[str]:
        country = pycountry.countries.get(alpha_2=code.upper())
        return country.name if country else None
