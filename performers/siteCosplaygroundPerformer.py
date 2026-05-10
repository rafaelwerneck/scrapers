import re
import scrapy

from tpdb.BasePerformerScraper import BasePerformerScraper


class SiteCosplaygroundPerformerSpider(BasePerformerScraper):
    selector_map = {
        'name': '//h1/text()',
        'image': '//div[contains(@class, "thumbnail")]/picture/source[contains(@srcset, "/star/")]/@srcset',
        'image_blob': True,
        'bio': '//div[contains(@class, "text-truncate-with-more")]//text()',
        'birthday': '//dt[contains(text(), "Birth:")]/following-sibling::dd/text()',
        'birthplace': '//dt[contains(text(), "Place:")]/following-sibling::dd/text()',
        'height': '//dt[contains(text(), "Height:")]/following-sibling::dd/text()',
        'measurements': '//dt[contains(text(), "Measurements:")]/following-sibling::dd/text()',
        'pagination': '/models?page=%s',
        'external_id': r'model/(.*)/'
    }

    name = 'CosplaygroundPerformer'
    network = 'Cosplayground'

    start_urls = [
        'https://cosplayground.com',
    ]

    def get_height(self, response):
        height = super().get_height(response)
        if height:
            tot_inches = 0
            feet = re.search(r"(\d+)'", height)
            if feet:
                tot_inches += int(feet.group(1)) * 12
            inches = re.search(r"'\s*(\d+)", height)
            if inches:
                tot_inches += int(inches.group(1))
            if tot_inches:
                return str(int(tot_inches * 2.54)) + "cm"
        return None

    def get_gender(self, response):
        return 'Female'

    def get_performers(self, response):
        performers = response.xpath('//div[@class="col"]/a/@href').getall()
        for performer in performers:
            yield scrapy.Request(url=self.format_link(response, performer), callback=self.parse_performer, cookies=self.cookies, headers=self.headers)

    def get_measurements(self, response):
        if 'measurements' in self.selector_map:
            measurements = self.process_xpath(response, self.get_selector_map('measurements')).get()
            if measurements and re.search(r'(\d+\w+-\d+-\d+)', measurements):
                measurements = re.search(r'(\d+\w+-\d+-\d+)', measurements).group(1)
                return measurements.strip()
        return ''

    def get_cupsize(self, response):
        if 'cupsize' in self.selector_map and self.get_selector_map('cupsize'):
            cupsize = self.process_xpath(response, self.get_selector_map('cupsize')).get()
            return cupsize.strip()
        else:
            if 'measurements' in self.selector_map:
                measurements = self.process_xpath(response, self.get_selector_map('measurements')).get()
                if measurements and re.search(r'(\d+\w+-\d+-\d+)', measurements):
                    cupsize = re.search(r'(\d+\w+)-\d+-\d+', measurements)
                    if cupsize:
                        cupsize = cupsize.group(1)
                        return cupsize.strip()
        return ''

    def get_haircolor(self, response):
        tags = response.xpath('//div[contains(text(), "Tags")]/following-sibling::a/text()').getall()
        hair_tags = ['blonde', 'brunette', 'redhead', 'black hair', 'auburn', 'gray hair', 'white hair', 'other hair']
        for tag in tags:
            if tag.lower() in hair_tags:
                return tag.lower().replace(" hair", "").strip().title()
        return ''

    def get_ethnicity(self, response):
        tags = response.xpath('//div[contains(text(), "Tags")]/following-sibling::a/text()').getall()
        eth_tags = ['asian', 'caucasian', 'latina', 'black']
        for tag in tags:
            if tag.lower() in eth_tags:
                return tag.title()
        return ''

    def get_nationality(self, response):
        birthplace = self.get_birthplace(response)
        if birthplace:
            bp = birthplace.lower()
            if any(x in bp for x in ['usa', 'states', 'america']):
                return 'American'
            elif any(x in bp for x in ['uk', 'england', 'britain']):
                return 'British'
            elif any(x in bp for x in ['canada', 'canadian']):
                return 'Canadian'
            elif any(x in bp for x in ['australia', 'australian']):
                return 'Australian'
        return None

    def get_birthplace_code(self, response):
        birthplace = self.get_birthplace(response)
        if birthplace:
            bp = birthplace.lower()
            if any(x in bp for x in ['usa', 'states', 'america']):
                return 'US'
            elif any(x in bp for x in ['uk', 'england', 'britain']):
                return 'GB'
            elif any(x in bp for x in ['canada', 'canadian']):
                return 'CA'
            elif any(x in bp for x in ['australia', 'australian']):
                return 'AU'
        return None