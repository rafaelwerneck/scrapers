## Stub scraper, this has been moved to NetworkAylo.py

from tpdb.BaseSceneScraper import BaseSceneScraper
from tpdb.items import SceneItem


class ProjectOneServiceBrazzersVRSpider(BaseSceneScraper):
    name = 'ProjectOneServiceBrazzersVR'

    start_urls = [
        '',
    ]

    selector_map = {
        'external_id': r'',
        'pagination': '',
        'type': 'Scene',
    }

    def get_scenes(self, response):
        meta = response.meta
        scenes = response.xpath('').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)