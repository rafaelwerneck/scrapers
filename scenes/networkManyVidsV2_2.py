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


class NetworkManyVidsV2_2Spider(BaseSceneScraper):

    start_urls = [
        ['Manyvids: ArgenDana', True, '1000732526'],
        ['Manyvids: Aria Allure', True, '1001620152'],
        ['Manyvids: AriaNicoleXXX', True, '1006336627'],
        ['Manyvids: Ariel Anderssen', True, '454058'],
        ['Manyvids: ArinaFox', True, '1005789601'],
        ['Manyvids: ARTEM SUCHKOV', True, '1004492966'],
        ['Manyvids: Ashe Maree', True, '666099'],
        ['Manyvids: Ashley Alban', True, '102036'],
        ['Manyvids: Ashley Aoki', True, '1001127010'],
        ['Manyvids: Asia Drake', True, '1002663330'],
        ['Manyvids: Asianbbcluvr', True, '1005194704'],
        ['Manyvids: AsiaXXXTour', False, '1004942285'],
        ['Manyvids: ASMRMaddy', True, '1004334654'],
        ['Manyvids: Athena Blaze', True, '4043'],
        ['Manyvids: AudreyReid', True, '1008673774'],
        ['Manyvids: August Skye', True, '1004206736'],
        ['Manyvids: Aurora Angel', True, '1004044394'],
        ['Manyvids: AuroraXoxo', True, '494106'],
        ['Manyvids: AvanelleJules', True, '1005755337'],
        ['Manyvids: AvaZev', True, '1008074349'],
        ['Manyvids: Aysha Paige', True, '1006744158'],
        ['Manyvids: Ayumi Anime', True, '1000907145'],
        ['Manyvids: Ayumikichi', True, '1006374960', 'Vertical'],
        ['Manyvids: Azumi Zeitline', True, '1003971662'],
        ['Manyvids: Azure Sky Films', False, '1001644775'],
        ['Manyvids: Babesafreak', True, '1004577792'],
        ['Manyvids: babychester', True, '1001336064'],
        ['Manyvids: Babygirlhazel', True, '796862'],
        ['Manyvids: Babykittyp', True, '1006603670'],
        ['Manyvids: Backdoorgf', True, '1007261232'],
        ['Manyvids: Bad Dolly', True, '1000030336'],
        ['Manyvids: Baddiesonlypov', False, '1005032015'],
        ['Manyvids: BadDragonSlayer', True, '1002931153'],
        ['Manyvids: BaileyLove6969', False, '1000594124'],
        ['Manyvids: Balenci Bby', True, '1006527632'],
        ['Manyvids: Bambii Mercedes', True, '1000333268'],
        ['Manyvids: BangedProductionsXXX', False, '1001618574'],
        ['Manyvids: Baxters Blowies', False, '1004417786'],
        ['Manyvids: BBC Worldwide', True, '1003626645'],
        ['Manyvids: bbybimbogamer', True, '1007319325'],
        ['Manyvids: Bea York', True, '1000611142'],
        ['Manyvids: Bea York', True, '1000611142'],
        ['Manyvids: Bella Bates', True, '1004323423'],
        ['Manyvids: Bettie Bondage', True, '590705'],
        ['Manyvids: Bianca Beauchamp', True, '8821'],
        ['Manyvids: Billy Boston', True, '1001072949'],
        ['Manyvids: BirdyLovesIt', True, '246789'],
        ['Manyvids: BlackpantherXXX', True, '1001027504'],
        ['Manyvids: Blake Blossom', True, '1003638619'],
        ['Manyvids: Blazed Brat', True, '1002996067'],
        ['Manyvids: Blissed XXX', False, '1000324638'],
        ['Manyvids: Blondelashes19', True, '1001067347'],
        ['Manyvids: BlowbyBlowAccts', False, '419500'],
        ['Manyvids: Blowketing', False, '1007848193'],
        ['Manyvids: BlowRayne', True, '1004052738'],
        ['Manyvids: Bluberrydreams', True, '1004835717'],
        ['Manyvids: Blue Dream', True, '752777'],
        ['Manyvids: Bluelah', True, '1005445063'],
        ['Manyvids: Boba_Bitch', True, '1003445334'],
        ['Manyvids: Bondagio', False, '1005448400'],
        ['Manyvids: Bosslady808', True, '1007877241'],
        ['Manyvids: Brad Newman XXX', True, '1001824648'],
        ['Manyvids: Brandibabes', False, '1003828607'],
        ['Manyvids: Bratty Lindsay', True, '1002606297'],
        ['Manyvids: Brazilian Girl', True, '1003088114'],
        ['Manyvids: Brea Rose', True, '1000024307'],
        ['Manyvids: Brea Rose', True, '1000024307'],
        ['Manyvids: Break Her In', False, '1003373430'],
        ['Manyvids: Brett TylerXXX', False, '1004700026'],
        ['Manyvids: Brickzilla', True, '1002868779'],
        ['Manyvids: Britney Amber', True, '1003387859'],
        ['Manyvids: Brittanythingoz', True, '1006754881'],
        ['Manyvids: Brooke Dillinger', True, '376796'],
        ['Manyvids: Brookelynne Briar', True, '48084'],
        ['Manyvids: Brooklyn Springvalley', True, '1001853938']
    ]

    name = 'ManyVidsV2_2'

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
