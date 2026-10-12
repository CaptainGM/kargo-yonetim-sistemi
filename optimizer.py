# -*- coding: utf-8 -*-
"""
Kargo & Rota Optimizasyon Motoru (Route Optimizer)
TSP (Gezgin Satıcı), 2-Opt, Bin-Packing ve Knapsack algoritmalarını barındırır.
"""
import math
from typing import Dict, List, Optional, Tuple


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """İki coğrafi koordinat arasındaki kuş uçuşu mesafeyi (km) hesaplar."""
    R = 6371.0  # Dünya yarıçapı (km)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return 2.0 * R * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


class RouteOptimizer:
    """
    Kocaeli ilçeleri arasında kargo dağıtım rotalarını optimize eden ana motor.
    """
    def __init__(self, stations: List[Dict], cargos: List[Dict], vehicles: List[Dict], params: Dict, optimize_for: str = 'balanced'):
        self.stations: Dict[int, Dict] = {int(s['id']): s for s in stations}
        self.cargos = list(cargos)
        self.vehicles = sorted(vehicles, key=lambda v: v.get('capacity', 0), reverse=True)
        self.params = params or {'cost_per_km': 1.0, 'rental_cost': 200.0, 'rental_capacity': 500}
        self.optimize_for = optimize_for
        self.depot: Optional[Dict] = None

        # Depo istasyonunu bul (is_depot veya Ana Lojistik Hub)
        for s in stations:
            if s.get('is_depot'):
                self.depot = s
                break

        if not self.depot:
            for s in stations:
                name_lower = s.get('name', '').lower()
                if 'depo' in name_lower or 'hub' in name_lower or 'merkez' in name_lower or 'kampüs' in name_lower:
                    self.depot = s
                    break

        if not self.depot and stations:
            self.depot = stations[0]

        if not self.depot:
            self.depot = {
                'id': -1,
                'name': 'Marmara Lojistik Ana Hub (Kocaeli)',
                'latitude': 40.8225,
                'longitude': 29.9213,
                'is_depot': True
            }
            self.stations[-1] = self.depot

    def get_real_road_distance(self, name1: str, name2: str) -> float:
        """Kocaeli ilçeleri arasındaki gerçek karayolu kilometre tablosundan mesafe döndürür."""
        def normalize(name: str) -> str:
            tr_map = str.maketrans('ıöüşçğİÖÜŞÇĞ', 'iouscgIOUSCG')
            return name.lower().translate(tr_map).strip()

        n1, n2 = normalize(name1), normalize(name2)
        if n1 == n2:
            return 0.0

        distances = {
            ('umuttepe', 'izmit'): 5,
            ('umuttepe', 'derince'): 8,
            ('umuttepe', 'korfez'): 15,
            ('umuttepe', 'gebze'): 45,
            ('umuttepe', 'cayirova'): 50,
            ('umuttepe', 'darica'): 55,
            ('umuttepe', 'dilovasi'): 35,
            ('umuttepe', 'basiskele'): 12,
            ('umuttepe', 'golcuk'): 18,
            ('umuttepe', 'karamursel'): 35,
            ('umuttepe', 'kartepe'): 20,
            ('umuttepe', 'kandira'): 45,

            ('izmit', 'derince'): 6,
            ('izmit', 'korfez'): 12,
            ('izmit', 'gebze'): 42,
            ('izmit', 'cayirova'): 48,
            ('izmit', 'darica'): 52,
            ('izmit', 'dilovasi'): 32,
            ('izmit', 'basiskele'): 10,
            ('izmit', 'golcuk'): 15,
            ('izmit', 'karamursel'): 32,
            ('izmit', 'kartepe'): 18,
            ('izmit', 'kandira'): 50,

            ('derince', 'korfez'): 8,
            ('derince', 'gebze'): 38,
            ('derince', 'cayirova'): 44,
            ('derince', 'darica'): 48,
            ('derince', 'dilovasi'): 28,
            ('derince', 'basiskele'): 15,
            ('derince', 'golcuk'): 20,
            ('derince', 'karamursel'): 38,
            ('derince', 'kartepe'): 22,
            ('derince', 'kandira'): 55,

            ('korfez', 'gebze'): 30,
            ('korfez', 'cayirova'): 36,
            ('korfez', 'darica'): 40,
            ('korfez', 'dilovasi'): 20,
            ('korfez', 'basiskele'): 22,
            ('korfez', 'golcuk'): 28,
            ('korfez', 'karamursel'): 45,
            ('korfez', 'kartepe'): 30,
            ('korfez', 'kandira'): 60,

            ('gebze', 'cayirova'): 8,
            ('gebze', 'darica'): 12,
            ('gebze', 'dilovasi'): 12,
            ('gebze', 'basiskele'): 52,
            ('gebze', 'golcuk'): 58,
            ('gebze', 'karamursel'): 55,
            ('gebze', 'kartepe'): 60,
            ('gebze', 'kandira'): 90,

            ('cayirova', 'darica'): 5,
            ('cayirova', 'dilovasi'): 18,
            ('cayirova', 'basiskele'): 58,
            ('cayirova', 'golcuk'): 64,
            ('cayirova', 'karamursel'): 60,
            ('cayirova', 'kartepe'): 68,
            ('cayirova', 'kandira'): 95,

            ('darica', 'dilovasi'): 22,
            ('darica', 'basiskele'): 62,
            ('darica', 'golcuk'): 68,
            ('darica', 'karamursel'): 65,
            ('darica', 'kartepe'): 72,
            ('darica', 'kandira'): 100,

            ('dilovasi', 'basiskele'): 42,
            ('dilovasi', 'golcuk'): 48,
            ('dilovasi', 'karamursel'): 45,
            ('dilovasi', 'kartepe'): 50,
            ('dilovasi', 'kandira'): 80,

            ('basiskele', 'golcuk'): 8,
            ('basiskele', 'karamursel'): 25,
            ('basiskele', 'kartepe'): 15,
            ('basiskele', 'kandira'): 55,

            ('golcuk', 'karamursel'): 18,
            ('golcuk', 'kartepe'): 22,
            ('golcuk', 'kandira'): 60,

            ('karamursel', 'kartepe'): 40,
            ('karamursel', 'kandira'): 75,

            ('kartepe', 'kandira'): 40,
        }

        for (k1, k2), dist in distances.items():
            if (k1 in n1 or n1 in k1) and (k2 in n2 or n2 in k2):
                return float(dist)
            if (k1 in n2 or n2 in k1) and (k2 in n1 or n1 in k2):
                return float(dist)

        return 0.0

    def calculate_distance_matrix(self) -> Dict[int, Dict[int, float]]:
        """Tüm istasyonlar arasındaki mesafe matrisini hesaplar."""
        station_ids = list(self.stations.keys())
        matrix: Dict[int, Dict[int, float]] = {}

        for i in station_ids:
            matrix[i] = {}
            for j in station_ids:
                if i == j:
                    matrix[i][j] = 0.0
                else:
                    s1, s2 = self.stations[i], self.stations[j]
                    real_dist = self.get_real_road_distance(s1.get('name', ''), s2.get('name', ''))
                    if real_dist > 0:
                        matrix[i][j] = real_dist
                    else:
                        base_dist = haversine(s1['latitude'], s1['longitude'], s2['latitude'], s2['longitude'])
                        matrix[i][j] = round(base_dist * 1.3, 1)

        return matrix

    def optimize_route_order(self, station_ids: List[int], depot_id: int, dist_matrix: Dict) -> List[int]:
        """Nearest Neighbor (En Yakın Komşu) sezgiseli ile başlangıç rotasını sıralar."""
        if not station_ids:
            return []
        if len(station_ids) == 1:
            return station_ids[:]

        def build_nn(start_id: int) -> Tuple[List[int], float]:
            route = [start_id]
            remaining = set(station_ids) - {start_id}
            total_dist = 0.0

            while remaining:
                curr = route[-1]
                nearest = None
                min_d = float('inf')
                for sid in remaining:
                    d = dist_matrix.get(curr, {}).get(sid, float('inf'))
                    if d < min_d:
                        min_d = d
                        nearest = sid
                if nearest is not None:
                    total_dist += min_d
                    route.append(nearest)
                    remaining.remove(nearest)
                else:
                    break

            if depot_id in dist_matrix and route:
                total_dist += dist_matrix[route[-1]].get(depot_id, 0.0)
            return route, total_dist

        best_route = None
        best_dist = float('inf')

        for s in station_ids:
            r, d = build_nn(s)
            if d < best_dist:
                best_dist = d
                best_route = r

        return best_route if best_route else station_ids[:]

    def two_opt(self, route: List[int]) -> List[int]:
        """2-Opt yerel arama algoritması ile rotadaki çapraz kesişmeleri çözer."""
        if len(route) < 4:
            return route

        dist_matrix = self.calculate_distance_matrix()
        improved = True
        max_iter = 100
        curr_iter = 0

        route = list(route)
        while improved and curr_iter < max_iter:
            improved = False
            curr_iter += 1
            best_delta = 0.0
            best_i, best_j = -1, -1

            for i in range(len(route) - 2):
                for j in range(i + 2, len(route)):
                    if j == len(route) - 1 and i == 0:
                        continue

                    d1 = dist_matrix.get(route[i], {}).get(route[i + 1], 0.0)
                    d2 = dist_matrix.get(route[j], {}).get(route[j + 1], 0.0) if j + 1 < len(route) else 0.0
                    d3 = dist_matrix.get(route[i], {}).get(route[j], 0.0)
                    d4 = dist_matrix.get(route[i + 1], {}).get(route[j + 1], 0.0) if j + 1 < len(route) else 0.0

                    delta = (d3 + d4) - (d1 + d2)
                    if delta < best_delta - 0.01:
                        best_delta = delta
                        best_i, best_j = i, j

            if best_i >= 0 and best_j >= 0:
                route[best_i + 1:best_j + 1] = list(reversed(route[best_i + 1:best_j + 1]))
                improved = True

        return route

    def greedy_route(self, available_cargos: List[Dict], capacity: float, vehicle: Optional[Dict] = None):
        """Açgözlü kargo seçimi ve optimize rota hesaplaması."""
        if not available_cargos:
            return [], [], 0.0, 0.0

        dist_matrix = self.calculate_distance_matrix()
        depot_id = self.depot['id'] if self.depot else None

        # Kargo sıralaması stratejiye göre
        if self.optimize_for == 'max_count':
            sorted_cargos = sorted(available_cargos, key=lambda c: c['weight'])
        elif self.optimize_for == 'max_weight':
            sorted_cargos = sorted(available_cargos, key=lambda c: c['weight'], reverse=True)
        else:
            # Dengeli: mesafeye ve ağırlığa göre
            sorted_cargos = sorted(
                available_cargos,
                key=lambda c: dist_matrix.get(c['station_id'], {}).get(depot_id, 100)
            )

        selected: List[Dict] = []
        curr_weight = 0.0
        selected_stations = set()

        for cargo in sorted_cargos:
            if curr_weight + cargo['weight'] <= capacity:
                selected.append(cargo)
                curr_weight += cargo['weight']
                selected_stations.add(cargo['station_id'])

        if not selected:
            return [], [], 0.0, 0.0

        station_list = list(selected_stations)
        route = self.optimize_route_order(station_list, depot_id, dist_matrix)
        if len(route) > 3:
            route = self.two_opt(route)

        # Depo başlangıç ve bitişini sağla
        full_route = []
        if depot_id is not None:
            full_route.append(depot_id)
        for sid in route:
            if sid != depot_id:
                full_route.append(sid)
        if depot_id is not None:
            full_route.append(depot_id)

        # Mesafe hesabı
        total_dist = 0.0
        for i in range(len(full_route) - 1):
            total_dist += dist_matrix.get(full_route[i], {}).get(full_route[i + 1], 0.0)

        fuel_consumption = vehicle.get('fuel_consumption', 0.1) if vehicle else 0.1
        cost = total_dist * self.params.get('cost_per_km', 1.0)

        return full_route, selected, round(total_dist, 2), round(cost, 2)

    def _build_route_result(self, vehicle: Dict, selected_cargos: List[Dict], dist_matrix: Dict, depot_id: Optional[int]) -> Optional[Dict]:
        """Tek bir araç için rota detay nesnesini yapılandırır."""
        if not selected_cargos:
            return None

        station_ids = list({c['station_id'] for c in selected_cargos})
        ordered = self.optimize_route_order(station_ids, depot_id, dist_matrix)
        if len(ordered) > 3:
            ordered = self.two_opt(ordered)

        # Rota başına ve sonuna depoyu ekle
        full_route = []
        if depot_id is not None:
            full_route.append(depot_id)
        for sid in ordered:
            if sid != depot_id:
                full_route.append(sid)
        if depot_id is not None:
            full_route.append(depot_id)

        dist = round(dist, 2)
        fuel_liters_100km = vehicle.get('fuel_liters_per_100km', 10.0)
        fuel_type = vehicle.get('fuel_type', 'diesel')
        fuel_prices = self.params.get('fuel_prices', {})
        unit_fuel_price = fuel_prices.get('gasoline_per_liter', 85.50) if fuel_type == 'gasoline' else fuel_prices.get('diesel_per_liter', 92.50)

        # 1. Gerçek Akaryakıt Tüketimi (Litre ve TL)
        fuel_liters = round((dist / 100.0) * fuel_liters_100km, 2)
        fuel_cost = round(dist * vehicle.get('fuel_consumption', (fuel_liters_100km * unit_fuel_price / 100.0)), 2)

        # 2. Güzergah Tercihi (D-100 / E-5 Devlet Yolu vs O-4 / KMO Otoyol)
        road_type = self.params.get('road_type', 'otoyol')
        speed_factor = vehicle.get('speed_factor', 1.0)

        if road_type == 'devlet_yolu':
            # D-100 / E-5: Trafik ışıkları, meskun mahal kısıtlamaları (65-72 km/s), 0 TL HGS/Köprü
            avg_speed = 68.0 * speed_factor
            toll_cost = 0.0
            road_type_label = "D-100 / E-5 Devlet Yolu (Ücretsiz)"
        else:
            # O-4 / KMO / O-5: Bölünmüş otoyol, yüksek seyir hızı (92-105 km/s), HGS/Köprü geçiş tarifesi
            avg_speed = 95.0 * speed_factor
            toll_cost = round(dist * 0.65, 2) if dist > 60 else 0.0
            road_type_label = "O-4 / KMO Anadolu Otoyolu (HGS)"

        # 3. Sefer Süresi (Saat & Dakika)
        est_duration_hours = round(dist / max(avg_speed, 30.0), 2)
        total_mins = int(round(est_duration_hours * 60))
        hours = total_mins // 60
        mins = total_mins % 60
        duration_formatted = f"{hours} sa {mins} dk" if hours > 0 else f"{mins} dk"

        # 4. Sürücü Günlük Yevmiye & Operasyon Payı (Saatlik 160 TL, Min 250 TL, Maks 2.500 TL)
        driver_cost = round(min(2500.0, max(250.0, est_duration_hours * 160.0)), 2)

        # 5. Kiralama ve Toplam Operasyonel Maliyet
        rental_cost = vehicle.get('rental_cost', 0.0) if not vehicle.get('is_owned', True) else 0.0
        total_cost = round(fuel_cost + toll_cost + rental_cost + driver_cost, 2)

        # 6. Karbon Ayak İzi (kg CO2)
        co2_g_km = vehicle.get('co2_g_per_km', 250.0)
        co2_emission_kg = round((dist * co2_g_km) / 1000.0, 2)

        # İstasyon bazlı kargo detayları
        station_cargo_details = []
        for sid in full_route:
            st = self.stations.get(sid, {})
            c_at_st = [c for c in selected_cargos if c['station_id'] == sid]
            station_cargo_details.append({
                'station_id': sid,
                'station_name': st.get('name', 'Bilinmiyor'),
                'is_depot': (sid == depot_id),
                'cargo_count': len(c_at_st),
                'cargo_weight': round(sum(c['weight'] for c in c_at_st), 2),
                'cargos': [{'id': c['id'], 'weight': c['weight'], 'user_id': c.get('user_id')} for c in c_at_st]
            })

        cargo_users = []
        for c in selected_cargos:
            cargo_users.append({
                'cargo_id': c['id'],
                'user_id': c.get('user_id'),
                'username': c.get('username', 'Misafir'),
                'weight': c['weight'],
                'station': self.stations.get(c['station_id'], {}).get('name', '')
            })

        return {
            'vehicle': vehicle,
            'route': full_route,
            'route_names': [self.stations.get(sid, {}).get('name', f'İstasyon {sid}') for sid in full_route],
            'cargos': selected_cargos,
            'cargo_users': cargo_users,
            'distance': dist,
            'fuel_liters': fuel_liters,
            'fuel_cost': fuel_cost,
            'toll_cost': toll_cost,
            'driver_cost': driver_cost,
            'cost': total_cost,
            'co2_emission_kg': co2_emission_kg,
            'duration_hours': est_duration_hours,
            'duration_formatted': duration_formatted,
            'road_type': road_type,
            'road_type_label': road_type_label,
            'weight': round(sum(c['weight'] for c in selected_cargos), 2),
            'cargo_count': len(selected_cargos),
            'is_rented': not bool(vehicle.get('is_owned', True)),
            'station_cargo_details': station_cargo_details
        }

    def _solve_with_backtracking(self, cargos: List[Dict], vehicles: List[Dict], dist_matrix: Dict, depot_id: Optional[int]) -> Dict:
        """20 veya daha az kargo için optimal Backtracking Bin-Packing çözümü."""
        n = len(cargos)
        v_caps = {v['id']: v['capacity'] for v in vehicles}
        best_assignment: Dict[int, List[Dict]] = {v['id']: [] for v in vehicles}
        best_count = -1
        best_weight = -1.0

        sorted_cargos = sorted(cargos, key=lambda c: c['weight'], reverse=True)

        def backtrack(idx: int, assign: Dict[int, List[Dict]], weights: Dict[int, float]):
            nonlocal best_assignment, best_count, best_weight
            if idx == n:
                cnt = sum(len(lst) for lst in assign.values())
                w = sum(weights.values())
                if self.optimize_for == 'max_count':
                    is_better = (cnt > best_count) or (cnt == best_count and w > best_weight)
                elif self.optimize_for == 'max_weight':
                    is_better = (w > best_weight) or (w == best_weight and cnt > best_count)
                else:
                    is_better = (cnt > best_count) or (cnt == best_count and w > best_weight)

                if is_better:
                    best_count = cnt
                    best_weight = w
                    best_assignment = {k: list(v) for k, v in assign.items()}
                return

            cargo = sorted_cargos[idx]
            # Her araca yerleştirmeyi dene
            for v in vehicles:
                vid = v['id']
                if weights[vid] + cargo['weight'] <= v_caps[vid]:
                    assign[vid].append(cargo)
                    weights[vid] += cargo['weight']
                    backtrack(idx + 1, assign, weights)
                    assign[vid].pop()
                    weights[vid] -= cargo['weight']

            # Kargoyu hiçbir araca vermemeyi de dene (kapasite dolduysa)
            backtrack(idx + 1, assign, weights)

        init_assign = {v['id']: [] for v in vehicles}
        init_weights = {v['id']: 0.0 for v in vehicles}
        backtrack(0, init_assign, init_weights)

        # Sonuçları derle
        routes = []
        assigned_c_ids = set()
        for v in vehicles:
            c_list = best_assignment.get(v['id'], [])
            if c_list:
                for c in c_list:
                    assigned_c_ids.add(c['id'])
                r_res = self._build_route_result(v, c_list, dist_matrix, depot_id)
                if r_res:
                    routes.append(r_res)

        undelivered = [c for c in cargos if c['id'] not in assigned_c_ids]
        undelivered_details = [{
            'id': c['id'],
            'weight': c['weight'],
            'station_id': c['station_id'],
            'station_name': self.stations.get(c['station_id'], {}).get('name', 'Bilinmiyor')
        } for c in undelivered]

        return {
            'routes': routes,
            'total_cost': round(sum(r['cost'] for r in routes), 2),
            'total_fuel_cost': round(sum(r['fuel_cost'] for r in routes), 2),
            'total_cargos': sum(r['cargo_count'] for r in routes),
            'total_weight': round(sum(r['weight'] for r in routes), 2),
            'undelivered': undelivered,
            'undelivered_count': len(undelivered),
            'undelivered_details': undelivered_details,
            'optimize_for': self.optimize_for
        }

    def _solve_with_greedy_best_fit(self, cargos: List[Dict], vehicles: List[Dict], dist_matrix: Dict, depot_id: Optional[int]) -> Dict:
        """20'den fazla kargo için açgözlü Best-Fit Bin-Packing sezgiseli."""
        sorted_vehicles = sorted(vehicles, key=lambda v: v['capacity'], reverse=True)
        if self.optimize_for == 'max_count':
            sorted_cargos = sorted(cargos, key=lambda c: c['weight'])
        else:
            sorted_cargos = sorted(cargos, key=lambda c: c['weight'], reverse=True)

        assign: Dict[int, List[Dict]] = {v['id']: [] for v in vehicles}
        weights: Dict[int, float] = {v['id']: 0.0 for v in vehicles}

        for c in sorted_cargos:
            for v in sorted_vehicles:
                vid = v['id']
                if weights[vid] + c['weight'] <= v['capacity']:
                    assign[vid].append(c)
                    weights[vid] += c['weight']
                    break

        routes = []
        assigned_ids = set()
        for v in vehicles:
            c_list = assign.get(v['id'], [])
            if c_list:
                for c in c_list:
                    assigned_ids.add(c['id'])
                r_res = self._build_route_result(v, c_list, dist_matrix, depot_id)
                if r_res:
                    routes.append(r_res)

        undelivered = [c for c in cargos if c['id'] not in assigned_ids]
        undelivered_details = [{
            'id': c['id'],
            'weight': c['weight'],
            'station_id': c['station_id'],
            'station_name': self.stations.get(c['station_id'], {}).get('name', 'Bilinmiyor')
        } for c in undelivered]

        return {
            'routes': routes,
            'total_cost': round(sum(r['cost'] for r in routes), 2),
            'total_fuel_cost': round(sum(r['fuel_cost'] for r in routes), 2),
            'total_cargos': sum(r['cargo_count'] for r in routes),
            'total_weight': round(sum(r['weight'] for r in routes), 2),
            'undelivered': undelivered,
            'undelivered_count': len(undelivered),
            'undelivered_details': undelivered_details,
            'optimize_for': self.optimize_for
        }

    def solve_limited_vehicles(self) -> Dict:
        """Sadece mevcut özmal araçları kullanarak dağıtımı çözer."""
        owned_vehicles = [v for v in self.vehicles if v.get('is_owned', 1)]
        if not self.cargos or not owned_vehicles:
            return {
                'routes': [],
                'total_cost': 0.0,
                'total_fuel_cost': 0.0,
                'total_cargos': 0,
                'total_weight': 0.0,
                'undelivered': self.cargos,
                'undelivered_count': len(self.cargos),
                'undelivered_details': [{
                    'id': c['id'],
                    'weight': c['weight'],
                    'station_id': c['station_id'],
                    'station_name': self.stations.get(c['station_id'], {}).get('name', 'Bilinmiyor')
                } for c in self.cargos],
                'optimize_for': self.optimize_for
            }

        dist_matrix = self.calculate_distance_matrix()
        depot_id = self.depot['id'] if self.depot else None

        if len(self.cargos) <= 20:
            return self._solve_with_backtracking(self.cargos, owned_vehicles, dist_matrix, depot_id)
        return self._solve_with_greedy_best_fit(self.cargos, owned_vehicles, dist_matrix, depot_id)

    def solve_unlimited_vehicles(self) -> Dict:
        """
        Sınırsız araç stratejisi:
        Önce özmal araçlar doldurulur. Kalan teslim edilmemiş kargolar için
        otomatik olarak kiralık araçlar kiralanır (500kg, 200 TL kira).
        """
        limited_result = self.solve_limited_vehicles()
        remaining = list(limited_result.get('undelivered', []))

        if not remaining:
            limited_result['rented_vehicles'] = 0
            limited_result['rental_cost'] = 0.0
            return limited_result

        routes = list(limited_result.get('routes', []))
        dist_matrix = self.calculate_distance_matrix()
        depot_id = self.depot['id'] if self.depot else None

        rental_capacity = self.params.get('rental_capacity', 500)
        rental_cost_fee = self.params.get('rental_cost', 200.0)
        rented_count = 0

        while remaining:
            rented_count += 1
            rented_vehicle = {
                'id': f'rented_{rented_count}',
                'name': f'Kiralık Araç {rented_count} ({rental_capacity}kg)',
                'capacity': rental_capacity,
                'rental_cost': rental_cost_fee,
                'fuel_consumption': 0.10,
                'is_owned': 0
            }

            # Bu kiralık araç için sığan kargoları seç
            selected_for_rent = []
            cur_w = 0.0
            unassigned_after = []

            for c in remaining:
                if cur_w + c['weight'] <= rental_capacity:
                    selected_for_rent.append(c)
                    cur_w += c['weight']
                else:
                    unassigned_after.append(c)

            if not selected_for_rent:
                # Kargo tek başına kiralık araç kapasitesini aşıyorsa
                break

            r_res = self._build_route_result(rented_vehicle, selected_for_rent, dist_matrix, depot_id)
            if r_res:
                routes.append(r_res)
            remaining = unassigned_after

        undelivered_details = [{
            'id': c['id'],
            'weight': c['weight'],
            'station_id': c['station_id'],
            'station_name': self.stations.get(c['station_id'], {}).get('name', 'Bilinmiyor')
        } for c in remaining]

        total_cost = sum(r['cost'] for r in routes)
        total_fuel = sum(r['fuel_cost'] for r in routes)

        return {
            'routes': routes,
            'total_cost': round(total_cost, 2),
            'total_fuel_cost': round(total_fuel, 2),
            'total_cargos': sum(r['cargo_count'] for r in routes),
            'total_weight': round(sum(r['weight'] for r in routes), 2),
            'rented_vehicles': rented_count,
            'rental_cost': round(rented_count * rental_cost_fee, 2),
            'undelivered': remaining,
            'undelivered_count': len(remaining),
            'undelivered_details': undelivered_details,
            'optimize_for': self.optimize_for
        }
