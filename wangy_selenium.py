# coding = "utf8"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from pyquery import PyQuery as pq
from lxml import etree
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class sele_try():
    def __init__(self):
        self.cli =pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.collection = self.cli["first_mongo"]["nihao"]
        # self.url = "https://music.163.com/#/playlist?id=2459233702"

    def get_page_content(self,url_li):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        for url in url_li:
            # dr = webdriver.Chrome()
            dr = webdriver.Chrome(chrome_options=chrome_options)
            wait = WebDriverWait(dr, 10)
            dr.get(url)
            dr.switch_to.frame("g_iframe")
            html = etree.HTML(dr.page_source)
            total = "".join(html.xpath("//div[@class='m-cmmt']/div[3]/div/a[last()-1]/text()"))
            if total :
                total = int(total)
            else:#只有一页时
                total = 0
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='itm']")))
                    html = etree.HTML(dr.page_source)
                    # print(etree.tostring(html))
                    song_name = "".join(html.xpath("//em[@class = 'f-ff2']/text()"))
                    song_singer = "".join(html.xpath("//p[@class = 'des s-fc4']/span/a[@class = 's-fc7']/text()"))
                    # song_album = "".join(html.xpath("//p[@class='s-fc7']/text()"))
                    comments = html.xpath("//div[@class='cmmts j-flag']/div")
                    for each in comments:
                        song_item = {}
                        song_item["song_singer"] = song_singer
                        # song_item["song_album"] =song_album
                        song_item["song_name"] = song_name
                        song_item["comment_author_id"] = "".join(each.xpath(".//div[@class = 'head']/a/@href"))
                        song_item["comment_author_name"] = "".join(
                            each.xpath(".//div[@class = 'cntwrap']//div[@class = 'cnt f-brk']/a/text()"))
                        song_item["comment_time"] = "".join(each.xpath(".//div[@class = 'time s-fc4']/text()"))
                        tmp = "".join(each.xpath(".//div[@class='rp']/a[1]/text()"))
                        if tmp:
                            song_item["comment_likes"] = re.compile("(\d+)").search(tmp).group()
                        else:
                            song_item["comment_likes"] = '0'
                        song_item["comment_content"] = "".join(each.xpath(".//div[@class = 'cnt f-brk']/text()"))
                        song_item["comment_inner_content"] = "".join(each.xpath(".//a[@class = 's-fc7']/text()"))
                        print(song_item)
                        self.collection.insert(song_item)
                    dr.close()
                except:
                    dr.close()
                    pass
            print(total)

            for i in range(total):
                # dr.switch_to.frame("g_iframe")
                choose_page = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='m-cmmt']/div[3]/div/a[last()]")))
                choose_page.send_keys(Keys.ENTER)
                # time.sleep(1)
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='itm']")))
                html = etree.HTML(dr.page_source)
                # print(etree.tostring(html))
                song_name =html.xpath("//em[@class = 'f-ff2']/text()")[0]

                song_singer ="".join(html.xpath("//p[@class = 'des s-fc4']/span/a[@class = 's-fc7']/text()"))
                # song_album = "".join(html.xpath("//p[@class='s-fc7']/text()"))
                comments = html.xpath("//div[@class='cmmts j-flag']/div")
                total = "".join(html.xpath("//div[@class='m-cmmt']/div[3]/div/a[last()-1]/text()"))
                for each in comments:
                    song_item = {}
                    song_item["song_singer"] = song_singer
                    # song_item["song_album"] =song_album
                    song_item["song_name"] = song_name
                    song_item["comment_author_id"] = "".join(each.xpath(".//div[@class = 'head']/a/@href"))
                    song_item["comment_author_name"] = "".join(each.xpath(".//div[@class = 'cntwrap']//div[@class = 'cnt f-brk']/a/text()"))
                    song_item["comment_time"] = "".join(each.xpath(".//div[@class = 'time s-fc4']/text()"))
                    tmp = "".join(each.xpath(".//div[@class='rp']/a[1]/text()"))
                    if tmp:
                        song_item["comment_likes"] = re.compile("(\d+)").search(tmp).group()
                    else:
                        song_item["comment_likes"] = '0'
                    song_item["comment_content"] = "".join(each.xpath(".//div[@class = 'cnt f-brk']/text()"))
                    song_item["comment_inner_content"] = "".join(each.xpath(".//a[@class = 's-fc7']/text()"))
                    print(song_item)
                    self.collection.insert(song_item)
            dr.close()

def main():
    now = sele_try()
    # urls = ["https://music.163.com/#/song?id=479223325","https://music.163.com/#/song?id=28828057","https://music.163.com/#/song?id=515501363","https://music.163.com/#/song?id=422977897","https://music.163.com/#/song?id=433103454"]
    urls = ['https://music.163.com/#/song?id=1296893537', 'https://music.163.com/#/song?id=1318004249', 'https://music.163.com/#/song?id=461650912', 'https://music.163.com/#/song?id=1312608386', 'https://music.163.com/#/song?id=563282238', 'https://music.163.com/#/song?id=422427763', 'https://music.163.com/#/song?id=1301835417', 'https://music.163.com/#/song?id=438801672', 'https://music.163.com/#/song?id=461846471', 'https://music.163.com/#/song?id=1294899063', 'https://music.163.com/#/song?id=491447490', 'https://music.163.com/#/song?id=410181330', 'https://music.163.com/#/song?id=545019506', 'https://music.163.com/#/song?id=571338279', 'https://music.163.com/#/song?id=410161216', 'https://music.163.com/#/song?id=422429636', 'https://music.163.com/#/song?id=562594267', 'https://music.163.com/#/song?id=489768079', 'https://music.163.com/#/song?id=29761124', 'https://music.163.com/#/song?id=442518503', 'https://music.163.com/#/song?id=556500742', 'https://music.163.com/#/song?id=419374177', 'https://music.163.com/#/song?id=461525011', 'https://music.163.com/#/song?id=490163629', 'https://music.163.com/#/song?id=543988388', 'https://music.163.com/#/song?id=523251118', 'https://music.163.com/#/song?id=28643203', 'https://music.163.com/#/song?id=434070771', 'https://music.163.com/#/song?id=416892296', 'https://music.163.com/#/song?id=432506367', 'https://music.163.com/#/song?id=455557328', 'https://music.163.com/#/song?id=503657885', 'https://music.163.com/#/song?id=448184048', 'https://music.163.com/#/song?id=502043537', 'https://music.163.com/#/song?id=543987400', 'https://music.163.com/#/song?id=30814948', 'https://music.163.com/#/song?id=28219407', 'https://music.163.com/#/song?id=28287010', 'https://music.163.com/#/song?id=456167591', 'https://music.163.com/#/song?id=548003394', 'https://music.163.com/#/song?id=552018701', 'https://music.163.com/#/song?id=438431324', 'https://music.163.com/#/song?id=410161204', 'https://music.163.com/#/song?id=529747142', 'https://music.163.com/#/song?id=481519556', 'https://music.163.com/#/song?id=28892385', 'https://music.163.com/#/song?id=26494530', 'https://music.163.com/#/song?id=407002483', 'https://music.163.com/#/song?id=452612088', 'https://music.163.com/#/song?id=36895430', 'https://music.163.com/#/song?id=468882985', 'https://music.163.com/#/song?id=410042104', 'https://music.163.com/#/song?id=33378325', 'https://music.163.com/#/song?id=418257910', 'https://music.163.com/#/song?id=399410918', 'https://music.163.com/#/song?id=31877581', 'https://music.163.com/#/song?id=27770540', 'https://music.163.com/#/song?id=25714352', 'https://music.163.com/#/song?id=413831749', 'https://music.163.com/#/song?id=444269912', 'https://music.163.com/#/song?id=439138075', 'https://music.163.com/#/song?id=512359558', 'https://music.163.com/#/song?id=471188016', 'https://music.163.com/#/song?id=25727660', 'https://music.163.com/#/song?id=29755058', 'https://music.163.com/#/song?id=450226742', 'https://music.163.com/#/song?id=416388594', 'https://music.163.com/#/song?id=29600714', 'https://music.163.com/#/song?id=408307966', 'https://music.163.com/#/song?id=33856567', 'https://music.163.com/#/song?id=399353380', 'https://music.163.com/#/song?id=410161283', 'https://music.163.com/#/song?id=411349440', 'https://music.163.com/#/song?id=452818051', 'https://music.163.com/#/song?id=28793052', 'https://music.163.com/#/song?id=33419432', 'https://music.163.com/#/song?id=28819878', 'https://music.163.com/#/song?id=409654891', 'https://music.163.com/#/song?id=438306457', 'https://music.163.com/#/song?id=31134170', 'https://music.163.com/#/song?id=31134193', 'https://music.163.com/#/song?id=28191532', 'https://music.163.com/#/song?id=33418862', 'https://music.163.com/#/song?id=35476734', 'https://music.163.com/#/song?id=447202288', 'https://music.163.com/#/song?id=32450986', 'https://music.163.com/#/song?id=33544375', 'https://music.163.com/#/song?id=25650033', 'https://music.163.com/#/song?id=446944022', 'https://music.163.com/#/song?id=183248', 'https://music.163.com/#/song?id=29848478', 'https://music.163.com/#/song?id=457640645']
    try:
        now.get_page_content(urls)
    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    main()