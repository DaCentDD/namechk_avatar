import os
import time
import shutil

import requests
import cv2
from selenium.common.exceptions import NoSuchElementException


def check_vk(nickname, data, driver):
    time.sleep(0.2)
    driver.get(f'https://www.vk.com/{nickname}')
    try:
        results = driver.find_element_by_class_name('page_avatar_img')
        avatar = results.get_attribute("src")
    except (NoSuchElementException, IndexError) as e:
        try:
            results = driver.find_element_by_class_name('post_img')
            avatar = results.get_attribute("src")
        except (NoSuchElementException, IndexError):
            avatar = None
            status_code = 404
            data['vk'] = [status_code, avatar]
        else:
            status_code = 200
            data['vk'] = [status_code, avatar]
            with open(os.path.join('chk/static/chk/img/' + nickname, 'vk.png'), 'wb') as png:
                png.write(requests.get(avatar).content)
    else:
        status_code = 200
        data['vk'] = [status_code, avatar]
        with open(os.path.join('chk/static/chk/img/' + nickname, 'vk.png'), 'wb') as png:
            png.write(requests.get(avatar).content)


def check_insta(nickname, data, driver):
    driver.get(f'https://www.instagram.com/{nickname}')
    time.sleep(0.2)
    try:
        results = driver.find_elements_by_tag_name('img')
        # if len(results) == 1:
        #     raise NoSuchElementException
        avatar = results[0].get_attribute("src")

    except (NoSuchElementException, IndexError) as e:
        avatar = None
        status_code = 404
        data['insta'] = [status_code, avatar]
    else:
        status_code = 200
        data['insta'] = [status_code, avatar]
        with open(os.path.join('chk/static/chk/img/' + nickname, 'insta.png'), 'wb') as png:
            png.write(requests.get(avatar).content)


def check_twitter(nickname, data, driver):
    driver.get(f'https://www.twitter.com/{nickname}')
    time.sleep(0.5)
    try:
        results = driver.find_elements_by_class_name('css-9pa8cd')
        if len(results) < 2:
            avatar = results[0].get_attribute("src")
        else:
            avatar = results[1].get_attribute("src")
    except (NoSuchElementException, IndexError):
        avatar = None
        status_code = 404
        data['twitter'] = [status_code, avatar]
    else:
        status_code = 200
        data['twitter'] = [status_code, avatar]
        with open(os.path.join('chk/static/chk/img/' + nickname, 'twitter.png'), 'wb') as png:
            png.write(requests.get(avatar).content)


def check_youtube(nickname, data, driver):
    driver.get(f'https://www.youtube.com/user/{nickname}')
    time.sleep(0.2)
    try:
        results = driver.find_element_by_xpath("//img[@id='img']")
    except NoSuchElementException:
        avatar = None
        status_code = 404
        data['youtube'] = [status_code, avatar]
    else:
        avatar = results.get_attribute("src")
        status_code = 200
        data['youtube'] = [status_code, avatar]
        with open(os.path.join('chk/static/chk/img/' + nickname, 'youtube.png'), 'wb') as png:
            png.write(requests.get(avatar).content)


def check_avatars(data, nickname):
    need_to_check = []
    potential_the_same = {}
    for service, response in data.items():
        if type(response) is list:
            if response[0] == 200:
                need_to_check.append(service)
    for service_1 in range(len(need_to_check)):
        for service_2 in range(len(need_to_check)):
            if service_1 == service_2:
                continue
            compare_result = compare_image_hash(f'chk/static/chk/img/{nickname}/{need_to_check[service_1]}.png',
                                                f'chk/static/chk/img/{nickname}/{need_to_check[service_2]}.png')
            if compare_result < 15:
                if need_to_check[service_1] in potential_the_same.keys():
                    if need_to_check[service_2] not in potential_the_same[need_to_check[service_1]]:
                        potential_the_same[need_to_check[service_1]].append(need_to_check[service_2])
                elif need_to_check[service_2] in potential_the_same.keys():
                    if need_to_check[service_1] not in potential_the_same[need_to_check[service_2]]:
                        potential_the_same[need_to_check[service_2]].append(need_to_check[service_1])
                else:
                    potential_the_same[need_to_check[service_1]] = [need_to_check[service_2]]
    user_number = 1
    printed = []
    for key, value in potential_the_same.items():
        if key in printed and all(elem in printed for elem in value):
            continue
        printed.extend([key, *value])
        data[key].append(f"User {user_number}")
        for val in value:
            data[val].append(f"User {user_number}")
        user_number += 1
    shutil.rmtree(f'chk/static/chk/img/{nickname}')


def get_image_hash(FileName):
    image = cv2.imread(FileName)
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу
    hash_ = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                hash_ = hash_ + "1"
            else:
                hash_ = hash_ + "0"
    return hash_


def compare_image_hash(img1, img2):
    try:
        hash1 = get_image_hash(img1)
        hash2 = get_image_hash(img2)
    except:
        return 100
    finish = len(hash1)
    pixel_number = 0
    count = 0
    while pixel_number < finish:
        if hash1[pixel_number] != hash2[pixel_number]:
            count = count + 1
        pixel_number += 1
    return count