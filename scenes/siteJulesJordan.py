import re
import requests
import scrapy
import tldextract

from tpdb.BaseSceneScraper import BaseSceneScraper


def match_site(argument):
    match = {
        'girlgirl': "Girl Girl",
        'julesjordan': "Jules Jordan",
        'manuelferrara': "Manuel Ferrara",
        'theassfactory': "The Ass Factory",
        'spermswallowers': "Sperm Swallowers",
    }
    return match.get(argument, argument)


class JulesJordanSpider(BaseSceneScraper):
    name = 'JulesJordan'
    network = 'julesjordan'

    start_urls = [
        'https://www.julesjordan.com',
    ]

    selector_map = {
        'title': '//h1[contains(@class, "title")]/text()',
        'description': '//div[contains(@class, "desc")]//text()',
        'date': '//script[contains(@type, "json") and contains(text(), "uploadDate")]/text()',
        're_date': r'"uploadDate": "(\d{4}-\d{2}-\d{2})',
        'date_formats': ['%Y-%m-%d'],
        'image': '//video/@poster',
        'performers': '//div[@class="scene-info"]//span[@class="update_models"]/a/text()',
        'tags': '//div[@class="scene-cats"]/a/text()',
        'duration': '//script[contains(@type, "json") and contains(text(), "uploadDate")]/text()',
        're_duration': r'"duration": "(PT.*?)"',
        'external_id': r'trial/scenes/(.+)\.html',
        'trailer': '',
        'pagination': '/trial/categories/movies_%s_d.html'
    }

    max_pages = 47

    def get_scenes(self, response):
        if "julesjordan" in response.url:
            scenes = response.xpath('//div[@class="jj-content-card"]/a/@href').getall()
        else:
            scenes = response.xpath('//div[@class="category_listing_wrapper_updates"]//a[1]/@href|//div[@class="grid-item"]/a/@href|//article[@class="grid-item"]/a/@href').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=scene, callback=self.parse_scene)

    def get_site(self, response):
        site = tldextract.extract(response.url).domain
        site = match_site(site)
        return site
    
    def get_image(self, response):
        image = super().get_image(response)
        if image:
            return self.find_best_image(response, image)
        return None

    def image_exists(self, url):
        try:
            r = requests.head(url, allow_redirects=True, timeout=5)
            return r.status_code == 200
        except requests.RequestException:
            return False
        
    def find_best_image(self, response, original_url):
        for suffix in ("-4x", "-3x", "-2x", "-1x"):
            candidate = original_url.replace("-1x", suffix)
            candidate = self.format_link(response, candidate).replace(" ", "%20")
            if self.image_exists(candidate):
                return candidate
        return None        