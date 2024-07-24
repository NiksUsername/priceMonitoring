from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

from back_scraping.utils import keepa_manager
from back_scraping.utils import links
from back_scraping.utils.discount_properties import is_big_discount

header = {
    'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    "Cookie": "sid=5bOjgi2n6KpsmJ6jhAzN7gtN9S4BTH5LK2U; dwanonymous_c1575c7fdffeee6c1c87c9bab9ccac08=abRsoDOFYas5iqUCWknTpeHOHA; __cq_dnt=0; dw_dnt=0; dwsid=hl_Mf99HDdLBLDnzC0X-M2ihmtPzrJszhtEEbBGA1FUBv3KPevIzCVJvqITJYirVH-1Ljk_a2lf6SePYDVAoGg==; __cf_bm=5H1BCFOa5yM04F7easaIEqFmCnFAf8HcgQ5LlkAAznI-1710340446-1.0.1.1-zdHyZQ8C4VesAi0zNK65FcskWjmxyTwM4NlswSzwFT60bQajS_gS0lMEHWqpZAT87yCYBgFe2dgrps9RneZ2xw; _cfuvid=ef769qDYgYan3RQ35Yh6gEOqoZk8cJxYu4Dr4vJk9Ws-1710338761968-0.0.1.1-604800000; gpv_pg=Keyboards; gpv_template=rendering/category/PLP; gpv_url=https://www.currys.co.uk/gaming/gaming-accessories/keyboards; gpv_login=logged_out; cf_clearance=eCPFqKhba0iqw_lzs3llYPNx.zZPUjVFaH.Ifa9jVCg-1710338763-1.0.1.1-dHrXarEoPHv95lJ0X0z3RSTTMBgqYEVnxx8hafkDP6v4GND0AQTDwBIc1XPkdNI6.LL5fcIwEn5SBfmmMl3unA; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+13+2024+16%3A17%3A33+GMT%2B0200+(Eastern+European+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=0e535f7d-8b94-4502-8c35-e9ec5d72b4c4&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0008%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false; dwOptanonConsentCookie=false; OptanonAlertBoxClosed=2024-03-13T14:06:51.970Z; gcpData=%7B%7D; _mibhv=anon-1710338813233-56683855_8082; smc_uid=1710338813572710; smc_tag=eyJpZCI6MTkyNCwibmFtZSI6ImN1cnJ5cy5jby51ayJ9; smc_session_id=SZN2cU0lq2NrrHhiUIAhZbZQ7XD5xGR7; smc_group_events=A; smc_group_test_value=A; smc_refresh=32305; smct_session=%7B%22s%22%3A1710338814621%2C%22l%22%3A1710341626434%2C%22lt%22%3A1710340853287%2C%22t%22%3A1043%2C%22p%22%3A119%7D; smct_dyn_BasketCount=0; smc_tpv=1; smc_spv=1; smc_sesn=1; smc_not=default; dwac_2657edce74737ed44718c8ec2e=5bOjgi2n6KpsmJ6jhAzN7gtN9S4BTH5LK2U%3D|dw-only|||GBP|false|Europe%2FLondon|true; cqcid=abRsoDOFYas5iqUCWknTpeHOHA; cquid=||; _cs_mk_aa=0.34880860349061416_1710340747553"
}

cookies = {
    '__cf_bm':	"5cT3bEl.ytRRD2Oqmv9AaNg4Si7.OgzA.rO4pp.G9iE-1710338761-1.0.1.1-N4gDlUUoBnrhagTeebw1xqczMu5ZCUAFt1Xkvso211SA1P8B0rto9IxoLuLjpRJdG1wSMVdL0vXDy81zvnqWdw",
    '__cq_dnt':	"0",
    '_cfuvid':	"ef769qDYgYan3RQ35Yh6gEOqoZk8cJxYu4Dr4vJk9Ws-1710338761968-0.0.1.1-604800000",
    '_cs_mk_aa':	"0.07594036318843012_1710338812081",
    '_mibhv':	"anon-1710338813233-56683855_8082",
    'cf_clearance':	"eCPFqKhba0iqw_lzs3llYPNx.zZPUjVFaH.Ifa9jVCg-1710338763-1.0.1.1-dHrXarEoPHv95lJ0X0z3RSTTMBgqYEVnxx8hafkDP6v4GND0AQTDwBIc1XPkdNI6.LL5fcIwEn5SBfmmMl3unA",
    'cqcid':	"abRsoDOFYas5iqUCWknTpeHOHA",
    'cquid':	"||",
    'dw_dnt':	"0",
    'dwac_2657edce74737ed44718c8ec2e':	"5bOjgi2n6KpsmJ6jhAzN7gtN9S4BTH5LK2U=|dw-only|||GBP|false|Europe/London|true",
    'dwanonymous_c1575c7fdffeee6c1c87c9bab9ccac08':	"abRsoDOFYas5iqUCWknTpeHOHA",
    'dwOptanonConsentCookie':	"false",
    'dwsid':	"hl_Mf99HDdLBLDnzC0X-M2ihmtPzrJszhtEEbBGA1FUBv3KPevIzCVJvqITJYirVH-1Ljk_a2lf6SePYDVAoGg==",
    'gcpData':	"{}",
    'gpv_login':	"logged_out",
    'gpv_pg':	"Keyboards",
    'gpv_template':	"rendering/category/PLP",
    'gpv_url':	"https://www.currys.co.uk/gaming/gaming-accessories/keyboards",
    'OptanonAlertBoxClosed':	"2024-03-13T14:06:51.970Z",
    'OptanonConsent':	"isGpcEnabled=0&datestamp=Wed+Mar+13+2024+16:17:33+GMT+0200+(Eastern+European+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=0e535f7d-8b94-4502-8c35-e9ec5d72b4c4&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001:1,C0008:1,C0002:1,C0003:1,C0004:1&geolocation=;&AwaitingReconsent=false",
    'sid':	"5bOjgi2n6KpsmJ6jhAzN7gtN9S4BTH5LK2U",
    'smc_group_events':	"A",
    'smc_group_test_value':	"A",
    'smc_not':	"default",
    'smc_refresh':	"32305",
    'smc_sesn':	"1",
    'smc_session_id':	"SZN2cU0lq2NrrHhiUIAhZbZQ7XD5xGR7",
    'smc_spv':	"1",
    'smc_tag':	"eyJpZCI6MTkyNCwibmFtZSI6ImN1cnJ5cy5jby51ayJ9",
    'smc_tpv':	"1",
    'smc_uid':	"1710338813572710",
    'smct_dyn_BasketCount':	"0",
    'smct_session':	'{"s":1710338814621,"l":1710340438446,"lt":1710340438446,"t":904,"p":101}'
}

prices = {}
temporary_discounts = {}


def get_links():
    return links.currys_links

def get_new_prices(url, page_number=1, cgid=""):
    if cgid:
        api_link = f"https://www.currys.co.uk/search-update-grid?cgid={cgid}&start={(page_number-1)*50}&sz=50&viewtype=listView"
    else:
        api_link = url+f"?start={(page_number-1)*50}&sz=50&viewtype=listView"
    try:
        response = requests.get(api_link, headers=header, cookies=cookies, impersonate="chrome120")
    except:
        return []
    discounts_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('div', class_='plp-productitem-id')

        for item in items:
            name = item.find('h2', class_='pdp-grid-product-name').text.strip()
            price = float(item.find('div', class_='price-info').find("span", class_="value")["content"])
            old_price = item.find("span", class_="worse-price")
            if old_price:
                old_price = old_price.text
                if "Was" in old_price:
                    old_price = float(old_price.replace("Was", "").strip().replace("£", ""))
                elif "Save" in old_price:
                    old_price = price + float(old_price.replace("Save", "").strip().replace("£", ""))
            else:
                old_price = price
            link = "https://www.currys.co.uk" + item.find("a", class_="pdpLink")["href"]
            image = item.find("img", class_="tile-image")["data-src"]

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

        items_count = int(soup.find("div", "page-result-count").text.strip().split(" ")[0])
        if 50*page_number < items_count:
            cgid = soup.find("input", "category-id")["value"]
            for discount in get_new_prices(url,page_number+1, cgid):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve the page")
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