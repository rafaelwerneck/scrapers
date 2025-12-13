import re
import string
import scrapy

from tpdb.BaseSceneScraper import BaseSceneScraper
true = True
false = False


class SiteAuntJudysSpider(BaseSceneScraper):
    name = 'AuntJudys'
    network = 'Aunt Judys'
    parent = 'Aunt Judys'

    start_urls = [
        'https://www.auntjudys.com',
        'https://www.auntjudysxxx.com',
    ]

    selector_map = {
        'title': '//span[contains(@class,"title_bar_hilite")]/text()',
        'description': '//span[@class="update_description"]/text()',
        'date': '//div[@class="gallery_info"]/div[@class="table"]/div[@class="row"]/div[contains(@class,"update_date")]/text()[1]',
        'image': '//span[@class="model_update_thumb"]/img/@src',
        'performers': '//div[@class="gallery_info"]/p/span[@class="update_models"]/a/text()',
        'tags': '//div[@class="gallery_info"]/span[@class="update_tags"]/a/text()',
        'external_id': r'.*/(.*?).html',
        'trailer': '//script[contains(text(),"df_movie")]/text()',
        're_trailer': '.*df_movie.*?path:\"(.*?.mp4)\"',
        'pagination': '/tour/categories/movies_%s_d.html'
    }

    def get_scenes(self, response):
        # print(response.text)
        meta = response.meta
        scenes = response.xpath('//div[@class="update_details"]')
        attrs = ["@src0_3x", "@src0_2x", "@src0_1x", "@src"]
        for scene in scenes:
            for attr in attrs:
                image = scene.xpath(f'./a/img/{attr}').get()
                if image:
                    break
            if image:
                meta['image'] = self.format_link(response, image)
                meta['image_blob'] = self.get_image_blob_from_link(meta['image'])

            scene = scene.xpath('./a/@href').get()
            if re.search(self.get_selector_map('external_id'), scene):
                url = self.format_link(response, scene)
                yield scrapy.Request(url=url, callback=self.parse_scene, meta=meta)

    def get_site(self, response):
        if "xxx" in response.url:
            return "Aunt Judys XXX"
        return "Aunt Judys"

    def get_parent(self, response):
        if "xxx" in response.url:
            return "Aunt Judys XXX"
        return "Aunt Judys"

    def get_trailer(self, response):
        if 'trailer' in self.get_selector_map() and self.get_selector_map('trailer'):
            trailer = self.process_xpath(response, self.get_selector_map('trailer'))
            if trailer:
                trailer = self.get_from_regex(trailer.get(), 're_trailer')
                if trailer:
                    trailer = "https://www.auntjudys.com" + trailer.replace(" ", "%20")
                    return trailer

        return ''

    def get_id(self, response):
        externid = super().get_id(response)
        return externid.lower()

    def get_performers(self, response):
        perf_list = response.xpath('//div[@class="gallery_info"]/p/span[@class="update_models"]/a')
        performers = []
        for performer in perf_list:
            performer_name = performer.xpath('./text()')
            performer_url = performer.xpath('./@href').get()
            if "auntjudys.com" in performer_url:
                performer_id = re.search(r'-(\w{2,4}\d{2,4})\.', performer_url)
                disambiguation = "999"
            elif "auntjudysxxx.com" in performer_url:
                performer_id = re.search(r'(\d+)\.', performer_url)
                disambiguation = "998"
            if performer_id:
                performer_id = performer_id.group(1)
            if performer_name:
                performer_name = performer_name.get().strip()
                performer_name = string.capwords(performer_name)
                if " " not in performer_name:
                    if performer_id:
                        performer_name = performer_name + " " + performer_id
                    else:
                        performer_name = performer_name + " " + disambiguation
                performers.append(performer_name)
        return performers
    
    def get_performers_data(self, response):
        perf_list = response.xpath('//div[@class="gallery_info"]/p/span[@class="update_models"]/a')
        performers_data = []
        for performer in perf_list:
            perf = {}
            performer_name = performer.xpath('./text()')
            performer_url = performer.xpath('./@href').get()
            if "auntjudys.com" in performer_url:
                performer_id = re.search(r'-(\w{2,4}\d{2,4})\.', performer_url)
                disambiguation = "999"
            elif "auntjudysxxx.com" in performer_url:
                performer_id = re.search(r'(\d+)\.', performer_url)
                disambiguation = "998"
            if performer_id:
                performer_id = performer_id.group(1)
            if performer_name:
                performer_name = performer_name.get().strip()
                performer_name = string.capwords(performer_name)
                if " " not in performer_name:
                    if performer_id:
                        performer_name = performer_name + " " + performer_id
                    else:
                        performer_name = performer_name + " " + disambiguation
                perf['name'] = performer_name
                perf['url'] = self.format_link(response, performer_url)
                perf['extra'] = {'gender': "Female"}
                perf['site'] = self.get_site(response)
                performers_data.append(perf)
        return performers_data