import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

from back_scraping.utils import keepa_manager
from back_scraping.utils import links
from back_scraping.utils.discount_properties import is_big_discount

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': 'sessionid=7jxrgyqybg3b5rsb89u3zq1lky74tw3j; CookieInformationConsent=%7B%22website_uuid%22%3A%22f1a0dc8b-de15-4dad-b007-d7a25ff24849%22%2C%22timestamp%22%3A%222024-03-29T08%3A29%3A05.445Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fwww.coolshop.co.uk%2Fs%2Fshow-only%3Din-stock%2F%3Fq%3Dvideo%2520games%22%2C%22consent_website%22%3A%22coolshop.co.uk%22%2C%22consent_domain%22%3A%22www.coolshop.co.uk%22%2C%22user_uid%22%3A%2271198724-135c-49be-9a01-d7750d704e96%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%3B%20rv%3A124.0%29%20Gecko%2F20100101%20Firefox%2F124.0%22%7D; raptor_coid=2db047afc7f042699c18491f1b61c224; raptor_sid=8c51e403b9db4a45ac6ddeb21ab0e87c; raptor_ruid=""; raptor_reaid=""'
}

cookies = {
    'CookieInformationConsent':	'{"website_uuid":"f1a0dc8b-de15-4dad-b007-d7a25ff24849","timestamp":"2024-03-29T08:29:05.445Z","consent_url":"https://www.coolshop.co.uk/s/show-only=in-stock/?q=video%20games","consent_website":"coolshop.co.uk","consent_domain":"www.coolshop.co.uk","user_uid":"71198724-135c-49be-9a01-d7750d704e96","consents_approved":["cookie_cat_necessary","cookie_cat_functional","cookie_cat_statistic","cookie_cat_marketing","cookie_cat_unclassified"],"consents_denied":[],"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"}',
    'raptor_coid':	"2db047afc7f042699c18491f1b61c224",
    'raptor_reaid':	'""',
    'raptor_ruid':	'""',
    'raptor_sid':	"8c51e403b9db4a45ac6ddeb21ab0e87c",
    'sessionid':	"7jxrgyqybg3b5rsb89u3zq1lky74tw3j"
}

prices = {}

temporary_discounts = {}


def get_links():
    return links.coolshop_links

def get_new_prices(url, page_number=1):
    body = {
        "path":"_/show-only=in-stock/",
        "add_facets":{},
        "remove_facets":{},
        "sort":"",
        "size":300,
        "offset":(page_number-1)*300
    }
    link = "https://www.coolshop.co.uk/api/search" + "?q" + url.split("?q")[1]
    response = requests.post(link, headers=header, data=body, cookies=cookies, impersonate="chrome120")

    if response.status_code == 200:
        data = response.json()
        items_content = data.get("results")
        soup = BeautifulSoup(items_content, 'html.parser')

        items = soup.find_all('div', class_='product-card')

        discounts_list = []
        for item in items:
            try:
                label = item.find('div', class_='product-cards__title').find("a")
            except:
                continue
            name = label.text.strip()

            price = item.find("div", class_="product-cards__price")
            decimal_price = price.find("span", class_="after-decimal")
            if decimal_price:
                price = price.text.strip().replace("£", "")
                price = float(price[0:len(price) - len(decimal_price.text.strip())] + "." + decimal_price.text.strip())
            else:
                price = float(price.text.strip().replace("£", ""))

            old_price = item.find('div', class_='product-cards__guide-price')
            if old_price:
                decimal_price = old_price.find("span", class_="after-decimal")
                if decimal_price:
                    old_price = old_price.find("span").text.strip().replace("£", "")
                    old_price = float(old_price[0:len(old_price)-len(decimal_price.text.strip())] + "." + decimal_price.text.strip())
                else:
                    old_price = float(old_price.find("span").text.strip().replace("£", ""))
            else:
                old_price = price
            link = "https://www.coolshop.co.uk" + label['href']
            image = item.find("img")["src"]

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

        item_count = int(data.get("count"))
        if 300*page_number < item_count:
            time.sleep(0.5)
            for discount in get_new_prices(url,page_number+1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve coolshop page")
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