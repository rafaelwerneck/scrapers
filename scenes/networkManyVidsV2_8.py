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


class NetworkManyVidsV2_8Spider(BaseSceneScraper):

    start_urls = [
        ['Manyvids: lenapolanski', True, '1008201765'],
        ['Manyvids: Lenorebunny', True, '1004313020'],
        ['Manyvids: LeoLulu', True, '1000585143'],
        ['Manyvids: Lev Lieben', True, '1005748422'],
        ['Manyvids: Lewdest Bunnie', True, '1005049819'],
        ['Manyvids: Lexa Lite', True, '1002827259'],
        ['Manyvids: Lexi Lore', True, '1001311376'],
        ['Manyvids: Lexia Lynx', True, '1000560155'],
        ['Manyvids: Lexia Lynx', True, '1000560155'],
        ['Manyvids: Lexxxi Luxe', True, '826394'],
        ['Manyvids: Lia Lennice', True, '1003079099'],
        ['Manyvids: Lilcanadiangirl', True, '683542'],
        ['Manyvids: lilcanadiangirl', True, '683542'],
        ['Manyvids: Lilijunex', True, '1006854117'],
        ['Manyvids: Lilith Petite', True, '1000322028'],
        ['Manyvids: LilRedVelvet', True, '1002065207'],
        ['Manyvids: Lily DeMure', True, '1001103504'],
        ['Manyvids: Lily Fox', True, '1006055071'],
        ['Manyvids: LilyGaia', False, '301576'],
        ['Manyvids: Lilyiskawaii', True, '1003844153'],
        ['Manyvids: LilyLoveles', True, '1002028291'],
        ['Manyvids: Lindsey Leigh', True, '481862'],
        ['Manyvids: Lisa the Succubrat', True, '1001433106'],
        ['Manyvids: Lissie Belle', True, '549738'],
        ['Manyvids: Little Miss Elle', True, '65933'],
        ['Manyvids: Little Puck', True, '419692'],
        ['Manyvids: LittleBunnyB', True, '1003962281'],
        ['Manyvids: LittleMouchette', True, '1006811545'],
        ['Manyvids: Littleponywife', True, '1006368600'],
        ['Manyvids: Littleredheadlisa', True, '1003426440'],
        ['Manyvids: LittleSubGirl', True, '358347'],
        ['Manyvids: Liz Raw', True, '1002632960'],
        ['Manyvids: Lola James', True, '1005990787'],
        ['Manyvids: Lola Rose', True, '1001106526'],
        ['Manyvids: Lola Tessa', True, '1001749834'],
        ['Manyvids: Lolliepopxxx', True, '1004243105'],
        ['Manyvids: Long Toe Sally', True, '1001734618'],
        ['Manyvids: LongHairLuna', True, '1004473027'],
        ['Manyvids: Loollypop24', True, '388869'],
        ['Manyvids: Lora Cross', True, '1002502469'],
        ['Manyvids: Lora Cross', True, '1002502469'],
        ['Manyvids: Lore Shane', True, '1001880948'],
        ['Manyvids: Loren Aprile', True, '1004728288'],
        ['Manyvids: Lorena Brink', True, '1000055009'],
        ['Manyvids: Lorena Brink', True, '1000055009'],
        ['Manyvids: Loretta Rose', True, '556632'],
        ['Manyvids: Loupanxxx', True, '1003128949'],
        ['Manyvids: Lourdes Noir', True, '1001422207'],
        ['Manyvids: Lovely Lilith', True, '105450'],
        ['Manyvids: Luci Power', True, '1002527111'],
        ['Manyvids: Lucy Alexandra', True, '1001339090'],
        ['Manyvids: Lucy Hyde', True, '1001152130'],
        ['Manyvids: Lucy Mochi', True, '1004503279'],
        ['Manyvids: Lucyy Avery', True, '451005'],
        ['Manyvids: Luiza Marcato', True, '1004862068'],
        ['Manyvids: Luke Cooper', True, '1003079493'],
        ['Manyvids: Lulu Blue x', True, '590554'],
        ['Manyvids: Luna Kyzz', True, '750209'],
        ['Manyvids: Luna Nyx', True, '1004858060'],
        ['Manyvids: Luna Roulette', True, '1002865441'],
        ['Manyvids: Lusciousx Luci', True, '1004732742'],
        ['Manyvids: Lydiagh0st', True, '1002402449'],
        ['Manyvids: Lyra Fae', True, '231529'],
        ['Manyvids: Lyra Fae', True, '231529'],
        ['Manyvids: Maasai Warrior BBC', True, '1006713480'],
        ['Manyvids: MadBros', False, '1007147288'],
        ['Manyvids: Made In Canarias', True, '1000567799'],
        ['Manyvids: Madiiitay', True, '1004382358'],
        ['Manyvids: Madison Volt', True, '1002671662'],
        ['Manyvids: madisynwood', True, '1005851612'],
        ['Manyvids: Maggie Landrin', True, '1002621924'],
        ['Manyvids: Maggie Rose xo', True, '1004575017'],
        ['Manyvids: Makayla Divine', True, '257117'],
        ['Manyvids: Mama Fiona', True, '1002612831'],
        ['Manyvids: Mandy Lohr', True, '297983']
    ]

    name = 'ManyVidsV2_8'

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
