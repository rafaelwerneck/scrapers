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


class NetworkManyVidsV2_10Spider(BaseSceneScraper):

    start_urls = [
        ['Manyvids: MyAsianGF', False, '1008083027'],
        ['Manyvids: Mylene', True, '620931'],
        ['Manyvids: MyLittleSwallow', True, '1004225528'],
        ['Manyvids: Mymindbreaks', False, '1002745086'],
        ['Manyvids: MZ NORMA STITZ', True, '1001723300'],
        ['Manyvids: Nalabrooksxxx', False, '1005934130'],
        ['Manyvids: Naomi Foxxx', True, '1005164499'],
        ['Manyvids: Natalia Grey', True, '69353'],
        ['Manyvids: Natalie Mars', True, '1000035308'],
        ['Manyvids: Natalie Mars', True, '1000035308'],
        ['Manyvids: Natalie Wonder', True, '1001768929'],
        ['Manyvids: Natasha Nice', True, '1000592171'],
        ['Manyvids: Natasha Nixx', True, '1002393375'],
        ['Manyvids: Natasha_4_love', True, '1003022080'],
        ['Manyvids: Natashas Bedroom', False, '375403'],
        ['Manyvids: NatashaTy9', True, '1001777859'],
        ['Manyvids: Naughty Midwest Girls', False, '518153'],
        ['Manyvids: NaughtyBonnie69', True, '1007210480'],
        ['Manyvids: NaughtyBoyPOV', False, '454725'],
        ['Manyvids: Nick Winter', True, '1005220898'],
        ['Manyvids: Nicole Belle', True, '1000182655'],
        ['Manyvids: Nicole Cheshire', True, '1004383440'],
        ['Manyvids: Nicole Doshi', True, '1002698505'],
        ['Manyvids: Nicole Kitt', True, '1004219823'],
        ['Manyvids: Nicole Nabors', True, '1002818112'],
        ['Manyvids: Nicole Riley', True, '30108'],
        ['Manyvids: Nicolebun', True, '1003188552'],
        ['Manyvids: Nicolette Bloom', True, '1005323080'],
        ['Manyvids: Nikita Belle', True, '1002437812'],
        ['Manyvids: Nikki Hugs', True, '1003352035'],
        ['Manyvids: Nikkiandleigh', False, '1000199434'],
        ['Manyvids: NikkiMagic', True, '1002937596'],
        ['Manyvids: Nina Crowne', True, '196659'],
        ['Manyvids: Ninacola', True, '1004836982'],
        ['Manyvids: Ninadoll', True, '113109'],
        ['Manyvids: Nivia Wolfe', True, '1001457753'],
        ['Manyvids: Nixlynka', True, '1002349390'],
        ['Manyvids: nokithai', True, '1006200966'],
        ['Manyvids: noramakesporn', True, '1001231266'],
        ['Manyvids: noratheo', True, '1003491188'],
        ['Manyvids: Nova Patra', True, '407165'],
        ['Manyvids: Numi R', True, '1000071471'],
        ['Manyvids: Nymph_Candy', True, '1005541669'],
        ['Manyvids: Nyxi Leon', True, '1000696554'],
        ['Manyvids: Octokuro', True, '1003906145'],
        ['Manyvids: ohaiNaomi', True, '115565'],
        ['Manyvids: OhItsEmmaRose', False, '1003513574'],
        ['Manyvids: Olive Glass', True, '1005338874'],
        ['Manyvids: Olive Wood', True, '124871'],
        ['Manyvids: Olivia Jay', True, '1003730153'],
        ['Manyvids: Olivia Robin', True, '1003562970'],
        ['Manyvids: Olivia Young', True, '149290'],
        ['Manyvids: OmankoVivi', False, '217682'],
        ['Manyvids: Ondrea Lee', True, '1000452244'],
        ['Manyvids: OnlyMikeWilliams', True, '1006548979'],
        ['Manyvids: OnlyOneRhonda', True, '1002756755'],
        ['Manyvids: Onlyping', True, '1006754211'],
        ['Manyvids: oopepperoo', True, '83782'],
        ['Manyvids: Oralsonly', False, '1002463312'],
        ['Manyvids: OUSweetheart', False, '106308'],
        ['Manyvids: OUSweetheart', True, '106308'],
        ['Manyvids: Owen Gray', True, '184119'],
        ['Manyvids: Paige Steele', True, '1001123043'],
        ['Manyvids: Panamero 088', True, '1008261778'],
        ['Manyvids: Patrappa', True, '1001799554'],
        ['Manyvids: Paypeaches', True, '173770'],
        ['Manyvids: Peachy Riya', True, '1002335610'],
        ['Manyvids: Peachy Skye', True, '1002980475'],
        ['Manyvids: peachycatsnack', True, '1005444885'],
        ['Manyvids: Peachypoppy', True, '1004271325'],
        ['Manyvids: peachypoppy', True, '1004271325'],
        ['Manyvids: Pearl Sage', True, '1001978110'],
        ['Manyvids: Penny Barber', True, '147843'],
        ['Manyvids: Penny Loren', True, '1003964373'],
        ['Manyvids: Pepper Kat', True, '1006003794']
    ]

    name = 'ManyVidsV2_10'

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
