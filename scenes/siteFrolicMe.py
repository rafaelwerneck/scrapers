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

    cookies = [{"domain":"www.frolicme.com","hostOnly":true,"httpOnly":false,"name":"PHPSESSID","path":"/","sameSite":"unspecified","secure":false,"session":true,"storeId":"0","value":"lukn5q3qb7ipfems5t80k8vh56"},{"domain":"www.frolicme.com","hostOnly":true,"httpOnly":false,"name":"fm_av_token","path":"/","sameSite":"unspecified","secure":true,"session":true,"storeId":"0","value":"1766863237.tier_2.2.yes.2a5f5d188ff2c24eee11a194fe46444472be48ae7a3ff41723c841ca14067126430d520cc8.2e51f2ada520babb6e3a08c9675507417a9e7b1a1b276caeff309cde951b59c5"},{"domain":".frolicme.com","expirationDate":1795807590,"hostOnly":false,"httpOnly":false,"name":"ph_phc_uJiIolIQ5UQvYwAjdRUv5ynCce9T80jxH61zPJm15M4_posthog","path":"/","sameSite":"lax","secure":true,"session":false,"storeId":"0","value":"%7B%22distinct_id%22%3A%2201996798-6ed2-7c39-b8f3-66f28b368b3a%22%2C%22%24sesid%22%3A%5B1764271590493%2C%22019ac6c2-c777-7378-b59a-8db44500df44%22%2C1764271245175%5D%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fwww.frolicme.com%2Ffilms%2F%3Forder_by%3Ddate_desc%22%7D%7D"}]


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
