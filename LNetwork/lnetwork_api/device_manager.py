from flask import request, jsonify
from ..models import DeviceModel, FlowModel
from pa import database as db
from sqlalchemy import asc, desc
import pa
from .summary import get_range_summary
from datetime import datetime, timedelta


def get_device():
    try:
        devices = db.session.query(FlowModel.mac.label('mac'))
        devices = devices.group_by(FlowModel.mac).all()
    except Exception as e:
        pa.log.error('unable query table {0}: {1}'.format(FlowModel.__tablename__, e))
        return 'unable query device', 500

    all_device_desc = []
    for dev in devices:
        try:
            device = DeviceModel.query.filter_by(mac=dev.mac).first()
        except Exception as e:
            pa.log.error('unable query table {0}: {1}'.format(DeviceModel.__tablename__, e))
            return 'unable query device', 500

        try:
            first_appear = FlowModel.query.filter_by(mac=dev.mac).order_by(asc(FlowModel.create_time)).first()
            first_appear_time = first_appear.create_time.strftime('%Y-%m-%d %H:%M:%S')
            last_appear = FlowModel.query.filter_by(mac=dev.mac).order_by(desc(FlowModel.create_time)).first()
            last_appear_time = last_appear.create_time.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            pa.log.error('unable query table {0}: {1}'.format(FlowModel.__tablename__, e))
            return 'unable query device', 500

        try:
            secondly = get_range_summary(dev.mac, datetime.now()-timedelta(minutes=1), timedelta(minutes=1))
            secondly['download'] = int(secondly['download'] / 60)
            secondly['upload'] = int(secondly['upload'] / 60)

            hourly = get_range_summary(dev.mac, datetime.now()-timedelta(hours=1), timedelta(hours=1))
            daily = get_range_summary(dev.mac, datetime.now()-timedelta(days=1), timedelta(days=1))
            monthly = get_range_summary(dev.mac, datetime.now()-timedelta(days=31), timedelta(days=31))
        except Exception as e:
            str(e)
            return 'unable get device summary', 500

        device_desc = {
            'mac': dev.mac,
            'first_record_time': first_appear_time,
            'last_record_time': last_appear_time,
            'last_record_ip': last_appear.ip,
            'secondly': {
                'upload': secondly['upload'],
                'download': secondly['download']
            },
            'hourly': {
                'upload': hourly['upload'],
                'download': hourly['download']
            },
            'daily': {
                'upload': daily['upload'],
                'download': daily['download']
            },
            'monthly': {
                'upload': monthly['upload'],
                'download': monthly['download']
            }
        }
        if device is not None:
            device_desc['name'] = device.name
            device_desc['type'] = device.type
            device_desc['comment'] = device.comment
            device_desc['create_time'] = device.create_time.strftime('%Y-%m-%d %H:%M:%S')
        all_device_desc.append(device_desc)

    try:
        devices = DeviceModel.query.all()
    except Exception as e:
        pa.log.error('unable query table {0}: {1}'.format(DeviceModel.__tablename__, e))
        return 'unable query device', 500

    for device in devices:
        device_exists = False
        for device_desc in all_device_desc:
            if device_desc.get('mac') == device.mac:
                device_exists = True
                break
        if device_exists:
            continue

        all_device_desc.append({
            'mac': device.mac,
            'name': device.name,
            'type': device.type,
            'comment': device.comment,
            'create_time': device.create_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(all_device_desc), 200


def set_device():
    mac = request.json.get('mac')
    device_name = request.json.get('name')
    device_type = request.json.get('type')
    device_comment = request.json.get('comment')

    if mac is None or len(mac) == 0:
        return 'mac format error', 400

    if device_name is None and device_type is None and device_comment is None:
        return 'name, type, comment are None', 400

    try:
        device = DeviceModel.query.filter_by(mac=mac).first()
    except Exception as e:
        pa.log.error('unable query table {0}: {1}'.format(DeviceModel.__tablename__, e))
        return 'unable query device', 500

    create_device = False
    if device is None:
        create_device = True
        device = DeviceModel(mac=mac)

    if device is None:
        return 'device not found', 400

    if device_name is not None:
        device.name = device_name
    if device_type is not None:
        device.type = device_type
    if device_comment is not None:
        device.comment = device_comment

    try:
        if create_device:
            db.session.add(device)
        db.session.commit()
    except Exception as e:
        pa.log.error('unable write table {0}: {1}'.format(DeviceModel.__tablename__, e))
        return 'unable write device', 500

    return '', 200
