import logging
from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

logger = logging.getLogger(__name__)

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
            hour='9,14,20',
            minute=0,
            id='news_parser_job')
        sheduler.start()
        logger.debug('Планировщик новостей запущен')

    def run_news_saver(self, job=None):
        try:
            call_command('update_daily_news')
        except Exception as e: 
            logger.debug(f"Во время парсинга и сохранения новостей возникла ошибка: {e}")
