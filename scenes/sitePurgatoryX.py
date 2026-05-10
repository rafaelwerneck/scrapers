import re
import string
import json

from tpdb.BaseSceneScraper import BaseSceneScraper


class PurgatoryXSpider(BaseSceneScraper):
    name = "PurgatoryX"
    network = 'Radical Entertainment'
    parent = "PurgatoryX"

    start_urls = [
        'https://tour.purgatoryx.com'
    ]

    selector_map = {
        'external_id': r'',
        'pagination': '/episodes?page=%s&order_by=publish_date&sort_by=desc',
        'type': 'Scene',
    }

    def get_scenes(self, response):
        jsoncode = response.xpath('//script[contains(@id, "NEXT_DATA")]/text()')
        if jsoncode:
            jsondata = json.loads(jsoncode.get())
            jsondata = jsondata['props']['pageProps']['contents']['data']
            for scene in jsondata:
                item = self.init_scene()
                scene_date = self.parse_date(scene['publish_date'], date_formats=['%Y/%m/%d %h:%m:%s']).strftime('%Y-%m-%d')
                if scene_date:
                    item['date'] = scene_date
                else:
                    item['date'] = self.parse_date('today').strftime('%Y-%m-%d')
                if self.check_item(item, self.days):
                    item['title'] = self.cleanup_title(scene['title'])
                    item['id'] = scene['id']
                    item['description'] = self.cleanup_description(re.sub('<[^<]+?>', '', scene['description'])).replace("\r", " ").replace("\n", " ").replace("\t", " ").strip()
                    item['image'] = scene['thumb']
                    if item['image'][:2] == '//':
                        item['image'] = "https:" + item['image']
                    item['image_blob'] = self.get_image_blob_from_link(item['image'])
                    item['trailer'] = scene['trailer_url']
                    item['url'] = f"https://tour.purgatoryx.com/episodes/{scene['slug']}?trilogy={scene['playlist']}"
                    item['tags'] = scene['tags']
                    item['tags'] = list(map(lambda x: string.capwords(x.strip()), item['tags']))
                    if "Hell" in item['tags']:
                        item['site'] = "Hell Series"
                        item['tags'].remove("Hell")
                    elif "Heaven" in item['tags']:
                        item['site'] = "Heaven Series"
                        item['tags'].remove("Heaven")
                    else:
                        item['site'] = "PurgatoryX"
                    if "Purgatoryx" in item['tags']:
                        item['tags'].remove("Purgatoryx")
                    if "Hell" in item['tags']:
                        item['tags'].remove("Hell")
                    if "Heaven" in item['tags']:
                        item['tags'].remove("Heaven")
                    try:
                        duration = str(int(float(scene['seconds_duration'])))
                        item['duration'] = duration
                    except:
                        item['duration'] = ''

                    item['parent'] = 'PurgatoryX'
                    item['network'] = 'Radical Entertainment'
                    item['performers'] = []
                    item['type'] = "Scene"
                    item['performers'], item['performers_data'] = self.get_performers_data(scene['models_thumbs'])

                    yield self.check_item(item, self.days)

    def get_performers_data(self, performer_list):
        performers_data = []
        performers = []
        if len(performer_list):
            for performer in performer_list:
                perf = {}
                perf['name'] = string.capwords(self.cleanup_title(performer['name']))
                performers.append(perf['name'])
                perf['extra'] = {}
                perf['network'] = "Radical Entertainment"
                perf['site'] = "PurgatoryX"
                perf['image'] = performer['thumb']
                if perf['image'][:2] == '//':
                    perf['image'] = "https:" + perf['image']
                if perf['image']:
                    perf['image_blob'] = self.get_image_blob_from_link(perf['image'])
                performers_data.append(perf)
        return performers, performers_data
