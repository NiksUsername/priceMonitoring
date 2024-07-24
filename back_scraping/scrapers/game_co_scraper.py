from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

from back_scraping.utils import keepa_manager
from back_scraping.utils import links
from back_scraping.utils.discount_properties import is_big_discount

url = "https://www.game.co.uk/en/playstation/games/?contentOnly=&inStockOnly=true&listerOnly=&pageSize=600"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'hashedemail=Guest; WC_PERSISTENT=TbQdUIMXh79ggUK0yWNt4jmzSjs%3D%0A%3B2024-02-17+23%3A04%3A06.05_1708211046048-596014_10151; WC_SESSION_ESTABLISHED=true; WC_ACTIVEPOINTER=44%2C10151; WC_USERACTIVITY_-1002=-1002%2C10151%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CABtLmXt%2FyjnsRlXUR6%2Bwf3mHQV%2BKIhEyRqmVnOOL8v8N8QOEkDlSwxxtdrrrNfSLqXtEFamVLHeVRGSf1fdcP7d8CphjlcQdYZZUHcQyTGhg7zj%2FQjagGlvkDrSEmOqhzXW085Gi7dSSrr7XR0Z7YTI5CW58PLIvM2aoBT4rLjF%2BqEUj0PPY1c3mX4VanFaMyejb4t5TlbdO3Z7KprBxaw%3D%3D; WC_GENERIC_ACTIVITYDATA=[23902279088%3Atrue%3Afalse%3A0%3AN97NznhAtLV2unaZ9S30WuBFEkc%3D][com.ibm.commerce.context.audit.AuditContext|1708211046048-596014][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.game.gameaccount.context.GameAccountAccessTokenContext|null][com.game.gameaccount.context.GameAccountContext|null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|44%26GBP%2644%26GBP][com.game.gameaccount.context.GameAccountPostLogonContext|null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10201%26null%26false%26false%26false][com.ibm.commerce.context.base.BaseContext|10151%26-1002%26-1002%26-1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|10002%2610002%26null%26-2000%26null%26null%26null]; _cq_duid=1.1708211046.JzxFz3cjJtU4thmc; _cq_suid=1.1708211046.6w1e2j8iQjzeu0q6; _gcl_au=1.1.893585599.1708211047; mmapi.p.ids=%7B%221%22%3A%22Guest%22%7D; ORA_FPC=id=a5fd6c23-eb70-4ed3-9166-2779654a2fe7; mmapi.e.lightbox1707910661244persistData=%221%2C1%2C1708211049%22; complianceCookie=true; gdprPurposesCookie=[1,2,3,4,5]; GAMESession=AR+U4h1nggY9UJgGLbGGkGFi+Dbi148uyM7b6bD91EGuBm9lhwpy+SJhuQpBJZgbYwTXXzsxwFU6rfxBUVD1caF+rfhm1ERUUTcv9fHMC1ZMhlCNI0kLNmVlQ1E990ez/ky9s40UCKgpo9mlccogKN0; X-Origin-Cookie=1; bm_sv=4E0E2201DA46C26D6BFCA0AAE7A430A1~YAAQDIR7XERHj8SNAQAANXJU0hbjPlQBD66gANmTWWbjvj537y9PybsPeGsPWwo8Cv/eOKVTuJ05RaZ2ihy7YclmKk84OK8Nn2rXVTjj9VpryrAaDKbsC5znJTcGrvwuK8r27H+0Cu2G1w2CUiccwOrWk7XECeX0T58sfVkhO4ZeHByuBo41Kj6jfhz5EpI519I/BMjRmKmPP5kCBtf5wPEobwGUKgEzCQ7riqGspgugqDmep4RbszClnKkcUZ/+~1; JSESSIONID=0000wSUNsBxv10lcMTQeV8Rh-Y2:18oae5lgj; hashedemail=Guest; _ga_BZM1F1D2W5=GS1.1.1708630767.5.0.1708630767.60.0.0; _rdt_uuid=1708211047355.917b9704-f9b5-4af9-a989-84f394e9040d; _ga=GA1.3.1136405655.1708211047; _gid=GA1.3.1434009465.1708630768; ak_bmsc=80FF04B6649A101BFDDF6E7FFB7BC523~000000000000000000000000000000~YAAQDIR7XO9Hj8SNAQAA8XZU0haRKhRWrrW1Dw5rztbyPprxsftS66P/4ekYzihOV5GOVsJgqTqxUQqJXw/INOZe6Noq9HDkJoreDYqqfJe5Sn2nCyMXZqLIodQCToFQ4ShgVwNmefkJNbCn3SuTxiOxQDOz0QIRKNAcsXJR36Ig3rnq+BB7NACX7c19TLvS9beLI7agKjlBY5DyMcUvLeicQWPJNkZ0GGeS5X6ik4Z3uOE03iFm3pO89/EExrpxOEUdV4Y4LPZGpU4DPnIVJVv1KvZLwvIcddOIWXHH9cdIVdFNa1CHilk2iAa0BxAS5Obh4kpiEdDXKT9QJS3G+a+AfEA/if0KGHUQRUt1EeZlZ7klIlnn6g38H5+1z03Zhn/zkhgyCL0oO2S6m1J1Hh1x/O3e734+FaONzvtQVMJyS84CdmbhjWOFer9ZKTmmd4ZMC+FrPpvAW7AwBjEZgScDFcvL03YrVwbMfmNvjydmjv68OkihxBTgfHKoYA==; mmapi.p.pd=%227qHpjsuhLerlwyPp8Zd7iAdI_4rdLY5lsHrYlcToTjw%3D%7CGgAAAApDH4sIAAAAAAAEAGNhSPafsLBA4p07q3tpanEJc05GEaMQA6MTg2NfwkUWhleXrH7fNb7j0ajDuJ_H4I4HAxD8hwIGNpfMotTkEsYCCRaQOBjAJEE0I4NDOyODlIy62PYCCbA2oNJSif__pRgYGEGqGZmfMTNs1mGFaGVgdAUA74BZdo8AAAA%3D%22; mmapi.p.bid=%22prodlhrcgeu06%22; mmapi.p.srv=%22prodlhrcgeu06%22',
    'Referer': 'https://www.game.co.uk/',
    'Sec-Ch-Ua': '"Chromium";v="120", "Not(A:Brand";v="24", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': '	Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36'
}

cookies = {
    "GAMESession": "AR+U4h1nggY9UJgGLbGGkGFi+Dbi148uyM7b6bD91EGuBm9lhwpy+SJhuQpBJZgbYwTXXzsxwFU6rfxBUVD1caF+rfhm1ERUUTcv9fHMC1ZMhlCNI0kLNmVlQ1E990ez/ky9s40UCKgpo9mlccogKN0",
    "JSESSIONID": "0000wSUNsBxv10lcMTQeV8Rh-Y2:18oae5lgj",
    "ORA_FPC": "id=a5fd6c23-eb70-4ed3-9166-2779654a2fe7 ",
    "WC_ACTIVEPOINTER": "44%2C10151",
    "WC_GENERIC_ACTIVITYDATA": "[23902279088%3Atrue%3Afalse%3A0%3AN97NznhAtLV2unaZ9S30WuBFEkc%3D][com.ibm.commerce.context.audit.AuditContext|1708211046048-596014][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.game.gameaccount.context.GameAccountAccessTokenContext|null][com.game.gameaccount.context.GameAccountContext|null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|44%26GBP%2644%26GBP][com.game.gameaccount.context.GameAccountPostLogonContext|null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10201%26null%26false%26false%26false][com.ibm.commerce.context.base.BaseContext|10151%26-1002%26-1002%26-1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|10002%2610002%26null%26-2000%26null%26null%26null]",
    "WC_PERSISTENT": "TbQdUIMXh79ggUK0yWNt4jmzSjs%3D%0A%3B2024-02-17+23%3A04%3A06.05_1708211046048-596014_10151",
    "WC_SESSION_ESTABLISHED": "true",
    "WC_USERACTIVITY_-1002": "-1002%2C10151%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CABtLmXt%2FyjnsRlXUR6%2Bwf3mHQV%2BKIhEyRqmVnOOL8v8N8QOEkDlSwxxtdrrrNfSLqXtEFamVLHeVRGSf1fdcP7d8CphjlcQdYZZUHcQyTGhg7zj%2FQjagGlvkDrSEmOqhzXW085Gi7dSSrr7XR0Z7YTI5CW58PLIvM2aoBT4rLjF%2BqEUj0PPY1c3mX4VanFaMyejb4t5TlbdO3Z7KprBxaw%3D%3D",
    "X-Origin-Cookie": "1",
    "_cq_duid": "1.1708211046.JzxFz3cjJtU4thmc",
    "_cq_suid": "1.1708211046.6w1e2j8iQjzeu0q6",
    "_ga": "GA1.3.1136405655.1708211047",
    "_ga_BZM1F1D2W5": "GS1.1.1708630767.5.0.1708630767.60.0.0",
    "_gcl_au": "1.1.893585599.1708211047",
    "_gid": "GA1.3.1434009465.1708630768",
    "_rdt_uuid": "1708211047355.917b9704-f9b5-4af9-a989-84f394e9040d",
    "ak_bmsc": "80FF04B6649A101BFDDF6E7FFB7BC523~000000000000000000000000000000~YAAQDIR7XO9Hj8SNAQAA8XZU0haRKhRWrrW1Dw5rztbyPprxsftS66P/4ekYzihOV5GOVsJgqTqxUQqJXw/INOZe6Noq9HDkJoreDYqqfJe5Sn2nCyMXZqLIodQCToFQ4ShgVwNmefkJNbCn3SuTxiOxQDOz0QIRKNAcsXJR36Ig3rnq+BB7NACX7c19TLvS9beLI7agKjlBY5DyMcUvLeicQWPJNkZ0GGeS5X6ik4Z3uOE03iFm3pO89/EExrpxOEUdV4Y4LPZGpU4DPnIVJVv1KvZLwvIcddOIWXHH9cdIVdFNa1CHilk2iAa0BxAS5Obh4kpiEdDXKT9QJS3G+a+AfEA/if0KGHUQRUt1EeZlZ7klIlnn6g38H5+1z03Zhn/zkhgyCL0oO2S6m1J1Hh1x/O3e734+FaONzvtQVMJyS84CdmbhjWOFer9ZKTmmd4ZMC+FrPpvAW7AwBjEZgScDFcvL03YrVwbMfmNvjydmjv68OkihxBTgfHKoYA==",
    "bm_sv": "4E0E2201DA46C26D6BFCA0AAE7A430A1~YAAQDIR7XERHj8SNAQAANXJU0hbjPlQBD66gANmTWWbjvj537y9PybsPeGsPWwo8Cv/eOKVTuJ05RaZ2ihy7YclmKk84OK8Nn2rXVTjj9VpryrAaDKbsC5znJTcGrvwuK8r27H+0Cu2G1w2CUiccwOrWk7XECeX0T58sfVkhO4ZeHByuBo41Kj6jfhz5EpI519I/BMjRmKmPP5kCBtf5wPEobwGUKgEzCQ7riqGspgugqDmep4RbszClnKkcUZ/+~1",
    "complianceCookie": "true",
    "gdprPurposesCookie": "[1,2,3,4,5]",
    "hashedemail": "Guest",
    "mmapi.e.lightbox1707910661244persistData": "%221%2C1%2C1708211049%22",
    "mmapi.p.bid": "%22prodlhrcgeu06%22	",
    "mmapi.p.ids": "%7B%221%22%3A%22Guest%22%7D	",
    "mmapi.p.pd": "%227qHpjsuhLerlwyPp8Zd7iAdI_4rdLY5lsHrYlcToTjw%3D%7CGgAAAApDH4sIAAAAAAAEAGNhSPafsLBA4p07q3tpanEJc05GEaMQA6MTg2NfwkUWhleXrH7fNb7j0ajDuJ_H4I4HAxD8hwIGNpfMotTkEsYCCRaQOBjAJEE0I4NDOyODlIy62PYCCbA2oNJSif__pRgYGEGqGZmfMTNs1mGFaGVgdAUA74BZdo8AAAA%3D%22",
    "mmapi.p.srv": "%22prodlhrcgeu06%22"
}

prices = {}

discounts = {}

first_run = True

def get_links():
    return links.game_links

def get_new_prices(url, page=1):
    response = requests.get(url, headers=headers, cookies=cookies, impersonate="chrome120")
    soup = BeautifulSoup(response.content, "html.parser")

    game_items = soup.find_all("div", class_="productWrapper")

    game_data = []
    for item in game_items:
        try:
            item_data = {}
            title = item.find("div", class_="productTitle")
            title = title.find("a")
            item_data["name"] = title.text.strip()
            item_data["price"] = float(item.find("span", class_="now").text.strip().split("£")[1].split("/")[0])
            if item_data["price"] == 0: continue
            item_data["link"] = title["href"]
            item_data["old_price"] = item_data["price"]
            item_data["image"] = "https:" + item.find("img")["data-src"]


            if item_data["link"] in prices:
                item_data["old_price"] = prices[item_data["link"]]["old_price"]
                if prices[item_data["link"]]["old_price"] > item_data["price"] and item_data["price"] != prices[item_data["link"]]["price"] and item_data["link"] not in discounts:
                    item_data["old_price"] = prices[item_data["link"]]["old_price"]
                    item_data["previous_price"] = prices[item_data["link"]]["price"]
                    prices[item_data["link"]]["price"] = item_data["price"]
                    game_data.append(item_data)
                    discounts[item_data["link"]] = datetime.now()
                elif item_data["link"] not in discounts:
                    if prices[item_data["link"]]["old_price"] < item_data["price"]:
                        prices[item_data["link"]]["old_price"] = item_data["price"]
                    prices[item_data["link"]]["price"] = item_data["price"]
            else:
                if not first_run:
                    item_data["old_price"] = 0
                    game_data.append(item_data)
                prices[item_data["link"]] = item_data.copy()
        except Exception:
            continue
    products = int(soup.find("div", class_="productCount").find_all("strong")[2].text.strip())
    if products > 600*page and page != 4:
        for data in get_new_prices(url.split("pageNumber=")[0]+f"pageNumber={page+1}", page+1):
            game_data.append(data)
    temp = discounts.items()
    for key, value in temp:
        if value < datetime.now() - timedelta(hours=12):
            discounts.pop(key)

    return game_data


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
