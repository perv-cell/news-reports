import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging
import fmpsdk
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
from django.urls import reverse
import asyncio

logger = logging.getLogger(__name__)

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
    views_number = 0
    list_ads:list[dict] = [] 
    if main_contents:
        for main_content in main_contents:
            for ad in main_content.find_all('li', class_='article-listing__item'):
                views_peaple_html = ad.find('span', class_='meta__text')
                views_peaple_text = views_peaple_html.get_text(strip=True) if views_peaple_html else ""
                views_number = 0
                if views_peaple_text:
                    # Извлекаем все цифры из строки
                    digits = ''.join(filter(str.isdigit, views_peaple_text))
                    if digits:
                        views_number = int(digits)
                    else:
                        views_number = 0
                picture_ad = ad.find('img', class_='listing-preview__image-content')
                img_url = picture_ad.get('src')
                header_ad = ad.find('h3' ,class_='listing-preview__title')
                header_ad_text = header_ad.get_text(strip=True)
                body_ad = ad.find('p' ,class_='listing-preview__desc')
                body_ad_text = body_ad.get_text(strip=True)
                author = str(ad.find('a' ,class_='article-preview__author'))
                source = f'https://www.mk.ru/{topic}/'
                dict_elements = {
                    'title':header_ad_text,
                    'image_url':img_url,
                    'main_text':body_ad_text,
                    'author':author,
                    'source':source,
                    'views':views_number,
                    'topic':topic,
                    'save_peaple_id':'parser',
                }
                list_ads.append(dict_elements)

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




#  для пагинации 
def generate_pagination_urls(page_obj, count_page, name_page_revers='MainPage',name_page_revers_index='MainPagePagination', pagination_dur_interva=8):
        urls = {}
        urls['pagination_dur_interva'] = pagination_dur_interva
        if page_obj.has_previous():
            prev_page = page_obj.previous_page_number()
            if prev_page == 1:
                urls['previous'] = {'url': reverse(name_page_revers), 'title': 'Популярные новости'}
                urls['pagination_start'] = 1 
            else:
                urls['previous'] = {
                    'url': reverse(name_page_revers_index, args=[prev_page]),
                    'text': f'Страница {prev_page}'
                }
                urls['pagination_start'] = prev_page
        
        if page_obj.has_next():
            next_page = page_obj.next_page_number()
            urls['next'] = {
                'url': reverse(name_page_revers_index, args=[next_page]),
                'title': f'Страница {next_page}' 
            }

        urls['page_range'] = []
        pagination_start = urls.get('pagination_start', 1)
        pagination_end = count_page
        if count_page < 8:
            pagination_end = count_page
        else: 
            pagination_dur_interval = urls.get('pagination_dur_interva')
            if pagination_start + pagination_dur_interval > count_page:
                while (pagination_start + pagination_dur_interval) >=  count_page:
                    pagination_start-=1  
            pagination_end = pagination_start+pagination_dur_interval


        for i in range(pagination_start, pagination_end + 1):
            if i == 1:
                urls['page_range'].append({
                    'number': i,
                    'url': reverse(name_page_revers),
                    'current': i == page_obj.number
                })
            else:
                urls['page_range'].append({
                    'number': i,
                    'url': reverse(name_page_revers_index, args=[i]),
                    'current': i == page_obj.number
                }
            )
        return urls 
