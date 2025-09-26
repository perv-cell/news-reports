import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import fmpsdk
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
import asyncio


# функция для парсинга с сайта https://www.mk.ru универсальная только для его тем, но не для других источников.

async def fetch_find_data_with_wwwmkru(day="", month="", year="", topic='economics'):

    ua = UserAgent()

    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://horo.mail.ru/prediction/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://www.mk.ru/{topic}/{year}/{month}/{day}',headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    main_contents = soup.find_all('ul', class_="article-listing__day-list")
    list_ads:list[list] = [] 
    list_elements = [] # сколько просмотров на сайте, картинка, заголовок, основной текст, 
    if main_contents:
        for main_content in main_contents:
            for ad in main_content.find_all('li', class_='article-listing__item'):
                views_peaple_html = ad.find('span', class_='meta__text')
                views_peaple_text = views_peaple_html.get_text(strip=True)
                picture_ad = ad.find('img', class_='listing-preview__image-content')
                img_url = picture_ad.get('src')
                header_ad = ad.find('h3' ,class_='listing-preview__title')
                header_ad_text = header_ad.get_text(strip=True)
                body_ad = ad.find('p' ,class_='listing-preview__desc')
                body_ad_text = body_ad.get_text(strip=True)
                author = ad.find('a' ,class_='article-preview__author')
                sourse = 'https://www.mk.ru/{topic}/'
                list_elements = [views_peaple_text,img_url,header_ad_text,body_ad_text,author,sourse]
                list_ads.append(list_elements)

    return list_ads


# для проверки работы 
async def main():
    try:
        list_ads = await fetch_find_data_with_wwwmkru()
        for res in list_ads:
            print(res)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())