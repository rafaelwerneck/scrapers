import re
from tpdb.BasePerformerScraper import BasePerformerScraper
from tpdb.items import PerformerItem


class NetworkGroobyPerformerSpider(BasePerformerScraper):
    selector_map = {
        'pagination': '/tour/models/%s/latest/?g=t',
        'external_id': r'model/(.*)/'
    }

    name = 'GroobyPerformer'
    network = 'Grooby'

    start_urls = [
        'https://www.black-tgirls.com',
        'https://www.blacktgirlshardcore.com',
        'https://www.bobstgirls.com',
        'https://www.brazilian-transsexuals.com',
        'https://www.braziltgirls.xxx',
        'https://www.grooby.club/',
        'https://www.femout.xxx',
        'https://www.femoutsex.xxx',
        'https://www.franks-tgirlworld.com',
        'https://www.futa.xxx',
        'https://www.grooby-archives.com',
        'https://www.groobygirls.com',
        'https://www.ladyboy.xxx',
        'https://www.tgirljapan.com',
        'https://www.tgirljapanhardcore.com',
        'https://www.tgirltops.com',
        'https://www.tgirls.porn',
        'https://www.tgirls.xxx',
        'https://www.tgirlsex.xxx',
        'https://www.tgirlsfuck.com',
        'https://www.transexpov.com',
        'https://www.transgasm.com',
    ]


    def get_next_page_url(self, base, page):
        if "braziltgirls" in base or "brazilian" in base or "grooby.club" in base or "tgirlsfuck" in base:
            pagination = '/tour/categories/models/%s/latest/'
        else:
            pagination = self.get_selector_map('pagination')
        return self.format_url(base, pagination % page)

    def get_performers(self, response):
        performers = response.xpath('//div[@class="model" or @class="model "]')
        for performer in performers:
            item = PerformerItem()

            name = performer.xpath('./h4/a/text()').get()
            item['name'] = self.cleanup_title(name)
            image =  performer.xpath('.//img/@src0_3x')
            if not image:
                image =  performer.xpath('.//img/@src0_2x')
            if not image:
                image = performer.xpath('.//img/@src')
            if image:
                item['image'] = self.format_link(response, image.get())
                item['image_blob'] = self.get_image_blob_from_link(item['image'])
            else:
                item['image'] = ''
                item['image_blob'] = ''
            item['bio'] = ''
            if "futa" in response.url:
                item['gender'] = ''
            else:
                item['gender'] = 'Transgender Female'
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
            item['network'] = 'Grooby'
            item['url'] = self.format_link(response, performer.xpath('./h4/a/@href').get())
            perf_url_segment = re.search(r'.*/(.*?)\.htm', item['url'])
            perf_id = re.search(r'(\d+)', perf_url_segment.group(1))
            if perf_id:
                item['name'] = f"{item['name']} {perf_id.group(1)}"
            yield item
