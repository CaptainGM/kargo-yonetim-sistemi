# -*- coding: utf-8 -*-
"""
Kargo İşlemleri ve Kullanıcı Rota Takibi HTTP İşleyicileri
"""
from datetime import datetime, timedelta
from typing import Dict
from database import get_db, get_next_id, serialize_docs
from handlers.base_handler import BaseHandler


def handle_get_cargos(handler):
    session = BaseHandler.get_session(handler)
    db = get_db()

    query = {}
    if session and session.get('role') != 'admin':
        query['user_id'] = session['user_id']

    cargos = list(db.cargos.find(query).sort('id', -1))

    # İstasyon ve kullanıcı bilgilerini zenginleştir
    stations_map = {s['id']: s for s in db.stations.find()}
    users_map = {u['id']: u.get('username', 'Misafir') for u in db.users.find()}

    result = []
    for c in cargos:
        st = stations_map.get(c.get('station_id'), {})
        doc = dict(c)
        if '_id' in doc:
            del doc['_id']
        doc['station_name'] = st.get('name', 'Bilinmiyor')
        doc['latitude'] = st.get('latitude')
        doc['longitude'] = st.get('longitude')
        doc['username'] = users_map.get(c.get('user_id'), 'Misafir')
        if isinstance(doc.get('created_at'), datetime):
            doc['created_at'] = doc['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        result.append(doc)

    BaseHandler.send_json(handler, result)


def handle_add_cargo(handler, data: Dict):
    session = BaseHandler.get_session(handler)
    user_id = session['user_id'] if session else None

    try:
        station_id = int(data.get('station_id', 0))
        weight = float(data.get('weight', 0))
        delivery_date = data.get('delivery_date') or (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        BaseHandler.send_json(handler, {'error': 'Geçersiz kargo parametreleri'}, 400)
        return

    if station_id <= 0 or weight <= 0:
        BaseHandler.send_json(handler, {'error': 'Geçerli bir istasyon ve ağırlık belirtiniz'}, 400)
        return

    db = get_db()
    cid = get_next_id('cargos')
    tracking_code = data.get('tracking_code') or f"LGT-TR{station_id:02d}-{cid:04d}"
    delivery_type = data.get('delivery_type', 'Standart Dağıtım')

    db.cargos.insert_one({
        'id': cid,
        'tracking_code': tracking_code,
        'delivery_type': delivery_type,
        'user_id': user_id,
        'station_id': station_id,
        'weight': weight,
        'status': 'pending',
        'delivery_date': delivery_date,
        'created_at': datetime.now()
    })

    BaseHandler.send_json(handler, {'success': True, 'id': cid, 'tracking_code': tracking_code})


def handle_delete_cargo(handler, cargo_id: int):
    session = BaseHandler.get_session(handler)
    if not session:
        BaseHandler.send_json(handler, {'error': 'Giriş yapmalısınız'}, 401)
        return

    db = get_db()
    query = {'id': cargo_id}
    if session.get('role') != 'admin':
        query['user_id'] = session['user_id']

    res = db.cargos.delete_one(query)
    if res.deleted_count > 0:
        BaseHandler.send_json(handler, {'success': True})
    else:
        BaseHandler.send_json(handler, {'error': 'Kargo bulunamadı veya silme yetkiniz yok'}, 404)


def handle_get_my_route(handler):
    """
    Kullanıcının kargosunun dağıtılacağı rotayı ve sırayı haritada göstermek üzere döner.
    """
    session = BaseHandler.get_session(handler)
    if not session:
        BaseHandler.send_json(handler, {'error': 'Giriş yapmalısınız'}, 401)
        return

    user_id = session['user_id']
    db = get_db()

    # Kullanıcının kargolarını bul
    user_cargos = list(db.cargos.find({'user_id': user_id}))
    if not user_cargos:
        BaseHandler.send_json(handler, {'routes': [], 'message': 'Henüz kayıtlı bir kargonuz bulunmamaktadır.'})
        return

    cargo_ids = [c['id'] for c in user_cargos]
    stations_map = {s['id']: s for s in db.stations.find()}

    # Bu kargoların içinde bulunduğu aktif rotaları bul
    routes = list(db.routes.find({'cargo_ids': {'$in': cargo_ids}}).sort('created_at', -1))

    results = []
    for r in routes:
        route_names = r.get('route_names', [])
        # Rota istasyonlarının koordinatlarını hazırla
        station_objects = []
        for name in route_names:
            st = db.stations.find_one({'name': name})
            if st:
                station_objects.append({
                    'id': st['id'],
                    'name': st['name'],
                    'latitude': st['latitude'],
                    'longitude': st['longitude'],
                    'is_depot': st.get('is_depot', False)
                })

        # Kullanıcının bu rotadaki kargoları
        user_cargos_in_route = [c for c in user_cargos if c['id'] in r.get('cargo_ids', [])]

        results.append({
            'route_id': r.get('id'),
            'vehicle_name': r.get('vehicle_name', 'Dağıtım Aracı'),
            'total_distance': r.get('total_distance', 0),
            'total_cost': r.get('total_cost', 0),
            'stations': station_objects,
            'route_names': route_names,
            'my_cargos': [{
                'id': c['id'],
                'weight': c['weight'],
                'status': c.get('status', 'pending'),
                'station_name': stations_map.get(c.get('station_id'), {}).get('name', '')
            } for c in user_cargos_in_route]
        })

    BaseHandler.send_json(handler, {'routes': results})
