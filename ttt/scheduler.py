import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, register_job

from django.conf import settings

from .transaction import cryptoExecute, stockMarketExecute, pendDayDelete

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)

def job_function():
    print("Hello World")

def start():
    if settings.DEBUG:
      	# Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.add_job(stockMarketExecute, 'cron', day_of_week='mon-fri', hour='9-15', minute='30-59', id="stockMarketExecute1", replace_existing=True)
    scheduler.add_job(stockMarketExecute, 'cron', day_of_week='mon-fri', hour='10-15', minute='0-29', id="stockMarketExecute2", replace_existing=True)

    scheduler.add_job(cryptoExecute, 'cron', day_of_week='*', hour='*', minute='*', id="cryptoExecute", replace_existing=True)
    scheduler.add_job(pendDayDelete, 'cron', day_of_week='tue-sat' , hour='0', id="pendDayDelete", replace_existing=True)
    
    # scheduler.add_job(job_function, 'interval', seconds=1)

    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job
    # scheduler.add_job("core.models.MyModel.my_class_method", "cron", id="my_class_method", hour=0, replace_existing=True)

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()
