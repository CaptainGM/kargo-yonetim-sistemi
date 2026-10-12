# -*- coding: utf-8 -*-
"""
Rota Optimizasyonu ve Senaryo Analiz HTTP İşleyicileri
"""
from datetime import datetime, timedelta
from typing import Dict, List
from database import get_db, get_next_id, serialize_docs
from handlers.base_handler import BaseHandler
from optimizer import RouteOptimizer


def handle_optimize(handler, data: Dict):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Bu işlem için yönetici yetkisi gereklidir'}, 403)
        return

    problem_type = data.get('type', 'limited')
    optimize_for = data.get('optimize_for', 'balanced')
    delivery_date = data.get('delivery_date')
    cargo_ids = data.get('cargo_ids', [])

    db = get_db()
    query = {'status': 'pending'}
    if cargo_ids:
        query['id'] = {'$in': [int(cid) for cid in cargo_ids]}
    elif delivery_date:
        query['delivery_date'] = delivery_date

    cargos = list(db.cargos.find(query))
    if not cargos:
        BaseHandler.send_json(handler, {'error': 'Optimizasyon için bekleyen kargo bulunamadı'}, 400)
        return

    # İstasyon ve kullanıcı adlarını kargolara ekle
    stations = list(db.stations.find({'is_active': 1}))
    stations_map = {s['id']: s for s in stations}
    users_map = {u['id']: u.get('username', 'Misafir') for u in db.users.find()}

    for c in cargos:
        st = stations_map.get(c.get('station_id'), {})
        c['station_name'] = st.get('name', 'Bilinmiyor')
        c['latitude'] = st.get('latitude')
        c['longitude'] = st.get('longitude')
        c['username'] = users_map.get(c.get('user_id'), 'Misafir')

    vehicles = list(db.vehicles.find({'is_owned': 1}))
    params = db.parameters.find_one({'id': 1}) or {'cost_per_km': 1.0, 'rental_cost': 200.0, 'rental_capacity': 500}

    optimizer = RouteOptimizer(stations, cargos, vehicles, params, optimize_for)
    if problem_type == 'unlimited':
        result = optimizer.solve_unlimited_vehicles()
    else:
        result = optimizer.solve_limited_vehicles()

    # Rotaları veritabanına kaydet ve kargoları 'assigned' yap
    for route_info in result.get('routes', []):
        v = route_info.get('vehicle', {})
        assigned_cargos = route_info.get('cargos', [])
        assigned_c_ids = [c['id'] for c in assigned_cargos]

        route_id = get_next_id('routes')
        db.routes.insert_one({
            'id': route_id,
            'vehicle_id': v.get('id'),
            'vehicle_name': v.get('name', 'Araç'),
            'vehicle_plate': v.get('plate', ''),
            'route_data': route_info.get('route', []),
            'route_names': route_info.get('route_names', []),
            'total_distance': route_info.get('distance', 0),
            'total_cost': route_info.get('cost', 0),
            'total_fuel_cost': route_info.get('fuel_cost', 0),
            'total_fuel_liters': route_info.get('fuel_liters', 0),
            'total_toll_cost': route_info.get('toll_cost', 0),
            'total_driver_cost': route_info.get('driver_cost', 0),
            'co2_emission_kg': route_info.get('co2_emission_kg', 0),
            'total_weight': route_info.get('weight', 0),
            'cargo_count': route_info.get('cargo_count', 0),
            'cargo_ids': assigned_c_ids,
            'created_at': datetime.now()
        })

        if assigned_c_ids:
            db.cargos.update_many(
                {'id': {'$in': assigned_c_ids}},
                {'$set': {'status': 'assigned', 'route_id': route_id}}
            )

    BaseHandler.send_json(handler, result)


def handle_load_scenario(handler, data: Dict):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    scenario = data.get('scenario', [])
    scenario_num = data.get('scenario_num', 1)

    db = get_db()
    # Mevcut bekleyen kargoları ve tamamlanmış rotaları temizle
    db.routes.delete_many({})
    db.cargos.delete_many({'status': 'pending'})

    stations = list(db.stations.find({'is_active': 1}))
    cargo_count = 0
    delivery_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    for item in scenario:
        district = item.get('district', '')
        count = int(item.get('count', 0))
        weight = float(item.get('weight', 0))

        if count > 0:
            target_station = next((s for s in stations if district.lower() in s['name'].lower()), None)
            if target_station:
                avg_weight = round(weight / count, 2)
                for _ in range(count):
                    cid = get_next_id('cargos')
                    db.cargos.insert_one({
                        'id': cid,
                        'user_id': None,
                        'station_id': target_station['id'],
                        'weight': avg_weight,
                        'status': 'pending',
                        'delivery_date': delivery_date,
                        'created_at': datetime.now()
                    })
                    cargo_count += 1

    BaseHandler.send_json(handler, {'success': True, 'cargo_count': cargo_count, 'scenario': scenario_num})


def handle_compare_scenarios(handler, data: Dict):
    """
    Test senaryoları üzerinde 3 farklı optimizasyon stratejisini (balanced, max_count, max_weight)
    veritabanını değiştirmeden simüle eder ve kıyaslama tablosunu döndürür.
    """
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    scenarios_data = data.get('scenarios', [])
    problem_type = data.get('type', 'limited')

    db = get_db()
    stations = list(db.stations.find({'is_active': 1}))
    vehicles = list(db.vehicles.find({'is_owned': 1}))
    params = db.parameters.find_one({'id': 1}) or {'cost_per_km': 1.0, 'rental_cost': 200.0, 'rental_capacity': 500}

    results = []
    for scenario_idx, scenario in enumerate(scenarios_data, 1):
        cargos = []
        cargo_id = 1
        for item in scenario:
            district = item.get('district', '')
            count = int(item.get('count', 0))
            weight = float(item.get('weight', 0))
            if count > 0:
                target_st = next((s for s in stations if district.lower() in s['name'].lower()), None)
                if target_st:
                    avg_w = round(weight / count, 2)
                    for _ in range(count):
                        cargos.append({
                            'id': cargo_id,
                            'station_id': target_st['id'],
                            'weight': avg_w,
                            'station_name': target_st['name']
                        })
                        cargo_id += 1

        if cargos:
            for opt_mode in ['balanced', 'max_count', 'max_weight']:
                try:
                    optimizer = RouteOptimizer(stations, cargos, vehicles, params, opt_mode)
                    if problem_type == 'unlimited':
                        res = optimizer.solve_unlimited_vehicles()
                    else:
                        res = optimizer.solve_limited_vehicles()

                    undelivered = res.get('undelivered', [])
                    undelivered_reason = ''
                    if undelivered:
                        tot_cap = sum(v['capacity'] for v in vehicles)
                        tot_w = sum(c['weight'] for c in cargos)
                        if problem_type == 'limited' and tot_w > tot_cap:
                            undelivered_reason = f'Kapasite yetersiz ({tot_cap}kg < {tot_w}kg)'
                        else:
                            undelivered_reason = 'Araç kapasitesi yetersiz'

                    results.append({
                        'scenario': scenario_idx,
                        'problem_type': problem_type,
                        'optimize_for': opt_mode,
                        'total_cost': round(res.get('total_cost', 0), 2),
                        'total_fuel_cost': round(res.get('total_fuel_cost', 0), 2),
                        'total_cargos': res.get('total_cargos', 0),
                        'total_weight': res.get('total_weight', 0),
                        'vehicle_count': len(res.get('routes', [])),
                        'rented_vehicles': res.get('rented_vehicles', 0),
                        'undelivered_count': len(undelivered),
                        'undelivered_reason': undelivered_reason,
                        'undelivered_details': res.get('undelivered_details', []),
                        'routes': [{
                            'vehicle_name': r['vehicle']['name'],
                            'route_names': r.get('route_names', []),
                            'distance': r.get('distance', 0),
                            'cost': r.get('cost', 0),
                            'weight': r.get('weight', 0),
                            'cargo_count': r.get('cargo_count', 0),
                            'station_cargo_details': r.get('station_cargo_details', [])
                        } for r in res.get('routes', [])]
                    })
                except Exception as err:
                    results.append({
                        'scenario': scenario_idx,
                        'problem_type': problem_type,
                        'optimize_for': opt_mode,
                        'error': str(err),
                        'total_cost': 0,
                        'total_cargos': 0,
                        'total_weight': 0,
                        'vehicle_count': 0,
                        'undelivered_count': len(cargos)
                    })

    BaseHandler.send_json(handler, {'success': True, 'comparison': results})


def handle_compare_pending(handler, data: Dict):
    """Mevcut bekleyen kargolar için 3 optimizasyon modunu kıyaslar."""
    problem_type = data.get('type', 'limited')
    delivery_date = data.get('delivery_date')
    cargo_ids = data.get('cargo_ids', [])

    db = get_db()
    query = {'status': 'pending'}
    if cargo_ids:
        query['id'] = {'$in': [int(cid) for cid in cargo_ids]}
    elif delivery_date:
        query['delivery_date'] = delivery_date

    cargos = list(db.cargos.find(query))
    if not cargos:
        BaseHandler.send_json(handler, {'error': 'Bekleyen kargo yok'}, 404)
        return

    stations = list(db.stations.find({'is_active': 1}))
    stations_map = {s['id']: s for s in stations}
    for c in cargos:
        st = stations_map.get(c.get('station_id'), {})
        c['station_name'] = st.get('name', 'Bilinmiyor')
        c['latitude'] = st.get('latitude')
        c['longitude'] = st.get('longitude')

    vehicles = list(db.vehicles.find({'is_owned': 1}))
    params = db.parameters.find_one({'id': 1}) or {'cost_per_km': 1.0, 'rental_cost': 200.0, 'rental_capacity': 500}

    results = []
    for opt_type in ['distance', 'cost', 'balanced']:
        try:
            mode = 'max_weight' if opt_type == 'cost' else ('max_count' if opt_type == 'distance' else 'balanced')
            opt = RouteOptimizer(stations, cargos, vehicles, params, mode)
            res = opt.solve_unlimited_vehicles() if problem_type == 'unlimited' else opt.solve_limited_vehicles()
            results.append({
                'problem_type': problem_type,
                'optimize_for': opt_type,
                'total_cost': round(res.get('total_cost', 0), 2),
                'total_fuel_cost': round(res.get('total_fuel_cost', 0), 2),
                'total_cargos': res.get('total_cargos', 0),
                'total_weight': res.get('total_weight', 0),
                'vehicle_count': len(res.get('routes', [])),
                'rented_vehicles': res.get('rented_vehicles', 0),
                'undelivered_count': len(res.get('undelivered', [])),
                'routes': [{
                    'vehicle_name': r['vehicle']['name'],
                    'route_names': r.get('route_names', []),
                    'distance': r.get('distance', 0),
                    'cost': r.get('cost', 0),
                    'weight': r.get('weight', 0),
                    'cargo_count': r.get('cargo_count', 0)
                } for r in res.get('routes', [])]
            })
        except Exception as err:
            results.append({
                'problem_type': problem_type,
                'optimize_for': opt_type,
                'error': str(err),
                'total_cost': 0,
                'total_cargos': 0,
                'total_weight': 0,
                'vehicle_count': 0,
                'undelivered_count': len(cargos)
            })

    BaseHandler.send_json(handler, {'success': True, 'comparison': results, 'cargo_count': len(cargos)})
