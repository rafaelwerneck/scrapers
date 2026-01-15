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


class NetworkManyVidsV2_14Spider(BaseSceneScraper):

    start_urls = [
        ['Manyvids: Violet Myers', True, '1002190635'],
        ['Manyvids: Virgo Peridot', True, '176608'],
        ['Manyvids: Visceratio', True, '1000775087'],
        ['Manyvids: Vitaduplez', True, '1003468856'],
        ['Manyvids: Vixenxmoon', True, '1001075493'],
        ['Manyvids: Wagabang', False, '1006541429'],
        ['Manyvids: WCA Productions', False, '602138'],
        ['Manyvids: webtolove', True, '1004633725'],
        ['Manyvids: Wendy Summers', True, '1000912164'],
        ['Manyvids: Wendy Warrior', True, '761263'],
        ['Manyvids: WetZemu', True, '1002818162'],
        ['Manyvids: Winterxxdoll', False, '1004591966'],
        ['Manyvids: WreccItRalph', True, '1006338300'],
        ['Manyvids: x_Luna_x', True, '1006971945'],
        ['Manyvids: Xoxolane', True, '1005604015'],
        ['Manyvids: xPrincessAura', True, '1001967166'],
        ['Manyvids: xxbebegrrlxx', True, '1002245098'],
        ['Manyvids: xxNaughtyGirlxx', True, '1001631391'],
        ['Manyvids: xxxCaligulaxxx', True, '150576'],
        ['Manyvids: xxxmultimediacom', False, '1001803967'],
        ['Manyvids: Yasmina Khan', True, '1006840318'],
        ['Manyvids: Yesimcheta', True, '1004914470'],
        ['Manyvids: Yessy D Waifu', True, '1007827546'],
        ['Manyvids: Yogabella', True, '1001244409'],
        ['Manyvids: Youngandadorbs', True, '1000964738'],
        ['Manyvids: Your_Father_Secret', True, '1004654702'],
        ['Manyvids: Yourboyfcisco', False, '1002986872'],
        ['Manyvids: yourgirlnextdoor', True, '1008423521'],
        ['Manyvids: YourLittleAngel', False, '1001186725'],
        ['Manyvids: Yui Peachpie', True, '1006316998'],
        ['Manyvids: Zac Wild', True, '1002955920'],
        ['Manyvids: Zara Sutra', True, '374487'],
        ['Manyvids: Zaria Stone', True, '1003771650'],
        ['Manyvids: ZIAxBITE', True, '1001721841'],
        ['Manyvids: Zirael Rem', True, '1002067521'],
        ['Manyvids: zivafey', True, '1001812120'],
        ['Manyvids: Zuzu Flowers', True, '1004604738'],
        ['MySweetApple', False, '423053'],
        ['Natalia Grey', False, '69353'],
        ['Sloppy Toppy', False, '1002638751'],
        ['Undercover Sluts', False, '1001483477'],
        ['YouthLust', False, '1001216419'],
        ['Manyvids: Cullenscuties', False, '1001105385'],
        ['Manyvids: Tiffany Flowers', True, '1007744280'],
        ['Manyvids: Alfiecinematic', False, '1007709627'],
        ['Manyvids: Gabby Stone', True, '1006663800'],
        ['Manyvids: Stephie Scarlet', True, '1000311150'],
        ['Manyvids: CupcakeUS', True, '1004897159'],
        ['Manyvids: Trulybyl', True, '1005013752'],
        ['Manyvids: Skylar Snow', True, '1000937585'],
        ['Manyvids: Riley Reign', True, '1005229984'],
        ['Manyvids: Lianna Lawson', True, '1000108329'],
        ['Manyvids: Meddle Blooms', True, '1007156262'],
        ['Manyvids: SemajXL', True, '1005089378'],
        ['Manyvids: Luna Lovelace', True, '1004796137'],
        ['Manyvids: Finny Fox', True, '1002809912'],
        ['Manyvids: itsloMFC', True, '1004392633'],
        ['Manyvids: Purosanguelucas', True, '1008810280'],
        ['Manyvids: Bigbootyandbeast10', False, '1005196355'],
        ['Manyvids: Jason Sweets', True, '1003620057'],
        ['Manyvids: Realpollypocket', True, '1004466870'],
        ['Manyvids: DCTrousersnakeXXX', True, '1007921628'],
        ['Manyvids: SLOPPY TEENS', False, '1001672444'],
        ['Manyvids: JuliaGoddess', True, '1004111161'],
        ['Manyvids: Daddys Sluts', False, '1000706151'],
        ['Manyvids: Stacy Pipedream', True, '1010240085'],
        ['Manyvids: Sloppy Teens', False, '1001672444'],
        ['Manyvids: Tony Rubino', True, '1001000668'],
        ['Manyvids: Fiona Mommy', True, '1008644744'],
        ['Manyvids: Divinebabe', True, '1005206763'],
        ['Manyvids: Rissa Rae', True, '1004234102'],
        ['Manyvids: Zoweybunny', True, '1009373839'],
        ['Manyvids: Glitterqueen1999', True, '1004246725'],
        ['Manyvids: Naughty Jemm', True, '1008504515'],
        ['Manyvids: Loreena Fox', True, '1008025324'],
        ['Manyvids: Ivy Wild', True, '1003824516'],
        ['Manyvids: Harley Taboo', True, '1006671930'],
        ['Manyvids: Kylee Nash', True, '131433'],
        ['Manyvids: CALAMITYSHERE', True, '1006561636'],
        ['Manyvids: Vince Karter', True, '1000948867'],
        ['Manyvids: PerfectStrokeMD', False, '1009761021'],
        ['Manyvids: Alex Adams Media', False, '1000176068'],
        ['Manyvids: Jennathestarr', False, '1005508934'],
        ['Manyvids: Melztube', True, '1007038073'],
        ['Manyvids: Chastity Charli', True, '1007978676'],
        ['Manyvids: Lexi Lela', True, '1004755812'],
        ['Manyvids: Skye Blue', True, '1000165264'],
        ['Manyvids: Trans Focus', True, '696072'],
        ['Manyvids: Kaethebrat', True, '1004999403'],
        ['Manyvids: GiGiLysettee', True, '1010538705'],
        ['Manyvids: Max Cartel', True, '1005746289'],
        ['Manyvids: Savannah Bond', True, '1002594101'],
        # ['Manyvids: ', True, ''],
        # ['Manyvids: ', True, ''],
        # ['Manyvids: ', True, ''],
        # ['Manyvids: ', True, ''],
    ]

    name = 'ManyVidsV2_14'

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
            if "Jennathestarr" in meta['site']:
                return ['Jenna Starr']
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
            if "Bigbootyandbeast10" in meta['site']:
                return ['Hotwife Peaches', 'Big Danny']
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
