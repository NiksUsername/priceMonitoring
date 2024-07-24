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
        time.sleep(1)
        get_website_update(web_scraper, link, False)
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
                            "data":value,
                            "type":type,
                            "website":name
                        })
                time.sleep(1)
            delta = datetime.now() - curr_time
            time.sleep(max(300 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=300)
        except Exception:
            print(f"Major {name} Exception")


Thread(check_for_new_notifications(argos_scraper, "argos")).start()
Thread(check_for_new_notifications(currys_scraper, "currys")).start()
Thread(check_for_new_notifications(game_co_scraper, "game")).start()
Thread(check_for_new_notifications(johnlewis_scraper, "johnlewis_scraper")).start()
Thread(check_for_new_notifications(selfridges_scraper, "selfridges")).start()
Thread(check_for_new_notifications(coolshop_scraper, "coolshop")).start()
Thread(check_for_new_notifications(houseoffraser_scraper, "houseoffraser")).start()
Thread(check_for_new_notifications(laptopsdirect_scraper, "laptopsdirect")).start()
Thread(check_for_new_notifications(ryman_scraper, "ryman")).start()
Thread(check_for_new_notifications(dell_scraper, "dell")).start()


