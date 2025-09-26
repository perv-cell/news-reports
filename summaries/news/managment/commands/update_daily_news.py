from django.core.management.base import BaseCommand
from news.models import NewsDate, save_news_in_db
from news.utilits import fetch_find_data_with_wwwmkru # новые функции под новые источники 
from asgiref.sync import sync_to_async
import asyncio


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        asyncio.run(self.save_data_db_today_news)
        
    async def save_data_db_today_news(self):
        
        source = {'https://www.mk.ru':
        ['economics','politics','sport','culture'],
        }
        
        tasks = []

        for key in source.items():
            if key == 'https://www.mk.ru':
                for topic in source[key]:
                    tasks.append(asyncio.create_task(fetch_find_data_with_wwwmkru(topic)))
            elif key =='':
                pass # здесь также пробегаюсь циклом по тема, но функция парса будет уже другой

        data_news = await asyncio.gather(*tasks)
        saved_count = await self.async_save_news(data_news)

        self.stdout.write(
            self.style.SUCCESS(f'Успешно сохранено {saved_count} новостей')
        )


    async def async_save_news(self,data_news:list):

        saved_count = 0
        for item_news in data_news:
            bool_save = await self.save_news_sync(item_news)
            if bool_save == True:
                saved_count+=1

        return saved_count

    @sync_to_async
    def save_news_sync(self,news_item):
        if not NewsDate.objects.filter(title=news_item['title']).exists():
            NewsDate.objects.create(**news_item)
            return True
        else:
            return False