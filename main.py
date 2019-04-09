#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import time
import urllib.request as urllib2
from socket import timeout
import sys
# import csv
import codecs

__author__ = 'artemiev'
print_result = 1


def load_helper(uri):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        thing = opener.open(uri, None, 10)
        soup = BeautifulSoup(thing.read(), "lxml")
        if not (soup is None):
            return soup
        else:
            print("soup is None")
            load_helper(uri)
    except (timeout, urllib2.HTTPError, urllib2.URLError) as error:
        sys.stdout.write("{} encountered, hold on, bro".format(error))
        sys.stdout.flush()
        time.sleep(30)
        load_helper(uri)


def get_number(tr):
    number_item = int(tr.find("span").get_text()[:-1])
    if print_result:
        print(number_item)
    return number_item


def get_metro_station(tr):
    metro_raw = tr.find('a', attrs={'href': re.compile("metro")})
    metro_station = metro_raw.get_text()
    if print_result:
        print(metro_station)
    return metro_station


def get_metro_distance(tr):
    # walk_type = u'пешком'
    metro_distance = tr.find("span", attrs={'class': re.compile('objects_item_metro_comment')}).get_text()
    metro_distance_minute = re.search(r'\d+', metro_distance).group()
    metro_distance_walk = re.search(u'пешком', metro_distance)
    metro_distance_car = re.search(u'на машине', metro_distance)

    distance_type = ""
    if metro_distance_walk:
        distance_type = "пешком"
        on_car = False
    elif metro_distance_car:
        distance_type = "на машине"
        on_car = True
    else:
        print("error with distance to metro")
        print(metro_distance)
        on_car = None
    distance_to_metro = str(metro_distance_minute) + " мин. " + distance_type
    if on_car:
        distance_to_metro_universal = int(metro_distance_minute) * 5
    else:
        distance_to_metro_universal = int(metro_distance_minute)
    if print_result:
        print(distance_to_metro)
    return distance_to_metro_universal


def get_address(tr):
    address = ""
    for addressField in tr.find_all("div", attrs={'class': 'objects_item_addr'}):
        address += addressField.get_text().strip() + " "
    if print_result:
        print(address)
    return address


def get_rooms(tr):
    how_many_rooms = tr.find("div", attrs={'class': 'objects_item_info_col_2'}).find("strong").get_text()
    if print_result:
        print(how_many_rooms)
    return how_many_rooms


def get_price_roubles(tr):
    print(tr)
    price_roubles = tr.find("div", attrs={'class': 'objects_item_price'}).get_text()
    price_roubles_digit = re.findall(r'\d+', price_roubles.strip())
    price_roubles = ""
    for i in price_roubles_digit:
        price_roubles += i
    price_roubles = int(price_roubles)
    if print_result:
        print("стоимость в рублях:" + str(price_roubles))
    return price_roubles


def get_square_all(tr):
    print(tr)
    td = tr.find("div", attrs={'class': 'objects_item_info_col_3'}).find_all("td")
    main_size = 0
    for square in td:
        main = re.search(r'Общая: \d+ м', square.get_text())
        if main is not None:
            main_size = re.search(r'\d+', main.group())
            main_size = main_size.group()
            if print_result: print("Общая:" + str(main_size))

    return int(main_size)


def get_square_kitchen(tr):
    td = tr.find("td", attrs={'class': 'objects_item_info_col_3'}).find_all("td")
    kitchen_size = 0
    for square in td:
        kitchen = re.search(r'Кухня: \d+ м', square.get_text())
        if kitchen is not None:
            kitchen_size = re.search(r'\d+', kitchen.group())
            kitchen_size = kitchen_size.group()
            if print_result: print("Кухня:" + str(kitchen_size))
    return int(kitchen_size)


def get_square_live(tr):
    td = tr.find("td", attrs={'class': 'objects_item_info_col_3'}).find_all("td")
    live_size = 0
    for square in td:
        live = re.search(r'Жилая: \d+ м', square.get_text())
        if live is not None:
            live_size = re.search(r'\d+', live.group())
            live_size = live_size.group()
            if print_result:
                print("Жилая:" + str(live_size))
    return int(live_size)


def get_price_per_meter(tr):
    td = tr.find("td", attrs={'class': 'objects_item_info_col_4'})
    price_per_meter = td.find('div', attrs={'style': 'color:green;'})
    price_per_meter = price_per_meter.get_text().strip()[3:]
    price_per_meter_digit = re.findall(r'\d+', price_per_meter)
    price_per_meter = ""
    for i in price_per_meter_digit:
        price_per_meter += i
    price_per_meter = int(price_per_meter)
    if print_result:
        print("цена в рублях за метр^2:" + str(price_per_meter))
    return price_per_meter


def get_building_type(tr):
    td = tr.find("td", attrs={'class': 'objects_item_info_col_5'})
    house_type = td.find('div', attrs={'class': 'objects_item_info_col_w'}).get_text()
    house_type_str = re.search(u'[-а-яА-Я]+', house_type)
    house_type = str(house_type_str.group().encode('utf-8')).strip()
    if print_result:
        print(house_type)
    return house_type


def get_floor(tr):
    td = tr.find("td", attrs={'class': 'objects_item_info_col_5'})
    floor = td.find('div', attrs={'class': 'objects_item_info_col_w'}).get_text()
    floor_info = re.search(r'\d+/*\d*', floor)
    floor = str(floor_info.group()).split('/')[0]
    if len(str(floor_info.group()).split('/')) > 1:
        floor_all = str(floor_info.group()).split('/')[1]
    floor = int(floor)
    if print_result:
        print("Этаж: " + str(floor))
    return floor


def get_floor_all(tr):
    td = tr.find("td", attrs={'class': 'objects_item_info_col_5'})
    floor = td.find('div', attrs={'class': 'objects_item_info_col_w'}).get_text()
    floor_all = 0
    floor_info = re.search(r'\d+/*\d*', floor)
    floor = str(floor_info.group()).split('/')[0]
    if len(str(floor_info.group()).split('/')) > 1:
        floor_all = str(floor_info.group()).split('/')[1]
    floor_all = int(floor_all)
    if print_result and floor_all: print("Этажность:" + str(floor_all))
    return floor_all


def get_additional_properties(tr):
    td = tr.find("td", attrs={'class': 'objects_item_info_col_6'})
    td = td.find("table", attrs={'class': 'objects_item_details'})
    td = td.find_all("td")
    lift = td[0]
    lift_exist = re.search(r'\d+', str(lift))
    if lift_exist is None:
        lift = 0
    else:
        lift = 1
    balcon = td[1]
    balcon_exist = re.search(r'\d+', str(balcon))
    if balcon_exist is None:
        balcon = 0
    else:
        balcon = 1

    window = td[3].get_text().encode('utf-8')
    window_street_exist = re.search('улица', window)
    if window_street_exist is not None:
        window_street = 1
    else:
        window_street = 0

    window_backyard_exist = re.search('двор', window)
    if window_backyard_exist is not None:
        window_backyard = 1
    else:
        window_backyard = 0

    phone = td[4].get_text().encode('utf-8')
    phone_exist = re.search('да', phone)
    if phone_exist is not None:
        phone = 1
    else:
        phone = 0

    if print_result:
        print("Есть ли лифт:" + str(lift))
    if print_result:
        print("Есть ли балкон:" + str(balcon))
    if print_result:
        print("Есть ли окно на улицу:" + str(window_street))
    if print_result:
        print("Есть ли окно во двор:" + str(window_backyard))
    if print_result:
        print("Есть ли телефон:" + str(phone))
    return [lift, balcon, window_street, window_backyard, phone]


def get_info(tr):
    number = get_number(tr)
    print(number)
    metro_station = get_metro_station(tr)
    metro_distance = get_metro_distance(tr)
    address = get_address(tr)
    rooms = get_rooms(tr)
    square_all = get_square_all(tr)
    square_kitchen = get_square_kitchen(tr)
    square_live = get_square_live(tr)
    # fix cian bug
    if square_kitchen + square_live > square_all:
        square_kitchen = 0
        square_live = 0
    price_roubles = get_price_roubles(tr)
    # price_dollars = get_price_dollars(tr) #  todo add get_price_dollars
    price_per_meter = get_price_per_meter(tr)
    building_type = get_building_type(tr)
    floor = get_floor(tr)
    floor_all = get_floor_all(tr)
    ap = get_additional_properties(tr)
    full_info = str(number) + "," + metro_station.encode('utf-8') + "," + str(metro_distance) + ',"' + \
                address.encode('utf-8') + '",' + rooms.encode('utf-8') + "," + str(square_all) + "," + \
                str(square_kitchen) + "," + str(square_live) + "," + str(price_roubles) + "," + str(price_dollars) + \
                "," + str(price_per_meter) + "," + building_type + "," + str(floor) + "," + str(floor_all) + "," \
                + str(ap[0]) + "," + str(ap[1]) + "," + str(ap[2]) + "," + str(ap[3]) + ',' + str(ap[4]) + '\n'
    full_info = full_info.decode('utf-8')
    print("saving file")
    file_table = codecs.open("6roomsflat.csv", "a", "utf-8")
    file_table.write(full_info)
    file_table.close()


rooms = 2
LINKORIGINAL = 'http://www.cian.ru/cat.php?deal_type=2&obl_id=1&city%5B0%5D=1&room' + str(rooms) + \
               '=1&sost_type=1&object_type=1&p='
for page_number in range(2, 3):
    time.sleep(2)
    LINK = LINKORIGINAL
    if page_number == 0:
        continue
    if page_number == 1:
        LINK = LINK[:-3]
    else:
        LINK += str(page_number)
    page = load_helper(LINK)

    tr_all = page.find_all("div", attrs={'class': re.compile('offer_container')})

    get_price_roubles(tr_all[3])

    # for tr in tr_all:
    # print tr
    #    get_rooms(tr)
    #     try:
    #         print(tr)
    #         getInfo(tr)
    #     except Exception:
    #         print("error")
    #         pass
