import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

from utils import keepa_manager
from utils import links
from utils.discount_properties import is_big_discount
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': 'requestId=f6b74973-d650-41d4-95f2-289422218e5b; form_key=sifpoRU80jL1pWxH; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; _br_uid_2; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; mage-messages=; bv_metrics=true'
}

cookies = {
    'form_key':	"sifpoRU80jL1pWxH",
    'mage-cache-sessid':	"true",
    'mage-cache-storage':	"{}",
    'mage-cache-storage-section-invalidation':	"{}",
    'mage-messages':	"",
    'product_data_storage':	"{}",
    'recently_compared_product':	"{}",
    'recently_compared_product_previous':	"{}",
    'recently_viewed_product':	"{}",
    'recently_viewed_product_previous':	"{}",
    'requestId':	"f6b74973-d650-41d4-95f2-289422218e5b"
}

prices = {}

temporary_discounts = {}

def get_links():
    return links.ryman_links

def get_new_prices(url, page_number=1):
    response = requests.get(url+f"?p={page_number}&product_list_limit=192", headers=header, cookies=cookies, impersonate="chrome120")

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('li', class_='product-item')

        discounts_list = []
        for item in items:
            label = item.find('a', class_='product-item-link')
            name = label.text.strip()
            old_price = item.find('span', class_='price-was_price')
            if old_price:
                old_price = float(old_price.find("span", class_="price").text.strip().replace("£", "").replace(",", ""))
                price = float(item.find('span', class_='price-including-tax').find("span", class_="price").text.strip().replace("£", "").replace(",", ""))
            else:
                price = float(item.find('span', class_='price').text.strip().replace("£", "").replace(",", ""))
                old_price = price
            link = label['href']
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
        try:
            item_count = int(soup.find_all("span", class_="toolbar-number")[2].text.strip())
        except Exception as e:
            item_count = 0
        if 196*page_number < item_count:
            time.sleep(1)
            for discount in get_new_prices(url,page_number+1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve ryman page")
        return []


def get_keepa_results(price_drops):
    keepa_drops = []
    for price_drop in price_drops:
        if price_drop["old_price"] == 0 or price_drop["price"]/price_drop["previous_price"] <= 0.85:
            bar_code = get_bar_code(price_drop["link"])
            if not bar_code:
                compare_price, fee, fee_percentage, asin, avg90, graph, sales_rank_drop_30, monthly_sold, percentage = keepa_manager.get_from_title(price_drop["name"])

            else:
                compare_price, fee, fee_percentage, asin, avg90, graph, sales_rank_drop_30, monthly_sold, percentage = keepa_manager.get_from_bar_code(bar_code)
            if not compare_price:
                continue
            profit = compare_price - price_drop["price"] - 0.5 - (compare_price / 6 - price_drop["price"] / 6) - fee - (compare_price * fee_percentage)
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


def get_bar_code(link):
    response = requests.get(link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find("div", class_="js-product-attribute-barcode").text.strip()

