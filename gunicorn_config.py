bind= "127.0.0.1"
workers=3
worker_class="sync"
accesslog="/news-reports/logs/gunicorn_access.log"
errorlog= "/news-reports/logs/gunicorn_error.log"
loglevel="info" 
