let currentUser = null;
let mainMap = null;
let optimizeMap = null;
let routeModalMap = null;
let stationChart = null;
let weightChart = null;
let stations = [];
let lastOptimizationResult = null;

const routeColors = ['#e74c3c', '#3498db', '#27ae60', '#9b59b6', '#f39c12', '#1abc9c', '#e67e22', '#34495e'];

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const btn = input.parentElement.querySelector('.toggle-pass, .toggle-password');
    if (!btn) return;
    const icon = btn.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye-slash', 'fa-eye');
        icon.classList.add('fa-eye');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye', 'fa-eye-slash');
        icon.classList.add('fa-eye-slash');
    }
}

let routeMap = null;
let myRouteMap = null;

const scenarios = {
    1: [
        { district: 'Başiskele', count: 10, weight: 120 },
        { district: 'Çayırova', count: 8, weight: 80 },
        { district: 'Darıca', count: 15, weight: 200 },
        { district: 'Derince', count: 10, weight: 150 },
        { district: 'Dilovası', count: 12, weight: 180 },
        { district: 'Gebze', count: 5, weight: 70 },
        { district: 'Gölcük', count: 7, weight: 90 },
        { district: 'Kandıra', count: 6, weight: 60 },
        { district: 'Karamürsel', count: 9, weight: 110 },
        { district: 'Kartepe', count: 11, weight: 130 },
        { district: 'Körfez', count: 6, weight: 75 },
        { district: 'İzmit', count: 14, weight: 160 }
    ],
    2: [
        { district: 'Başiskele', count: 40, weight: 200 },
        { district: 'Çayırova', count: 35, weight: 175 },
        { district: 'Darıca', count: 10, weight: 150 },
        { district: 'Derince', count: 5, weight: 100 },
        { district: 'Dilovası', count: 0, weight: 0 },
        { district: 'Gebze', count: 8, weight: 120 },
        { district: 'Gölcük', count: 0, weight: 0 },
        { district: 'Kandıra', count: 0, weight: 0 },
        { district: 'Karamürsel', count: 0, weight: 0 },
        { district: 'Kartepe', count: 0, weight: 0 },
        { district: 'Körfez', count: 0, weight: 0 },
        { district: 'İzmit', count: 20, weight: 160 }
    ],
    3: [
        { district: 'Başiskele', count: 0, weight: 0 },
        { district: 'Çayırova', count: 3, weight: 700 },
        { district: 'Darıca', count: 0, weight: 0 },
        { district: 'Derince', count: 0, weight: 0 },
        { district: 'Dilovası', count: 4, weight: 800 },
        { district: 'Gebze', count: 5, weight: 900 },
        { district: 'Gölcük', count: 0, weight: 0 },
        { district: 'Kandıra', count: 0, weight: 0 },
        { district: 'Karamürsel', count: 0, weight: 0 },
        { district: 'Kartepe', count: 0, weight: 0 },
        { district: 'Körfez', count: 0, weight: 0 },
        { district: 'İzmit', count: 5, weight: 300 }
    ],
    4: [
        { district: 'Başiskele', count: 30, weight: 300 },
        { district: 'Çayırova', count: 0, weight: 0 },
        { district: 'Darıca', count: 0, weight: 0 },
        { district: 'Derince', count: 0, weight: 0 },
        { district: 'Dilovası', count: 0, weight: 0 },
        { district: 'Gebze', count: 0, weight: 0 },
        { district: 'Gölcük', count: 15, weight: 220 },
        { district: 'Kandıra', count: 5, weight: 250 },
        { district: 'Karamürsel', count: 20, weight: 180 },
        { district: 'Kartepe', count: 10, weight: 200 },
        { district: 'Körfez', count: 8, weight: 400 },
        { district: 'İzmit', count: 0, weight: 0 }
    ]
};

document.addEventListener('DOMContentLoaded', () => {
    checkSession();
    setupEventListeners();
    setupLoginTabs();
});

function setTomorrowDate() {

    const dateInput = document.getElementById('deliveryDate');
    if (dateInput) {
        dateInput.value = '';
    }
}

function setupLoginTabs() {
    const tabs = document.querySelectorAll('.login-tab');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const tabName = tab.dataset.tab;
            if (tabName === 'login') {
                loginForm.style.display = 'block';
                if (registerForm) registerForm.style.display = 'none';
            } else if (tabName === 'register') {
                loginForm.style.display = 'none';
                if (registerForm) registerForm.style.display = 'block';
            }
        });
    });
}

function setupEventListeners() {
    document.getElementById('loginForm').addEventListener('submit', handleLogin);

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    const forgotForm = document.getElementById('forgotPasswordForm');
    if (forgotForm) {
        forgotForm.addEventListener('submit', handleForgotPassword);
    }

    const resetForm = document.getElementById('resetPasswordForm');
    if (resetForm) {
        resetForm.addEventListener('submit', handleResetPassword);
    }

    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            showPage(page);
        });
    });

    document.getElementById('cargoForm').addEventListener('submit', handleAddCargo);
    document.getElementById('stationForm').addEventListener('submit', handleAddStation);
    document.getElementById('vehicleForm').addEventListener('submit', handleAddVehicle);
    document.getElementById('settingsForm').addEventListener('submit', handleSaveSettings);
}

async function checkSession() {
    try {
        const res = await fetch('/api/session');
        const data = await res.json();

        if (data.logged_in) {
            currentUser = data;
            showApp();
        } else {
            showLogin();
        }
    } catch (err) {
        showLogin();
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const errorDiv = document.getElementById('loginError');

    try {
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (data.success) {
            if (errorDiv) errorDiv.style.display = 'none';
            currentUser = data;
            showApp();
        } else {
            if (errorDiv) {
                errorDiv.style.display = 'flex';
                errorDiv.querySelector('span').textContent = data.error || 'Kullanici adi veya sifre hatali!';
            } else {
                alert(data.error || 'Giris basarisiz');
            }
        }
    } catch (err) {
        if (errorDiv) {
            errorDiv.style.display = 'flex';
            errorDiv.querySelector('span').textContent = 'Baglanti hatasi!';
        } else {
            alert('Baglanti hatasi');
        }
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const passwordConfirm = document.getElementById('regPasswordConfirm').value;
    const errorDiv = document.getElementById('registerError');
    const successDiv = document.getElementById('registerSuccess');

    if (password !== passwordConfirm) {
        if (errorDiv) {
            errorDiv.style.display = 'flex';
            errorDiv.querySelector('span').textContent = 'Sifreler eslesiyor!';
        }
        if (successDiv) successDiv.style.display = 'none';
        return;
    }

    try {
        const res = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await res.json();

        if (data.success) {
            if (errorDiv) errorDiv.style.display = 'none';
            if (successDiv) {
                successDiv.style.display = 'flex';
                successDiv.querySelector('span').textContent = 'Kayit basarili! Giris yapabilirsiniz.';
            }
            setTimeout(() => {
                const loginTab = document.querySelector('.login-tab[data-tab="login"]');
                if (loginTab) loginTab.click();
            }, 2000);
        } else {
            if (successDiv) successDiv.style.display = 'none';
            if (errorDiv) {
                errorDiv.style.display = 'flex';
                errorDiv.querySelector('span').textContent = data.error || 'Kayit basarisiz';
            }
        }
    } catch (err) {
        if (successDiv) successDiv.style.display = 'none';
        if (errorDiv) {
            errorDiv.style.display = 'flex';
            errorDiv.querySelector('span').textContent = 'Baglanti hatasi';
        }
    }
}

let resetEmail = '';

function showForgotPassword() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const forgotForm = document.getElementById('forgotPasswordForm');
    const resetForm = document.getElementById('resetPasswordForm');
    const tabs = document.querySelector('.login-tabs');
    const demoAccounts = document.querySelector('.demo-accounts');

    if (loginForm) loginForm.style.display = 'none';
    if (registerForm) registerForm.style.display = 'none';
    if (forgotForm) forgotForm.style.display = 'block';
    if (resetForm) resetForm.style.display = 'none';
    if (tabs) tabs.style.display = 'none';
    if (demoAccounts) demoAccounts.style.display = 'none';
}

function hideForgotPassword() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const forgotForm = document.getElementById('forgotPasswordForm');
    const resetForm = document.getElementById('resetPasswordForm');
    const tabs = document.querySelector('.login-tabs');
    const demoAccounts = document.querySelector('.demo-accounts');

    if (loginForm) loginForm.style.display = 'block';
    if (registerForm) registerForm.style.display = 'none';
    if (forgotForm) forgotForm.style.display = 'none';
    if (resetForm) resetForm.style.display = 'none';
    if (tabs) tabs.style.display = 'flex';
    if (demoAccounts) demoAccounts.style.display = 'block';

    const loginTab = document.querySelector('.login-tab[data-tab="login"]');
    const registerTab = document.querySelector('.login-tab[data-tab="register"]');
    if (loginTab) loginTab.classList.add('active');
    if (registerTab) registerTab.classList.remove('active');
}

function showResetPasswordForm() {
    const forgotForm = document.getElementById('forgotPasswordForm');
    const resetForm = document.getElementById('resetPasswordForm');

    if (forgotForm) forgotForm.style.display = 'none';
    if (resetForm) resetForm.style.display = 'block';
}

async function handleForgotPassword(e) {
    e.preventDefault();
    const email = document.getElementById('forgotEmail').value;
    const errorDiv = document.getElementById('forgotError');
    const successDiv = document.getElementById('forgotSuccess');

    try {
        const res = await fetch('/api/forgot-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });

        const data = await res.json();

        if (data.success) {
            resetEmail = email;
            if (errorDiv) errorDiv.style.display = 'none';
            if (successDiv) {
                successDiv.style.display = 'flex';
                successDiv.querySelector('span').textContent = data.message || 'Kod gonderildi!';
            }
            setTimeout(() => {
                showResetPasswordForm();
            }, 2000);
        } else {
            if (successDiv) successDiv.style.display = 'none';
            if (errorDiv) {
                errorDiv.style.display = 'flex';
                errorDiv.querySelector('span').textContent = data.error || 'Hata olustu';
            }
        }
    } catch (err) {
        if (successDiv) successDiv.style.display = 'none';
        if (errorDiv) {
            errorDiv.style.display = 'flex';
            errorDiv.querySelector('span').textContent = 'Baglanti hatasi';
        }
    }
}

async function handleResetPassword(e) {
    e.preventDefault();
    const code = document.getElementById('resetCode').value;
    const newPassword = document.getElementById('newPassword').value;
    const newPasswordConfirm = document.getElementById('newPasswordConfirm').value;
    const errorDiv = document.getElementById('resetError');
    const successDiv = document.getElementById('resetSuccess');

    if (newPassword !== newPasswordConfirm) {
        if (errorDiv) {
            errorDiv.style.display = 'flex';
            errorDiv.querySelector('span').textContent = 'Sifreler eslesiyor!';
        }
        if (successDiv) successDiv.style.display = 'none';
        return;
    }

    try {
        const res = await fetch('/api/reset-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: resetEmail, code, new_password: newPassword })
        });

        const data = await res.json();

        if (data.success) {
            if (errorDiv) errorDiv.style.display = 'none';
            if (successDiv) {
                successDiv.style.display = 'flex';
                successDiv.querySelector('span').textContent = data.message || 'Sifre degistirildi!';
            }
            setTimeout(() => {
                hideForgotPassword();
            }, 2000);
        } else {
            if (successDiv) successDiv.style.display = 'none';
            if (errorDiv) {
                errorDiv.style.display = 'flex';
                errorDiv.querySelector('span').textContent = data.error || 'Hata olustu';
            }
        }
    } catch (err) {
        if (successDiv) successDiv.style.display = 'none';
        if (errorDiv) {
            errorDiv.style.display = 'flex';
            errorDiv.querySelector('span').textContent = 'Baglanti hatasi';
        }
    }
}

async function logout() {
    await fetch('/api/logout', { method: 'POST' });
    currentUser = null;
    showLogin();
}

function showLogin() {
    document.getElementById('loginScreen').style.display = 'flex';
    document.getElementById('app').style.display = 'none';
}

function showApp() {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('app').style.display = 'flex';
    document.getElementById('currentUser').textContent = currentUser.username;

    if (currentUser.role === 'admin') {
        document.body.classList.add('is-admin');
    } else {
        document.body.classList.remove('is-admin');
    }

    showPage('dashboard');
}

function showLoginTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`.tab-btn:${tab === 'login' ? 'first-child' : 'last-child'}`).classList.add('active');
    document.getElementById('loginForm').style.display = tab === 'login' ? 'block' : 'none';
    document.getElementById('registerForm').style.display = tab === 'register' ? 'block' : 'none';
}

function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(page).classList.add('active');

    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector(`.nav-item[data-page="${page}"]`).classList.add('active');

    switch (page) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'map':
            setTimeout(initMainMap, 100);
            break;
        case 'cargos':
            loadCargos();
            break;
        case 'myroute':
            loadMyRoute();
            break;
        case 'stations':
            loadStations();
            break;
        case 'vehicles':
            loadVehicles();
            break;
        case 'optimize':
            loadPendingCargos();
            setTomorrowDate();
            break;
        case 'routes':
            loadRoutes();
            break;
        case 'settings':
            loadSettings();
            break;
        case 'database':
            loadDatabaseView();
            break;
    }
}

async function loadDashboard() {
    try {
        const res = await fetch('/api/stats');
        const stats = await res.json();

        if (stats.error) {
            document.getElementById('statTotalCargos').textContent = '-';
            document.getElementById('statPendingCargos').textContent = '-';
            document.getElementById('statTotalRoutes').textContent = '-';
            document.getElementById('statTotalDistance').textContent = '-';
            document.getElementById('statTotalCost').textContent = '-';
            document.getElementById('statTotalWeight').textContent = '-';
            return;
        }

        document.getElementById('statTotalCargos').textContent = stats.total_cargos;
        document.getElementById('statPendingCargos').textContent = stats.pending_cargos;
        document.getElementById('statTotalRoutes').textContent = stats.total_routes;
        document.getElementById('statTotalDistance').textContent = stats.total_distance.toFixed(1) + ' km';
        document.getElementById('statTotalCost').textContent = stats.total_cost.toFixed(0) + ' TL';
        document.getElementById('statTotalWeight').textContent = stats.total_weight.toFixed(0) + ' kg';

        renderCharts(stats);
    } catch (err) {
        console.error('Dashboard yuklenemedi:', err);
    }
}

function renderCharts(stats) {
    if (!stats.station_distribution) return;

    const labels = stats.station_distribution.map(s => s.name);
    const cargoCounts = stats.station_distribution.map(s => s.cargo_count);
    const weights = stats.station_distribution.map(s => s.total_weight);

    const ctx1 = document.getElementById('stationChart').getContext('2d');
    if (stationChart) stationChart.destroy();
    stationChart = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Kargo Sayisi',
                data: cargoCounts,
                backgroundColor: 'rgba(52, 152, 219, 0.7)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });

    const ctx2 = document.getElementById('weightChart').getContext('2d');
    if (weightChart) weightChart.destroy();

    const nonZeroLabels = [];
    const nonZeroWeights = [];
    labels.forEach((label, i) => {
        if (weights[i] > 0) {
            nonZeroLabels.push(label);
            nonZeroWeights.push(weights[i]);
        }
    });

    weightChart = new Chart(ctx2, {
        type: 'pie',
        data: {
            labels: nonZeroLabels,
            datasets: [{
                data: nonZeroWeights,
                backgroundColor: [
                    '#e74c3c', '#3498db', '#27ae60', '#9b59b6', '#f39c12',
                    '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b',
                    '#2980b9', '#8e44ad'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right' }
            }
        }
    });
}

async function initMainMap() {
    await loadStationsData();

    if (!mainMap) {
        mainMap = L.map('mainMap').setView([40.7654, 29.9408], 10);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: ' OpenStreetMap'
        }).addTo(mainMap);
    }

    mainMap.eachLayer(layer => {
        if (layer instanceof L.Marker || layer instanceof L.Polyline) {
            mainMap.removeLayer(layer);
        }
    });

    stations.forEach(station => {

        const isDepot = station.name.toLowerCase().includes('umuttepe') || station.name.toLowerCase().includes('koü') || station.name.toLowerCase().includes('kampüs');
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background:${isDepot ? '#e74c3c' : '#3498db'}; width:24px; height:24px; border-radius:50%; border:3px solid white; box-shadow:0 2px 5px rgba(0,0,0,0.3);"></div>`,
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });

        L.marker([station.latitude, station.longitude], { icon })
            .bindPopup(`<b>${station.name}</b>${isDepot ? '<br><i style="color:#e74c3c">Varış Noktası (KOÜ)</i>' : ''}<br>Enlem: ${station.latitude}<br>Boylam: ${station.longitude}`)
            .addTo(mainMap);
    });

    if (currentUser.role === 'admin') {
        await showRoutesOnMap(mainMap);
    }

    setTimeout(() => mainMap.invalidateSize(), 100);
}

async function showRoutesOnMap(map) {
    try {
        const res = await fetch('/api/routes');
        const routes = await res.json();

        const recentRoutes = routes.slice(0, 5);

        for (let i = 0; i < recentRoutes.length; i++) {
            const route = recentRoutes[i];
            if (route.route_data) {
                const routeStations = JSON.parse(route.route_data);
                await drawRoute(map, routeStations, routeColors[i % routeColors.length]);
            }
        }
    } catch (err) {
        console.error('Rotalar yuklenemedi:', err);
    }
}

async function drawRoute(map, stationNames, color) {
    try {
        const res = await fetch('/api/route-geometry', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stations: stationNames })
        });

        const data = await res.json();

        if (data.geometry && data.geometry.coordinates) {
            const coordinates = data.geometry.coordinates.map(c => [c[1], c[0]]);
            L.polyline(coordinates, {
                color: color,
                weight: 4,
                opacity: 0.8
            }).addTo(map);
        }
    } catch (err) {
        console.error('Rota cizilemedi:', err);
    }
}

function refreshMap() {
    initMainMap();
}

async function loadCargos() {
    try {
        const res = await fetch('/api/cargos');
        const cargos = await res.json();

        const tbody = document.getElementById('cargosTable');
        const isAdmin = currentUser && currentUser.role === 'admin';

        tbody.innerHTML = cargos.map(c => {
            const deliveryDate = c.delivery_date ? new Date(c.delivery_date).toLocaleDateString('tr-TR') : '-';
            const createdDate = new Date(c.created_at).toLocaleDateString('tr-TR');
            return `
            <tr>
                <td>${c.id}</td>
                <td>${c.station_name}</td>
                <td>${c.weight}</td>
                <td><span class="status status-${c.status}">${getStatusText(c.status)}</span></td>
                <td>${deliveryDate}</td>
                <td>
                    ${c.status === 'pending' ? `<button onclick="deleteCargo(${c.id})" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>` :
                    (c.status === 'assigned' ? `<button onclick="showMyCargoRoute(${c.id})" class="btn btn-primary btn-sm" title="Rotayi Gor"><i class="fas fa-map"></i></button>` : '-')}
                </td>
            </tr>
        `}).join('');
    } catch (err) {
        console.error('Kargolar yuklenemedi:', err);
    }
}

let selectedCargoIdForRoute = null;

function showMyCargoRoute(cargoId) {
    selectedCargoIdForRoute = cargoId;
    showPage('myroute');
}

function getStatusText(status) {
    const texts = {
        'pending': 'Bekliyor',
        'assigned': 'Atandi',
        'delivered': 'Teslim Edildi'
    };
    return texts[status] || status;
}

function showCargoModal() {
    loadStationsData().then(() => {
        const select = document.getElementById('cargoStation');

        const cargoStations = stations.filter(s => {
            const name = s.name.toLowerCase();
            return !name.includes('umuttepe') &&
                !name.includes('koü') &&
                !name.includes('kou') &&
                !name.includes('kampüs') &&
                !name.includes('kampus') &&
                !name.includes('üniversite') &&
                !name.includes('universite');
        });
        select.innerHTML = cargoStations.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        document.getElementById('cargoModal').classList.add('active');
    });
}

async function handleAddCargo(e) {
    e.preventDefault();

    try {
        const res = await fetch('/api/cargos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                station_id: document.getElementById('cargoStation').value,
                weight: document.getElementById('cargoWeight').value
            })
        });

        const data = await res.json();

        if (data.success) {
            closeModal('cargoModal');
            loadCargos();
            alert('Kargo eklendi!');
        } else {
            alert(data.error || 'Kargo eklenemedi');
        }
    } catch (err) {
        alert('Baglanti hatasi');
    }
}

async function loadStationsData() {
    try {
        const res = await fetch('/api/stations');
        stations = await res.json();
    } catch (err) {
        console.error('Istasyonlar yuklenemedi:', err);
    }
}

async function loadStations() {
    await loadStationsData();

    const tbody = document.getElementById('stationsTable');
    tbody.innerHTML = stations.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.name}</td>
            <td>${s.latitude}</td>
            <td>${s.longitude}</td>
            <td>
                <button onclick="deleteStation(${s.id})" class="btn btn-danger btn-sm">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function showStationModal() {
    document.getElementById('stationModal').classList.add('active');
}

async function handleAddStation(e) {
    e.preventDefault();

    try {
        const res = await fetch('/api/stations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: document.getElementById('stationName').value,
                latitude: document.getElementById('stationLat').value,
                longitude: document.getElementById('stationLon').value
            })
        });

        const data = await res.json();

        if (data.success) {
            closeModal('stationModal');
            loadStations();
            alert('Istasyon eklendi!');
        } else {
            alert(data.error || 'Istasyon eklenemedi');
        }
    } catch (err) {
        alert('Baglanti hatasi');
    }
}

async function deleteStation(id) {
    if (!confirm('Bu istasyonu silmek istediginize emin misiniz?')) return;

    try {
        await fetch(`/api/stations/${id}`, { method: 'DELETE' });
        loadStations();
    } catch (err) {
        alert('Silme hatasi');
    }
}

async function loadVehicles() {
    try {
        const res = await fetch('/api/vehicles');
        const vehicles = await res.json();

        const tbody = document.getElementById('vehiclesTable');
        tbody.innerHTML = vehicles.map(v => `
            <tr>
                <td>${v.id}</td>
                <td>${v.name}</td>
                <td>${v.capacity}</td>
                <td>${v.rental_cost} birim</td>
                <td>${v.fuel_consumption} lt/km</td>
                <td><span class="status ${v.is_owned ? 'status-assigned' : 'status-pending'}">${v.is_owned ? 'Sahip' : 'Kiralik'}</span></td>
                <td>
                    <button onclick="deleteVehicle(${v.id})" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `).join('');
    } catch (err) {
        console.error('Araclar yuklenemedi:', err);
    }
}

function showVehicleModal() {
    document.getElementById('vehicleModal').classList.add('active');
}

async function handleAddVehicle(e) {
    e.preventDefault();

    try {
        const res = await fetch('/api/vehicles', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: document.getElementById('vehicleName').value,
                capacity: document.getElementById('vehicleCapacity').value,
                fuel_consumption: document.getElementById('vehicleFuel').value
            })
        });

        const data = await res.json();

        if (data.success) {
            closeModal('vehicleModal');
            loadVehicles();
            alert('Arac eklendi!');
        } else {
            alert(data.error || 'Arac eklenemedi');
        }
    } catch (err) {
        alert('Baglanti hatasi');
    }
}

let selectedCargoIds = new Set();

async function loadPendingCargos() {
    try {
        const res = await fetch('/api/cargos');
        const cargos = await res.json();

        const allCargos = cargos.filter(c => c.status === 'pending' || c.status === 'assigned');
        const pending = cargos.filter(c => c.status === 'pending');
        const assigned = cargos.filter(c => c.status === 'assigned');

        const summaryDiv = document.getElementById('pendingCargosSummary');

        if (!summaryDiv) {
            console.error('pendingCargosSummary div bulunamadi!');
            return;
        }

        if (allCargos.length === 0) {
            summaryDiv.innerHTML = '<p class="alert alert-info"><i class="fas fa-info-circle"></i> Kargo bulunmuyor.</p>';
            return;
        }

        let html = '<div style="margin-bottom:10px;">';
        html += '<button onclick="selectAllCargos()" class="btn btn-sm btn-outline" style="margin-right:5px;"><i class="fas fa-check-square"></i> Tumunu Sec</button>';
        html += '<button onclick="deselectAllCargos()" class="btn btn-sm btn-outline" style="margin-right:5px;"><i class="fas fa-square"></i> Secimi Kaldir</button>';
        html += '<span style="margin-left:10px; font-size:12px;"><span style="color:#ffc107;">●</span> Bekliyor <span style="color:#28a745;">●</span> Atandi</span>';
        html += '</div>';

        html += '<table class="summary-table"><thead><tr><th style="width:40px;"><input type="checkbox" id="selectAllCheckbox" onchange="toggleAllCargos(this)"></th><th>ID</th><th>Istasyon</th><th>Agirlik (kg)</th><th>Durum</th><th>Tarih</th></tr></thead><tbody>';

        allCargos.forEach(c => {
            const formattedDate = c.delivery_date ? new Date(c.delivery_date).toLocaleDateString('tr-TR') : '-';
            const isChecked = selectedCargoIds.has(c.id) ? 'checked' : '';
            const statusColor = c.status === 'pending' ? '#ffc107' : '#28a745';
            const statusText = c.status === 'pending' ? 'Bekliyor' : 'Atandi';
            const rowStyle = c.status === 'assigned' ? 'background-color: rgba(40, 167, 69, 0.1);' : '';
            html += `<tr style="${rowStyle}">
                <td><input type="checkbox" class="cargo-checkbox" value="${c.id}" ${isChecked} onchange="updateCargoSelection(${c.id}, this.checked)"></td>
                <td>${c.id}</td>
                <td>${c.station_name}</td>
                <td>${c.weight}</td>
                <td><span style="color:${statusColor}; font-weight:bold;">${statusText}</span></td>
                <td>${formattedDate}</td>
            </tr>`;
        });

        const totalWeight = allCargos.reduce((sum, c) => sum + c.weight, 0);
        html += `<tr style="font-weight:bold;background:#e3f2fd;"><td></td><td></td><td>TOPLAM</td><td>${totalWeight.toFixed(1)}</td><td>${pending.length} bekliyor / ${assigned.length} atandi</td><td>${allCargos.length} kargo</td></tr>`;
        html += '</tbody></table>';

        html += '<div id="selectedCargosSummary" style="margin-top:10px;padding:10px;background:#fff3cd;border-radius:5px;display:none;"></div>';

        summaryDiv.innerHTML = html;
        updateSelectedSummary();
    } catch (err) {
        console.error('Bekleyen kargolar yuklenemedi:', err);
    }
}

function updateCargoSelection(cargoId, isSelected) {
    cargoId = parseInt(cargoId);
    if (isSelected) {
        selectedCargoIds.add(cargoId);
    } else {
        selectedCargoIds.delete(cargoId);
    }
    updateSelectedSummary();
}

function toggleAllCargos(checkbox) {
    const checkboxes = document.querySelectorAll('.cargo-checkbox');
    checkboxes.forEach(cb => {
        cb.checked = checkbox.checked;
        const cargoId = parseInt(cb.value);
        if (checkbox.checked) {
            selectedCargoIds.add(cargoId);
        } else {
            selectedCargoIds.delete(cargoId);
        }
    });
    updateSelectedSummary();
}

function selectAllCargos() {
    const checkboxes = document.querySelectorAll('.cargo-checkbox');
    checkboxes.forEach(cb => {
        cb.checked = true;
        selectedCargoIds.add(parseInt(cb.value));
    });
    document.getElementById('selectAllCheckbox').checked = true;
    updateSelectedSummary();
}

function deselectAllCargos() {
    const checkboxes = document.querySelectorAll('.cargo-checkbox');
    checkboxes.forEach(cb => {
        cb.checked = false;
    });
    selectedCargoIds.clear();
    document.getElementById('selectAllCheckbox').checked = false;
    updateSelectedSummary();
}

function updateSelectedSummary() {
    const summaryDiv = document.getElementById('selectedCargosSummary');
    if (!summaryDiv) return;

    if (selectedCargoIds.size === 0) {
        summaryDiv.style.display = 'none';
        return;
    }

    summaryDiv.style.display = 'block';
    summaryDiv.innerHTML = `<i class="fas fa-check-circle" style="color:#28a745;"></i> <strong>${selectedCargoIds.size}</strong> kargo secildi. "Rota Planla" butonuna basarak bu kargolar icin rota olusturabilirsiniz.`;
}

async function runOptimization() {
    if (selectedCargoIds.size === 0) {
        alert('Lutfen en az bir kargo secin!');
        return;
    }

    const problemType = document.getElementById('problemType').value;
    const optimizeFor = document.getElementById('optimizeFor').value;
    const deliveryDateEl = document.getElementById('deliveryDate');
    const deliveryDate = deliveryDateEl ? deliveryDateEl.value : null;

    const cargoIds = Array.from(selectedCargoIds);

    const checkboxes = document.querySelectorAll('.cargo-checkbox:checked');
    let pendingCount = 0;
    let assignedCount = 0;

    checkboxes.forEach(cb => {
        const row = cb.closest('tr');
        const statusCell = row.querySelector('td:nth-child(5)');
        if (statusCell) {
            const statusText = statusCell.textContent.trim().toLowerCase();
            if (statusText.includes('bekliyor') || statusText.includes('pending')) {
                pendingCount++;
            } else {
                assignedCount++;
            }
        }
    });

    if (pendingCount === 0) {
        alert('Sectiginiz kargolarin hepsi zaten atanmis durumda!\nSadece "Bekliyor" durumundaki kargolar planlanabilir.\n\nKarsilastirma yapmak icin "Secilenleri Karsilastir" butonunu kullanin.');
        return;
    }

    if (assignedCount > 0) {
        const devam = confirm(`Sectiginiz ${cargoIds.length} kargodan ${assignedCount} tanesi zaten atanmis.\nSadece ${pendingCount} bekleyen kargo planlanacak.\n\nDevam etmek istiyor musunuz?`);
        if (!devam) return;
    }

    try {
        const res = await fetch('/api/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: problemType,
                optimize_for: optimizeFor,
                delivery_date: deliveryDate || null,
                cargo_ids: cargoIds
            })
        });

        const result = await res.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        lastOptimizationResult = result;

        alert(`✅ Rota planlamasi tamamlandi!\n\n📦 ${result.total_cargos} kargo planlandi\n🚚 ${result.routes.length} rota olusturuldu\n📏 Toplam mesafe: ${result.routes.reduce((sum, r) => sum + r.distance, 0).toFixed(1)} km\n💰 Toplam maliyet: ${result.total_cost.toFixed(0)} birim`);

        selectedCargoIds.clear();

        await loadPendingCargos();

        displayOptimizationResults(result);
    } catch (err) {
        alert('Optimizasyon hatasi');
        console.error(err);
    }
}

async function displayOptimizationResults(result) {
    const container = document.getElementById('optimizationResults');
    container.style.display = 'block';

    document.getElementById('resultTotalCost').textContent = result.total_cost.toFixed(0) + ' birim';
    document.getElementById('resultTotalCargos').textContent = result.total_cargos;
    document.getElementById('resultTotalWeight').textContent = result.total_weight.toFixed(0) + ' kg';

    if (result.total_fuel_cost) {
        document.getElementById('fuelCostInfo').style.display = 'block';
        document.getElementById('resultFuelCost').textContent = result.total_fuel_cost.toFixed(0) + ' birim';
    } else {
        document.getElementById('fuelCostInfo').style.display = 'none';
    }

    if (result.rented_vehicles > 0) {
        document.getElementById('rentedInfo').style.display = 'block';
        document.getElementById('resultRentedVehicles').textContent = result.rented_vehicles + ` (${result.rental_cost} birim)`;
    } else {
        document.getElementById('rentedInfo').style.display = 'none';
    }

    const detailsDiv = document.getElementById('routeDetails');
    detailsDiv.innerHTML = result.routes.map((route, i) => {
        let usersHtml = '';
        if (route.cargo_users && route.cargo_users.length > 0) {
            usersHtml = `<div class="cargo-users"><strong>Kargo Sahipleri:</strong><ul>${route.cargo_users.map(u => `<li>${u.username || 'Anonim'} - ${u.weight}kg (${u.station})</li>`).join('')}</ul></div>`;
        }
        return `
        <div class="route-card ${route.is_rented ? 'rented' : ''}">
            <h4>
                <i class="fas fa-truck" style="color:${routeColors[i % routeColors.length]}"></i>
                ${route.vehicle.name}
                ${route.is_rented ? '<span class="status status-pending">Kiralik</span>' : ''}
            </h4>
            <div class="route-info">
                <span>Mesafe: <strong>${route.distance} km</strong></span>
                <span>Yakit: <strong>${route.fuel_cost || 0} birim</strong></span>
                <span>Maliyet: <strong>${route.cost} birim</strong></span>
                <span>Agirlik: <strong>${route.weight} kg</strong></span>
                <span>Kargo: <strong>${route.cargo_count} adet</strong></span>
            </div>
            <div class="route-path">
                <strong>Guzergah:</strong> ${route.route_names.join(' <i class="fas fa-arrow-right"></i> ')}
            </div>
            ${usersHtml}
        </div>
    `}).join('');

    if (result.undelivered && result.undelivered.length > 0) {
        let undeliveredHtml = `
            <div class="alert alert-warning" style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 15px; margin-top: 15px;">
                <h5 style="color: #856404; margin-bottom: 10px;">
                    <i class="fas fa-exclamation-triangle"></i> 
                    ${result.undelivered.length} kargo teslim edilemedi
                </h5>
                <p style="color: #856404; margin-bottom: 10px; font-size: 13px;">
                    <strong>Sebep:</strong> Kargo ağırlığı mevcut araç kapasitelerini aşıyor veya araç kapasitesi doldu.
                </p>
                <table style="width: 100%; background: white; border-radius: 5px; overflow: hidden;">
                    <thead style="background: #ffc107; color: #333;">
                        <tr>
                            <th style="padding: 8px; text-align: left;">Kargo ID</th>
                            <th style="padding: 8px; text-align: left;">İstasyon</th>
                            <th style="padding: 8px; text-align: left;">Ağırlık</th>
                            <th style="padding: 8px; text-align: left;">Sebep</th>
                        </tr>
                    </thead>
                    <tbody>`;

        const rentalCapacity = 500;
        const maxOwnedCapacity = 1000;

        result.undelivered.forEach(cargo => {
            const stationName = cargo.station_name || 'Bilinmiyor';
            const weight = cargo.weight || 0;
            let reason = 'Araç kapasitesi yetersiz';

            if (weight > maxOwnedCapacity) {
                reason = `Kargo çok ağır (${weight}kg > max ${maxOwnedCapacity}kg)`;
            } else if (weight > rentalCapacity) {
                reason = `Kiralık araç kapasitesini aşıyor (${weight}kg > ${rentalCapacity}kg)`;
            }

            undeliveredHtml += `
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 8px; color: #333;">#${cargo.id}</td>
                    <td style="padding: 8px; color: #333;"><strong>${stationName}</strong></td>
                    <td style="padding: 8px; color: #e74c3c; font-weight: bold;">${weight} kg</td>
                    <td style="padding: 8px; color: #856404;">${reason}</td>
                </tr>`;
        });

        undeliveredHtml += `</tbody></table></div>`;
        detailsDiv.innerHTML += undeliveredHtml;
    }

    await initOptimizeMap(result.routes);
}

async function initOptimizeMap(routes) {
    await loadStationsData();

    if (!optimizeMap) {
        optimizeMap = L.map('optimizeMap').setView([40.7654, 29.9408], 10);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: ' OpenStreetMap'
        }).addTo(optimizeMap);
    }

    optimizeMap.eachLayer(layer => {
        if (layer instanceof L.Marker || layer instanceof L.Polyline) {
            optimizeMap.removeLayer(layer);
        }
    });

    stations.forEach(station => {
        const isDepot = station.name.toLowerCase().includes('umuttepe') || station.name.toLowerCase().includes('koü') || station.name.toLowerCase().includes('kampüs');
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background:${isDepot ? '#e74c3c' : '#3498db'}; width:20px; height:20px; border-radius:50%; border:2px solid white; box-shadow:0 2px 5px rgba(0,0,0,0.3);"></div>`,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        L.marker([station.latitude, station.longitude], { icon })
            .bindPopup(`<b>${station.name}</b>${isDepot ? '<br><i style="color:#e74c3c">Varış Noktası</i>' : ''}`)
            .addTo(optimizeMap);
    });

    for (let i = 0; i < routes.length; i++) {
        const route = routes[i];
        await drawRoute(optimizeMap, route.route_names, routeColors[i % routeColors.length]);
    }

    setTimeout(() => optimizeMap.invalidateSize(), 100);
}

async function loadRoutes() {
    try {
        const res = await fetch('/api/routes');
        const routes = await res.json();

        const tbody = document.getElementById('routesTable');

        if (routes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10" class="text-center">Henuz rota bulunmuyor</td></tr>';
            return;
        }

        const isAdmin = currentUser && currentUser.role === 'admin';

        tbody.innerHTML = routes.map(r => {
            let routeStations = '-';
            try {
                const parsed = JSON.parse(r.route_data);
                routeStations = (parsed.stations || parsed).join(' -> ');
            } catch (e) { }

            const cargoIds = r.cargo_ids ? r.cargo_ids.join(', ') : '-';

            return `
            <tr>
                <td>${r.id}</td>
                <td>${r.vehicle_name || 'Kiralik'}</td>
                <td>${routeStations}</td>
                <td>${r.total_distance?.toFixed(1) || '-'}</td>
                <td>${r.total_cost?.toFixed(0) || '-'} birim</td>
                <td>${r.total_weight?.toFixed(0) || '-'}</td>
                <td>${r.cargo_count || '-'}</td>
                <td><small title="Kargo ID'leri: ${cargoIds}">${cargoIds}</small></td>
                <td>${new Date(r.created_at).toLocaleDateString('tr-TR')}</td>
                <td>
                    <button onclick="showRouteOnMap(${r.id}, '${encodeURIComponent(r.route_data)}')" class="btn btn-primary btn-sm" title="Haritada Goster">
                        <i class="fas fa-map"></i>
                    </button>
                    ${isAdmin ? `<button onclick="deleteRoute(${r.id})" class="btn btn-danger btn-sm" title="Sil">
                        <i class="fas fa-trash"></i>
                    </button>` : ''}
                </td>
            </tr>
        `}).join('');
    } catch (err) {
        console.error('Rotalar yuklenemedi:', err);
    }
}

async function showRouteOnMap(routeId, routeDataEncoded) {
    const routeDataStr = decodeURIComponent(routeDataEncoded);
    let routeStations;
    try {
        const parsed = JSON.parse(routeDataStr);
        routeStations = parsed.stations || parsed;
    } catch (e) {
        alert('Rota verisi okunamadi');
        return;
    }

    document.getElementById('routeModal').classList.add('active');

    document.getElementById('routeModalContent').innerHTML = `
        <p><strong>Guzergah:</strong> ${routeStations.join(' -> ')}</p>
    `;

    setTimeout(async () => {
        await loadStationsData();

        if (!routeModalMap) {
            routeModalMap = L.map('routeModalMap').setView([40.7654, 29.9408], 10);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: ' OpenStreetMap'
            }).addTo(routeModalMap);
        }

        routeModalMap.eachLayer(layer => {
            if (layer instanceof L.Marker || layer instanceof L.Polyline) {
                routeModalMap.removeLayer(layer);
            }
        });

        for (const stationName of routeStations) {
            const station = stations.find(s => s.name === stationName);
            if (station) {
                const isDepot = station.name.includes('zmit');
                const icon = L.divIcon({
                    className: 'custom-marker',
                    html: `<div style="background:${isDepot ? '#e74c3c' : '#3498db'}; width:20px; height:20px; border-radius:50%; border:2px solid white;"></div>`,
                    iconSize: [20, 20],
                    iconAnchor: [10, 10]
                });

                L.marker([station.latitude, station.longitude], { icon })
                    .bindPopup(`<b>${station.name}</b>`)
                    .addTo(routeModalMap);
            }
        }

        await drawRoute(routeModalMap, routeStations, '#27ae60');

        routeModalMap.invalidateSize();
    }, 200);
}

async function deleteCargo(id) {
    if (!confirm('Bu kargoyu silmek istediginize emin misiniz?')) return;
    try {
        await fetch(`/api/cargos/${id}`, { method: 'DELETE' });
        loadCargos();
    } catch (err) {
        alert('Silme hatasi');
    }
}

async function deleteVehicle(id) {
    if (!confirm('Bu araci silmek istediginize emin misiniz?')) return;
    try {
        await fetch(`/api/vehicles/${id}`, { method: 'DELETE' });
        loadVehicles();
    } catch (err) {
        alert('Silme hatasi');
    }
}

async function deleteRoute(id) {
    if (!confirm('Bu rotayi silmek istediginize emin misiniz? Kargolar tekrar bekleyen durumuna alinacak.')) return;
    try {
        await fetch(`/api/routes/${id}`, { method: 'DELETE' });
        loadRoutes();
    } catch (err) {
        alert('Silme hatasi');
    }
}

async function loadSettings() {
    try {
        const res = await fetch('/api/parameters');
        const params = await res.json();

        document.getElementById('costPerKm').value = params.cost_per_km;
        document.getElementById('rentalCost').value = params.rental_cost;
        document.getElementById('rentalCapacity').value = params.rental_capacity;
    } catch (err) {
        console.error('Ayarlar yuklenemedi:', err);
    }
}

async function handleSaveSettings(e) {
    e.preventDefault();

    try {
        const res = await fetch('/api/parameters', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                cost_per_km: parseFloat(document.getElementById('costPerKm').value),
                rental_cost: parseFloat(document.getElementById('rentalCost').value),
                rental_capacity: parseInt(document.getElementById('rentalCapacity').value)
            })
        });

        const data = await res.json();

        if (data.success) {
            alert('Ayarlar kaydedildi!');
        } else {
            alert(data.error || 'Kaydetme hatasi');
        }
    } catch (err) {
        alert('Baglanti hatasi');
    }
}

async function loadDatabaseView() {
    window.open('/db-view.html', '_blank');
}

async function loadUsers() {
    try {
        const res = await fetch('/api/users');
        const users = await res.json();

        if (users.error) {
            console.error(users.error);
            return;
        }

        const tbody = document.getElementById('usersTable');
        tbody.innerHTML = users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td><strong>${user.username}</strong></td>
                <td>${user.email || '<span style="color:#888">-</span>'}</td>
                <td><code style="font-size:10px; color:#888">${user.password ? user.password.substring(0, 20) + '...' : '-'}</code></td>
                <td>
                    <span class="badge ${user.role === 'admin' ? 'badge-danger' : 'badge-primary'}">
                        ${user.role === 'admin' ? '<i class="fas fa-crown"></i> Admin' : '<i class="fas fa-user"></i> Kullanici'}
                    </span>
                </td>
                <td>${user.created_at ? new Date(user.created_at).toLocaleString('tr-TR') : '-'}</td>
                <td>
                    ${user.role !== 'admin' ? `
                        <button onclick="deleteUser(${user.id})" class="btn btn-danger btn-sm">
                            <i class="fas fa-trash"></i>
                        </button>
                    ` : '<span style="color:#888">-</span>'}
                </td>
            </tr>
        `).join('');
    } catch (err) {
        console.error('Kullanicilar yuklenemedi:', err);
    }
}

async function loadResetCodes() {
    try {
        const res = await fetch('/api/reset-codes');
        const codes = await res.json();

        if (codes.error) {
            console.error(codes.error);
            return;
        }

        const tbody = document.getElementById('resetCodesTable');

        if (codes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#888">Henuz sifre sifirlama kodu yok</td></tr>';
            return;
        }

        tbody.innerHTML = codes.map(code => {
            const isExpired = new Date(code.expires_at) < new Date();
            const statusClass = code.used ? 'badge-success' : (isExpired ? 'badge-danger' : 'badge-warning');
            const statusText = code.used ? 'Kullanildi' : (isExpired ? 'Suresi Doldu' : 'Aktif');

            return `
                <tr>
                    <td>${code.id}</td>
                    <td>${code.user_id} (${code.username || 'Bilinmiyor'})</td>
                    <td><code style="font-size:16px; letter-spacing:2px">${code.code}</code></td>
                    <td>${new Date(code.created_at).toLocaleString('tr-TR')}</td>
                    <td>${new Date(code.expires_at).toLocaleString('tr-TR')}</td>
                    <td><span class="badge ${statusClass}">${statusText}</span></td>
                </tr>
            `;
        }).join('');
    } catch (err) {
        console.error('Reset kodlari yuklenemedi:', err);
    }
}

async function loadDbStats() {
    try {
        const res = await fetch('/api/db-stats');
        const stats = await res.json();

        if (stats.error) {
            console.error(stats.error);
            return;
        }

        document.getElementById('totalUsers').textContent = stats.total_users;
        document.getElementById('totalAdmins').textContent = stats.total_admins;
        document.getElementById('totalStations').textContent = stats.total_stations;
        document.getElementById('totalCargosDb').textContent = stats.total_cargos;
    } catch (err) {
        console.error('DB istatistikleri yuklenemedi:', err);
    }
}

async function deleteUser(userId) {
    if (!confirm('Bu kullaniciyi silmek istediginize emin misiniz?')) {
        return;
    }

    try {
        const res = await fetch(`/api/users/${userId}`, { method: 'DELETE' });
        const data = await res.json();

        if (data.success) {
            loadUsers();
            loadDbStats();
        } else {
            alert(data.error || 'Silme hatasi');
        }
    } catch (err) {
        alert('Baglanti hatasi');
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal') && !e.target.id.includes('login')) {
        e.target.classList.remove('active');
    }
});

async function loadMyRoute() {
    try {
        let url = '/api/my-route';
        if (selectedCargoIdForRoute) {
            url += '?cargo_id=' + selectedCargoIdForRoute;
        }

        const res = await fetch(url);
        const data = await res.json();

        const container = document.getElementById('myRouteInfo');
        if (!container) return;

        if (!data.found) {
            container.innerHTML = '<div class="alert alert-info"><i class="fas fa-info-circle"></i> ' + data.message + '</div>';
            return;
        }

        const allRoutes = data.all_routes || [{ route: data.route, my_cargos: data.my_cargos }];

        let html = '';
        let allStations = [];

        for (let i = 0; i < allRoutes.length; i++) {
            const routeInfo = allRoutes[i];
            const route = routeInfo.route;
            const myCargos = routeInfo.my_cargos;

            let routeStations = [];
            try {
                const routeData = JSON.parse(route.route_data);
                routeStations = routeData.stations || routeData;
                allStations = allStations.concat(routeStations);
            } catch (e) {
                routeStations = [];
            }

            let deliveryDateStr = '';
            if (myCargos && myCargos.length > 0 && myCargos[0].delivery_date) {
                deliveryDateStr = new Date(myCargos[0].delivery_date).toLocaleDateString('tr-TR');
            }

            html += `
                <div class="my-route-card" style="margin-bottom: 15px; ${i > 0 ? 'border-top: 2px solid #ddd; padding-top: 15px;' : ''}">
                    <h4 style="color:#e74c3c;"><i class="fas fa-truck"></i> ${route.vehicle_name || 'Arac'}${route.vehicle_capacity ? ` (${route.vehicle_capacity}kg)` : ''}</h4>
                    <div class="route-info">
                        <p><strong>Guzergah:</strong> ${routeStations.join(' → ')}</p>
                        <p><strong>Toplam Mesafe:</strong> ${route.total_distance} km</p>
                        <p><strong>Tahmini Maliyet:</strong> ${route.total_cost} birim</p>
                        ${deliveryDateStr ? `<p><strong><i class="fas fa-calendar-check" style="color:#27ae60;"></i> Tahmini Teslim Tarihi:</strong> <span style="color:#27ae60; font-weight:bold;">${deliveryDateStr}</span></p>` : ''}
                    </div>
                    <h5>Kargolariniz:</h5>
                    <ul class="my-cargos-list">
                        ${myCargos.map(c => {
                const cargoDate = c.delivery_date ? new Date(c.delivery_date).toLocaleDateString('tr-TR') : '';
                return `<li><i class="fas fa-box"></i> ${c.station_name} - ${c.weight}kg <span class="status status-${c.status}">${getStatusText(c.status)}</span>${cargoDate ? ` <small style="color:#888;">Teslim: ${cargoDate}</small>` : ''}</li>`;
            }).join('')}
                    </ul>
                </div>
            `;
        }

        container.innerHTML = html;

        const firstRouteStations = allStations.length > 0 ? allStations : [];
        if (firstRouteStations.length >= 1) {
            setTimeout(() => initMyRouteMap(firstRouteStations), 100);
        }
    } catch (err) {
        console.error('Rota bilgisi yuklenemedi:', err);
        const container = document.getElementById('myRouteInfo');
        if (container) {
            container.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> Rota bilgisi yuklenirken hata olustu.</div>';
        }
    }
}

async function initMyRouteMap(routeStations) {
    await loadStationsData();

    const mapContainer = document.getElementById('myRouteMap');
    if (!mapContainer) return;

    let myRouteMap = L.map('myRouteMap').setView([40.7654, 29.9408], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: ' OpenStreetMap'
    }).addTo(myRouteMap);

    for (const stationName of routeStations) {
        const station = stations.find(s => s.name === stationName);
        if (station) {
            const isDepot = station.name.toLowerCase().includes('umuttepe') || station.name.toLowerCase().includes('koü') || station.name.toLowerCase().includes('kampüs');
            const icon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="background:${isDepot ? '#e74c3c' : '#27ae60'}; width:20px; height:20px; border-radius:50%; border:2px solid white;"></div>`,
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            });
            L.marker([station.latitude, station.longitude], { icon })
                .bindPopup(`<b>${station.name}</b>${isDepot ? '<br><i style="color:#e74c3c">Varış Noktası</i>' : '<br><i style="color:#27ae60">Kargo Alım Noktası</i>'}`)
                .addTo(myRouteMap);
        }
    }

    if (routeStations.length >= 2) {
        await drawRoute(myRouteMap, routeStations, '#27ae60');
    }

    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = function (map) {
        const div = L.DomUtil.create('div', 'map-legend-box');
        div.style.cssText = 'background:white; padding:10px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.2);';
        div.innerHTML = `
            <div style="font-weight:bold; margin-bottom:5px;">Gösterim</div>
            <div style="display:flex; align-items:center; gap:5px; margin:3px 0;">
                <div style="background:#27ae60; width:12px; height:12px; border-radius:50%;"></div>
                <span style="font-size:12px;">Kargo Alım Noktası</span>
            </div>
            <div style="display:flex; align-items:center; gap:5px; margin:3px 0;">
                <div style="background:#e74c3c; width:12px; height:12px; border-radius:50%;"></div>
                <span style="font-size:12px;">Varış (Umuttepe KOÜ)</span>
            </div>
            <div style="display:flex; align-items:center; gap:5px; margin:3px 0;">
                <div style="background:#27ae60; width:20px; height:3px;"></div>
                <span style="font-size:12px;">Rota</span>
            </div>
        `;
        return div;
    };
    legend.addTo(myRouteMap);

    myRouteMap.invalidateSize();
}

// loadSelectedScenario removed - only compareSelectedScenario is used

async function compareSelectedScenario() {
    const scenarioNum = document.getElementById('scenarioSelect').value || '1';
    const problemType = document.getElementById('problemType').value;
    const scenario = scenarios[scenarioNum];

    try {
        const res = await fetch('/api/compare-scenarios', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                scenarios: [scenario],
                scenario_num: scenarioNum,
                type: problemType
            })
        });

        const data = await res.json();

        if (!data.success) {
            alert(data.error || 'Karsilastirma yapilamadi');
            return;
        }

        displayComparisonResults(data.comparison, problemType, `Senaryo ${scenarioNum}`);
    } catch (err) {
        alert('Baglanti hatasi');
        console.error(err);
    }
}

async function comparePendingCargos() {
    const problemType = document.getElementById('problemType').value;
    const deliveryDate = document.getElementById('deliveryDate').value;

    try {
        const res = await fetch('/api/compare-pending', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: problemType,
                delivery_date: deliveryDate || null
            })
        });

        const data = await res.json();

        if (!data.success) {
            alert(data.error || 'Karsilastirma yapilamadi');
            return;
        }

        displayComparisonResults(data.comparison, problemType, `Bekleyen Kargolar (${data.cargo_count} adet)`);
    } catch (err) {
        alert('Baglanti hatasi');
        console.error(err);
    }
}

function runOptimizationSelected() {
    runOptimization();
}

async function compareSelectedCargos() {
    if (selectedCargoIds.size === 0) {
        alert('Lutfen en az bir kargo secin!');
        return;
    }

    const problemType = document.getElementById('problemType').value;
    const cargoIds = Array.from(selectedCargoIds);

    try {
        const res = await fetch('/api/compare-pending', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ problem_type: problemType, cargo_ids: cargoIds })
        });

        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        displayComparisonResults(data.comparison, problemType, `Secili Kargolar (${cargoIds.length} adet)`);
    } catch (err) {
        alert('Baglanti hatasi');
        console.error(err);
    }
}

function displayComparisonResults(comparison, problemType, title) {
    const container = document.getElementById('comparisonResults');
    container.style.display = 'block';

    const problemTypeNames = {
        'limited': 'Belirli Sayida Arac',
        'unlimited': 'Sinirsiz Arac'
    };

    const maxDelivered = Math.max(...comparison.map(r => r.total_cargos));
    const validResults = comparison.filter(r => r.total_cargos === maxDelivered);
    const minCost = Math.min(...validResults.map(r => r.total_cost));
    const bestResult = validResults.find(r => r.total_cost === minCost) || comparison[0];

    let html = `<p class="text-info mb-3"><i class="fas fa-info-circle"></i> <strong>${title}</strong> - Problem Tipi: <strong>${problemTypeNames[problemType]}</strong></p>`;

    let undeliveredReason = '-';
    if (bestResult.undelivered_count > 0) {
        const totalCap = (bestResult.vehicle_count || 3) > 0 ? '2250kg' : '?';
        undeliveredReason = `Kapasite yetersiz (${totalCap} < ${bestResult.total_weight + (bestResult.undelivered_weight || 0)}kg)`;
    }

    html += '<table class="comparison-table"><thead><tr><th>Problem Tipi</th><th>Toplam Maliyet</th><th>Kargo Sayisi</th><th>Toplam Agirlik</th><th>Arac Sayisi</th><th>Kiralik</th><th>Teslim Edilemedi</th><th>Teslim Edilememe Sebebi</th></tr></thead><tbody>';
    html += `<tr style="background-color: #d4edda;">
        <td>${problemTypeNames[problemType]}</td>
        <td><strong>${bestResult.total_cost.toFixed(2)}</strong> birim</td>
        <td>${bestResult.total_cargos}</td>
        <td>${bestResult.total_weight} kg</td>
        <td>${bestResult.vehicle_count}</td>
        <td>${bestResult.rented_vehicles}</td>
        <td>${bestResult.undelivered_count > 0 ? '<span class="text-danger">' + bestResult.undelivered_count + '</span>' : '0'}</td>
        <td>${bestResult.undelivered_count > 0 ? '<span class="text-warning">' + undeliveredReason + '</span>' : '-'}</td>
    </tr>`;
    html += '</tbody></table>';

    html += '<div class="comparison-routes" style="margin-top: 20px;">';
    html += '<h4 style="color: #3498db; margin-bottom: 15px;"><i class="fas fa-route"></i> Rota Detaylari</h4>';

    const r = bestResult;
    html += `<div style="background: #d4edda; border-radius: 8px; padding: 15px; margin-bottom: 15px; border: 1px solid #28a745;">`;

    if (r.routes && r.routes.length > 0) {
        r.routes.forEach((route, i) => {
            const color = routeColors[i % routeColors.length];
            const routeNamesJson = JSON.stringify(route.route_names).replace(/'/g, "\\'");

            let stationDetails = '';
            if (route.station_cargo_details) {
                stationDetails = route.station_cargo_details.map(s =>
                    `<span style="background:#e3f2fd;padding:2px 6px;border-radius:3px;margin-right:5px;font-size:11px;">${s.name}: ${s.cargo_count} kargo (${s.weight.toFixed(1)} kg)</span>`
                ).join('');
            }

            html += `<div style="background: white; border-left: 4px solid ${color}; padding: 12px; margin: 8px 0; border-radius: 4px;">`;
            html += `<div style="display: flex; align-items: center; justify-content: space-between;">`;
            html += `<div style="flex: 1;">`;
            html += `<strong style="color: ${color};"><i class="fas fa-truck"></i> ${route.vehicle_name}</strong>`;
            html += `<span style="margin-left: 15px; color: #666;">📏 ${route.distance} km | 💰 ${route.cost} birim | ⚖️ ${route.weight} kg | 📦 ${route.cargo_count} kargo</span>`;
            html += `<div style="margin-top: 5px; font-size: 13px; color: #555;">`;
            html += `<strong>Guzergah:</strong> ${route.route_names.join(' → ')}`;
            html += `</div>`;
            if (stationDetails) {
                html += `<div style="margin-top: 8px;">${stationDetails}</div>`;
            }
            html += `</div>`;
            html += `<button onclick='showSimulationRouteOnMap(${routeNamesJson}, "${color}")' class="btn btn-primary btn-sm" style="margin-left: 10px;" title="Haritada Goster">`;
            html += `<i class="fas fa-map"></i>`;
            html += `</button>`;
            html += `</div></div>`;
        });
    } else {
        html += `<p style="color: #888;"><i class="fas fa-info-circle"></i> Rota detayi mevcut degil</p>`;
    }

    if (r.undelivered_details && r.undelivered_details.length > 0) {
        html += `<div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 8px 0; border-radius: 4px;">`;
        html += `<strong style="color: #856404;"><i class="fas fa-exclamation-triangle"></i> Teslim Edilemeyen Kargolar (${r.undelivered_details.length} adet):</strong>`;
        html += `<div style="margin-top: 8px; display: flex; flex-wrap: wrap; gap: 8px;">`;

        const byStation = {};
        r.undelivered_details.forEach(cargo => {
            const station = cargo.station_name || 'Bilinmiyor';
            if (!byStation[station]) byStation[station] = [];
            byStation[station].push(cargo);
        });

        Object.keys(byStation).forEach(station => {
            const cargos = byStation[station];
            const totalWeight = cargos.reduce((sum, c) => sum + c.weight, 0);
            html += `<span style="background: #fff; padding: 4px 8px; border-radius: 4px; font-size: 12px; border: 1px solid #ffc107;">`;
            html += `<strong>${station}:</strong> ${cargos.length} kargo (${totalWeight.toFixed(1)} kg)`;
            html += `</span>`;
        });

        html += `</div></div>`;
    }

    html += '</div></div>';

    document.getElementById('comparisonTable').innerHTML = html;
}

async function showSimulationRouteOnMap(routeStations, color) {

    document.getElementById('routeModal').classList.add('active');

    document.getElementById('routeModalContent').innerHTML = `
        <p><strong>Simülasyon Rotası</strong> (Veritabanına kaydedilmedi)</p>
        <p><strong>Güzergah:</strong> ${routeStations.join(' → ')}</p>
    `;

    setTimeout(async () => {
        await loadStationsData();

        if (!routeModalMap) {
            routeModalMap = L.map('routeModalMap').setView([40.7654, 29.9408], 10);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: ' OpenStreetMap'
            }).addTo(routeModalMap);
        }

        routeModalMap.eachLayer(layer => {
            if (layer instanceof L.Marker || layer instanceof L.Polyline) {
                routeModalMap.removeLayer(layer);
            }
        });

        for (let i = 0; i < routeStations.length; i++) {
            const stationName = routeStations[i];
            const station = stations.find(s => s.name === stationName);
            if (station) {
                const isDepot = stationName.toLowerCase().includes('umuttepe') || stationName.toLowerCase().includes('koü');
                const isStart = i === 0;
                const isEnd = i === routeStations.length - 1;

                let markerColor = '#3498db';
                if (isDepot) markerColor = '#e74c3c';
                else if (isStart) markerColor = '#27ae60';

                const icon = L.divIcon({
                    className: 'custom-marker',
                    html: `<div style="background:${markerColor}; width:24px; height:24px; border-radius:50%; border:3px solid white; box-shadow:0 2px 5px rgba(0,0,0,0.3); display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:12px;">${i + 1}</div>`,
                    iconSize: [24, 24],
                    iconAnchor: [12, 12]
                });

                L.marker([station.latitude, station.longitude], { icon })
                    .bindPopup(`<b>${i + 1}. ${station.name}</b>${isStart ? '<br><i style="color:#27ae60">Başlangıç</i>' : (isDepot ? '<br><i style="color:#e74c3c">Varış (KOÜ)</i>' : '')}`)
                    .addTo(routeModalMap);
            }
        }

        await drawRoute(routeModalMap, routeStations, color || '#27ae60');

        routeModalMap.invalidateSize();
    }, 200);
}

