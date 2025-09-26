from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from news.managment.commands.update_daily_news import Command

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        self.start_scheduler()

    def start_scheduler(self):
        sheduler = BackgroundScheduler()
        sheduler.add_job(
            self.run_news_saver,
            'cron',
            hour='9,18',
            minute=0,
            id='news_parser_job')
        sheduler.start()
        print('Планировщик новостей запущен')

    async def run_news_saver():
        try:
            command = Command()
            await command.handle()
        except Exception as e: 
            print(e)
