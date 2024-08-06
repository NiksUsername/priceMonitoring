import traceback
from datetime import datetime, timedelta
import time
from threading import Thread

import requests

from back_scraping import config
from back_scraping.scrapers import argos_scraper, currys_scraper, game_co_scraper, johnlewis_scraper, dell_scraper, \
    ryman_scraper, laptopsdirect_scraper, houseoffraser_scraper, coolshop_scraper, selfridges_scraper
from back_scraping.utils.discount_properties import is_big_discount


def get_website_update(web_scraper, link, check_keepa=True):
    prices = web_scraper.get_new_prices(link)
    if check_keepa:
        keepa_updates = web_scraper.get_keepa_results(prices)
    else:
        keepa_updates = []
    site_updates = filter_drops(prices)
    return site_updates + (keepa_updates,)


def filter_drops(drops):
    messages = []
    unfiltered = []
    for drop in drops:
        if not drop.get("old_price"): continue
        if is_big_discount(drop):
            messages.append(drop)
        else:
            unfiltered.append(drop)
    return messages, unfiltered


def check_for_new_notifications(web_scraper, name):
    curr_time = datetime.now()
    for link in web_scraper.get_links():
        try:
            time.sleep(1)
            get_website_update(web_scraper, link, False)
        except:
            traceback.print_exc()
            continue
    if name == "coolshop":
        for link in web_scraper.get_links():
            try:
                time.sleep(1)
                get_website_update(web_scraper, link, False)
            except:
                traceback.print_exc()
                continue
    while True:
        try:
            for link in web_scraper.get_links():
                try:
                    return_value = get_website_update(web_scraper, link, True)
                except Exception:
                    traceback.print_exc()
                    continue
                for type in range(len(return_value)):
                    for value in return_value[type]:
                        requests.post(url=config.api_urls[type], json={
                            "data":[value],
                            "type":type,
                            "website":name
                        })
                time.sleep(1)
            delta = datetime.now() - curr_time
            time.sleep(max(300 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=300)
        except Exception:
            print(f"Major {name} Exception")


Thread(target=check_for_new_notifications, args=(argos_scraper, "argos")).start()
Thread(target=check_for_new_notifications, args=(currys_scraper, "currys")).start()
Thread(target=check_for_new_notifications, args=(game_co_scraper, "game")).start()
Thread(target=check_for_new_notifications, args=(johnlewis_scraper, "johnlewis_scraper")).start()
Thread(target=check_for_new_notifications, args=(selfridges_scraper, "selfridges")).start()
Thread(target=check_for_new_notifications, args=(coolshop_scraper, "coolshop")).start()
Thread(target=check_for_new_notifications, args=(houseoffraser_scraper, "houseoffraser")).start()
Thread(target=check_for_new_notifications, args=(laptopsdirect_scraper, "laptopsdirect")).start()
Thread(target=check_for_new_notifications, args=(ryman_scraper, "ryman")).start()
Thread(target=check_for_new_notifications, args=(dell_scraper, "dell")).start()


