import re
import scrapy

from tpdb.BasePerformerScraper import BasePerformerScraper


class SiteDieselVidsPerformerSpider(BasePerformerScraper):
    selector_map = {
        'name': '//div[contains(@class,"bioDetails")]//h2/text()',
        'image': '//div[@class="bioPic"]/img/@src',
        'image_blob': True,
        'cupsize': '//div[contains(@class,"bioDetails")]//span[contains(text(), "Measurements:")]/following-sibling::text()',
        'ethnicity': '//div[contains(@class,"bioDetails")]//span[contains(text(), "Ethnicity:")]/following-sibling::text()',
        'eyecolor': '//div[contains(@class,"bioDetails")]//span[contains(text(), "Eyes:")]/following-sibling::text()',
        'haircolor': '//div[contains(@class,"bioDetails")]//span[contains(text(), "Hair:")]/following-sibling::text()',
        'height': '//div[contains(@class,"bioDetails")]//span[contains(text(), "Height:")]/following-sibling::text()',
        'weight': '//div[contains(@class,"bioDetails")]//span[contains(text(), "Height:")]/following-sibling::text()',

        'pagination': '/models/page%s.html',
        'external_id': r'model/(.*)/'
    }

    name = 'DieselVidsPerformer'
    network = 'DieselVids'

    start_urls = [
        'https://dieselvids.com',
    ]

    def get_gender(self, response):
        return 'Female'

    def get_performers(self, response):
        performers = response.xpath('//h3/a/@href').getall()
        for performer in performers:
            yield scrapy.Request(url=self.format_link(response, performer), callback=self.parse_performer, cookies=self.cookies, headers=self.headers)

    def get_ethnicity(self, response):
        ethnicity = super().get_ethnicity(response)
        if ethnicity.lower().strip() == "white":
            return "Caucasian"
        return ethnicity

    def get_height(self, response):
        height = super().get_height(response)
        if "'" in height:
            height = re.sub(r'[^0-9\']', '', height)
            feet = re.search(r'(\d+)\'', height)
            if feet:
                feet = feet.group(1)
                feet = int(feet) * 12
            else:
                feet = 0
            inches = re.search(r'\'(\d+)', height)
            if inches:
                inches = inches.group(1)
                inches = int(inches)
            else:
                inches = 0
            return str(int((feet + inches) * 2.54)) + "cm"
        return None    

    def get_weight(self, response):
        weight = super().get_weight(response)
        weight = re.search(r'^(\d+)', weight)
        if weight:
            weight = weight.group(1)
            weight = str(int(int(weight) * .453592))
            return weight
        return None    