import re
import string
import requests
import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper


class SiteKingBreedersSpider(BaseSceneScraper):
    name = 'KingBreeders'
    network = 'CarnalPlus'
    site = 'King Breeders'

    start_urls = [
        'https://kingbreeders.net',
    ]

    selector_map = {
        'title': '//h2/text()',
        'description': '//div[@id="header-inside"]//p[strong[contains(., "Description:")]]//text()[not(contains(., "Description:")) and not(contains(., "...")) and not(contains(., "Read more"))]',
        'date': '//div[@id="title-single"]/span[1]/img/following-sibling::text()',
        'image': '//video/@poster',
        'performers': '//div[@id="title-single"]//strong[contains(text(), "Starring")]/following-sibling::a/text()',
        'external_id': r'',
        'pagination': '',
        'type': 'Scene',
    }

    async def start(self):
        ip = requests.get('https://api.ipify.org').content.decode('utf8')
        print('My public IP address is: {}'.format(ip))

        meta = {}

        singleurl = self.settings.get('url')
        if singleurl:
            yield scrapy.Request(singleurl, callback=self.parse_scene, meta=meta, headers=self.headers, cookies=self.cookies)
        else:
            for link in self.start_urls:
                yield scrapy.Request('https://kingbreeders.net', callback=self.get_scenes, meta=meta, headers=self.headers, cookies=self.cookies)

    def get_scenes(self, response):
        meta = response.meta
        scenes = response.xpath('//div[contains(@id, "post-")]')
        for scene in scenes:
            sceneid = scene.xpath('./@id').get()
            meta['id'] = re.search(r'post-(\d+)', sceneid).group(1)

            scene = scene.xpath('.//h2/a/@href').get()

            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)

    def get_tags(self, response):
        return ['Gay']

    def get_performers_data(self, response):
        performers = super().get_performers(response)
        performers_data = []
        for performer in performers:
            performer = string.capwords(performer.strip())
            performer_extra = {}
            performer_extra['name'] = performer
            performer_extra['site'] = "King Breeders"
            performer_extra['extra'] = {}
            performer_extra['extra']['gender'] = "Male"
            performers_data.append(performer_extra)
        return performers_data    