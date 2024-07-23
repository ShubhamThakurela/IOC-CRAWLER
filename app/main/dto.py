from flask_restx import Namespace


class IocDto:
    """
    data transfer object (DTO) responsible for carrying data between processes. used for marshaling data
    for our API calls.
    """
    api = Namespace('CTI IOC', description='User Interface for CTI API')
    raw = api.model('CTI IOC', {})


class DownloadDto:
    """
    data transfer object (DTO) responsible for carrying data between processes. used for marshaling data
    for our API calls.
    """
    api = Namespace('IOC DB crawler', description='IOC DOWNLOADER')
    raw = api.model('IOC DB crawler', {})


class LoginDto:
    api = Namespace('App Login', description='User Interface for access the API')
    raw = api.model('App Login', {})


class MonitorDto:
    api = Namespace('Network Monitoring', description='User Interface for Monitor the API')
    raw = api.model('Network Monitoring', {})


class ALLMonitorDto:
    api = Namespace('Network Monitoring ALL', description='User Interface for Monitor the API')
    raw = api.model('Network Monitoring ALL', {})


class RulesDto:
    api = Namespace('Rules DB crawler', description='SIGMA/YARA RULES DOWNLOADER')
    raw = api.model('Rules DB crawler', {})


class TelegramDto:
    api = Namespace('Telegram DB crawler', description='TELEGRAM DOWNLOADER')
    raw = api.model('Telegram DB crawler', {})
