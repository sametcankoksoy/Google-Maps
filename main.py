from seleniumbase import SB
from lxml import html
import pandas as pd 
from itertools import zip_longest
import json,csv

with SB(uc=True,incognito=True,test=True,locale='en') as sb:
    sb.open('https://www.google.com/maps/search/taksim+barlar/@41.0322737,28.975409,15.75z?entry=ttu&g_ep=EgoyMDI1MDcyMC4wIKXMDSoASAFQAw%3D%3D?hl=en')

    scroll_box = sb.find_element('div[role="feed"]')
    data_list = []

    while True:
        if sb.is_element_visible("span.HlvSq"):
            tree = html.fromstring(sb.get_page_source())

            name = tree.xpath('//div[@class="NrDZNb"]/div[2]/text()')
            ratings = tree.xpath('//span[@class="ZkP5Je"]/@aria-label')
            status = tree.xpath('//div[@class="W4Efsd"]/span//span[contains(text(), "Kapalı") or contains(text(), "Açık") or contains(text(),"Açılmak üzere") or contains(text(),"Kapanmak üzere") or contains(text(),"24 saat açık")]/text()')
            opening_time = tree.xpath('//div[@class="W4Efsd"]//span[@style="font-weight: 400;"]/text()')
            venue_type = tree.xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div/div/div[2]/div[4]/div[1]/div/div/div[2]/div[4]/div[1]/span[1]/span/text()')
            url= tree.xpath('//div[@class="Nv2PK THOPZb CpccDe "]/a/@href')
            
            for a,b,c,d,e,f in zip_longest(name,ratings,status,opening_time,venue_type,url,fillvalue='-'):
                data = {
                    'Name':a.strip(),
                    'Rating': b.strip(),
                    'Status':c.strip(),
                    'Opening/Closing Time':d.strip(),
                    'Venue Type': e.strip(),
                    'Url': f.strip()
                }
                data_list.append(data)
            

            break
    
        sb.execute_script("arguments[0].scrollTop += 150", scroll_box)
        sb.sleep(2)

    with open("maps.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data_list[0].keys())
        writer.writeheader()
        writer.writerows(data_list)

