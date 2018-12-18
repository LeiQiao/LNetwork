from plugins.base.config_model import ConfigModel


class LNetworkConfig(ConfigModel):
    __configname__ = 'LNetwork'

    router_address = ConfigModel.Column('http://127.0.0.1')
    username = ConfigModel.Column('')
    password = ConfigModel.Column('')
