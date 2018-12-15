from flask import request, jsonify
from datetime import datetime, timedelta
import pa
from pa import database as db
from ..models import FlowModel
from sqlalchemy import and_, func


def summary():
    mac = request.args.get('mac')
    summary_type = request.args.get('type')
    begin_date = request.args.get('begin_date')
    end_date = request.args.get('end_date')

    if mac is None or len(mac) == 0:
        return 'mac is empty', 400

    if summary_type is None or len(summary_type) == 0:
        return 'type is empty', 400

    try:
        begin_date = datetime.strptime(begin_date, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        pa.log.error('begin_date format error {0}'.format(e))
        return 'begin_date format error', 400

    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        pa.log.error('end_date format error {0}'.format(e))
        return 'end_date format error', 400

    all_summary = []

    summary_type = summary_type.lower()
    if summary_type == 'secondly':
        time_interval = timedelta(seconds=1)
    elif summary_type == 'minutely':
        time_interval = timedelta(minutes=1)
    elif summary_type == 'hourly':
        time_interval = timedelta(hours=1)
    elif summary_type == 'daily':
        time_interval = timedelta(days=1)
    elif summary_type == 'monthly':
        time_interval = timedelta(days=31)
    else:
        return 'type error, (secondly, minutely, hourly, daily, monthly)', 400

    max_count = 1000
    current_count = 0
    while begin_date < end_date:
        try:
            all_summary.append(get_range_summary(mac, begin_date, time_interval))
        except Exception as e:
            str(e)
            return 'query hour summary error', 500
        begin_date += time_interval
        current_count += 1
        if current_count > max_count:
            return 'server max query first 1000 records', 400

    return jsonify(all_summary), 200


def get_range_summary(mac, time, timeinterval):
    # 统计某个时间段的流量
    time_start = time
    time_end = time_start + timeinterval

    time_sum = db.session.query(FlowModel.mac.label('mac'),
                                func.sum(FlowModel.upload).label('upload'),
                                func.sum(FlowModel.download).label('download'))
    time_sum = time_sum.filter(and_(FlowModel.create_time >= time_start,
                                    FlowModel.create_time < time_end))
    time_sum = time_sum.filter_by(mac=mac).group_by(FlowModel.mac)

    try:
        time_sum = time_sum.first()
    except Exception as e:
        pa.log.error('query table {0} error: {1}'.format(FlowModel.__tablename__, e))
        raise e

    if time_sum is not None:
        return {
            'time': time_start.strftime('%Y-%m-%d %H:%M:%S'),
            'upload': int(time_sum.upload),
            'download': int(time_sum.download)
        }
    else:
        return {
            'time': time_start.strftime('%Y-%m-%d %H:%M:%S'),
            'upload': 0,
            'download': 0
        }
