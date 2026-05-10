import re
import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper
true = True
false = False


class FrolicMeSpider(BaseSceneScraper):
    name = 'FrolicMe'
    network = 'Frolic Me'
    parent = 'Frolic Me'
    site = 'Frolic Me'

    start_urls = [
        'https://www.frolicme.com',
    ]

    title_trash = ['- film', '- Film']

    cookies = [{"domain":"www.frolicme.com","hostOnly":true,"httpOnly":false,"name":"fm_av_token","path":"/","sameSite":"unspecified","secure":true,"session":true,"storeId":"0","value":"1779160158.tier_2.2.yes.9c1db0771b07e03fc661286ed85437c3ec4e5729c43d22b3f4fc9143b7f6a082b62b4a2fdb.bfff2b087808b427bf3e94b19be2c02d0c8eeaf4816736b1065eb50aa6479968"},{"domain":"www.frolicme.com","hostOnly":true,"httpOnly":true,"name":"PHPSESSID","path":"/","sameSite":"lax","secure":true,"session":true,"storeId":"0","value":"39db385e6fad63bbc3bd9a4debd6e581"},{"domain":".frolicme.com","expirationDate":1808143593,"hostOnly":false,"httpOnly":false,"name":"ph_phc_uJiIolIQ5UQvYwAjdRUv5ynCce9T80jxH61zPJm15M4_posthog","path":"/","sameSite":"lax","secure":true,"session":false,"storeId":"0","value":"%7B%22distinct_id%22%3A%2201996798-6ed2-7c39-b8f3-66f28b368b3a%22%2C%22%24sesid%22%3A%5B1776607593517%2C%22019da610-7a4c-7a94-9cd7-a9b05bf158a8%22%2C1776607590988%5D%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fwww.frolicme.com%2Ffilms%2F%3Forder_by%3Ddate_desc%22%7D%7D"}]


    selector_map = {
        'title': '//div[@class="entry-title"]/text()',
        'description': '//div[@class="entry-content"]/p/span//text()',
        'date': '//script[contains(text(), "datePublished")]/text()',
        're_date': r'datePublished[\'\"]:.*?(\d{4}-\d{2}-\d{2}.*?)[\'\"]',
        'image': '//meta[@property="og:image"]/@content',
        'duration': '//span[contains(@class,"inline-flex")]//i[contains(@class, "clock")]/following-sibling::text()',
        're_duration': r'((?:\d{1,2}\:)?\d{2}\:\d{2})',
        'performers': '//span[contains(@class,"inline-flex")]/a[contains(@href, "/models/")]/text()',
        'tags': '//span[contains(@class,"inline-flex")]//i[contains(@class, "tag")]/following-sibling::a/text()',
        'external_id': r'.*\/(.*?)\/$',
        'trailer': '',
        'pagination': '/films/page/%s/?order_by=date_desc'
    }

    # ~ def start_requests(self):
        # ~ meta = {}
        # ~ meta['page'] = self.page
        # ~ yield scrapy.Request('https://www.frolicme.com', callback=self.age_verify, meta=meta, headers=self.headers, cookies=self.cookies)

    # ~ def age_verify(self, response):
        # ~ meta = response.meta
        # ~ yield scrapy.FormRequest(url="https://www.frolicme.com/wp-json/frolic/v1/verify", meta=meta, formdata={"dob": "1985-05-02", "country": "US", "search_terms": ""}, callback=self.start_requests_2)

    # ~ def start_requests_2(self, response):
        # ~ meta = response.meta

        # ~ for link in self.start_urls:
            # ~ yield scrapy.Request(url=self.get_next_page_url(link, self.page), callback=self.parse, meta=meta, headers=self.headers, cookies=self.cookies)

    def get_scenes(self, response):
        meta = response.meta
        scenes = response.xpath('//article[contains(@class, "post")]/a/@href').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)

    def get_title(self, response):
        title = super().get_title(response)
        for trash in self.title_trash:
            title = title.replace(trash, "").strip()
        return title
