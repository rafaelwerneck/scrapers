import re
import scrapy

from tpdb.BasePerformerScraper import BasePerformerScraper


class SiteCumLouderPerformerSpider(BasePerformerScraper):
    selector_map = {
        'name': '//h1/a/text()',
        'image': '//img[contains(@class, "thumb-bio")]/@data-src',
        'image_blob': True,
        'bio': '//div[@class="box-biografia"]//p//text()',
        'birthday': '//strong[contains(text(), "Date of Birth")]/following-sibling::text()',
        'eyecolor': '//strong[contains(text(), "Eye")]/following-sibling::text()',
        'haircolor': '//strong[contains(text(), "Hair")]/following-sibling::text()',
        'nationality': '//strong[contains(text(), "Nationality")]/following-sibling::text()',

        'pagination': '/girls/%s/',
        'external_id': r'model/(.*)/'
    }

    name = 'CumLouderPerformer'
    network = 'Cum Louder'

    start_urls = [
        'https://www.cumlouder.com',
    ]

    def get_gender(self, response):
        return 'Female'

    def get_performers(self, response):
        performers = response.xpath('//a[contains(@class, "muestra-pornostar")]/@href').getall()
        for performer in performers:
            yield scrapy.Request(url=self.format_link(response, performer), callback=self.parse_performer, cookies=self.cookies, headers=self.headers)

    def get_height(self, response):
        height = response.xpath('//strong[contains(text(), "Height")]/following-sibling::text()')
        if height:
            height = height.get().strip()
            try:
                height = float(height.strip()) * 100
                return str(int(height)) + "cm"
            except (ValueError, AttributeError):
                return None
        return None

    def get_weight(self, response):
        weight = response.xpath('//strong[contains(text(), "Weight")]/following-sibling::text()')
        if weight:
            weight = weight.get().strip()
            weight = re.sub(r'[^0-9]+', '', weight)
            if weight:
                return weight + "kg"
        return None
    
    def get_birthday(self, response):
        birthday = response.xpath('//strong[contains(text(), "Date of Birth")]/following-sibling::text()')
        if birthday:
            birthday = birthday.get().strip()
            return self.parse_date(birthday, date_formats=['%d-%m-%Y']).strftime('%Y-%m-%d')
        return None