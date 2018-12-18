import requests
import random
import json


class Router:
    def __init__(self, router_address):
        self.username = ''
        self.password = ''
        self.auth = ''
        self.connected = False

        self.login_url = '{0}/cgi-bin/luci'.format(router_address)
        self.devinfo_url = '{0}/cgi-bin/luci/admin/device/devInfo?type=1&_={0}'.format(router_address)

    def login(self, username, password):
        self.username = username
        self.password = password

        form_data = {
            'username': self.username,
            'psd': self.password
        }
        response = requests.post(self.login_url, data=form_data, allow_redirects=False, timeout=10)
        if response.status_code != 302:
            return False

        cookies = response.cookies.get_dict()
        if 'sysauth' in cookies:
            self.auth = cookies['sysauth']
        else:
            return False

        if len(self.auth) > 0:
            self.connected = True
            return True

        return False

    def get_device_traffic(self):
        if not self.connected:
            self.login(self.username, self.password)

        url = self.devinfo_url.format(random.uniform(0, 1))
        cookie = {
            'sysauth': self.auth
        }
        response = requests.get(url, cookies=cookie, timeout=10)
        if response.status_code != 200:
            self.connected = False
            return None

        dev_info = json.loads(response.text)
        return dev_info
