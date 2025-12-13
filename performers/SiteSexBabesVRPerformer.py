import re
import scrapy

from tpdb.BasePerformerScraper import BasePerformerScraper


class PerformerSpider(BasePerformerScraper):
    selector_map = {
        'name': '//h1/text()',
        'image': '//img[@class="mobile"]/@src',
        'image_blob': True,
        'bio': '//h2[contains(text(), "Biography")]/following-sibling::p//text()',
        'birthplace': '//h3[contains(text(), "Country")]/following-sibling::span[1]/text()',
        'eyecolor': '//h3[contains(text(), "Eyes")]/following-sibling::span[1]/text()',
        're_eyecolor': r'/(.*)',
        'haircolor': '//h3[contains(text(), "Hair")]/following-sibling::span[1]/text()',
        're_haircolor': r'(.*)/',
        'height': '//h3[contains(text(), "Height")]/following-sibling::span[1]/text()',
        're_height': r'/.*?(\d+)',
        'nationality': '//h3[contains(text(), "Country")]/following-sibling::span[1]/text()',
        'weight': '//h3[contains(text(), "Weight")]/following-sibling::span[1]/text()',
        're_weight': r'(\d+).*?/',

        'pagination': '/vr-pornstars/%s/?sort_by=added_date',
        'external_id': r'model/(.*)/'
    }

    name = 'SexBabesVRPerformer'
    network = 'SexBabesVR'

    start_urls = [
        'https://sexbabesvr.com',
    ]

    def get_gender(self, response):
        return 'Female'

    def get_performers(self, response):
        performers = response.xpath('//a[@class="item models-container" and contains(@href, "/model/")]/@href').getall()
        for performer in performers:
            yield scrapy.Request(url=self.format_link(response, performer), callback=self.parse_performer, cookies=self.cookies, headers=self.headers)

    def get_name(self, response):
        name = super().get_name(response)
        if "vr" in name.lower():
            name = re.sub(r'(?i)vr', '', name)
        return name.strip()