from django.apps import AppConfig
from django.conf import settings

class TttConfig(AppConfig):
    name = 'ttt'

    def ready(self):
    	from . import scheduler
    	if settings.SCHEDULER_AUTOSTART:
        	scheduler.start()