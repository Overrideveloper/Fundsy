from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from pytz import utc
from .jobs.investment_appreciation import customerInvestmentAppreciation
from common.config import REDIS_HOST, REDIS_PORT

jobstores = {
    'default': RedisJobStore(db=2, host=REDIS_HOST, port=REDIS_PORT)
}

job_scheduler = AsyncIOScheduler(jobstores=jobstores, timezone=utc)

def initialize_cron():
    job_scheduler.start()
    job_scheduler.add_job(customerInvestmentAppreciation, "cron", hour=0, replace_existing=True, id=customerInvestmentAppreciation.__name__)

def shutdown_cron():
    job_scheduler.shutdown()
