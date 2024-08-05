import io

import requests

import config
import urllib.parse
import re

def get_from_bar_code(bar_code: str):
    url = f"https://api.keepa.com/product?key={config.KEEPA_API}&domain=2&code={bar_code}&stats=7"
    content = requests.get(url).json()
    try:
        content["products"][0]
    except:
        return [None] * 9
    try:
        price = content["products"][0]["stats"]["current"][1]/100
        avg90 = content["products"][0]["stats"]["avg90"][1]/100
        if price<0:
            raise Exception
        if avg90<0:
            avg90="N/A"
        else:
            avg90=f"£{round(avg90, 2)}"
        fba_fee = content["products"][0]["fbaFees"]
        fba_fee = fba_fee["pickAndPackFee"] if fba_fee else 0
        fba_fee = fba_fee/100 if fba_fee and fba_fee > 0 else 0
        percentage_fee = content["products"][0].get("referralFeePercentage")
        percentage_fee = percentage_fee/100 if percentage_fee else 0
        asin = content["products"][0]["asin"]
        sales_rank_drop_30 = content["stats"]["salesRankDrops30"]
        monthly_sold = content.get("monthlySold")
        graph = get_fba_graph(asin)
        if fba_fee == 0 or percentage_fee == 0: return [None] * 9

        return price, fba_fee, percentage_fee, asin, avg90, graph,sales_rank_drop_30, monthly_sold, 0
    except Exception:
        return [None] * 9

def get_from_title(title: str):
    url_title = urllib.parse.quote(title)
    url = f"https://api.keepa.com/search?key={config.KEEPA_API}&domain=2&type=product&term={url_title}&stats=7"
    content = requests.get(url).json()
    try:
        content["products"][0]
    except:
        return [None] * 9
    match = find_best_match(title, content["products"])
    if not match:
        return [None] * 9
    try:
        product, percentage = match
        price = product["stats"]["current"][1] / 100
        avg90 = product["stats"]["avg90"][1] / 100
        if price < 0:
            raise Exception
        if avg90 < 0:
            avg90 = "N/A"
        else:
            avg90 = f"£{round(avg90, 2)}"
        fba_fee = product["fbaFees"]
        fba_fee = fba_fee["pickAndPackFee"] if fba_fee else 0
        fba_fee = fba_fee / 100 if fba_fee and fba_fee > 0 else 0
        percentage_fee = product.get("referralFeePercentage")
        percentage_fee = percentage_fee / 100 if percentage_fee else 0
        asin = product["asin"]
        sales_rank_drop_30 = content["stats"]["salesRankDrops30"]
        monthly_sold = content.get("monthlySold")
        graph = get_fba_graph(asin)
        if fba_fee == 0 or percentage_fee == 0: return  [None] * 9

        return price, fba_fee, percentage_fee, asin, avg90, graph, sales_rank_drop_30, monthly_sold, percentage
    except Exception:
        return [None] * 9


def find_best_match(title, keepa_objects):
    best_match_percentage = 0
    best_match = {}
    words = re.findall(r'\b\w+\b', title)
    for object in keepa_objects:
        matches = 0
        code_matches = 0
        obj_title = object["title"].lower().replace(" ", "")
        codes = [word for word in words if is_code(word)]
        for word in codes:
            if word.lower() in obj_title:
                code_matches += 1
        for word in words:
            if word.lower() in obj_title:
                matches += 1
        try:
            percentage = matches/len(words) * code_matches/len(codes)
        except ZeroDivisionError:
            percentage = matches/len(words)
        if percentage > best_match_percentage:
            best_match = object
            best_match_percentage = percentage

    if best_match_percentage >= 0.70:
        return best_match, best_match_percentage
    return False


def get_fba_graph(asin: str):
    r_url = (
        f"https://api.keepa.com/graphimage?key={config.KEEPA_API}&domain=2&asin={asin}&salesrank=1&amazon=0&used=0&bb=1&fba=0&width=750&height=300"
        f"&range=180&cNew=8888DD&cBB=FF00B4&cSales=8FBC8F"
    )
    with requests.get(r_url) as r:
        if r.status_code == 200:
            return io.BytesIO(r.content)
        else:
            return False

def is_code(word):
    if word.isupper():
        return True
    num_digits = sum(c.isdigit() for c in word)
    return num_digits / len(word) > 0.4

