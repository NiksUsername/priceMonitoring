import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from back_scraping.utils import keepa_manager
from back_scraping.utils import links
from back_scraping.utils.discount_properties import is_big_discount

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': 'analytics_channel=ecomm; _abck=F00624B0353064CB97EE9E72FB0043F3~0~YAAQvHnKF1/mD9SNAQAAA/qdFAvMk9mVVtZhrpBX9rQ25AruU4RPGK8/ixu0ur26qz+2UFQYSazKRnLy7wlhkfg9TuJiUS0MU3Zm5dGZf+1dM1cBmbcHnfuyAnHwPql7o+7PHOPIjJTewG/0vv3b++PXKB2H0Ju5i/J6nq4dXyFtiFrPOnzkGvJOpxOq6lgtRSy60DihntJ2Y7x2R8xhasNs80XweOq6LqmQf/1p8HNimhtayaStLhReJuivc92wbTk/KCYOUf3bn4IsJHZSJjH6fiZwpCLvff+iYIEzna5/8JW4gWgcZ5eKg1RShQrsM/QhdEqv4+t9auJt9CbfG7dD8h8Lg0NS9Edq1n2DXypB0Yt2wzlliT4E7APo0UD/AyQ4tAZyJBkZP3CxKLflFOpSAuO9irMx3Ms=~-1~-1~-1; utag_main=v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:3$_se:49$_ss:0$_st:1709745846025$vapi_domain:argos.co.uk$dc_visit:3$ses_id:1709742556035%3Bexp-session$_pn:17%3Bexp-session$dc_event:46%3Bexp-session; sessionId=I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/; cisId=df3edbe5444348fb94aada50caa99e64; CONSENTMGR=consent:true%7Cts:1708004268257%7Cid:018dacfc0c9c004ff4950a12766c05050005700d00bd0; AMCV_095C467352782EB30A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19789%7CMCMID%7C87286231597634338936380337387751060019%7CMCAID%7CNONE%7CMCOPTOUT-1709751244s%7CNONE%7CvVersion%7C5.5.0; _cls_v=9da0bcf3-1541-4815-b22b-6738aa4b3584; akaas_arg_uk_global=1710953642~rv=69~id=031734d66bbfafffb2ffaaa01a3e2b87; localisationTooltip=closed; Checkout_Test_Group_2=NEW_HD|NEW_HD_SI|NEW_HD_LI; _taggstar_vid=2dca6491-d708-11ee-8214-537a6449f81f; _taggstar_exp=v:3|id:|group:; prev_vals=ar%3Acat%3Atechnology%3Avideogamesandconsoles%3Aps5%3Aps5games%3A*%7C*ar%3Acat%3A; AMCVS_095C467352782EB30A490D45%40AdobeOrg=1; ArgosPopUp_customer1In20Chance=false; _cls_s=83163b84-2088-4dce-b68c-dc371616079d:0; Bc=d:1*1_p:0*0.005_r:null*null; ufvd=~~clp_29351-e!events_easter-gifts-U!clp_29203-U!clp_29949-Ba; mdr_browser=Akamai; bm_sz=5DD834F92FFA2768F0196948A6815AC8~YAAQrHnKF193uNSNAQAAc/2YFBcyH2PqZrOOciCNQidawAD3EOP/u7y1XesyAvf6NbaSRqOlTBafaSgj7dbq8s+lNe5nF2VF4ybZCeDigfgtjtkZp0YDBxKeA1OF4bkCEiIcHV5yMt22fR4u4opsb50p5xf0kVoXrBA+TDJG7/l5FTJRbFlJBkWAuKpAYHaFZCkZ4LQijU2TRF0oJ+I15hLVaBkh7JPWjbH4+wmrdi9WmqHmOBWmfP1HlnT/JPKqATi15+DwwNQe3bArfD1zxuknGNmthrxR7IUmJQtbahwNUTEaNAXcEXKKNU7creeGKWONWEu5Gbs8sThnPkZOGnpFYTyt4OPlb1offL3kAgjZ9YZdi3ciuA==~4468792~3485749; ak_bmsc=4215E1B6C593A8688598DD9627FD0654~000000000000000000000000000000~YAAQvHnKF+DlD9SNAQAA6tudFBeukAmsssMf8XbnPWJIbEYTPMuBIyMwZ1KdrO0n/O8oepqNuNJjzXEeZJx6t9aJs2WtChbf7Anu5E4h2/+NFvaqHnXQZ9MLxVKpuiZkLzSsWRaCd5IWkhHzjaxcCWWvHB6bK71BOClRecpLcmzB7u9GafzOJxIr2h58Erz3yXa65oTA9EmdqWjSuFGeKdrl583EhcvQGwhwzHHhcHVeOzgre9C9HXTYU5kTsRXTkx0WBmHrOw9QVd1tfBcUr59zaPGwrtLxEozn+NSw4PKRN2wrvmGDfYYkQoR+afXI33Wz7XFdB6RQl42Al8/W6S4O6upuLaDLayfZwHs2rq6rgUxqsvb+utl3MrVd2LZMNC0e+n8XJpdiGRK+AEyYiPRQC5xwIICF6FRLfoG4KPdaGN7blIX/Ghz/MbXX6hO10RnAt63mbMdW5zmZpEWPUHZZAByEJRuC/CGME/NDjb8zIvSAVWZw4a2yo45jtFs613Ot19Vg4Ae9yveYHm4=; bm_sv=489F557737FDBDB0FEB7A4F125462FAF~YAAQrHnKF3yWudSNAQAAHrWvFBdzFfMFUjWKDhOQFEnQ2J6Bk06bVHeFQ6+OUme1DA4nvtez8b95GIfEnIgPhNCWk5NqBPnp9tkO+LWSE/flIAD06q+RUDTpLDaqbeF7Vs7SJn9Ah/+RnRzZEODv1vDJAd7DbXceMMdiDmagRsd0VSgJvf+cTF2ZxjiL80tTzEy/KPOzU38++NCNLH2E5eFfoA2nq6bPVIR8jtvIWfegX5GEsAt/FZTIDKmZKjb9uZc=~1; bm_mi=6EAF1C8E2815941D8F5B4C0524966061~YAAQvHnKFyvjD9SNAQAADmqdFBeaR4nFjLYC9QsjVO8blgedBsFSqWavvpZ+swf/WLshj/hKIcZsmGSB8k4gXR0/l1gdrBPHFaT0Xkh9NYNvmoHSoXDjUZpEDly3bipSx4jKi9CJR/Jz3+6mUTRFAptaxXUsNfRAKFgtV4etLRM09tTe6ZcNQk55o7FX0MfWH1nIsjbxjEg1P5BywfLxkVHe3iTq81jiPljVlMqUbzFYC0oDlLPFWi1wBUSaaxyP3qxxx6xq9hYz3Ixn5KR+RWDs5rvZmXn2WICNE9g7MEjI9cIwY0Bo8NcN1VcoNxe6zi2ilHgYso2bQI+9neLMqnSjKbWnY+UI6O36GYh292+Rc79EigK3JoKVZGwwOkvh4AumjP9ZulEDnWymIpv3zt/OtNoymA==~1; akavpau_vpc_gcd=1709744329~id=61190d81c53eb6701ea7850ecac2d81c'
}

prices = {}

temporary_discounts = {}

def get_links():
    return links.dell_links

def get_new_prices(url, page_number=1):
    response = requests.get(url+f"?page={page_number}", headers=header)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('article', class_='ps-stack')

        discounts_list = []
        for item in items:
            label = item.find('h3', class_='ps-title').find("a")
            name = label.text.strip()
            old_price = item.find('span', class_='strike-through')
            if old_price:
                old_price = float(old_price.text.strip().replace("£", "").replace(",", ""))
                price = float(item.find('div', class_='ps-dell-price').find_all("span")[1].text.strip().replace("£", "").replace(",", ""))
            else:
                price = float(item.find('div', class_='ps-dell-price').text.strip().replace("£", "").replace(",", ""))
                old_price = price
            link = "https:" + label['href']
            image = "https:" + item.find("img")["src"]

            item_data = {
                "name": name,
                "price": price,
                "link": link,
                "old_price": old_price,
                "image": image
            }
            if link in prices:
                item_data["old_price"] = prices[link]["old_price"]
                if prices[link]["old_price"] > price and price != prices[link]["price"] and link not in temporary_discounts:
                    item_data["old_price"] = prices[link]["old_price"]
                    item_data["previous_price"] = prices[link]["price"]
                    prices[link]["price"] = price
                    discounts_list.append(item_data)
                    temporary_discounts[link] = datetime.now()
                elif link not in temporary_discounts:
                    if prices[link]["old_price"] < old_price:
                        prices[link]["old_price"] = old_price
                    prices[link]["price"] = price
            else:
                prices[link] = item_data.copy()
                item_data["old_price"] = 0
                discounts_list.append(item_data)
        try:
            item_count = soup.find("span", class_="pageinfo")
            if item_count:
                item_count = int(item_count.text.strip().split(" ")[4])
            else:
                item_count = int(soup.find(id = "result-count").find("h2").text.strip().split("\xa0")[0])
        except:
            item_count = 0
        if 12*page_number < item_count:
            time.sleep(0.5)
            for discount in get_new_prices(url,page_number+1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve dell page")
        return []

def get_keepa_results(price_drops):
    keepa_drops = []
    for price_drop in price_drops:
        if price_drop["old_price"] == 0 or price_drop["price"]/price_drop["previous_price"] <= 0.85:
            compare_price, fee, fee_percentage, asin, avg90, graph, sales_rank_drop_30, monthly_sold, percentage = keepa_manager.get_from_title(price_drop["name"])
            if not compare_price:
                continue
            profit = compare_price - price_drop["price"] - 0.5 - (compare_price / 6 - price_drop["price"] / 6) - fee - (
                        compare_price * fee_percentage)

            profit_margin = profit / compare_price
            if profit_margin >= 0.1:
                margin_ping = {
                    "keepa_price": compare_price,
                    "price": price_drop["price"],
                    "name": price_drop["name"],
                    "link": price_drop["link"],
                    "margin": profit_margin,
                    "ASIN": asin,
                    "avg": avg90,
                    "image": price_drop["image"],
                    "graph": graph,
                    "rank_drop": sales_rank_drop_30,
                    "monthly_sold": monthly_sold,
                    "match_percentage": percentage
                }
                keepa_drops.append(margin_ping)
    return keepa_drops
