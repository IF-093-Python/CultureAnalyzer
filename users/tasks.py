from celery.utils.log import get_task_logger
from datetime import datetime
from django.contrib.sessions.models import Session

from CultureAnalyzer import celery_app
from django.utils.timezone import get_current_timezone

logger = get_task_logger(__name__)


@celery_app.task(name='clear-expired-sessions', ignore_result=True)
def clear_expired_sessions():
    now = datetime.now(tz=get_current_timezone())
    Session.objects.filter(expire_date__lt=now).delete()
    logger.info(f'Sessions were cleared at: {now}')
