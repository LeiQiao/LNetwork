from plugins.base_schedule.schedule import Schedule
from .lnetwork_plugin import LNetworkPlugin
from .models import FlowModel
from pa import database as db
import pa
from .router import Router


class ScheduleRecordLANTraffic(Schedule):
    def __init__(self):
        super(ScheduleRecordLANTraffic, self).__init__()
        self.router = Router(pa.plugin_config[LNetworkPlugin.__pluginname__]['router_address'])

    def first_run(self):
        self.router.login(pa.plugin_config[LNetworkPlugin.__pluginname__]['username'],
                          pa.plugin_config[LNetworkPlugin.__pluginname__]['password'])

    def run(self):
        devs = self.router.get_device_traffic()
        if devs is None:
            pa.log.error('unable get device traffic, retry in next loop')
            return

        count = int(devs['count'])
        for i in range(1, count+1):
            dev = devs['dev{0}'.format(i)]
            mac = dev['mac']
            download = int(dev['downSpeed'])
            upload = int(dev['upSpeed'])
            if download < 0 or upload < 0:
                continue
            flow = FlowModel(mac=mac, upload=upload, download=download, ip=dev['ip'])
            try:
                db.session.add(flow)
                db.session.commit()
            except Exception as e:
                pa.log.error('unable insert table {0}: {1}'.format(FlowModel.__tablename__, e))
