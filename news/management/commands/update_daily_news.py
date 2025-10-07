from django.core.management.base import BaseCommand
from news.models import NewsDate
from news.utilits import fetch_find_data_with_wwwmkru # новые функции под новые источники 
from asgiref.sync import sync_to_async
import asyncio
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand): # класс для парсинга данных и сохранения их в базе данных 

#эти аргументы можно добавить для гибкости, то есть передавать в apps параметры с которыми будет запускаться крон и здесь их ловить
    """
    def add_arguments(self, parser):
        parser.add_argument(
            '--topics',                   
            type=str,                     
            help='Темы для парсинга',      
            default='economics,politics,sport,culture'  
        )
"""
    def handle(self, *args, **kwargs):
        asyncio.run(self.save_data_db_today_news())
        
    async def save_data_db_today_news(self):
        

        source = {'https://www.mk.ru':
        ['economics','politics','sport','culture','auto'],}
        
        tasks = []

        for key in source.keys():
            if key == 'https://www.mk.ru':
                for topic in source[key]:                 
                    tasks.append(asyncio.create_task(fetch_find_data_with_wwwmkru(topic=topic)))
            elif key =='':
                pass # здесь также пробегаюсь циклом по темам, но функция парса будет уже другой

        data_news = await asyncio.gather(*tasks)
        saved_count = await self.async_save_news(data_news)

        logger.debug(f"Успешное сохранение в базу данных новых {saved_count} новостей ")


    async def async_save_news(self,data_news:list):

        saved_count = 0
        for item_news_topic in data_news:
            for news_item in item_news_topic:
                bool_save = await self.save_news_sync(news_item)
                if bool_save == True:
                    saved_count+=1

        return saved_count

    @sync_to_async
    def save_news_sync(self, news_item):
        try:
            logger.debug(f"Сохранение: {news_item.get('title', 'No title')}")
        
            if NewsDate.objects.filter(title=news_item['title']).exists():
                logger.info(f"Дубликат: {news_item['title']}")
                return False
        
            news_data = {
            'title': news_item['title'],
            'image_url': news_item.get('image_url') or '',
            'main_text': news_item.get('main_text') or '',
            'author': news_item.get('author') or 'Неизвестен',
            'source': news_item.get('source') or 'mk.ru',
            'views': news_item.get('views', 0),
            'topic': news_item.get('topic') or 'general',
            'save_peaple_id': news_item.get('save_peaple_id') or 'parser'
            }
        
            NewsDate.objects.create(**news_data)
            logger.info(f"Успешно сохранено: {news_data['title'][:50]}...")
            return True
        
        except Exception as e:
            logger.error(f"Ошибка сохранения: {e}")
            return False 
   
