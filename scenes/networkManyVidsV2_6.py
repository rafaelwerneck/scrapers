"""
Scraper for ManyVids network.
If adding sites, please use the 'Manyvids: <site/performername>' format
This helps keep them together on the site without mixing in what are
usually more or less camgirls into the regular sites
"""
import re
import html
import json
import string
import scrapy

from tpdb.BaseSceneScraper import BaseSceneScraper
from tpdb.items import SceneItem


class NetworkManyVidsV2_6Spider(BaseSceneScraper):

    start_urls = [
        ['Manyvids: HulkandIsa', True, '1006335580'],
        ['Manyvids: HuneyBaked', True, '1003427367'],
        ['Manyvids: hungfemboy', True, '1006707041'],
        ['Manyvids: Hxllywxxdz', True, '1007287757'],
        ['Manyvids: iamannawilde', True, '1007454708'],
        ['Manyvids: icanbeurnuocmami', True, '1004549717'],
        ['Manyvids: Icy Winters', True, '697815'],
        ['Manyvids: Im Heather Harmon', False, '1003667583'],
        ['Manyvids: ImMeganLive', True, '491714'],
        ['Manyvids: Indian BabeXX69XX', True, '1001903948'],
        ['Manyvids: Indian Sneha', True, '1005941597'],
        ['Manyvids: IndiscreetHotAndFit', True, '1005093292'],
        ['Manyvids: InkedMonster', True, '1001576946'],
        ['Manyvids: InsideTatum', True, '1008353358'],
        ['Manyvids: Irish Skylar', True, '1006518930'],
        ['Manyvids: Irisxjase', True, '1007053479'],
        ['Manyvids: Isiah Maxwell', True, '1001687261'],
        ['Manyvids: Island Boy Vids', False, '1007765381'],
        ['Manyvids: Island Peach', True, '1001402896'],
        ['Manyvids: ItsReeseRobins', False, '1005302009'],
        ['Manyvids: itstommyking', True, '1001037206'],
        ['Manyvids: Ittybittycherry', True, '1007813826'],
        ['Manyvids: Ivy Starshine', True, '362540'],
        ['Manyvids: Izzy Rosse', True, '1005964496'],
        ['Manyvids: Jack and Jill', False, '1001495638'],
        ['Manyvids: Jack Blaque', True, '536056'],
        ['Manyvids: Jack Ripher', True, '1001692458'],
        ['Manyvids: Jackie Synn', True, '194026'],
        ['Manyvids: Jada Kai', True, '1000722201'],
        ['Manyvids: Jada Stevens', True, '1004539081'],
        ['Manyvids: Jade Vow', True, '1002042328'],
        ['Manyvids: JadedJuneBug', True, '1007315738'],
        ['Manyvids: Jakknife', True, '1006789072'],
        ['Manyvids: Jameshardon007', True, '1005403401'],
        ['Manyvids: Jane Cane', True, '1000718761'],
        ['Manyvids: Jane Judge', True, '1000197274'],
        ['Manyvids: Janet Mason', True, '1005452249'],
        ['Manyvids: Japanstraycat', True, '1007451603'],
        ['Manyvids: Jasmine Teaa', True, '1001524782'],
        ['Manyvids: Jasper Nyx', True, '1003787164'],
        ['Manyvids: Jaybbgirl', True, '1001317123'],
        ['Manyvids: Jayinne', True, '1003837091'],
        ['Manyvids: JaySmoothXXX', False, '525062'],
        ['Manyvids: JayToy', True, '1002541986'],
        ['Manyvids: JazminTorresBBW', True, '1001552380'],
        ['Manyvids: JazzzBerrry', True, '1004935662'],
        ['Manyvids: Jenna Creed', True, '1001071635'],
        ['Manyvids: Jenna J Ross', True, '562476'],
        ['Manyvids: Jenni Knight', True, '1000534648'],
        ['Manyvids: JennyBlighe', True, '103563'],
        ['Manyvids: Jeri Lynn', True, '13343'],
        ['Manyvids: Jessica Bloom', True, '1005013740'],
        ['Manyvids: Jessica Starling', True, '1000109566'],
        ['Manyvids: JessieHH', True, '1008264323'],
        ['Manyvids: JessRyan', True, '184888'],
        ['Manyvids: Jewelz Blu', True, '1002322838'],
        ['Manyvids: Jia lulu', True, '1007367342'],
        ['Manyvids: Jill Kassidy', True, '1001466952'],
        ['Manyvids: JMacsPOV', False, '1003290494'],
        ['Manyvids: Jodi West', True, '1004388132'],
        ['Manyvids: John Legendary', True, '1005086754'],
        ['Manyvids: Johnny Sins', True, '1000255726'],
        ['Manyvids: Johnny767', False, '1009535595'],
        ['Manyvids: JohnnyGotBlown', False, '1006247385'],
        ['Manyvids: JohnnyLovexxx', True, '1002514420'],
        ['Manyvids: Jolie Lyon', True, '1001506737'],
        ['Manyvids: Joshua Lewis', True, '1004083778'],
        ['Manyvids: JuicyGao', True, '1006897026'],
        ['Manyvids: juicyxjaden', True, '1004101467'],
        ['Manyvids: JuliaSoftdome', True, '1004595211'],
        ['Manyvids: Julie Prim', True, '1000877561'],
        ['Manyvids: Julie Snow', True, '1000053441'],
        ['Manyvids: Juliette Crimson', True, '1005821442'],
        ['Manyvids: Just Bondage Sex', False, '341832'],
        ['Manyvids: Kakao Chan', True, '1005489816']
    ]

    name = 'ManyVidsV2_6'

    custom_settings = {'AUTOTHROTTLE_ENABLED': 'True', 'AUTOTHROTTLE_DEBUG': 'False', 'HTTPERROR_ALLOWED_CODES': [403, 404]}

    selector_map = {
        'title': '',
        'description': '//div[contains(@class, "desc-text")]/text()',
        'date': '//div[@class="mb-1"]/span[1]/span[2]|//div[@class="mb-1"]/span[2]/text()',
        'image': '//meta[@name="twitter:image"]/@content',
        'performers': '',
        'tags': '//script[contains(text(),"tagListApp")]/text()',
        'duration': '//div[@class="video-details"]//i[contains(@class, "mv-icon-video-length")]/following-sibling::text()[contains(., "min")]',
        're_duration': r'(\d{1,2}\:.*?) min',
        'external_id': '',
        'trailer': '',
        'pagination': ''
    }

    headers = {
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        url = "https://www.manyvids.com/Profile/1001216419/YouthLust/Store/Videos/"
        yield scrapy.Request(url, callback=self.start_requests2, headers=self.headers, cookies=self.cookies)

    def start_requests2(self, response):
        meta = response.meta
        self.headers['referer'] = 'https://www.manyvids.com/Profile/1003004427/Sweetie-Fox/Store/Videos/'

        for link in self.start_urls:
            meta['page'] = self.page
            meta['siteid'] = link[2]
            meta['site'] = link[0]
            meta['parse_performer'] = link[1]
            meta['pagination'] = "landscape"
            next_page = self.get_next_page_url(self.page, meta)
            yield scrapy.Request(next_page, callback=self.parse, meta=meta, headers=self.headers)

            if len(link) > 3:
                meta['pagination'] = "vertical"
                next_page = self.get_next_page_url(self.page, meta)
                yield scrapy.Request(next_page, callback=self.parse, meta=meta, headers=self.headers)


    def parse(self, response):
        meta = response.meta
        scenes = self.get_scenes(response)
        count = 0
        for scene in scenes:
            count += 1
            yield scene
        if count:
            if 'page' in response.meta and response.meta['page'] < self.limit_pages:
                meta['page'] = meta['page'] + 1
                print('NEXT PAGE: ' + str(meta['page']))
                yield scrapy.Request(url=self.get_next_page_url(meta['page'], meta), callback=self.parse, meta=meta, headers=self.headers)

    def get_next_page_url(self, page, meta):
        if meta['pagination'] == "vertical":
            link = f"https://www.manyvids.com/bff/store/videos/{meta['siteid']}/?page={page}&vertical=1"
        else:
            link = f"https://www.manyvids.com/bff/store/videos/{meta['siteid']}/?page={page}"
        return link

    def get_scenes(self, response):
        meta = response.meta
        jsondata = json.loads(response.text)
        if "data" in jsondata and jsondata['data']:
            data = jsondata['data']
            for jsonentry in data:
                meta['id'] = jsonentry['id']
                meta['title'] = string.capwords(html.unescape(jsonentry['title']))
                scenelink = f"https://www.manyvids.com/bff/store/video/{meta['id']}"
                if meta['id']:
                    # ~ print(meta)
                    yield scrapy.Request(scenelink, callback=self.parse_scene, meta=meta)

    def get_performers(self, response):
        meta = response.meta
        if meta['parse_performer']:
            performer = re.search(r'Manyvids:(.*)$', meta['site']).group(1).strip()
            return [performer]
        else:
            if meta['site'] == "Cattie":
                return ['Cattie Candescent']
            if "VicaTS" in meta['site']:
                return ['Victoria Gar', 'Milla']
            if "Brandibabes" in meta['site']:
                return ['Brandi Babes']
            if "Gogofukmexxx" in meta['site']:
                return ['Gogo Fukme']
            if "FreyaJade" in meta['site']:
                return ['Freya Jade']
            if "420SexTime" in meta['site']:
                return ['Asteria']
            if "RocketPowersXXX" in meta['site']:
                return ['Rocket Powers']
            if "Queen Zara Sutra" in meta['site']:
                return ['Zara Sutra']
            if "MarySweetCherry" in meta['site']:
                return ['Mary Cherry']
            if "Miss_Vexx" in meta['site']:
                return ['Alexandra Vexx']
            if "OhItsEmmaRose" in meta['site']:
                return ['Emma Rose']
            if "OmankoVivi" in meta['site']:
                return ['Omanko Vivi']
            if "RhiannonRyder1995" in meta['site']:
                return ['Rhiannon Ryder']
            if "Kiittenymph" in meta['site']:
                return ['Lex Kiittenymph']
            if "Misscjmiles" in meta['site']:
                return ['CJ Miles']
            if "Aathenatheslut" in meta['site']:
                return ['Athena May']
            if "AliceNZ" in meta['site']:
                return ['MissAlice']
            if "Ecchievement" in meta['site']:
                return ['Jane Helsing']
            if "BaileyLove6969" in meta['site']:
                return ['Bailey Love']
            if "Brett TylerXXX" in meta['site']:
                return ['Brett Tyler']
            if "Manyvids: Cattie" in meta['site']:
                return ['Cattie Candescent']
            if "Cherry Fae" in meta['site']:
                return ['Krystal Orchid']
            if "JazminTorresBBW" in meta['site']:
                return ['Jazmin Torres']
            if "CuckoldingMILF" in meta['site']:
                return ['Mila Rose']
            if "CutieElly" in meta['site']:
                return ['Hot Cum Challenge']
            if "Danny Blaq Videos" in meta['site']:
                return ['Danny Blaq']
            if "Dinkybum" in meta['site']:
                return ['Didi Demure']
            if "DirtyGardenGirl" in meta['site']:
                return ['Donna Flower']
            if "Doschers Production" in meta['site']:
                return ['Black Ghost']
            if "Dotadasp" in meta['site']:
                return ['Muniky Flor']
            if "FFeZine" in meta['site']:
                return ['UnicornDisney21']
            if "Elunaxc" in meta['site']:
                return ['Jade Skyee']
            if "Fiery Redhead" in meta['site']:
                return ['Fiery Cassie']
            if "FitSid" in meta['site']:
                return ['Fit Sidney']
            if "ForbiddenFruitsFilms" in meta['site']:
                return ['Jodi West']
            if "Funaussiecouple" in meta['site']:
                return ['Goddess Mercy']
            if "Goddess Tangent" in meta['site']:
                return ['Tangent']
            if "HannahJames710" in meta['site']:
                return ['Hannah James']
            if "Hannibal Damage" in meta['site']:
                return ['Cam Damage']
            if "Hottalicia1" in meta['site']:
                return ['Hott Alicia']
            if "Hotwife Heidi Haze" in meta['site']:
                return ['Heidi Haze']
            if "ItsReeseRobins" in meta['site']:
                return ['Reese Robbins']
            if "KalicoKats" in meta['site']:
                return ['Destination Kat', 'KatsCalico']
            if "Karabella" in meta['site']:
                return ['Kayden Harley']
            if "KarmannAndJosie" in meta['site']:
                return ['Josie', 'Karmann']
            if "Katilingus" in meta['site']:
                return ['Kat Danz']
            if "Katy_Ann_XO" in meta['site']:
                return ['Katy Ann']
            if "MaryVincXXX" in meta['site']:
                return ['Maria Romanova']
            if "Playfulsolesandtoes" in meta['site']:
                return ['Lady Waverly']
            if "LilyGaia" in meta['site']:
                return ['Lily Ivy']
            if "Mymindbreaks" in meta['site']:
                return ['RiRi']
            if "Missvioletstarr" in meta['site']:
                return ['Violet Starr']
            if "Nikkiandleigh" in meta['site']:
                return ['Nikki Hearts']
            if "Nalabrooksxxx" in meta['site']:
                return ['Nala Brooks']
            if "OnlyOneRhonda" in meta['site']:
                return ['Rhonda']
            if "PocketRocketMimi" in meta['site']:
                return ['Mimi P']
            if "Puertorockxxx20" in meta['site']:
                return ['Puerto Rock']
            if "PurpleHailStorm" in meta['site']:
                return ['Sara Storm']
            if "OUSweetheart" in meta['site']:
                return ['Summer Hart']
            if "SaintVirginPro" in meta['site']:
                return ['Liza Virgin']
            if "ScarletteD_xo" in meta['site']:
                return ['Scarlette D']
            if "Senorita Satan" in meta['site']:
                return ['Chloe Temple']
            if "TheSophieJames" in meta['site']:
                return ['Sophie James']
            if "TheStartOfUs" in meta['site']:
                return ['Adhara Skai']
            if "TheLedaLotharia" in meta['site']:
                return ['Leda Lotharia']
            if "TheFleshMechanic" in meta['site']:
                return ['The Flesh Mechanic']
            if "Theangelyoungs" in meta['site']:
                return ['Angel Youngs']
            if "TheLunaLain" in meta['site']:
                return ['Luna Lain']
            if "THEYLOVEFLAXK" in meta['site']:
                return ['They Love Flaxk']
            if "tgirloneguy" in meta['site'].lower():
                return ['Kendall Penny']
            if "ThisIsFuckingFun" in meta['site']:
                return ['Eli']
            if "Vince May" in meta['site']:
                return ['Vince May']
            if "Vera1995" in meta['site']:
                return ['Vera']
            if "Yourboyfcisco" in meta['site']:
                performers = ['Troy Francisco']
                title = meta['title']
                if title and ":" in title:
                    title = re.search(r'.*:(.*?)$', title)
                    if title:
                        title = title.group(1)
                        title = title.lower().replace("&amp;", "&").replace(" and ", "&").replace(",", "&")
                        performer_list = title.split("&")
                        for performer in performer_list:
                            if " pt" in performer:
                                performer = re.search(r'(.*) pt', performer).group(1)
                            if " part" in performer:
                                performer = re.search(r'(.*) part', performer).group(1)
                            performers.append(performer)
                        performers = list(map(lambda x: self.cleanup_title(x.strip()), performers))
                        return performers

            if "YourLittleAngel" in meta['site']:
                return ['Katie Darling']
            if "Winterxxdoll" in meta['site']:
                return ['Winter Doll']
        return []

    def get_site(self, response):
        meta = response.meta
        if meta['site']:
            return meta['site']
        return "Manyvids"

    def get_parent(self, response):
        meta = response.meta
        if meta['site']:
            if "Manyvids" in meta['site']:
                return "Manyvids"
            return meta['site']
        return "Manyvids"

    def get_network(self, response):
        return "Manyvids"

    def parse_tags(self, tags):
        re_outer = re.compile(r'([^A-Z ])([A-Z])')
        re_inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
        tags2 = []
        for tag in tags:
            tag = re_outer.sub(r'\1 \2', re_inner.sub(r' \1\2', tag))
            tags2.append(tag)
        return tags2

    def parse_scene(self, response):
        if response.status not in [403]:
            item = SceneItem()
            meta = response.meta
            jsondata = json.loads(response.text)
            jsondata = jsondata['data']
            item['title'] = meta['title']
            item['id'] = meta['id']
            if 'description' in jsondata:
                item['description'] = jsondata['description'].replace("\n", " ").replace("\r", " ").replace("\t", " ")
            else:
                item['description'] = ""
            if "tags" in jsondata:
                item['tags'] = jsondata['tags']
            else:
                item['tags'] = []
            if "tagList" in jsondata and jsondata['tagList']:
                for tag in jsondata['tagList']:
                    item['tags'].append(tag['label'])

            item['tags'] = self.parse_tags(item['tags'])

            if "screenshot" in jsondata:
                item['image'] = jsondata['screenshot'].replace(" ", "%20")
                item['image_blob'] = self.get_image_blob_from_link(item['image'])
                item['image'] = re.sub(r'(.*)(\.\w{3,4})$', r'\1_1\2', item['image'])
            else:
                item['image'] = ''
                item['image_blob'] = ''
            item['date'] = jsondata['launchDate']
            item['trailer'] = None
            item['type'] = 'Scene'
            item['network'] = "Manyvids"
            item['performers'] = self.get_performers(response)
            item['site'] = self.get_site(response)
            item['parent'] = self.get_parent(response)
            item['url'] = "https://www.manyvids.com" + jsondata['url']
            if "videoDuration" in jsondata and jsondata['videoDuration']:
                if ":" in jsondata['videoDuration']:
                    duration = re.search(r'(\d{1,2}:\d{1,2}:?\d{1,2}?)', jsondata['videoDuration'])
                    item['duration'] = self.duration_to_seconds(duration.group(1))
                elif jsondata['videoDuration']:
                    duration = int(jsondata['videoDuration'])
                    if duration:
                        item['duration'] = str(duration * 60)
            else:
                item['duration'] = ""
            parse_scene = True
            if "eastcoastxxx" in item['site'].lower():
                matches = ['-free', '-tube', 'free-preview', 'free preview', '-teaser']
                if any(x in item['url'].lower() for x in matches):
                    parse_scene = False
            if parse_scene:
                yield self.check_item(item, self.days)
