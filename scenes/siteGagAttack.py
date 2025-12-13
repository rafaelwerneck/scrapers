import re
import html
import unidecode
import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper


class SiteGagAttackSpider(BaseSceneScraper):
    name = 'GagAttack'
    network = 'GagAttack'
    parent = 'GagAttack'
    site = 'GagAttack'

    cookies = [{"name": "cwarn", "value": "true"}, {"name": "warn", "value": "true"}]

    start_urls = [
        'https://gagattack.org',
    ]

    selector_map = {
        'title': '//span[contains(@class, "update_title")]/text()',
        'description': '//span[contains(@class, "latest_update_description")]//text()',
        'date': '//span[contains(@class, "availdate")]//text()',
        'image': '//div[@class="update_image"]//img[contains(@class, "thumb")]/@src0_4x',
        'performers': '//span[contains(@class, "tour_update_models")]/a/text()',
        'tags': '//span[contains(@class, "update_tags")]//a/text()',
        'trailer': '',
        'external_id': r'',
        'pagination': '/categories/movies_%s_d.html',
        'type': 'Scene',
    }

    def get_scenes(self, response):
        meta = response.meta
        scenes = response.xpath('//div[@class="updateItem"]')
        for scene in scenes:
            scenedate = scene.xpath('.//span[contains(text(), "/") and string-length(normalize-space(.)) = 10]/text()')
            if scenedate:
                scenedate = self.parse_date(scenedate.get().strip(), date_formats=['%m/%d/%Y']).strftime('%Y-%m-%d')
                meta['date'] = scenedate

            sceneid = scene.xpath('.//img/@id').get()
            if sceneid:
                meta['id'] = re.search(r'-(\d+)', sceneid).group(1)
            sceneurl = scene.xpath('./a[1]/@href').get()

            image = scene.xpath('.//img/@src0_4x').get()
            if not image:
                image = scene.xpath('.//img/@src0_3x').get()
            if not image:
                image = scene.xpath('.//img/@src0_2x').get()
            if not image:
                image = scene.xpath('.//img/@src0_1x').get()

            if image:
                meta['image'] = self.format_link(response, image.strip())

            if meta['id'] and self.check_item(meta, self.days):
                if "image" in meta and meta['image']:
                    meta['image_blob'] = self.get_image_blob_from_link(meta['image'])
                yield scrapy.Request(url=self.format_link(response, sceneurl), callback=self.parse_scene, meta=meta)

    def get_duration(self, response):
        duration = response.xpath('//div[@class="update_counts_preview_table"]/text()')
        if duration:
            duration = duration.get()
            duration = unidecode.unidecode(html.unescape(duration.lower().replace("&nbsp;", " ").replace("\xa0", " "))).replace(" ", "")
            duration = re.search(r'(\d+)min', duration)
            if duration:
                return str(int(duration.group(1)) * 60)
        return None          

    def get_performers_data(self, response):
        performers = super().get_performers(response)
        perf_data = []
        for performer in performers:
            perf = {}
            perf['name'] = performer
            perf['url'] = f"https://gagattack.org/models/{performer.replace(' ', '')}.html"
            perf['site'] = 'GagAttack'
            perf['network'] = 'GagAttack'
            perf['extra'] = {'gender': "Female"}
            perf_data.append(perf)
        return perf_data