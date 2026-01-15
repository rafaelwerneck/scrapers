from tpdb.BasePerformerScraper import BasePerformerScraper
from tpdb.items import PerformerItem


class SiteFilthyFemdomPerformerSpider(BasePerformerScraper):
    selector_map = {
        'pagination': '/models/%s/latest/?g=f',
        # ~ 'pagination': '/models/%s/latest/?g=m',
        'external_id': r'model/(.*)/'
    }

    name = 'FilthyFemdomPerformer'

    start_urls = [
        'https://filthyfemdom.com',
    ]

    def get_performers(self, response):
        performers = response.xpath('//div[contains(@class, "item-portrait")]')
        for performer in performers:
            item = PerformerItem()

            item['name'] = self.cleanup_title(performer.xpath('.//h4/a/text()').get())
            image = performer.xpath('.//img/@src0_2x')
            if image:
                item['image'] = self.format_link(response, image.get())
                item['image_blob'] = self.get_image_blob_from_link(item['image'])
                if "?" in item['image']:
                    item['image'] = item['image'].split("?")[0]
            else:
                item['image'] = ""
                item['image_blob'] = ""
            item['bio'] = ''

            if "g=f" in response.url:
                item['gender'] = 'Female'
            else:
                item['gender'] = 'Male'

            item['astrology'] = ''
            item['birthday'] = ''
            item['birthplace'] = ''
            item['cupsize'] = ''
            item['ethnicity'] = ''
            item['eyecolor'] = ''
            item['fakeboobs'] = ''
            item['haircolor'] = ''
            item['height'] = ''
            item['measurements'] = ''
            item['nationality'] = ''
            item['piercings'] = ''
            item['tattoos'] = ''
            item['weight'] = ''
            item['network'] = 'FilthyFemdom'
            item['url'] = self.format_link(response, performer.xpath('.//h4/a/@href').get())

            yield item
