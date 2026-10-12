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
        // Senaryo 1: Marmara Bölgesel Dağıtım Ağı
        { district: 'Kadıköy', count: 12, weight: 350 },
        { district: 'Pendik', count: 15, weight: 600 },
        { district: 'Gebze', count: 20, weight: 1100 },
        { district: 'İzmit', count: 18, weight: 850 },
        { district: 'Adapazarı', count: 14, weight: 700 },
        { district: 'Nilüfer', count: 16, weight: 950 },
        { district: 'Çorlu', count: 10, weight: 650 },
        { district: 'Yalova', count: 8, weight: 400 }
    ],
    2: [
        // Senaryo 2: Metropoller Arası Ana Hat (Linehaul Express: İst - Kocaeli - Ankara - İzmir)
        { district: 'İkitelli', count: 25, weight: 2400 },
        { district: 'Gebze', count: 20, weight: 1800 },
        { district: 'Nilüfer', count: 18, weight: 1600 },
        { district: 'OSTİM', count: 22, weight: 2200 },
        { district: 'Çankaya', count: 25, weight: 2500 },
        { district: 'Eskişehir', count: 14, weight: 1200 },
        { district: 'Konak', count: 20, weight: 2100 }
    ],
    3: [
        // Senaryo 3: Ege & Akdeniz Kargo Koridoru
        { district: 'Bornova', count: 15, weight: 900 },
        { district: 'Efeler', count: 12, weight: 600 },
        { district: 'Bodrum', count: 14, weight: 800 },
        { district: 'Pamukkale', count: 16, weight: 1100 },
        { district: 'Muratpaşa', count: 22, weight: 1800 },
        { district: 'Akdeniz', count: 18, weight: 1500 },
        { district: 'Seyhan', count: 20, weight: 1700 }
    ],
    4: [
        // Senaryo 4: Türkiye Geneli 81 İl Sevk Dağıtımı (Tüm Coğrafi Bölgeler)
        { district: 'Kadıköy', count: 10, weight: 800 },
        { district: 'Çankaya', count: 12, weight: 1200 },
        { district: 'Konak', count: 10, weight: 900 },
        { district: 'Nilüfer', count: 8, weight: 700 },
        { district: 'Muratpaşa', count: 10, weight: 850 },
        { district: 'İlkadım', count: 8, weight: 650 },
        { district: 'Trabzon', count: 7, weight: 600 },
        { district: 'Melikgazi', count: 9, weight: 750 },
        { district: 'Selçuklu', count: 10, weight: 850 },
        { district: 'Şehitkamil', count: 12, weight: 1100 },
        { district: 'Kayapınar', count: 8, weight: 700 },
        { district: 'Yakutiye', count: 6, weight: 500 }
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
            return;
        }

        // 8 KPI Kartları
        const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
        setEl('statTotalCargos', stats.total_cargos || 0);
        setEl('statPendingCargos', stats.pending_cargos || 0);
        setEl('statTotalRoutes', stats.total_routes || 0);
        setEl('statTotalDistance', (stats.total_distance || 0).toLocaleString('tr-TR', { maximumFractionDigits: 1 }) + ' km');
        setEl('statTotalCost', (stats.total_cost || 0).toLocaleString('tr-TR', { maximumFractionDigits: 0 }) + ' TL');
        setEl('statTotalFuel', (stats.total_fuel_liters || 0).toLocaleString('tr-TR', { maximumFractionDigits: 1 }) + ' L');
        setEl('statTotalWeight', (stats.total_weight || 0).toLocaleString('tr-TR', { maximumFractionDigits: 0 }) + ' kg');
        setEl('statFleetUtilization', '%' + (stats.fleet_utilization_rate || 82.5));

        // Canlı Akaryakıt & Piyasa Şeridi
        if (stats.fuel_prices) {
            setEl('tickerDiesel', `${stats.fuel_prices.diesel_per_liter?.toFixed(2) || '92.50'} TL/L`);
            setEl('tickerGasoline', `${stats.fuel_prices.gasoline_per_liter?.toFixed(2) || '85.50'} TL/L`);
            setEl('tickerAdblue', `${stats.fuel_prices.adblue_per_liter?.toFixed(2) || '36.50'} TL/L`);
        }
        setEl('tickerCo2', `${(stats.total_co2_kg || 685.4).toLocaleString('tr-TR', { maximumFractionDigits: 1 })} kg CO₂`);
        setEl('tickerOnTime', `%${stats.on_time_delivery_rate || 99.2}`);

        // Canlı Kargo Akış Tablosu
        const activityTbody = document.getElementById('dashboardActivityTable');
        if (activityTbody && stats.activity_log) {
            activityTbody.innerHTML = stats.activity_log.map(act => `
                <tr>
                    <td><span style="display:inline-block; background:#0f172a; color:#f8fafc; padding:2px 8px; border-radius:6px; font-family:'Outfit',sans-serif; font-weight:700; font-size:11px; letter-spacing:0.5px;">${act.tracking_code}</span></td>
                    <td><strong>${act.station_name}</strong></td>
                    <td><span style="color:#64748b; font-size:12px;">${act.city}</span></td>
                    <td><strong>${act.weight} kg</strong></td>
                    <td>${act.username || 'Misafir'}</td>
                    <td>${act.delivery_date}</td>
                    <td><span class="status status-${act.status}">${getStatusText(act.status)}</span></td>
                </tr>
            `).join('');
        }

        renderCharts(stats);
    } catch (err) {
        console.error('Dashboard yuklenemedi:', err);
    }
}

function renderCharts(stats) {
    const ctx1El = document.getElementById('stationChart');
    const ctx2El = document.getElementById('weightChart');
    if (!ctx1El || !ctx2El) return;

    // 1. Bölgesel Dağıtım Bar Grafiği
    const regData = stats.regional_distribution || {
        'Marmara': 34,
        'İç Anadolu': 18,
        'Ege': 14,
        'Akdeniz': 9,
        'Karadeniz': 5,
        'Güneydoğu & Doğu': 4
    };

    if (stationChart) stationChart.destroy();
    stationChart = new Chart(ctx1El.getContext('2d'), {
        type: 'bar',
        data: {
            labels: Object.keys(regData),
            datasets: [{
                label: 'Kargo Hacmi (Paket)',
                data: Object.values(regData),
                backgroundColor: [
                    'rgba(99, 102, 241, 0.85)',
                    'rgba(14, 165, 233, 0.85)',
                    'rgba(16, 185, 129, 0.85)',
                    'rgba(245, 158, 11, 0.85)',
                    'rgba(239, 68, 68, 0.85)',
                    'rgba(168, 85, 247, 0.85)'
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.raw} Paket / Sevkiyat`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0, 0, 0, 0.04)' },
                    ticks: { font: { family: 'Inter', size: 11 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Inter', size: 11, weight: '500' } }
                }
            }
        }
    });

    // 2. Lojistik Operasyonel Maliyet Dağılımı (Doughnut Grafiği)
    const costData = stats.cost_breakdown || {
        labels: ['Akaryakıt (Motorin/Benzin)', 'Otoyol & Köprü Geçişi', 'Sürücü & İş Gücü', 'Araç Amortismanı'],
        values: [1250, 480, 620, 180]
    };

    if (weightChart) weightChart.destroy();
    weightChart = new Chart(ctx2El.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: costData.labels,
            datasets: [{
                data: costData.values,
                backgroundColor: [
                    '#ef4444',
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b'
                ],
                borderWidth: 3,
                borderColor: '#ffffff',
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 12,
                        padding: 12,
                        font: { family: 'Inter', size: 11, weight: '500' },
                        color: '#334155'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.label}: ${ctx.raw.toLocaleString('tr-TR')} TL`
                    }
                }
            },
            cutout: '62%'
        }
    });
}

let darkLayer = null;
let standardLayer = null;
let isDarkMap = false;
let stationMarkers = [];
let routeLayers = [];
let routeLinesVisible = true;
let simulationMarker = null;
let simulationInterval = null;
let currentSimulationCoords = [];

const TURKEY_REGIONS_MAP = {
    "Marmara": { center: [40.7, 29.5], zoom: 8, cities: ["Kocaeli", "İstanbul", "Bursa", "Sakarya", "Yalova", "Tekirdağ", "Edirne", "Kırklareli", "Balıkesir", "Çanakkale", "Bilecik"] },
    "Ege": { center: [38.3, 27.8], zoom: 8, cities: ["İzmir", "Manisa", "Aydın", "Denizli", "Muğla", "Afyonkarahisar", "Kütahya", "Uşak"] },
    "İç Anadolu": { center: [39.3, 33.2], zoom: 7, cities: ["Ankara", "Konya", "Eskişehir", "Kayseri", "Sivas", "Aksaray", "Kırıkkale", "Kırşehir", "Nevşehir", "Niğde", "Karaman", "Yozgat", "Çankırı"] },
    "Akdeniz": { center: [36.9, 32.5], zoom: 7, cities: ["Antalya", "Adana", "Mersin", "Hatay", "Kahramanmaraş", "Osmaniye", "Isparta", "Burdur"] },
    "Karadeniz": { center: [41.2, 35.5], zoom: 7, cities: ["Samsun", "Trabzon", "Ordu", "Giresun", "Rize", "Artvin", "Zonguldak", "Bolu", "Düzce", "Karabük", "Bartın", "Kastamonu", "Sinop", "Amasya", "Çorum", "Tokat", "Gümüşhane", "Bayburt"] },
    "Güneydoğu Anadolu": { center: [37.5, 39.5], zoom: 7, cities: ["Gaziantep", "Diyarbakır", "Şanlıurfa", "Batman", "Mardin", "Adıyaman", "Siirt", "Şırnak", "Kilis"] },
    "Doğu Anadolu": { center: [39.2, 41.8], zoom: 7, cities: ["Malatya", "Elazığ", "Erzurum", "Van", "Erzincan", "Kars", "Ağrı", "Muş", "Bitlis", "Bingöl", "Tunceli", "Iğdır", "Ardahan", "Hakkari"] }
};

async function initMainMap() {
    await loadStationsData();

    if (!mainMap) {
        // Tüm Türkiye'yi kapsayan merkez koordinatı ve görünüm
        mainMap = L.map('mainMap', {
            zoomControl: true,
            preferCanvas: true
        }).setView([39.1, 35.2], 6);

        standardLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap katkıda bulunanlar',
            maxZoom: 19
        }).addTo(mainMap);

        darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '© CartoDB DarkMatter',
            maxZoom: 19
        });
    }

    // Harita üzerindeki mevcut marker ve rotaları temizle
    stationMarkers.forEach(m => mainMap.removeLayer(m));
    stationMarkers = [];
    routeLayers.forEach(l => mainMap.removeLayer(l));
    routeLayers = [];

    // İl seçim kutusunu doldur
    populateMapCityFilter();

    // HUD Sayaçlarını Güncelle
    updateMapHud();

    // İstasyon markerlarını oluştur
    stations.forEach(station => {
        const isDepot = Boolean(station.is_depot) || station.name.toLowerCase().includes('hub') || station.name.toLowerCase().includes('depo');
        
        const markerHtml = isDepot
            ? `<div style="background:linear-gradient(135deg, #ef4444, #b91c1c); width:28px; height:28px; border-radius:50%; border:3px solid white; box-shadow:0 0 14px rgba(239,68,68,0.7); display:flex; align-items:center; justify-content:center; color:white; font-size:12px;"><i class="fas fa-warehouse"></i></div>`
            : `<div style="background:linear-gradient(135deg, #3b82f6, #1d4ed8); width:22px; height:22px; border-radius:50%; border:2px solid white; box-shadow:0 2px 8px rgba(0,0,0,0.3); display:flex; align-items:center; justify-content:center; color:white; font-size:10px;"><i class="fas fa-cube"></i></div>`;

        const icon = L.divIcon({
            className: 'custom-marker',
            html: markerHtml,
            iconSize: isDepot ? [28, 28] : [22, 22],
            iconAnchor: isDepot ? [14, 14] : [11, 11]
        });

        const popupContent = `
            <div style="font-family:'Inter',sans-serif; min-width:180px; padding:4px;">
                <div style="font-size:14px; font-weight:700; color:#0f172a; margin-bottom:4px;">${station.name}</div>
                ${isDepot ? '<div style="display:inline-block; background:#fee2e2; color:#ef4444; font-size:11px; font-weight:700; padding:2px 8px; border-radius:12px; margin-bottom:6px;"><i class="fas fa-star"></i> Ana Lojistik Hub (Merkez Depo)</div>' : '<div style="font-size:12px; color:#64748b; margin-bottom:4px;"><i class="fas fa-map-pin"></i> Dağıtım İstasyonu</div>'}
                <div style="font-size:11px; color:#475569; border-top:1px solid #e2e8f0; padding-top:4px;">
                    <div><strong>İl / İlçe:</strong> ${station.city || '-'} / ${station.district || '-'}</div>
                    <div><strong>Koordinat:</strong> ${station.latitude.toFixed(4)}, ${station.longitude.toFixed(4)}</div>
                </div>
            </div>
        `;

        const marker = L.marker([station.latitude, station.longitude], { icon })
            .bindPopup(popupContent)
            .addTo(mainMap);

        marker.stationData = station;
        stationMarkers.push(marker);
    });

    // Rotaları haritaya çiz
    if (currentUser && currentUser.role === 'admin') {
        await showRoutesOnMap(mainMap);
    }

    // Leaflet'in tam ekran oturmasını sağla
    setTimeout(() => {
        if (mainMap) mainMap.invalidateSize();
    }, 150);
}

function updateMapHud() {
    const elStation = document.getElementById('hudStationCount');
    const elCity = document.getElementById('hudCityCount');
    const elVehicle = document.getElementById('hudVehicleCount');

    if (elStation) elStation.textContent = stations.length;
    if (elCity) {
        const uniqueCities = new Set(stations.map(s => s.city).filter(Boolean));
        elCity.textContent = uniqueCities.size || '81';
    }
}

function populateMapCityFilter() {
    const select = document.getElementById('mapCityFilter');
    if (!select) return;

    const cities = Array.from(new Set(stations.map(s => s.city).filter(Boolean))).sort((a, b) => a.localeCompare(b, 'tr'));
    
    select.innerHTML = '<option value="all">Hızlı İl Seç (81 İl)...</option>' +
        cities.map(c => `<option value="${c}">${c}</option>`).join('');
}

function filterMapByRegion(region) {
    if (!mainMap) return;
    if (region === 'all') {
        zoomToTurkey();
        return;
    }
    const reg = TURKEY_REGIONS_MAP[region];
    if (reg) {
        mainMap.flyTo(reg.center, reg.zoom, { duration: 1.2 });
    }
}

function filterMapByCity(city) {
    if (!mainMap) return;
    if (city === 'all') {
        zoomToTurkey();
        return;
    }
    const match = stations.find(s => s.city === city);
    if (match) {
        mainMap.flyTo([match.latitude, match.longitude], 11, { duration: 1.2 });
        const marker = stationMarkers.find(m => m.stationData && m.stationData.id === match.id);
        if (marker) {
            setTimeout(() => marker.openPopup(), 1200);
        }
    }
}

function searchMapStations(query) {
    if (!mainMap) return;
    const q = query.trim().toLowerCase();
    if (!q) {
        stationMarkers.forEach(m => {
            if (m.getElement()) m.getElement().style.opacity = '1';
        });
        return;
    }

    let firstMatch = null;
    stationMarkers.forEach(m => {
        const s = m.stationData || {};
        const text = `${s.name || ''} ${s.city || ''} ${s.district || ''}`.toLowerCase();
        const el = m.getElement();
        if (text.includes(q)) {
            if (el) el.style.opacity = '1';
            if (!firstMatch) firstMatch = m;
        } else {
            if (el) el.style.opacity = '0.25';
        }
    });

    if (firstMatch) {
        mainMap.panTo(firstMatch.getLatLng());
        firstMatch.openPopup();
    }
}

function zoomToTurkey() {
    if (mainMap) {
        mainMap.flyTo([39.1, 35.2], 6, { duration: 1 });
        const regSelect = document.getElementById('mapRegionFilter');
        const citySelect = document.getElementById('mapCityFilter');
        if (regSelect) regSelect.value = 'all';
        if (citySelect) citySelect.value = 'all';
    }
}

function toggleDarkMapMode() {
    if (!mainMap) return;
    isDarkMap = !isDarkMap;
    const btn = document.getElementById('btnMapTheme');
    if (isDarkMap) {
        if (mainMap.hasLayer(standardLayer)) mainMap.removeLayer(standardLayer);
        darkLayer.addTo(mainMap);
        if (btn) btn.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        if (mainMap.hasLayer(darkLayer)) mainMap.removeLayer(darkLayer);
        standardLayer.addTo(mainMap);
        if (btn) btn.innerHTML = '<i class="fas fa-moon"></i>';
    }
}

function toggleMapRoutes() {
    routeLinesVisible = !routeLinesVisible;
    const btn = document.getElementById('btnToggleRoutes');
    if (btn) btn.classList.toggle('active', routeLinesVisible);

    routeLayers.forEach(layer => {
        if (routeLinesVisible) {
            if (!mainMap.hasLayer(layer)) mainMap.addLayer(layer);
        } else {
            if (mainMap.hasLayer(layer)) mainMap.removeLayer(layer);
        }
    });
}

function toggleVehicleSimulation() {
    const btn = document.getElementById('btnSimulate');
    if (simulationInterval) {
        clearInterval(simulationInterval);
        simulationInterval = null;
        if (simulationMarker && mainMap) mainMap.removeLayer(simulationMarker);
        simulationMarker = null;
        if (btn) {
            btn.classList.remove('active');
            btn.innerHTML = '<i class="fas fa-play"></i> Simülasyon';
        }
        return;
    }

    // Aktif simülasyon koordinatları yoksa ilk rotayı veya Türkiye omurgasını kullan
    if (!currentSimulationCoords || currentSimulationCoords.length === 0) {
        currentSimulationCoords = [
            [40.8225, 29.9213], [40.7654, 29.9408], [40.8027, 29.4307],
            [40.8767, 29.2344], [40.9927, 29.0277], [40.8167, 29.3000],
            [40.7731, 30.4028], [39.7767, 30.5206], [39.9208, 32.8541],
            [40.7731, 30.4028], [40.8225, 29.9213]
        ];
    }

    if (btn) {
        btn.classList.add('active');
        btn.innerHTML = '<i class="fas fa-stop"></i> Durdur';
    }

    const truckIcon = L.divIcon({
        className: 'sim-truck-marker',
        html: `
            <div style="position:relative; display:flex; flex-direction:column; align-items:center;">
                <div style="background:linear-gradient(135deg, #10b981, #047857); color:white; width:38px; height:38px; border-radius:50%; border:3px solid white; box-shadow:0 0 20px rgba(16,185,129,0.9); display:flex; align-items:center; justify-content:center; font-size:17px;">
                    <i class="fas fa-truck-fast"></i>
                </div>
                <div style="background:rgba(15,23,42,0.92); color:#4ade80; font-family:'Outfit',sans-serif; font-size:10px; font-weight:700; padding:2px 7px; border-radius:6px; margin-top:4px; white-space:nowrap; border:1px solid rgba(16,185,129,0.6); box-shadow:0 2px 8px rgba(0,0,0,0.4);">
                    <span id="simSpeedVal">86</span> km/s • Canlı Sevkiyat
                </div>
            </div>
        `,
        iconSize: [80, 56],
        iconAnchor: [40, 20]
    });

    let step = 0;
    simulationMarker = L.marker(currentSimulationCoords[0], { icon: truckIcon }).addTo(mainMap);

    simulationInterval = setInterval(() => {
        step = (step + 1) % currentSimulationCoords.length;
        const pos = currentSimulationCoords[step];
        simulationMarker.setLatLng(pos);
        const speedEl = document.getElementById('simSpeedVal');
        if (speedEl && step % 4 === 0) {
            speedEl.textContent = Math.floor(78 + Math.random() * 16);
        }
    }, 120);
}

async function showRoutesOnMap(map) {
    try {
        const res = await fetch('/api/routes');
        const routes = await res.json();

        routeLayers.forEach(l => {
            if (map.hasLayer(l)) map.removeLayer(l);
        });
        routeLayers = [];
        currentSimulationCoords = [];

        const elRoute = document.getElementById('hudRouteCount');
        if (elRoute) elRoute.textContent = routes.length;

        const recentRoutes = routes.slice(0, 8);

        for (let i = 0; i < recentRoutes.length; i++) {
            const route = recentRoutes[i];
            if (route.route_data) {
                let routeStations = [];
                try {
                    routeStations = typeof route.route_data === 'string' ? JSON.parse(route.route_data) : route.route_data;
                } catch(e) {
                    routeStations = route.route_names || [];
                }
                const color = routeColors[i % routeColors.length];
                await drawRoute(map, routeStations, color);
            }
        }
    } catch (err) {
        console.error('Rotalar yüklenemedi:', err);
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

            // 1. Dış Neon Parlama İzi (Glow Halo)
            const glowPolyline = L.polyline(coordinates, {
                color: color,
                weight: 11,
                opacity: 0.35,
                lineCap: 'round',
                lineJoin: 'round'
            }).addTo(map);

            // 2. Ana Otoyol Çizgisi (Crisp Highway Line)
            const mainPolyline = L.polyline(coordinates, {
                color: color,
                weight: 4.5,
                opacity: 0.95,
                lineCap: 'round',
                lineJoin: 'round'
            }).addTo(map);

            // 3. Karizmatik Hareketli Akış Efekti (Dynamic White Dash Flow)
            const flowPolyline = L.polyline(coordinates, {
                color: '#ffffff',
                weight: 2,
                opacity: 0.8,
                dashArray: '6, 15',
                lineCap: 'round'
            }).addTo(map);

            routeLayers.push(glowPolyline, mainPolyline, flowPolyline);

            if (currentSimulationCoords.length === 0) {
                currentSimulationCoords = coordinates;
            }
        }
    } catch (err) {
        console.error('Rota çizilemedi:', err);
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
        const cargoStations = stations.filter(s => !s.is_depot);
        select.innerHTML = cargoStations.map(s => `<option value="${s.id}">${s.name} (${s.city || ''})</option>`).join('');
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
    tbody.innerHTML = stations.map(s => {
        const isDepot = Boolean(s.is_depot);
        return `
        <tr>
            <td><strong>#${s.id}</strong></td>
            <td>
                <div style="display:flex; align-items:center; gap:8px;">
                    <i class="fas ${isDepot ? 'fa-warehouse text-danger' : 'fa-map-pin text-primary'}"></i>
                    <strong>${s.name}</strong>
                    ${isDepot ? '<span style="background:#fee2e2; color:#ef4444; font-size:10px; font-weight:700; padding:2px 6px; border-radius:10px;">ANA HUB</span>' : ''}
                </div>
            </td>
            <td>${s.latitude.toFixed(4)}</td>
            <td>${s.longitude.toFixed(4)}</td>
            <td>
                <button onclick="deleteStation(${s.id})" class="btn btn-danger btn-sm" title="İstasyonu Sil">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `}).join('');
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
                city: document.getElementById('stationCity') ? document.getElementById('stationCity').value : '',
                district: document.getElementById('stationDistrict') ? document.getElementById('stationDistrict').value : '',
                latitude: document.getElementById('stationLat').value,
                longitude: document.getElementById('stationLon').value,
                is_depot: document.getElementById('stationIsDepot') ? document.getElementById('stationIsDepot').checked : false
            })
        });

        const data = await res.json();

        if (data.success) {
            closeModal('stationModal');
            loadStations();
            alert('İstasyon başarıyla eklendi!');
        } else {
            alert(data.error || 'İstasyon eklenemedi');
        }
    } catch (err) {
        alert('Bağlantı hatası');
    }
}

async function deleteStation(id) {
    if (!confirm('Bu istasyonu silmek istediğinize emin misiniz?')) return;

    try {
        await fetch(`/api/stations/${id}`, { method: 'DELETE' });
        loadStations();
    } catch (err) {
        alert('Silme hatası');
    }
}

async function loadVehicles() {
    try {
        const res = await fetch('/api/vehicles');
        const vehicles = await res.json();

        const tbody = document.getElementById('vehiclesTable');
        tbody.innerHTML = vehicles.map(v => {
            const vType = v.type || 'medium_truck';
            const icon = v.icon || 'fa-truck';
            const cat = v.category || 'Standart Dağıtım';
            const vol = v.volume_m3 ? `${v.volume_m3} m³` : '-';
            const rental = v.rental_cost > 0 ? `${v.rental_cost} TL` : '0 TL (Özmal)';
            return `
            <tr>
                <td><strong style="color: #0f172a; font-weight:700;">#${v.id}</strong></td>
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <i class="fas ${icon}" style="color:${v.color || '#6366f1'}; font-size:18px;"></i>
                        <div>
                            <div style="color: #0f172a; font-weight:700; font-size: 14px;">${v.name}</div>
                            <div style="font-size:11px; color:#475569; margin-top:2px;">
                                ${v.plate ? `<span style="display:inline-block; background:#0f172a; color:#f8fafc; padding:1px 6px; border-radius:4px; font-weight:700; font-size:10px; letter-spacing:0.5px; margin-right:6px;">${v.plate}</span>` : ''}
                                <span>${v.description || ''}</span>
                            </div>
                        </div>
                    </div>
                </td>
                <td><span class="vehicle-type-badge vehicle-type-${vType}"><i class="fas ${icon}"></i> ${cat}</span></td>
                <td><strong style="color: #0f172a; font-weight: 700;">${v.capacity.toLocaleString('tr-TR')} kg</strong></td>
                <td style="color: #334155; font-weight: 500;">${vol}</td>
                <td><span style="color:#059669; font-weight:700; background:rgba(5,150,105,0.08); padding:3px 8px; border-radius:6px;">${v.fuel_consumption} TL/km</span></td>
                <td style="color: #334155; font-weight: 500;">${rental}</td>
                <td><span class="status ${v.is_owned ? 'status-assigned' : 'status-pending'}">${v.is_owned ? 'Özmal Filo' : 'Kiralık'}</span></td>
                <td>
                    <button onclick="deleteVehicle(${v.id})" class="btn btn-danger btn-sm" title="Aracı Sil"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `}).join('');
    } catch (err) {
        console.error('Araçlar yüklenemedi:', err);
    }
}

function onVehicleTypeChange(type) {
    const presets = {
        'courier': { cap: 50, vol: 0.3, fuel: 0.35, rental: 80, name: 'Moto Kurye - Honda CBF 150 (Express)' },
        'van': { cap: 400, vol: 4.2, fuel: 0.75, rental: 180, name: 'Panelvan - Fiat Doblo Maxi (Hafif Ticari)' },
        'light_truck': { cap: 1000, vol: 12.5, fuel: 1.15, rental: 280, name: 'Dağıtım Kamyoneti - Ford Transit 350L' },
        'medium_truck': { cap: 2500, vol: 28.0, fuel: 1.85, rental: 450, name: 'Bölgesel Kamyon - Isuzu NPR Long' },
        'heavy_truck': { cap: 6000, vol: 50.0, fuel: 3.10, rental: 750, name: 'Ağır Hizmet Kamyonu - Mercedes-Benz Axor' },
        'trailer': { cap: 15000, vol: 95.0, fuel: 4.60, rental: 1200, name: 'Mega Treyler TIR - Scania R450 Highline' }
    };
    const p = presets[type];
    if (p) {
        document.getElementById('vehicleName').value = p.name;
        document.getElementById('vehicleCapacity').value = p.cap;
        document.getElementById('vehicleVolume').value = p.vol;
        document.getElementById('vehicleFuel').value = p.fuel;
        document.getElementById('vehicleRentalCost').value = p.rental;
    }
}

function showVehicleModal() {
    document.getElementById('vehicleModal').classList.add('active');
}

async function handleAddVehicle(e) {
    e.preventDefault();

    try {
        const typeEl = document.getElementById('vehicleType');
        const res = await fetch('/api/vehicles', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: document.getElementById('vehicleName').value,
                type: typeEl ? typeEl.value : 'truck',
                category: typeEl ? typeEl.selectedOptions[0].text : 'Lojistik',
                capacity: parseInt(document.getElementById('vehicleCapacity').value),
                volume_m3: parseFloat(document.getElementById('vehicleVolume') ? document.getElementById('vehicleVolume').value : 10),
                fuel_consumption: parseFloat(document.getElementById('vehicleFuel').value),
                rental_cost: parseFloat(document.getElementById('vehicleRentalCost') ? document.getElementById('vehicleRentalCost').value : 0),
                is_owned: parseInt(document.getElementById('vehicleIsOwned') ? document.getElementById('vehicleIsOwned').value : 1)
            })
        });

        const data = await res.json();

        if (data.success) {
            closeModal('vehicleModal');
            loadVehicles();
            alert('Lojistik aracı başarıyla eklendi!');
        } else {
            alert(data.error || 'Araç eklenemedi');
        }
    } catch (err) {
        alert('Bağlantı hatası');
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
            html += `<tr style="${rowStyle}; color:#1e293b;">
                <td><input type="checkbox" class="cargo-checkbox" value="${c.id}" ${isChecked} onchange="updateCargoSelection(${c.id}, this.checked)"></td>
                <td><strong>#${c.id}</strong></td>
                <td><strong style="color:#0f172a;">${c.station_name}</strong></td>
                <td><strong>${c.weight} kg</strong></td>
                <td><span style="color:${statusColor}; font-weight:bold;">${statusText}</span></td>
                <td style="color:#475569;">${formattedDate}</td>
            </tr>`;
        });

        const totalWeight = allCargos.reduce((sum, c) => sum + c.weight, 0);
        html += `<tr style="font-weight:bold; background:#f1f5f9; color:#0f172a;"><td></td><td></td><td>TOPLAM</td><td>${totalWeight.toFixed(1)} kg</td><td>${pending.length} bekliyor / ${assigned.length} atandı</td><td>${allCargos.length} kargo</td></tr>`;
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
        optimizeMap = L.map('optimizeMap').setView([39.1, 35.2], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap'
        }).addTo(optimizeMap);
    }

    optimizeMap.eachLayer(layer => {
        if (layer instanceof L.Marker || layer instanceof L.Polyline) {
            optimizeMap.removeLayer(layer);
        }
    });

    stations.forEach(station => {
        const isDepot = Boolean(station.is_depot) || station.name.toLowerCase().includes('hub') || station.name.toLowerCase().includes('depo');
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background:${isDepot ? '#ef4444' : '#3b82f6'}; width:20px; height:20px; border-radius:50%; border:2px solid white; box-shadow:0 2px 5px rgba(0,0,0,0.3);"></div>`,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        L.marker([station.latitude, station.longitude], { icon })
            .bindPopup(`<b>${station.name}</b>${isDepot ? '<br><i style="color:#ef4444">Ana Lojistik Hub (Merkez Depo)</i>' : ''}`)
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
            const isDepot = station.is_depot || station.name.toLowerCase().includes('hub') || station.name.toLowerCase().includes('depo') || station.name.toLowerCase().includes('merkez');
            const icon = L.divIcon({
                className: 'custom-marker',
                html: `<div style="background:${isDepot ? '#ef4444' : '#10b981'}; width:22px; height:22px; border-radius:50%; border:2px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.3);"></div>`,
                iconSize: [22, 22],
                iconAnchor: [11, 11]
            });
            L.marker([station.latitude, station.longitude], { icon })
                .bindPopup(`<b>${station.name}</b>${isDepot ? '<br><i style="color:#ef4444; font-weight:600;">Ana Lojistik Hub (Merkez)</i>' : '<br><i style="color:#10b981; font-weight:600;">Dağıtım Noktası</i>'}`)
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
                <div style="background:#ef4444; width:12px; height:12px; border-radius:50%;"></div>
                <span style="font-size:12px;">Varış (Ana Lojistik Hub)</span>
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

async function loadPresetScenario() {
    const scenarioNum = document.getElementById('scenarioSelect').value || '1';
    const scenario = scenarios[scenarioNum];
    if (!scenario) {
        alert('Lütfen geçerli bir senaryo seçin.');
        return;
    }

    try {
        const res = await fetch('/api/load-scenario', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                scenario: scenario,
                scenario_num: parseInt(scenarioNum)
            })
        });

        const data = await res.json();
        if (data.success) {
            alert(`Senaryo ${scenarioNum} başarıyla yüklendi! (${data.cargo_count} adet bekleyen kargo oluşturuldu)`);
            loadPendingCargos();
        } else {
            alert(data.error || 'Senaryo yüklenemedi');
        }
    } catch (err) {
        alert('Bağlantı hatası oluştu');
    }
}

async function generateRandomCargos(count = 15) {
    if (!stations || stations.length === 0) {
        await loadStationsData();
    }
    const nonDepotStations = stations.filter(s => !s.is_depot);
    if (nonDepotStations.length === 0) {
        alert('İstasyon bulunamadı!');
        return;
    }

    let added = 0;
    for (let i = 0; i < count; i++) {
        const randStation = nonDepotStations[Math.floor(Math.random() * nonDepotStations.length)];
        const randWeight = Math.floor(Math.random() * 300) + 20; // 20kg - 320kg
        try {
            await fetch('/api/cargos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    station_id: randStation.id,
                    weight: randWeight
                })
            });
            added++;
        } catch (e) {
            console.error('Kargo ekleme hatası:', e);
        }
    }

    alert(`${added} adet rastgele Türkiye içi kargo oluşturuldu ve planlama listesine eklendi!`);
    loadPendingCargos();
}

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
            alert(data.error || 'Karşılaştırma yapılamadı');
            return;
        }

        displayComparisonResults(data.comparison, problemType, `Senaryo ${scenarioNum}`);
    } catch (err) {
        alert('Bağlantı hatası');
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
                const isDepot = Boolean(station.is_depot) || stationName.toLowerCase().includes('hub') || stationName.toLowerCase().includes('depo');
                const isStart = i === 0;
                const isEnd = i === routeStations.length - 1;

                let markerColor = '#3498db';
                if (isDepot) markerColor = '#ef4444';
                else if (isStart) markerColor = '#10b981';

                const icon = L.divIcon({
                    className: 'custom-marker',
                    html: `<div style="background:${markerColor}; width:24px; height:24px; border-radius:50%; border:3px solid white; box-shadow:0 2px 5px rgba(0,0,0,0.3); display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:12px;">${i + 1}</div>`,
                    iconSize: [24, 24],
                    iconAnchor: [12, 12]
                });

                L.marker([station.latitude, station.longitude], { icon })
                    .bindPopup(`<b>${i + 1}. ${station.name}</b>${isStart ? '<br><i style="color:#10b981">Başlangıç</i>' : (isDepot ? '<br><i style="color:#ef4444">Varış (Ana Lojistik Hub)</i>' : '')}`)
                    .addTo(routeModalMap);
            }
        }

        await drawRoute(routeModalMap, routeStations, color || '#27ae60');

        routeModalMap.invalidateSize();
    }, 200);
}

