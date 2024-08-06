import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

from back_scraping.utils import keepa_manager
from back_scraping.utils import links
from back_scraping.utils.discount_properties import is_big_discount

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    "X-Requested-With": "XMLHttpRequest",
    "Api-Key": "sh5d2d2ph9rgbps3ntrshxqn",
    "Cookie": 'utag_main=v_id:018d994d1bcf001cd2c3728cdee805050005200d00bd0$_sn:8$_ss:1$_st:1712520018162$dc_visit:7$_pn:1%3Bexp-session$ses_id:1712518182468%3Bexp-session$dc_event:1%3Bexp-session; cf_clearance=B3L.RKiNqj6ffwGBDlyasou2Yk2x2D1CZ6o2QXav2ec-1712518181-1.0.1.1-Q89kT5Ar1klt7fc9NvTqARzlHBc.D_KEYkNqQYF2F3Vt00BaviV4CfwJbzpz5_zBrbAbZGYDaNBs3femd0I_vQ; utag_chan={"channel":"","channel_set":"","channel_converted":false,"awc":""}; CONSENTMGR=consent:true%7Cts:1711706920402; COOKIE_NOTICE_SEEN=seen; SIGNUP_POPUP_SEEN=seen; NEWSLETTER_DISMISSED=true; _cfuvid=hjXtrJ_RDNGPiTVuB5.T7pHNBDaYgqy2nStfpJXfK4M-1712518179201-0.0.1.1-604800000; SF_COUNTRY_LANG=GB_en; JSESSIONID=0000D-BStWRm7WlnSWW1qnRlbcz:-1; __cf_bm=d8ttwLkGTbGENMii1E3Vhcf0i.GiXK6LCXolMk9aX9w-1712518179-1.0.1.1-dPtuwnSz0oJ5XzwhLWW__TtU1HMsWio_4_XAVgrrIcS9ddmMW8g3mclFAjGYQu1j5cwgG6eN5Uo5eYP6_Os5bD9Ldftf1x.vb2qij_RHY1g; _cs_mk=0.11211387893016123_1712518183186'
}

cookies = {
    '__cf_bm':	"d8ttwLkGTbGENMii1E3Vhcf0i.GiXK6LCXolMk9aX9w-1712518179-1.0.1.1-dPtuwnSz0oJ5XzwhLWW__TtU1HMsWio_4_XAVgrrIcS9ddmMW8g3mclFAjGYQu1j5cwgG6eN5Uo5eYP6_Os5bD9Ldftf1x.vb2qij_RHY1g",
    '_cfuvid':	"hjXtrJ_RDNGPiTVuB5.T7pHNBDaYgqy2nStfpJXfK4M-1712518179201-0.0.1.1-604800000",
    '_cs_mk':	"0.11211387893016123_1712518183186",
    'cf_clearance':	"B3L.RKiNqj6ffwGBDlyasou2Yk2x2D1CZ6o2QXav2ec-1712518181-1.0.1.1-Q89kT5Ar1klt7fc9NvTqARzlHBc.D_KEYkNqQYF2F3Vt00BaviV4CfwJbzpz5_zBrbAbZGYDaNBs3femd0I_vQ",
    'CONSENTMGR':	"consent:true|ts:1711706920402",
    'COOKIE_NOTICE_SEEN':	"seen",
    'JSESSIONID':	"0000D-BStWRm7WlnSWW1qnRlbcz:-1",
    'NEWSLETTER_DISMISSED':	"true",
    'SF_COUNTRY_LANG':	"GB_en",
    'SIGNUP_POPUP_SEEN':	"seen",
    'utag_chan':	'{"channel":"","channel_set":"","channel_converted":false,"awc":""}',
    'utag_main':	"v_id:018d994d1bcf001cd2c3728cdee805050005200d00bd0$_sn:8$_ss:1$_st:1712520018162$dc_visit:7$_pn:1;exp-session$ses_id:1712518182468;exp-session$dc_event:1;exp-session"
}

prices = {}
temporary_discounts = {}

def get_links():
    return links.selfridges_links

def get_new_prices(url, page_number=1):
    category = url.split("/cat/")[1].replace("/", "|")
    category = category[0:len(category)-1]
    api_url = f"https://www.selfridges.com/api/cms/ecom/v1/GB/en/productview/byCategory/byIds?ids={category}&pageNumber={page_number}&pageSize=180"
    response = requests.get(api_url, headers=header, cookies=cookies, impersonate="chrome120")
    discounts_list = []

    if response.status_code == 200:

        items = response.json()

        for item in items["catalogEntryNavView"]:
            try:
                name = item["name"]
                price_object = item["price"][0]
                price = float(price_object["lowestPrice"])
                old_price = price_object.get("lowestWasWasPrice")
                if old_price:
                    old_price = float(old_price)
                else:
                    old_price = price_object.get("lowestWasPrice")
                    if old_price:
                        old_price = float(old_price)
                    else:
                        old_price = price
                link = "https://www.selfridges.com/GB/en/product/"+str(item["seoKey"])
                imageName = item["imageName"]
                id = item["imageName"].replace("_M", "")
                image = f"https://images.selfridges.com/is/image/selfridges/{id}_ALT10?defaultImage={imageName}&$PLP_ALL$"
                item_data = {
                    "name": name,
                    "price": price,
                    "link": link,
                    "old_price": old_price,
                    "image":image
                }
                if link in prices:
                    item_data["old_price"] = prices[link]["old_price"]
                    if prices[link]["old_price"] > price and price != prices[link]["price"] and prices[link][image] == image and link not in temporary_discounts:
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
            except:
                pass

        item_count = int(items["recordSetTotal"])
        if 180 * page_number < item_count:
            time.sleep(1)
            for discount in get_new_prices(url, page_number + 1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=24):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve selfridges page")
        return discounts_list


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
            if profit_margin >= 0.15:
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
