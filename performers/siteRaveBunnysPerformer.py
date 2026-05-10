import re
import string
import scrapy

from tpdb.BasePerformerScraper import BasePerformerScraper


class SiteRaveBunnysPerformerSpider(BasePerformerScraper):
    selector_map = {
        'image': '//img[contains(@class, "model_bio_thumb")]/@src0_3x',
        'image_blob': True,
        'bio': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Bio")]/strong/following-sibling::text()',
        'birthday': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Date of")]/strong/following-sibling::text()',
        'birthplace': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Birthplace")]/strong/following-sibling::text()',
        'ethnicity': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Ethnicity")]/strong/following-sibling::text()',
        'eyecolor': '',
        'haircolor': '',
        'height': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Height")]/strong/following-sibling::text()',
        'measurements': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Measurements")]/strong/following-sibling::text()',
        'nationality': '',
        'piercings': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Piercings")]/strong/following-sibling::text()',
        'tattoos': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Tattoos")]/strong/following-sibling::text()',
        'weight': '//div[@class="stats"]/ul/li[contains(./strong/text(), "Weight")]/strong/following-sibling::text()',

        'pagination': '/models/%s/name/?g=f',
        'external_id': r'model/(.*)/'
    }

    name = 'RaveBunnysPerformer'
    network = 'RaveBunnys'

    start_urls = [
        'https://ravebunnys.com',
    ]

    def get_gender(self, response):
        return 'Female'

    def get_performers(self, response):
        performers = response.xpath('//div[contains(@class, "item-portrait")]/a/@href').getall()
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

    def get_name(self, response):
        name = response.xpath('//h1/text()').get()
        name = name.lower()
        name = name.replace("bio ", "").replace("for ","").strip()
        if name:
            return string.capwords(name)
        return ''
    
    def get_height(self, response):
        height = super().get_height(response)
        if height:
            height = re.search(r'(\d+).*(\d+)', height)
            if height:
                feet = int(height.group(1))
                inches = int(height.group(2))
                feet = int(feet) * 12
                height = str(int((feet + inches) * 2.54)) + "cm"
        return height

    def get_weight(self, response):
        weight = super().get_weight(response)
        if weight:
            weight = re.search(r'(\d+)', weight)
            if weight:
                weight = weight.group(1)
                weight = str(int(int(weight) * .453592)) + "kg"
        return weight
    
    def get_fakeboobs(self, response):
        natural = response.xpath('//div[@class="stats"]/ul/li[contains(./strong/text(), "Natural")]/strong/following-sibling::text()')
        if natural:
            natural = natural.get().strip()
            if "yes" in natural.lower():
                return 'Yes'
            elif "no" in natural.lower():
                return 'No'
        return ''