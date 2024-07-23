import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Blueprint
from flask_restx import Api
from main import paths
from main.constan_service import ConstantService
from main.ioc_controller import api as iocpost
from main.fetched_controller import api as DownloadDto
from main.login_controller import api as LoginDto
from main.monitoring_controller import api as MonitorDto
from main.telegram_controller import api as teleDto
from main.rules_controller import api as rulesDto
from main.all_monitor_controller import api as ALLMonitorDto


logging.basicConfig(
    handlers=[
        RotatingFileHandler(os.path.join(paths.LOG_PATH, 'cti_analyst-app.log'), maxBytes=1024 * 1024, backupCount=10)],
    level=logging.DEBUG,
    format=f'%(asctime)s %(api_key)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d %(levelname)s %('
           f'message)s'
)

old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.api_key = "SignalZeroAPP00001"
    return record


logging.setLogRecordFactory(record_factory)

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='IOC Crawler API',
          version='1.0.0 _(Beta)',
          description='Data Crawler for IOC',
          )
api.add_namespace(iocpost, path='/ioc-crawler')
api.add_namespace(MonitorDto, path='/latest-ioc')
api.add_namespace(ALLMonitorDto, path='/all-ioc')
api.add_namespace(DownloadDto, path='/ioc-downloader')
api.add_namespace(rulesDto, path='/rules-downloader')
api.add_namespace(teleDto, path='/telegram-downloader')
api.add_namespace(LoginDto, path='/user')
