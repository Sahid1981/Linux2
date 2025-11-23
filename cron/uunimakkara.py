import requests

import re

import time

from bs4 import BeautifulSoup

from datetime import date



# --- Uunimakkaravahti ---

DAY_NAMES_FI = ["Maanantaina", "Tiistaina", "Keskiviikkona",

                "Torstaina", "Perjantaina", "Lauantaina", "Sunnuntaina"]

KEYWORDS = ["uunimakkara", "uunilenkki", "uunimakkarat", "uunilenkkiä"]

HEADERS = {"User-Agent": "Mozilla/5.0"}



def today_heading():

    today = date.today()

    dn = DAY_NAMES_FI[today.weekday()]

    return f"{dn} {today.day}.{today.month}."



def contains_keyword(text):

    t = text.lower()

    return any(k in t for k in KEYWORDS)



def extract_today_block(full_text):

    th = today_heading()

    pattern = rf"{re.escape(th)}(.*?)(?:{'|'.join(DAY_NAMES_FI)}|$)"

    m = re.search(pattern, full_text, flags=re.S | re.I)

    return m.group(1) if m else ""



def get_restaurant_links(city):

    url = f"https://www.lounaat.info/{city}"

    resp = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(resp.text, "lxml")

    links = []

    for a in soup.select("a[href^='/lounas/']"):

        name = a.get_text(strip=True)

        href = a.get("href")

        if href and name:

            links.append((name, "https://www.lounaat.info" + href))

    return list(dict(links).items())  # poistaa duplikaatit



def restaurant_has_oven_sausage(url):

    resp = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(resp.text, "lxml")

    txt = soup.get_text(separator="\n", strip=True)

    today_txt = extract_today_block(txt)

    return contains_keyword(today_txt)



def find_places(city):

    results = []

    for name, url in get_restaurant_links(city):

        try:

            if restaurant_has_oven_sausage(url):

                results.append((name, url))

        except:

            pass

        time.sleep(0.5)

    return results



def find_week_places(city):

    week_results = []

    for name, url in get_restaurant_links(city):

        try:

            resp = requests.get(url, headers=HEADERS)

            soup = BeautifulSoup(resp.text, "lxml")

            txt = soup.get_text(separator="\n", strip=True)

            days_found = []

            for dn in DAY_NAMES_FI:

                pattern = rf"{dn}.*?(?:{'|'.join(DAY_NAMES_FI)}|$)"

                m = re.search(pattern, txt, flags=re.S | re.I)

                if m and contains_keyword(m.group(0)):

                    days_found.append(dn)

            if days_found:

                week_results.append((name, url, days_found))

        except:

            pass

        time.sleep(0.5)

    return week_results


