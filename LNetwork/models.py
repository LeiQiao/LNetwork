from pa import database as db
from datetime import datetime


class DeviceModel(db.Model):
    __tablename__ = 'lan_device'

    mac = db.Column(db.String(128), primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64), default='<unknown>')
    comment = db.Column(db.String(1024), default='')
    create_time = db.Column(db.DateTime, default=datetime.now)


class FlowModel(db.Model):
    __tablename__ = 'lan_device_traffic'

    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(128), nullable=False)
    upload = db.Column(db.BigInteger, default=0)
    download = db.Column(db.BigInteger, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    ip = db.Column(db.String(64), default='')
