# noinspection PyStatementEffect
{
    'name': 'LNetwork',
    'summary': '局域网流量监控',
    'description': '基于电信天翼智能网管，定时统计当前局域网的设备流量',
    'author': '',
    'website': '',
    'source': {'git': 'git@github.com:LeiQiao/LNetwork.git', 'branch': 'master'},

    'category': '',
    'version': '0.1',

    'schedule': {
        'ScheduleRecordLANTraffic': '*/10 * * * * *'
    },

    'api': {
        '/lnetwork/summary': 'lnetwork_api.summary',
        '/lnetwork/device': {
            'GET': 'lnetwork_api.get_device',
            'PUT': 'lnetwork_api.set_device'
        }
    },

    # any plugin necessary for this one to work correctly
    'depends': ['base', 'base_schedule', 'base_api_wrapper']
}
