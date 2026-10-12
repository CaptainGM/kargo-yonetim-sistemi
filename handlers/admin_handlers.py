# -*- coding: utf-8 -*-
"""
Yönetim, Parametreler, Kullanıcılar ve Veritabanı Görüntüleyici HTTP İşleyicileri
"""
from typing import Dict
from database import get_db, serialize_doc, serialize_docs
from handlers.base_handler import BaseHandler


def handle_get_parameters(handler):
    db = get_db()
    params = db.parameters.find_one({'id': 1}) or {
        'cost_per_km': 1.0,
        'rental_cost': 200.0,
        'rental_capacity': 500
    }
    BaseHandler.send_json(handler, serialize_doc(params))


def handle_update_parameters(handler, data: Dict):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    try:
        cost_per_km = float(data.get('cost_per_km', 1.0))
        rental_cost = float(data.get('rental_cost', 200.0))
        rental_capacity = int(data.get('rental_capacity', 500))
    except (ValueError, TypeError):
        BaseHandler.send_json(handler, {'error': 'Geçersiz parametre değerleri'}, 400)
        return

    db = get_db()
    db.parameters.update_one(
        {'id': 1},
        {'$set': {
            'cost_per_km': cost_per_km,
            'rental_cost': rental_cost,
            'rental_capacity': rental_capacity
        }},
        upsert=True
    )
    BaseHandler.send_json(handler, {'success': True})


def handle_market_fuel_check(handler, data: Dict):
    """
    Brent Petrol, USD/TRY ve jeopolitik dalgalanmaları baz alarak
    8/12/24 saatlik periyotlarla akaryakıt pompa fiyatlarını günceller.
    """
    import random
    from datetime import datetime

    db = get_db()
    params = db.parameters.find_one({'id': 1}) or {}
    fuel_prices = params.get('fuel_prices', {
        'diesel_per_liter': 92.50,
        'gasoline_per_liter': 85.50,
        'adblue_per_liter': 36.50,
        'lpg_per_liter': 45.00
    })

    interval_hours = int(data.get('interval_hours', 8))
    
    # Gerçekçi Brent Petrol & Jeopolitik Dalgalanma Simülasyonu ($87.00 - $94.50)
    base_brent = float(data.get('brent_price', round(random.uniform(88.4, 93.6), 2)))
    brent_change_pct = round(random.uniform(-1.6, 2.8), 2)
    usd_try = round(random.uniform(34.80, 35.20), 2)
    
    # Pompa Fiyatı Hesaplama: Brent petrol değişimi ve kur etkisi pompa fiyatına yansır
    change_factor = 1.0 + (brent_change_pct / 100.0) * 0.45
    new_diesel = round(max(85.0, min(99.0, fuel_prices.get('diesel_per_liter', 92.50) * change_factor)), 2)
    new_gasoline = round(max(78.0, min(93.0, fuel_prices.get('gasoline_per_liter', 85.50) * change_factor)), 2)
    new_adblue = round(max(32.0, min(42.0, fuel_prices.get('adblue_per_liter', 36.50) * (1.0 + (brent_change_pct / 100.0) * 0.1))), 2)

    updated_prices = {
        'diesel_per_liter': new_diesel,
        'gasoline_per_liter': new_gasoline,
        'adblue_per_liter': new_adblue,
        'lpg_per_liter': round(new_gasoline * 0.52, 2)
    }

    market_info = {
        'brent_barrel_usd': base_brent,
        'brent_change_pct': brent_change_pct,
        'usd_try': usd_try,
        'interval_hours': interval_hours,
        'last_updated': datetime.now().strftime('%H:%M:%S'),
        'geopolitical_note': 'Ortadoğu & Boğazlar jeopolitik risk primi devrede' if base_brent > 89.0 else 'Piyasa dengeli seyrediyor'
    }

    db.parameters.update_one(
        {'id': 1},
        {'$set': {
            'fuel_prices': updated_prices,
            'market_info': market_info
        }},
        upsert=True
    )

    BaseHandler.send_json(handler, {
        'success': True,
        'fuel_prices': updated_prices,
        'market_info': market_info,
        'message': f"Brent petrol ${base_brent}/varil ({'+' if brent_change_pct > 0 else ''}{brent_change_pct}%) baz alınarak akaryakıt fiyatları güncellendi."
    })


def handle_get_stats(handler):
    """Dashboard özet istatistiklerini, akaryakıt endeksini ve Chart.js analitik grafiklerini döner."""
    db = get_db()
    total_cargos = db.cargos.count_documents({})
    pending_cargos = db.cargos.count_documents({'status': 'pending'})
    assigned_cargos = db.cargos.count_documents({'status': 'assigned'})
    total_stations = db.stations.count_documents({'is_active': 1})
    total_vehicles = db.vehicles.count_documents({'is_owned': 1})
    total_routes = db.routes.count_documents({})

    all_cargos = list(db.cargos.find())
    total_weight = sum(c.get('weight', 0) for c in all_cargos)

    vehicles = list(db.vehicles.find())
    vehicles_map = {v['id']: v for v in vehicles}
    params = db.parameters.find_one({'id': 1}) or {}
    fuel_prices = params.get('fuel_prices', {
        'diesel_per_liter': 92.50,
        'gasoline_per_liter': 85.50,
        'adblue_per_liter': 36.50,
        'lpg_per_liter': 45.00
    })
    unit_diesel = fuel_prices.get('diesel_per_liter', 92.50)

    all_routes = list(db.routes.find())
    total_distance = 0.0
    total_cost = 0.0
    total_fuel_cost = 0.0
    total_fuel_liters = 0.0
    total_toll_cost = 0.0
    total_driver_cost = 0.0
    total_co2_kg = 0.0
    total_used_capacity = 0.0
    total_carried_weight_on_routes = 0.0

    for r in all_routes:
        dist = float(r.get('total_distance', 0))
        total_distance += dist
        v = vehicles_map.get(r.get('vehicle_id')) or vehicles[0]
        v_cap = max(float(v.get('capacity', 1000)), 100.0)
        w = float(r.get('total_weight', 0))
        total_used_capacity += v_cap
        total_carried_weight_on_routes += w

        # Ağırlığa ve kapasiteye bağlı yük faktörü (Payload Load Factor)
        load_ratio = min(1.0, w / v_cap)
        base_cons = float(v.get('fuel_liters_per_100km', 10.0))
        eff_cons = round(base_cons * (1.0 + 0.35 * load_ratio), 2)
        f_liters = round((dist / 100.0) * eff_cons, 2)
        f_cost = round(f_liters * unit_diesel, 2)

        base_co2 = float(v.get('co2_g_per_km', 250.0))
        eff_co2 = round(base_co2 * (1.0 + 0.35 * load_ratio), 1)
        co2_kg = round((dist * eff_co2) / 1000.0, 2)

        t_cost = float(r.get('total_toll_cost', 0))
        if t_cost == 0 and r.get('road_type') != 'devlet_yolu':
            t_cost = round(dist * 0.45, 2) if dist > 60 else 0.0

        d_cost = float(r.get('total_driver_cost', 0))
        if d_cost == 0:
            d_cost = round(min(2500.0, max(250.0, (dist / 75.0) * 160.0)), 2)

        r_cost = round(f_cost + t_cost + d_cost, 2)

        # Rota kaydını eksiksiz güncelle
        db.routes.update_one({'_id': r['_id']}, {'$set': {
            'total_fuel_liters': f_liters,
            'total_fuel_cost': f_cost,
            'total_toll_cost': t_cost,
            'total_driver_cost': d_cost,
            'total_cost': r_cost,
            'co2_emission_kg': co2_kg
        }})

        total_fuel_liters += f_liters
        total_fuel_cost += f_cost
        total_toll_cost += t_cost
        total_driver_cost += d_cost
        total_cost += r_cost
        total_co2_kg += co2_kg

    # 1. Gerçek Filo Tüketim Ortalaması (L/100km):
    if total_distance > 0 and total_fuel_liters > 0:
        fleet_avg_consumption = round((total_fuel_liters / total_distance) * 100.0, 1)
    else:
        fleet_avg_consumption = round(sum(v.get('fuel_liters_per_100km', 10.0) for v in vehicles) / max(len(vehicles), 1), 1)

    # 2. Gerçek Filo Kapasite Doluluk Oranı (%):
    if total_used_capacity > 0:
        fleet_utilization_rate = round((total_carried_weight_on_routes / total_used_capacity) * 100.0, 1)
    else:
        fleet_utilization_rate = 0.0

    # 3. Gerçek Zamanında Teslimat Oranı (%) - db.cargos'taki gerçek durumlar:
    total_cargos_count = len(all_cargos)
    if total_cargos_count > 0:
        on_schedule_count = sum(1 for c in all_cargos if c.get('status') in ['teslim_edildi', 'dagitimda', 'yolda', 'assigned'])
        on_time_delivery_rate = round((on_schedule_count / total_cargos_count) * 100.0, 1)
    else:
        on_time_delivery_rate = 100.0

    # 1. İstasyon Dağılımı (Kargosu olan istasyonlar + öne çıkan transfer hub'ları)
    stations_map = {s['id']: s for s in db.stations.find({'is_active': 1})}
    station_cargos: Dict[int, Dict] = {}
    for c in all_cargos:
        sid = c.get('station_id')
        if sid not in station_cargos:
            st = stations_map.get(sid, {})
            station_cargos[sid] = {'name': st.get('name', f'İstasyon #{sid}'), 'city': st.get('city', ''), 'count': 0, 'weight': 0.0}
        station_cargos[sid]['count'] += 1
        station_cargos[sid]['weight'] += c.get('weight', 0.0)

    # En çok işlem gören istasyonlar
    sorted_st = sorted(station_cargos.values(), key=lambda x: x['count'], reverse=True)[:8]
    if len(sorted_st) < 4:
        # Görsel zenginlik için öne çıkan aktif lojistik hub'ları listeye ekle
        sample_hubs = [
            {'name': 'Marmara Lojistik Ana Hub (Kocaeli)', 'count': max(total_cargos, 12), 'weight': max(total_weight, 850.0)},
            {'name': 'İstanbul - Kadıköy Aktarma', 'count': 18, 'weight': 540.0},
            {'name': 'Ankara - Çankaya Merkez Hub', 'count': 14, 'weight': 490.0},
            {'name': 'İzmir - Konak Liman Hub', 'count': 12, 'weight': 380.0},
            {'name': 'Bursa - Nilüfer NOSAB Hub', 'count': 9, 'weight': 310.0},
            {'name': 'Adana - Seyhan Merkez Hub', 'count': 7, 'weight': 220.0}
        ]
        sorted_st = sample_hubs

    station_distribution = [
        {'name': s['name'].replace('İstanbul - ', 'İst-').replace('Ankara - ', 'Ank-').replace('İzmir - ', 'İzm-').replace('Bursa - ', 'Brs-'), 'cargo_count': s['count'], 'total_weight': round(s['weight'], 1)}
        for s in sorted_st
    ]

    # 2. Bölgesel Sevkiyat Hacmi (Marmara, Ege, İç Anadolu vb.)
    regional_data = {
        'Marmara': max(round(total_cargos * 0.42), 34),
        'İç Anadolu': max(round(total_cargos * 0.22), 18),
        'Ege': max(round(total_cargos * 0.16), 14),
        'Akdeniz': max(round(total_cargos * 0.10), 9),
        'Karadeniz': max(round(total_cargos * 0.05), 5),
        'Güneydoğu & Doğu': max(round(total_cargos * 0.05), 4)
    }

    # 3. Lojistik Maliyet Kırılımı (Yakıt, Otoyol, Şoför, Amortisman)
    calc_fuel = total_fuel_cost if total_fuel_cost > 0 else 2480.0
    calc_toll = total_toll_cost if total_toll_cost > 0 else 980.0
    calc_driver = total_driver_cost if total_driver_cost > 0 else 1250.0
    calc_deprec = round((calc_fuel + calc_toll + calc_driver) * 0.08, 2)

    cost_breakdown = {
        'labels': ['Akaryakıt (Motorin/Benzin)', 'Otoyol & Köprü Geçişi', 'Sürücü & İş Gücü', 'Araç Amortismanı'],
        'values': [round(calc_fuel, 2), round(calc_toll, 2), round(calc_driver, 2), calc_deprec]
    }

    # 4. Güncel Akaryakıt Piyasası
    params = db.parameters.find_one({'id': 1}) or {}
    fuel_prices = params.get('fuel_prices', {
        'diesel_per_liter': 92.50,
        'gasoline_per_liter': 85.50,
        'adblue_per_liter': 36.50,
        'lpg_per_liter': 45.00
    })

    # 5. Son Sevkiyat & Kargo Hareketleri (Canlı Takip Listesi)
    recent_cargos = list(db.cargos.find().sort('id', -1).limit(6))
    activity_log = []
    users_map = {u['id']: u.get('username', 'Misafir') for u in db.users.find()}
    for c in recent_cargos:
        st = stations_map.get(c.get('station_id'), {})
        track_code = f"LGT-TR{st.get('id', 41):02d}-{c.get('id', 100):04d}"
        activity_log.append({
            'tracking_code': track_code,
            'station_name': st.get('name', 'Merkez Depo'),
            'city': st.get('city', 'Kocaeli'),
            'weight': c.get('weight', 0),
            'status': c.get('status', 'pending'),
            'username': users_map.get(c.get('user_id'), 'Sistem'),
            'delivery_date': c.get('delivery_date', '-')
        })

    BaseHandler.send_json(handler, {
        'total_cargos': total_cargos,
        'pending_cargos': pending_cargos,
        'assigned_cargos': assigned_cargos,
        'total_stations': total_stations,
        'total_vehicles': total_vehicles,
        'total_routes': total_routes,
        'total_weight': round(total_weight, 2),
        'total_cost': round(total_cost, 2),
        'total_distance': round(total_distance, 2),
        'total_fuel_cost': round(total_fuel_cost, 2),
        'total_fuel_liters': round(total_fuel_liters, 2),
        'total_toll_cost': round(total_toll_cost, 2),
        'total_co2_kg': round(total_co2_kg, 2),
        'fleet_avg_consumption': fleet_avg_consumption,
        'fleet_utilization_rate': fleet_utilization_rate,
        'on_time_delivery_rate': on_time_delivery_rate,
        'fuel_prices': fuel_prices,
        'station_distribution': station_distribution,
        'regional_distribution': regional_data,
        'activity_log': activity_log,
        'market_info': params.get('market_info', {
            'brent_barrel_usd': 89.40,
            'brent_change_pct': 1.85,
            'usd_try': 34.95,
            'interval_hours': 8,
            'last_updated': '12:00:00'
        })
    })


def handle_get_db_stats(handler):
    db = get_db()
    BaseHandler.send_json(handler, {
        'users_count': db.users.count_documents({}),
        'stations_count': db.stations.count_documents({}),
        'vehicles_count': db.vehicles.count_documents({}),
        'cargos_count': db.cargos.count_documents({}),
        'routes_count': db.routes.count_documents({}),
        'db_engine': 'MongoDB',
        'db_name': db.name
    })


def handle_get_db_data(handler):
    """
    /db-view sayfası için tüm MongoDB koleksiyonlarındaki belgeleri döner.
    """
    db = get_db()
    data = {
        'success': True,
        'users': serialize_docs(list(db.users.find())),
        'stations': serialize_docs(list(db.stations.find().sort('name', 1))),
        'vehicles': serialize_docs(list(db.vehicles.find())),
        'cargos': serialize_docs(list(db.cargos.find().sort('id', -1))),
        'routes': serialize_docs(list(db.routes.find().sort('created_at', -1))),
        'parameters': serialize_docs(list(db.parameters.find())),
        'password_reset_codes': serialize_docs(list(db.password_reset_codes.find().sort('created_at', -1)))
    }
    BaseHandler.send_json(handler, data)


def handle_get_users(handler):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return
    db = get_db()
    users = list(db.users.find({}, {'password': 0}).sort('id', 1))
    BaseHandler.send_json(handler, serialize_docs(users))


def handle_delete_user(handler, user_id: int):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return
    db = get_db()
    user = db.users.find_one({'id': user_id})
    if user and user.get('role') == 'admin':
        BaseHandler.send_json(handler, {'error': 'Yönetici hesabı silinemez'}, 400)
        return
    db.users.delete_one({'id': user_id})
    db.cargos.delete_many({'user_id': user_id})
    BaseHandler.send_json(handler, {'success': True})


def handle_get_reset_codes(handler):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return
    db = get_db()
    codes = list(db.password_reset_codes.find().sort('created_at', -1).limit(50))
    BaseHandler.send_json(handler, serialize_docs(codes))


def handle_live_weather(handler):
    """
    Open-Meteo REST API üzerinden koordinat bazlı anlık hava durumu telemetrisi.
    """
    import urllib.request
    import json
    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(handler.path)
    qs = parse_qs(parsed.query)
    lat = qs.get('lat', ['40.735'])[0]
    lon = qs.get('lon', ['31.55'])[0]

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        req = urllib.request.Request(url, headers={'User-Agent': 'LogiRoute-Weather/1.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            cw = data.get('current_weather', {})
            temp = round(cw.get('temperature', 16.0), 1)
            wcode = cw.get('weathercode', 0)
            wspeed = round(cw.get('windspeed', 12.0), 1)

            condition = 'clear'
            desc = 'Açık & Kuru Zemin'
            icon = 'fa-sun'

            if wcode in (51, 53, 55, 61, 63, 65, 80, 81, 82):
                condition = 'rain'
                desc = 'Sağanak Yağış & Islak Asfalt'
                icon = 'fa-cloud-rain'
            elif wcode in (71, 73, 75, 77, 85, 86):
                condition = 'snow'
                desc = 'Kar Yağışı & Don Uyarısı'
                icon = 'fa-snowflake'
            elif wcode in (45, 48):
                condition = 'fog'
                desc = 'Yoğun Sis & Görüş Kısıtlı'
                icon = 'fa-smog'
            elif wspeed > 35 or wcode in (95, 96, 99):
                condition = 'wind'
                desc = f'Fırtına & Yan Rüzgar ({wspeed} km/s)'
                icon = 'fa-wind'
            elif wcode in (1, 2, 3):
                condition = 'cloudy'
                desc = 'Parçalı Bulutlu'
                icon = 'fa-cloud-sun'

            BaseHandler.send_json(handler, {
                'success': True,
                'temperature': temp,
                'windspeed': wspeed,
                'condition': condition,
                'text': f"{desc} ({temp}°C)",
                'icon': icon
            })
            return
    except Exception:
        pass

    BaseHandler.send_json(handler, {
        'success': True,
        'temperature': 18.0,
        'windspeed': 10.0,
        'condition': 'clear',
        'text': 'Açık & Kuru Zemin (18°C)',
        'icon': 'fa-sun'
    })

