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
                successDiv.querySelector('span').textContent = data.message || 'Doğrulama kodu oluşturuldu!';
            }
            if (data.code) {
                const resetCodeInput = document.getElementById('resetCode');
                if (resetCodeInput) resetCodeInput.value = data.code;
            }
            setTimeout(() => {
                showResetPasswordForm();
            }, 1200);
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

        if (stats.market_info) {
            updateMarketUI(stats.market_info);
        }

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
    const mainEl = document.getElementById('mainMap');
    const optEl = document.getElementById('optimizeMap');
    const btn = document.getElementById('btnMapTheme');

    if (isDarkMap) {
        if (mainEl) mainEl.classList.add('dark-map-tiles');
        if (optEl) optEl.classList.add('dark-map-tiles');
        if (btn) btn.innerHTML = '<i class="fas fa-sun theme-sun-icon" id="themeIcon"></i>';
    } else {
        if (mainEl) mainEl.classList.remove('dark-map-tiles');
        if (optEl) optEl.classList.remove('dark-map-tiles');
        if (btn) btn.innerHTML = '<i class="fas fa-moon theme-moon-icon" id="themeIcon"></i>';
    }
}

// ==========================================
// CANLI AKARYAKIT VE BRENT PETROL PİYASA MASASI
// ==========================================
let fuelMarketCheckIntervalId = null;

async function triggerMarketFuelCheck() {
    const btn = document.getElementById('btnCheckFuel') || document.getElementById('btnMarketScan');
    if (btn) {
        btn.classList.add('scanning');
        btn.disabled = true;
    }

    try {
        const intervalSelect = document.getElementById('fuelCheckInterval') || document.getElementById('marketFuelInterval');
        const intervalHours = intervalSelect ? parseInt(intervalSelect.value) : 12;

        const res = await fetch('/api/market-fuel-check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ interval_hours: intervalHours })
        });
        const data = await res.json();

        if (data.success && data.market_info) {
            updateMarketUI(data.market_info);
            if (data.fuel_prices) {
                const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
                setEl('tickerDiesel', `${data.fuel_prices.diesel_per_liter?.toFixed(2) || '92.50'} TL/L`);
                setEl('tickerGasoline', `${data.fuel_prices.gasoline_per_liter?.toFixed(2) || '85.50'} TL/L`);
                setEl('tickerAdblue', `${data.fuel_prices.adblue_per_liter?.toFixed(2) || '36.50'} TL/L`);
            }
            alert(`⛽ Brent Petrol ve Akaryakıt Piyasası Güncellendi!\n\n• Brent Petrol: $${data.market_info.brent_barrel_usd} / varil (${data.market_info.brent_change_pct >= 0 ? '+' : ''}${data.market_info.brent_change_pct}%)\n• Dolar Kuru: ₺${data.market_info.usd_try}\n• Yeni Motorin: ₺${data.fuel_prices.diesel_per_liter} / L\n• Yeni Benzin: ₺${data.fuel_prices.gasoline_per_liter} / L\n• Durum: ${data.market_info.geopolitical_note}`);
        }
    } catch(err) {
        console.error('Market tarama hatası:', err);
    } finally {
        if (btn) {
            btn.classList.remove('scanning');
            btn.disabled = false;
        }
    }
}

function updateMarketUI(market) {
    if (!market) return;
    const brentVal = document.getElementById('brentPriceVal') || document.getElementById('hudBrentVal');
    const brentChange = document.getElementById('brentTrendVal') || document.getElementById('hudBrentChange');
    const lastCheckDateTime = document.getElementById('lastFuelCheckDateTime');

    if (brentVal && market.brent_barrel_usd) {
        brentVal.textContent = `$${market.brent_barrel_usd}`;
    }
    if (brentChange && market.brent_change_pct !== undefined) {
        const isPos = market.brent_change_pct >= 0;
        brentChange.textContent = `${isPos ? '▲ +' : '▼ '}${market.brent_change_pct}%`;
        brentChange.className = `trend-badge ${isPos ? 'trend-up' : 'trend-down'}`;
    }
    if (lastCheckDateTime) {
        const now = new Date();
        const dateStr = now.toLocaleDateString('tr-TR');
        const timeStr = market.last_updated ? market.last_updated.substring(0, 5) : now.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
        lastCheckDateTime.textContent = `${dateStr} ${timeStr}`;
    }
}

function setFuelInterval(hours) {
    if (fuelMarketCheckIntervalId) {
        clearInterval(fuelMarketCheckIntervalId);
        fuelMarketCheckIntervalId = null;
    }
    const h = parseInt(hours) || 12;
    console.log(`[Akaryakıt Masası] Otomatik tarama periyodu: ${h} saat.`);
    fuelMarketCheckIntervalId = setInterval(() => {
        triggerMarketFuelCheck();
    }, h * 60 * 60 * 1000);
}

// =========================================================================
// 14 TÜRKİYE LOJİSTİK KORİDORU & GERÇEKÇİ OTOYOL SİMÜLASYONU ENGINE
// =========================================================================
const CURATED_SCENARIOS = {
    marmara_d100: {
        title: 'Marmara Bölgesel Ring (D-100 & D-130 Sahil)',
        vehicle: 'Fiat Doblo Maxi Panelvan',
        plate: '34 KRG 102',
        fleetText: '1x Doblo Maxi Panelvan',
        costText: '₺1.420 TL',
        etaText: '03 sa 15 dk',
        etaMinutes: 195,
        totalDistance: 178,
        cargoText: '380 kg / 24 Koli',
        tollText: '0 TL (Ücretsiz D-100)',
        fuelText: '7.8 L/100km (~14 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-100 / E-5 (Ücretsiz Sahil)',
        speedRange: [65, 82],
        rpmRange: [2100, 2400],
        weather: {"text": "D-100 Körfez: Yağmurlu (14°C)", "icon": "fa-cloud-rain", "rain": true},
        savingsText: '🌱 38 kg CO₂ • ₺550 Köprü Gişe Tasarrufu',
        tachoRemain: '02 sa 45 dk',
        uetdsCode: 'UETDS-2026-TR-418029',
        driver: 'Mustafa Çelik (SRC-4: TR-34-99120)',
        incident: {
            title: 'D-100 Hereke Geçişi: Zincirleme Kaza & Kilit',
            headline: 'D-100 HEREKE: ZİNCİRLEME KAZA & KİLİT',
            subText: 'Sahil Yolu Çift Şerit Kapalı • +40 Dk Bekleme',
            delayMinutes: 40,
            blockedPoint: [40.7890, 29.5400],
            bypassTitle: 'Kuzey Marmara Otoyolu (KMO) Kaçış Rotası (32 Dk Kazanç)',
            savingsInfo: '⚡ 32 dk süre kurtarıldı • Akıcı KMO Transit Geçiş',
            alternativeBadge: 'KMO Kuzey Marmara Kaçış Hattı',
            triggerStepRatio: 0.28
        },
        alternativePath: [
            [40.8027, 29.4307], // Gebze KMO Bağlantısı
            [40.8500, 29.6200], // KMO Sevindikli Viyadüğü
            [40.8300, 29.8200], // KMO İzmit Batı Kavşağı
            [40.7654, 29.9408], // Kocaeli / İzmit Dağıtım Hub
            [40.7100, 29.9300], // Başiskele
            [40.6552, 29.2769], // Yalova
            [40.1885, 29.0610]  // Bursa
        ],
        path: [
            [40.9927, 29.0277], // İstanbul Kadıköy Transfer
            [40.8767, 29.2344], // Pendik D-100
            [40.8167, 29.3000], // Tuzla D-100
            [40.8027, 29.4307], // Gebze Lojistik Hub
            [40.7890, 29.5400], // Dilovası D-100
            [40.7750, 29.7500], // Körfez Sahil Yolu
            [40.7654, 29.9408], // Kocaeli / İzmit Dağıtım Hub
            [40.7100, 29.9300], // Başiskele D-130
            [40.7180, 29.8200], // Gölcük D-130
            [40.6900, 29.6150], // Karamürsel Sahil
            [40.6700, 29.5000], // Altınova D-575
            [40.6552, 29.2769], // Yalova Merkez Depo
            [40.5000, 29.3000], // Süpürgelik Geçidi
            [40.4200, 29.3000], // Orhangazi
            [40.3200, 29.2200], // Gemlik Sanayi
            [40.2400, 29.1300], // Ovaakça
            [40.1885, 29.0610]  // Bursa Nilüfer Hub
        ]
    },
    ege_osmangazi: {
        title: 'Ege Otoyol Ekspres (Osmangazi Köprüsü & O-5)',
        vehicle: 'Mercedes-Benz Actros 1845 Çekici TIR',
        plate: '35 LOG 770',
        fleetText: '1x Actros 1845 Çekici TIR',
        costText: '₺7.850 TL',
        etaText: '04 sa 45 dk',
        etaMinutes: 285,
        totalDistance: 480,
        cargoText: '14.500 kg / 12 Palet',
        tollText: '₺1.150 TL (Osmangazi & O-5)',
        fuelText: '29.5 L/100km (~142 L)',
        roadType: 'otoyol',
        roadBadge: 'O-5 Otoyolu & Osmangazi Köprüsü',
        speedRange: [88, 98],
        rpmRange: [1300, 1500],
        weather: {"text": "Osmangazi & Susurluk: Rüzgarlı (17°C)", "icon": "fa-wind", "rain": false},
        savingsText: '⚡ Otoyol Ekspres: 2 sa 15 dk Zaman Kazanımı',
        tachoRemain: '03 sa 10 dk',
        uetdsCode: 'UETDS-2026-TR-354921',
        driver: 'Barış Demir (SRC-4: TR-35-77291)',
        incident: {
            title: 'O-5 Susurluk Rampaları: Ağır Vasıta Devrilmesi',
            headline: 'O-5 SUSURLUK VARYANTI: KAZA & TIKANIKLIK',
            subText: 'Tek Şerit Kapalı • 7 km Ağır Vasıta Kuyruğu (+45 Dk)',
            delayMinutes: 45,
            blockedPoint: [39.9120, 28.1600],
            bypassTitle: 'Bandırma-Balıkesir D-565 Kaçış Hattı (36 Dk Kazanç)',
            savingsInfo: '⚡ 36 dk süre kurtarıldı • ₺220 TL Rölanti Tasarrufu',
            alternativeBadge: 'D-565 Bandırma Alternatif Koridoru',
            triggerStepRatio: 0.38
        },
        alternativePath: [
            [40.1885, 29.0610], // Bursa
            [40.0000, 28.7000], // Karacabey Ayrımı
            [40.1000, 28.2500], // D-565 Bandırma Yolu (Bypass)
            [39.7500, 28.0500], // Manyas-Balıkesir Devlet Yolu
            [39.6484, 27.8826], // Balıkesir Merkez
            [39.3000, 27.7000], // Soma
            [39.1200, 27.5000], // Akhisar
            [38.6191, 27.4289], // Manisa
            [38.4192, 27.1287]  // İzmir
        ],
        path: [
            [41.0082, 28.9784], // İstanbul Avrupa Hub
            [40.9927, 29.0277], // Kadıköy
            [40.8027, 29.4307], // Gebze Otoyol
            [40.7600, 29.5130], // Osmangazi Köprüsü Kuzey Gişeleri
            [40.7450, 29.5150], // Osmangazi Köprüsü Asma Kuleler
            [40.7300, 29.5180], // Osmangazi Köprüsü Güney Gişeleri
            [40.6552, 29.2769], // Yalova Otoyol Bağlantısı
            [40.1885, 29.0610], // Bursa Batı Çevre Otoyolu
            [40.0000, 28.7000], // Karacabey Kavşağı
            [39.6484, 27.8826], // Balıkesir O-5
            [39.3000, 27.7000], // Soma Kavşağı
            [39.1200, 27.5000], // Akhisar Çevre Otoyolu
            [38.6191, 27.4289], // Manisa Hub
            [38.5000, 27.2500], // Sabuncubeli Tüneli
            [38.4192, 27.1287]  // İzmir Bornova Ana Dağıtım Merkezi
        ]
    },
    baskent_anadolu: {
        title: 'Başkent D-100 Anadolu Koridoru (Bolu Dağı Geçidi)',
        vehicle: 'Isuzu NPR Long Kamyon',
        plate: '06 TR 1923',
        fleetText: '1x Isuzu NPR Kamyon',
        costText: '₺4.280 TL',
        etaText: '06 sa 20 dk',
        etaMinutes: 380,
        totalDistance: 452,
        cargoText: '2.400 kg / 85 Koli',
        tollText: '0 TL (Ücretsiz D-100)',
        fuelText: '21.0 L/100km (~95 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-100 Devlet Yolu (0 TL Geçiş)',
        speedRange: [62, 76],
        rpmRange: [1950, 2250],
        weather: {"text": "Bolu Dağı: -2°C Kar & Yoğun Sis", "icon": "fa-snowflake", "rain": true},
        savingsText: '🌱 45 kg CO₂ • ₺420 Otoyol Gişe Tasarrufu',
        tachoRemain: '01 sa 50 dk (Mola Yaklaşıyor)',
        uetdsCode: 'UETDS-2026-TR-061942',
        driver: 'Hasan Kurt (SRC-4: TR-06-88124)',
        incident: {
            title: 'O-4 Bolu Dağı Tüneli: 3 Araçlı Zincirleme Kaza',
            headline: 'O-4 BOLU DAĞI TÜNELİ: ZİNCİRLEME KAZA',
            subText: 'Otoyol Çift Şerit Kapalı • +55 Dk Bekleme & Tüketim',
            delayMinutes: 55,
            blockedPoint: [40.7350, 31.5500],
            bypassTitle: 'D-100 Dağ Geçidi Serbest (42 Dk Kazanç)',
            savingsInfo: '⚡ 42 dk süre kurtarıldı • ₺190 TL Yakıt Tasarrufu',
            alternativeBadge: 'D-100 Eski Dağ Geçidi Bypass',
            triggerStepRatio: 0.35
        },
        alternativePath: [
            [40.8438, 31.1565], // Düzce Merkez
            [40.7400, 31.4500], // Kaynaşlı Sapağı
            [40.7100, 31.4850], // D-100 Eski Dağ Yolu Girişi (Bypass)
            [40.6900, 31.5400], // Abant Kavşağı Yan Yolu
            [40.7100, 31.5900], // Bolu Güney Çevre Yolu
            [40.7350, 31.6080], // Bolu Merkez (Bağlantı)
            [40.7600, 32.2000], // Gerede Kavşağı
            [40.4000, 32.5500], // Kızılcahamam
            [40.1000, 32.6500], // Kahramankazan
            [39.9334, 32.8597]  // Ankara Ana Lojistik Hub
        ],
        path: [
            [41.0082, 28.9784], // İstanbul
            [40.8027, 29.4307], // Gebze D-100
            [40.7654, 29.9408], // Kocaeli Hub
            [40.7731, 30.4028], // Sakarya / Adapazarı
            [40.7500, 30.7500], // Hendek D-100
            [40.8438, 31.1565], // Düzce Merkez
            [40.7400, 31.4500], // Kaynaşlı - Bolu Dağı Eteği
            [40.7350, 31.5500], // Bolu Dağı Geçidi D-100 Zirve
            [40.7350, 31.6080], // Bolu Merkez
            [40.7600, 32.2000], // Gerede Kavşağı
            [40.4000, 32.5500], // Kızılcahamam D-750
            [40.1000, 32.6500], // Kahramankazan
            [39.9334, 32.8597]  // Ankara Ana Lojistik Hub
        ]
    },
    akdeniz_afyon_antalya: {
        title: 'Akdeniz Sevkiyat Koridoru (D-650 & D-685 Göller)',
        vehicle: 'Ford Transit Kamyonet (2 Araç Konvoy)',
        plate: '41 KRG 045 • 41 KRG 046',
        fleetText: '2x Ford Transit (Konvoy)',
        costText: '₺5.650 TL (Toplam)',
        etaText: '07 sa 30 dk',
        etaMinutes: 450,
        totalDistance: 560,
        cargoText: '1.950 kg / 60 Koli',
        tollText: '0 TL (Devlet Yolu)',
        fuelText: '11.5 L/100km (~64 L/araç)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-650 & D-685 Göller Hattı',
        speedRange: [65, 80],
        rpmRange: [2000, 2300],
        weather: {"text": "Çubuk Boğazı: Açık & Güneşli (24°C)", "icon": "fa-sun", "rain": false},
        savingsText: '🌱 52 kg CO₂ • 2 Araç Filo Optimizasyonu',
        tachoRemain: '02 sa 15 dk',
        uetdsCode: 'UETDS-2026-TR-074128',
        driver: 'Emre Koç & Murat Ak (SRC-4 Konvoy)',
        path: [
            [40.7654, 29.9408], // Kocaeli Hub
            [40.5000, 30.1500], // Pamukova
            [40.1400, 29.9800], // Bilecik Merkez
            [39.9000, 30.0300], // Bozüyük
            [39.4200, 29.9800], // Kütahya
            [38.7507, 30.5567], // Afyonkarahisar Hub
            [38.4700, 30.2700], // Sandıklı
            [37.9500, 30.2200], // Keçiborlu
            [37.7200, 30.2800], // Burdur Merkez
            [37.2000, 30.5000], // Çubuk Boğazı
            [36.8969, 30.7133]  // Antalya Kepez Dağıtım Hub
        ]
    },
    trakya_sanayi: {
        title: 'Trakya Sanayi & İhracat Koridoru (O-3 & D-100)',
        vehicle: 'Scania R450 Streamline TIR',
        plate: '34 IHR 88',
        fleetText: '1x Scania R450 TIR',
        costText: '₺3.450 TL',
        etaText: '03 sa 10 dk',
        etaMinutes: 190,
        totalDistance: 245,
        cargoText: '12.000 kg / 18 Palet',
        tollText: '₺180 TL (O-3 Otoyolu)',
        fuelText: '31.5 L/100km (~77 L)',
        roadType: 'otoyol',
        roadBadge: 'O-3 & D-100 Avrupa Hattı',
        speedRange: [85, 95],
        rpmRange: [1200, 1400],
        weather: {"text": "Çorlu & Kapıkule: Sisli (11°C)", "icon": "fa-smog", "rain": false},
        savingsText: '⚡ Uluslararası İhracat Gümrük Koridoru',
        tachoRemain: '03 sa 30 dk',
        uetdsCode: 'UETDS-2026-TR-220194',
        driver: 'Kemal Güneş (SRC-3 & SRC-4 Uluslararası)',
        path: [
            [41.0082, 28.9784], // İstanbul
            [41.0800, 28.7800], // İkitelli OSB
            [41.1400, 28.4600], // Çatalca
            [41.2800, 27.9900], // Çerkezköy OSB
            [41.1600, 27.8000], // Çorlu
            [40.9833, 27.5167], // Tekirdağ Merkez
            [41.4000, 27.3500], // Lüleburgaz
            [41.4300, 27.0900], // Babaeski
            [41.6772, 26.5557]  // Edirne Kapıkule Lojistik Hub
        ]
    },
    cukurova_toroslar: {
        title: 'Çukurova - Toroslar Ağır Vasıta Hattı (Pozantı Boğazı)',
        vehicle: 'Mercedes Axor 1840 TIR (2 Araç Konvoy)',
        plate: '06 LOG 01 • 06 LOG 02',
        fleetText: '2x Axor 1840 TIR (Konvoy)',
        costText: '₺9.200 TL (2 TIR Toplam)',
        etaText: '06 sa 50 dk',
        etaMinutes: 410,
        totalDistance: 530,
        cargoText: '22.000 kg (Konteyner Yükü)',
        tollText: '₺320 TL (O-21 Otoyolu)',
        fuelText: '33.0 L/100km (~175 L/TIR)',
        roadType: 'otoyol',
        roadBadge: 'D-750 & O-21 Anadolu Otoyolu',
        speedRange: [80, 92],
        rpmRange: [1350, 1550],
        weather: {"text": "Pozantı Boğazı: Serin Rüzgar (16°C)", "icon": "fa-wind", "rain": false},
        savingsText: '🌱 Ağır Vasıta Konvoy Optimizasyonu',
        tachoRemain: '02 sa 05 dk',
        uetdsCode: 'UETDS-2026-TR-018247',
        driver: 'Ahmet Şahin & Ali Kaya (SRC-4 Konvoy)',
        path: [
            [39.9334, 32.8597], // Ankara Hub
            [39.7800, 32.8000], // Gölbaşı
            [39.4000, 33.1000], // Kulu Kavşağı
            [38.8600, 33.5300], // Şereflikoçhisar
            [38.4025, 33.4147], // Aksaray - Eskil Dağıtım Şubesi (Düzeltilen Konum!)
            [38.3687, 34.0370], // Aksaray OSB
            [37.9667, 34.6833], // Niğde
            [37.5400, 34.4800], // Ulukışla
            [37.2500, 34.8700], // Pozantı Boğazı Geçidi
            [36.9167, 34.8950], // Tarsus
            [36.8000, 34.6300], // Mersin Liman Hub
            [37.0000, 35.3213]  // Adana Seyhan Hub
        ]
    },
    karadeniz_sahil: {
        title: 'Karadeniz Sahil Yolu Ekspresi (D-010 Koridoru)',
        vehicle: 'Isuzu NPR Long Kamyon',
        plate: '55 SAMSUN 01',
        fleetText: '1x Isuzu NPR Kamyon',
        costText: '₺4.800 TL',
        etaText: '05 sa 40 dk',
        etaMinutes: 340,
        totalDistance: 390,
        cargoText: '2.200 kg / 72 Koli',
        tollText: '0 TL (Devlet Yolu)',
        fuelText: '20.5 L/100km (~80 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-010 Sahil Yolu (0 TL Geçiş)',
        speedRange: [68, 82],
        rpmRange: [1900, 2200],
        weather: {"text": "Karadeniz Sahil: Sağanak Yağış (13°C)", "icon": "fa-cloud-showers-heavy", "rain": true},
        savingsText: '🌱 48 kg CO₂ • 0 TL Devlet Sahil Yolu',
        tachoRemain: '02 sa 50 dk',
        uetdsCode: 'UETDS-2026-TR-554109',
        driver: 'Zafer Aydın (SRC-4: TR-55-12048)',
        path: [
            [41.2867, 36.33],   // Samsun Liman Hub
            [41.1300, 36.7200], // Çarşamba
            [41.0900, 37.0400], // Terme
            [41.1300, 37.2800], // Ünye
            [41.0300, 37.5000], // Fatsa
            [40.9839, 37.8764], // Ordu Merkez
            [40.9128, 38.3895], // Giresun
            [41.0000, 38.8200], // Tirebolu
            [41.0027, 39.7168], // Trabzon Liman Hub
            [41.0201, 40.5234], // Rize
            [41.4000, 41.4300]  // Hopa Sınır Terminali
        ]
    },
    guneydogu_sanayi: {
        title: 'Güneydoğu Sanayi & Lojistik Arter Koridoru',
        vehicle: 'Scania R500 V8 TIR',
        plate: '27 ANTEP 99',
        fleetText: '1x Scania R500 V8 TIR',
        costText: '₺6.900 TL',
        etaText: '06 sa 15 dk',
        etaMinutes: 375,
        totalDistance: 495,
        cargoText: '15.000 kg (Sanayi Mamulü)',
        tollText: '₺160 TL (O-52 Otoyolu)',
        fuelText: '33.5 L/100km (~165 L)',
        roadType: 'otoyol',
        roadBadge: 'O-52 & D-400 İpekyolu Hattı',
        speedRange: [82, 95],
        rpmRange: [1250, 1450],
        weather: {"text": "Gaziantep OSB: Açık & Kuru Zemin (26°C)", "icon": "fa-sun", "rain": false},
        savingsText: '🌱 60 kg CO₂ • Sanayi Ağır Transit',
        tachoRemain: '03 sa 45 dk',
        uetdsCode: 'UETDS-2026-TR-270381',
        driver: 'Mehmet Polat (SRC-4: TR-27-99412)',
        path: [
            [37.0000, 35.3213], // Adana
            [37.0300, 35.8100], // Ceyhan
            [37.0742, 36.2478], // Osmaniye
            [37.1800, 36.7300], // Nurdağı
            [37.0662, 37.3833], // Gaziantep OSB Hub
            [37.0300, 37.9900], // Birecik
            [37.1591, 38.7969], // Şanlıurfa Hub
            [37.2300, 39.7600], // Viranşehir
            [37.1900, 40.5800], // Kızıltepe
            [37.3212, 40.7245]  // Mardin Lojistik Hub
        ]
    },
    dogu_anadolu_arter: {
        title: 'Doğu Anadolu Ana Arter Koridoru (D-200 & D-100)',
        vehicle: 'Mercedes Axor 1840 Ağır Vasıta',
        plate: '25 DADAŞ 01',
        fleetText: '1x Axor 1840 Ağır Vasıta',
        costText: '₺11.400 TL',
        etaText: '10 sa 30 dk',
        etaMinutes: 630,
        totalDistance: 875,
        cargoText: '11.500 kg / 10 Palet',
        tollText: '0 TL (Devlet Yolu)',
        fuelText: '30.0 L/100km (~260 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-200 & D-100 Doğu Arter',
        speedRange: [65, 80],
        rpmRange: [1400, 1600],
        weather: {"text": "Refahiye & Kızıldağ: 3°C Sis & Kırağı", "icon": "fa-snowflake", "rain": true},
        savingsText: '🌱 75 kg CO₂ • D-100 Ana Doğu Transit',
        tachoRemain: '01 sa 30 dk (Mola Önerilir)',
        uetdsCode: 'UETDS-2026-TR-250819',
        driver: 'İsmail Dadaş (SRC-4: TR-25-33418)',
        path: [
            [39.9334, 32.8597], // Ankara Hub
            [39.8600, 33.5100], // Kırıkkale
            [39.8181, 34.8147], // Yozgat
            [39.7100, 35.1800], // Sorgun
            [39.7477, 37.0179], // Sivas Hub
            [39.8900, 37.7500], // Zara
            [39.7500, 38.7700], // Refahiye
            [39.7500, 39.5000], // Erzincan Merkez
            [39.9200, 40.7000], // Aşkale
            [39.9000, 41.2700]  // Erzurum Palandöken Hub
        ]
    },
    guney_ege_bodrum: {
        title: 'Güney Ege Turizm & Dağıtım Ringi',
        vehicle: 'Ford Transit 350L Kamyonet',
        plate: '48 BDR 007',
        fleetText: '1x Ford Transit 350L',
        costText: '₺3.600 TL',
        etaText: '04 sa 50 dk',
        etaMinutes: 290,
        totalDistance: 365,
        cargoText: '950 kg / 40 Koli',
        tollText: '₺45 TL (Aydın Otoyolu)',
        fuelText: '11.2 L/100km (~41 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-550 & D-330 Ege Turizm',
        speedRange: [70, 85],
        rpmRange: [2050, 2350],
        weather: {"text": "Bodrum & Yatağan: Güneşli (25°C)", "icon": "fa-sun", "rain": false},
        savingsText: '🌱 32 kg CO₂ • Ege Bölgesel Dağıtım',
        tachoRemain: '03 sa 15 dk',
        uetdsCode: 'UETDS-2026-TR-480921',
        driver: 'Caner Öz (SRC-4: TR-48-55291)',
        path: [
            [38.4192, 27.1287], // İzmir Bornova Hub
            [38.1500, 27.3600], // Torbalı
            [37.9500, 27.3700], // Selçuk
            [37.8560, 27.8416], // Aydın Merkez
            [37.9100, 28.3200], // Nazilli
            [37.7765, 29.0864], // Denizli Hub
            [37.2153, 28.3636], // Muğla Merkez
            [37.3400, 28.1400], // Yatağan
            [37.3100, 27.7800], // Milas
            [37.0344, 27.4305]  // Bodrum Yalıkavak Dağıtım Şubesi
        ]
    },
    icanadolu_sanayi_ring: {
        title: 'İç Anadolu Sanayi & Tahıl Ringi',
        vehicle: 'Isuzu NPR Long Kamyon',
        plate: '42 KNY 100',
        fleetText: '1x Isuzu NPR Kamyon',
        costText: '₺5.100 TL',
        etaText: '06 sa 45 dk',
        etaMinutes: 405,
        totalDistance: 510,
        cargoText: '2.450 kg (Sanayi & Tahıl)',
        tollText: '0 TL (Devlet Yolu)',
        fuelText: '20.5 L/100km (~104 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-715 & D-350 Ova Hattı',
        speedRange: [65, 78],
        rpmRange: [1950, 2200],
        weather: {"text": "Konya Ovası: Rüzgarlı & Kuru (19°C)", "icon": "fa-wind", "rain": false},
        savingsText: '🌱 44 kg CO₂ • 0 TL Ova Devlet Yolu',
        tachoRemain: '02 sa 20 dk',
        uetdsCode: 'UETDS-2026-TR-420194',
        driver: 'Süleyman Çelik (SRC-4: TR-42-88192)',
        path: [
            [39.9334, 32.8597], // Ankara Hub
            [39.5500, 33.1200], // Bala
            [39.0900, 33.0800], // Kulu
            [38.6500, 32.9200], // Cihanbeyli
            [37.8667, 32.4833], // Konya Selçuklu OSB Hub
            [37.1759, 33.2287], // Karaman OSB
            [37.5100, 34.0500], // Ereğli
            [37.9667, 34.6833], // Niğde
            [38.6244, 34.7144]  // Nevşehir Kapadokya Hub
        ]
    },
    bati_karadeniz_maden: {
        title: 'Batı Karadeniz Maden & Demir-Çelik Hattı',
        vehicle: 'Mercedes Axor 1840 Ağır Vasıta',
        plate: '67 ZNG 067',
        fleetText: '1x Axor 1840 Ağır Vasıta',
        costText: '₺4.400 TL',
        etaText: '05 sa 20 dk',
        etaMinutes: 320,
        totalDistance: 380,
        cargoText: '8.500 kg (Ağır Sanayi)',
        tollText: '0 TL (Devlet Yolu)',
        fuelText: '29.5 L/100km (~112 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-010 & D-750 Dağ Koridoru',
        speedRange: [60, 75],
        rpmRange: [1450, 1650],
        weather: {"text": "Mengen & Devrek: Yağmurlu (12°C)", "icon": "fa-cloud-rain", "rain": true},
        savingsText: '🌱 40 kg CO₂ • Maden & KARDEMİR Hattı',
        tachoRemain: '02 sa 35 dk',
        uetdsCode: 'UETDS-2026-TR-670412',
        driver: 'Recep Maden (SRC-4: TR-67-11029)',
        path: [
            [40.7654, 29.9408], // Kocaeli Hub
            [40.7731, 30.4028], // Sakarya
            [40.8438, 31.1565], // Düzce
            [40.7350, 31.6080], // Bolu
            [40.9800, 32.0500], // Mengen
            [41.2200, 31.9500], // Devrek
            [41.4564, 31.7987], // Zonguldak Liman Hub
            [41.6344, 32.3375], // Bartın
            [41.2061, 32.6276]  // Karabük KARDEMİR Hub
        ]
    },
    ipekyolu_zigana: {
        title: 'Tarihi İpek Yolu & Yeni Zigana Tüneli Koridoru',
        vehicle: 'Isuzu NPR Long Kamyon',
        plate: '61 TRB 061',
        fleetText: '1x Isuzu NPR Kamyon',
        costText: '₺3.250 TL',
        etaText: '03 sa 45 dk',
        etaMinutes: 225,
        totalDistance: 260,
        cargoText: '2.100 kg (Deniz Kargo & Transit)',
        tollText: '0 TL (Devlet Yolu)',
        fuelText: '22.0 L/100km (~57 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-885 Dağ Geçidi & Yeni Tünel',
        speedRange: [60, 74],
        rpmRange: [2000, 2300],
        weather: {"text": "Yeni Zigana Tüneli: Tünel İçi Kuru (15°C)", "icon": "fa-road", "rain": false},
        savingsText: '🌱 35 kg CO₂ • 14.5 km Çift Tüp Tünel',
        tachoRemain: '03 sa 00 dk',
        uetdsCode: 'UETDS-2026-TR-610992',
        driver: 'Turgut Karadeniz (SRC-4: TR-61-44019)',
        path: [
            [41.0027, 39.7168], // Trabzon Liman Hub
            [40.8100, 39.6000], // Maçka
            [40.6300, 39.4000], // Yeni Zigana Tüneli Girişi (14.5 km)
            [40.5600, 39.2900], // Torul
            [40.4600, 39.4700], // Gümüşhane Merkez
            [40.3500, 39.7500], // Kale
            [40.2552, 40.2249], // Bayburt Hub
            [40.0200, 40.5000], // Kop Geçidi (2.409m)
            [39.9200, 40.7000], // Aşkale
            [39.9000, 41.2700]  // Erzurum Palandöken Hub
        ]
    },
    vangolu_sinir: {
        title: 'Van Gölü & Doğu Sınır Ticaret Koridoru',
        vehicle: 'Scania R450 Highline TIR',
        plate: '65 VAN 65',
        fleetText: '1x Scania R450 TIR',
        costText: '₺5.950 TL',
        etaText: '05 sa 15 dk',
        etaMinutes: 315,
        totalDistance: 385,
        cargoText: '13.000 kg (Sınır Ticareti)',
        tollText: '0 TL (Devlet Yolu)',
        fuelText: '32.0 L/100km (~123 L)',
        roadType: 'devlet_yolu',
        roadBadge: 'D-100 & D-975 Sınır Hattı',
        speedRange: [72, 86],
        rpmRange: [1250, 1450],
        weather: {"text": "Doğubayazıt & Tendürek: 4°C Rüzgarlı", "icon": "fa-wind", "rain": false},
        savingsText: '🌱 Sınır Ticareti Transit Avantajı',
        tachoRemain: '02 sa 10 dk',
        uetdsCode: 'UETDS-2026-TR-650331',
        driver: 'Diyar Yıldız (SRC-4: TR-65-88219)',
        path: [
            [39.9000, 41.2700], // Erzurum Hub
            [39.9800, 41.6700], // Pasinler
            [40.0400, 42.1700], // Horasan
            [39.8100, 42.5800], // Eleşkirt
            [39.7191, 43.0503], // Ağrı Merkez
            [39.5300, 43.5500], // Taşlıçay
            [39.5500, 44.0800], // Doğubayazıt (Gürbulak Sınır Kapısı Yakını)
            [39.1400, 43.9100], // Çaldıran
            [38.9800, 43.7500], // Muradiye
            [38.4891, 43.4089]  // Van İpekyolu Merkez Hub
        ]
    }
};

let curatedSimState = {
    key: null,
    scenario: null,
    polylineCasing: null,
    polyline: null,
    marker: null,
    interpolatedPoints: [],
    step: 0,
    intervalId: null,
    isPaused: false,
    isRunning: false,
    speedMultiplier: 1,
    laneState: 'right',
    laneStepCount: 0,
    incidentTriggered: false,
    rerouted: false,
    incidentMarker: null,
    altPolyline: null
};

// =========================================================================
// CANLI TÜRKİYE KARAYOLLARI TRAFİK AKIŞI & KAZA VERİLERİ (TRAFFIC TELEMETRY)
// =========================================================================
let isTrafficLayerActive = false;
let trafficLayerGroup = null;

const TURKEY_TRAFFIC_INCIDENTS_DATA = [
    {
        id: 'inc_bolu',
        coords: [40.7350, 31.5500],
        type: 'accident',
        headline: 'O-4 Bolu Dağı Tüneli: 3 Araçlı Zincirleme Kaza',
        sub: 'Otoyol çift şerit kapalı. Bekleme süresi +55 dk.',
        delay: 55,
        bypass: 'D-100 Dağ Geçidi Serbest (42 Dk Kazanç)'
    },
    {
        id: 'inc_susurluk',
        coords: [39.9120, 28.1600],
        type: 'works',
        headline: 'O-5 Susurluk Rampaları: Asfalt Yenileme',
        sub: 'Gidiş istikameti tek şerit. Ağır vasıta kuyruğu: 7 km.',
        delay: 35,
        bypass: 'D-565 Bandırma-Balıkesir Devlet Yolu (28 Dk Kazanç)'
    },
    {
        id: 'inc_fsm',
        coords: [41.0910, 29.0620],
        type: 'jam',
        headline: 'FSM Köprüsü: Aşırı Yoğun Mesai Trafiği',
        sub: 'Anadolu-Avrupa yönü dur-kalk ilerliyor. Ortalama hız: 12 km/s.',
        delay: 45,
        bypass: 'Yavuz Sultan Selim Köprüsü & KMO (35 Dk Kazanç)'
    },
    {
        id: 'inc_hereke',
        coords: [40.7890, 29.5400],
        type: 'accident',
        headline: 'D-100 Hereke Viyadüğü: Hasarlı Kaza',
        sub: 'Körfez sahil yolu kilitlendi. Bekleme: +40 dk.',
        delay: 40,
        bypass: 'Kuzey Marmara Otoyolu (KMO) Bypass Hattı'
    },
    {
        id: 'inc_pozanti',
        coords: [37.4200, 34.8700],
        type: 'jam',
        headline: 'Pozantı - Toroslar: Ağır Vasıta Yangını & Tıkanıklık',
        sub: 'Rampa çıkışında arızalanan TIR nedeniyle sağ şerit kapalı.',
        delay: 50,
        bypass: 'D-750 Eski Dağ Boğazı Kaçış Yolu (38 Dk Kazanç)'
    }
];

const TURKEY_TRAFFIC_FLOW_LINES = [
    // 1. İstanbul - Kocaeli D-100 (Kırmızı / Kilit)
    {
        coords: [[41.0082, 28.9784], [40.9927, 29.0277], [40.8767, 29.2344], [40.8027, 29.4307]],
        color: '#ef4444',
        weight: 6,
        opacity: 0.85,
        title: 'İstanbul E-5 / D-100 (Kilitli • Hız: 18 km/s)'
    },
    // 2. Kuzey Marmara Otoyolu (Yeşil / Akıcı)
    {
        coords: [[41.1400, 28.4600], [41.1800, 29.0500], [40.8500, 29.6200], [40.8300, 29.8200]],
        color: '#10b981',
        weight: 5,
        opacity: 0.85,
        title: 'Kuzey Marmara Otoyolu (Akıcı • Hız: 115 km/s)'
    },
    // 3. Bolu Dağı O-4 Tünel Yaklaşımı (Kırmızı / Kaza Kilit)
    {
        coords: [[40.8438, 31.1565], [40.7400, 31.4500], [40.7350, 31.5500], [40.7350, 31.6080]],
        color: '#dc2626',
        weight: 7,
        opacity: 0.9,
        dashArray: '6, 6',
        title: 'O-4 Bolu Dağı Tüneli (KAZA NEDENİYLE KAPALI • +55 Dk)'
    },
    // 4. D-100 Bolu Dağ Geçidi Kaçış (Yeşil / Akıcı)
    {
        coords: [[40.7400, 31.4500], [40.7100, 31.4850], [40.6900, 31.5400], [40.7100, 31.5900], [40.7350, 31.6080]],
        color: '#10b981',
        weight: 5,
        opacity: 0.9,
        title: 'D-100 Alternatif Dağ Geçidi (Açık ve Akıcı • 55 km/s)'
    },
    // 5. O-5 Osmangazi - Bursa (Yeşil / Akıcı)
    {
        coords: [[40.8027, 29.4307], [40.7450, 29.5150], [40.6552, 29.2769], [40.1885, 29.0610]],
        color: '#10b981',
        weight: 5,
        opacity: 0.85,
        title: 'O-5 Osmangazi - Bursa (Akıcı • Hız: 120 km/s)'
    },
    // 6. Susurluk O-5 Rampaları (Turuncu / Yol Çalışması)
    {
        coords: [[40.0000, 28.7000], [39.9120, 28.1600], [39.6484, 27.8826]],
        color: '#f59e0b',
        weight: 6,
        opacity: 0.85,
        title: 'O-5 Susurluk Varyantı (Yoğun / Yol Çalışması • +35 Dk)'
    },
    // 7. Balıkesir - Manisa - İzmir (Yeşil / Akıcı)
    {
        coords: [[39.6484, 27.8826], [39.1200, 27.5000], [38.6191, 27.4289], [38.4192, 27.1287]],
        color: '#10b981',
        weight: 5,
        opacity: 0.85,
        title: 'O-5 Balıkesir - İzmir Ekspres (Akıcı • 110 km/s)'
    },
    // 8. Bolu - Gerede - Ankara O-4 (Yeşil / Akıcı)
    {
        coords: [[40.7350, 31.6080], [40.7600, 32.2000], [40.1000, 32.6500], [39.9334, 32.8597]],
        color: '#10b981',
        weight: 5,
        opacity: 0.85,
        title: 'Gerede - Ankara Anadolu Otoyolu (Akıcı • 110 km/s)'
    },
    // 9. Pozantı - Toroslar Geçidi (Kırmızı / Yoğun)
    {
        coords: [[37.9600, 34.6800], [37.4200, 34.8700], [37.0000, 35.3213]],
        color: '#ef4444',
        weight: 6,
        opacity: 0.85,
        title: 'Toroslar Pozantı Koridoru (TIR Tıkanıklığı • +50 Dk)'
    }
];

function interpolatePath(points, segmentsPerLeg = 14) {
    const result = [];
    for (let i = 0; i < points.length - 1; i++) {
        const p1 = points[i];
        const p2 = points[i + 1];
        for (let s = 0; s < segmentsPerLeg; s++) {
            const frac = s / segmentsPerLeg;
            result.push([
                p1[0] + (p2[0] - p1[0]) * frac,
                p1[1] + (p2[1] - p1[1]) * frac
            ]);
        }
    }
    result.push(points[points.length - 1]);
    return result;
}

function renderCockpitWeather(scenario) {
    const box = document.getElementById('weatherParticlesBox');
    const badge = document.getElementById('hudWeatherBadge');
    const wiper = document.getElementById('cockpitWiper');
    if (!box) return;

    box.innerHTML = '';
    const initialWeather = scenario.weather || { text: 'Açık & Kuru Zemin (22°C)', icon: 'fa-sun', condition: 'clear', rain: false };

    if (badge) {
        badge.innerHTML = `<i class="fas ${initialWeather.icon}"></i> <span id="hudWeatherText">${initialWeather.text}</span>`;
    }

    const cond = initialWeather.condition || (initialWeather.rain ? 'rain' : 'clear');

    if (cond === 'rain') {
        for (let i = 0; i < 24; i++) {
            const drop = document.createElement('div');
            drop.className = 'rain-drop';
            drop.style.left = `${Math.floor(Math.random() * 100)}%`;
            drop.style.animationDelay = `${(Math.random() * 0.5).toFixed(2)}s`;
            drop.style.animationDuration = `${(0.32 + Math.random() * 0.15).toFixed(2)}s`;
            box.appendChild(drop);
        }
        if (wiper) wiper.classList.add('active');
    } else if (cond === 'snow') {
        for (let i = 0; i < 18; i++) {
            const flake = document.createElement('div');
            flake.className = 'snow-flake';
            flake.style.left = `${Math.floor(Math.random() * 100)}%`;
            flake.style.animationDelay = `${(Math.random() * 2.5).toFixed(2)}s`;
            flake.style.width = `${Math.floor(3 + Math.random() * 3)}px`;
            flake.style.height = flake.style.width;
            box.appendChild(flake);
        }
        if (wiper) wiper.classList.add('active');
    } else if (cond === 'wind') {
        for (let i = 0; i < 6; i++) {
            const gust = document.createElement('div');
            gust.className = 'wind-gust';
            gust.style.top = `${15 + Math.floor(Math.random() * 70)}%`;
            gust.style.animationDelay = `${(Math.random() * 1.5).toFixed(2)}s`;
            box.appendChild(gust);
        }
        if (wiper) wiper.classList.remove('active');
    } else if (cond === 'fog') {
        const fog = document.createElement('div');
        fog.className = 'fog-layer';
        box.appendChild(fog);
        if (wiper) wiper.classList.remove('active');
    } else {
        if (wiper) wiper.classList.remove('active');
    }

    // Koordinata göre gerçek zamanlı Open-Meteo canlı hava durumu çekimi (CORS destekli)
    if (scenario.path && scenario.path.length > 0) {
        const p = scenario.path[0];
        fetch(`https://api.open-meteo.com/v1/forecast?latitude=${p[0]}&longitude=${p[1]}&current_weather=true`)
            .then(res => res.json())
            .then(data => {
                if (data && data.current_weather) {
                    const temp = Math.round(data.current_weather.temperature);
                    const wind = Math.round(data.current_weather.windspeed);
                    const weatherText = document.getElementById('hudWeatherText');
                    if (weatherText) {
                        weatherText.textContent = `${scenario.weather ? scenario.weather.text.split('(')[0].trim() : 'Bölgesel Hava Durumu'} (${temp}°C • ${wind} km/s rüzgar)`;
                    }
                }
            })
            .catch(() => {});
    }
}

function startCuratedSimulation(scenarioKey) {
    if (!mainMap) return;
    const scenario = CURATED_SCENARIOS[scenarioKey];
    if (!scenario) return;

    // Temizle ve yeni rota çiz
    if (curatedSimState.polyline && mainMap.hasLayer(curatedSimState.polyline)) {
        mainMap.removeLayer(curatedSimState.polyline);
    }
    if (curatedSimState.polylineCasing && mainMap.hasLayer(curatedSimState.polylineCasing)) {
        mainMap.removeLayer(curatedSimState.polylineCasing);
    }
    if (curatedSimState.marker && mainMap.hasLayer(curatedSimState.marker)) {
        mainMap.removeLayer(curatedSimState.marker);
    }
    if (curatedSimState.incidentMarker && mainMap.hasLayer(curatedSimState.incidentMarker)) {
        mainMap.removeLayer(curatedSimState.incidentMarker);
        curatedSimState.incidentMarker = null;
    }
    if (curatedSimState.altPolyline && mainMap.hasLayer(curatedSimState.altPolyline)) {
        mainMap.removeLayer(curatedSimState.altPolyline);
        curatedSimState.altPolyline = null;
    }
    if (curatedSimState.intervalId) {
        clearInterval(curatedSimState.intervalId);
        curatedSimState.intervalId = null;
    }

    curatedSimState.key = scenarioKey;
    curatedSimState.scenario = scenario;
    curatedSimState.interpolatedPoints = interpolatePath(scenario.path, 16);
    curatedSimState.step = 0;
    curatedSimState.isPaused = false;
    curatedSimState.isRunning = true;
    curatedSimState.laneState = 'right';
    curatedSimState.laneStepCount = 0;
    curatedSimState.incidentTriggered = false;
    curatedSimState.rerouted = false;

    const incidentCard = document.getElementById('hudIncidentAlertCard');
    if (incidentCard) incidentCard.style.display = 'none';

    // Yüksek kontrastlı çift katmanlı neon otoyol çizgisi
    curatedSimState.polylineCasing = L.polyline(scenario.path, {
        color: '#0f172a',
        weight: 9,
        opacity: 0.85
    }).addTo(mainMap);

    curatedSimState.polyline = L.polyline(scenario.path, {
        color: '#06b6d4',
        weight: 5,
        opacity: 1.0,
        dashArray: scenario.roadType === 'devlet_yolu' ? '10, 8' : '14, 6'
    }).addTo(mainMap);

    // Harita odaklanma
    mainMap.flyToBounds(curatedSimState.polyline.getBounds(), {
        padding: [60, 60],
        maxZoom: 10,
        duration: 1.5
    });

    // HUD Paneli Aç
    const hud = document.getElementById('simTelemetryHud');
    if (hud) {
        hud.style.display = 'block';
        hud.classList.add('active');
        hud.classList.remove('sim-paused');
    }

    const hudView = document.getElementById('hudCockpitView');
    if (hudView) {
        hudView.classList.remove('is-paused');
        hudView.classList.remove('speed-1x', 'speed-2x', 'speed-5x');
        hudView.classList.add(`speed-${curatedSimState.speedMultiplier}x`);
    }

    // Araç Modeli Başlangıcı: Sağ Şeride Tam Oturmuş
    const carChassis = document.getElementById('cockpitCarChassis');
    if (carChassis) {
        carChassis.className = 'cockpit-car-chassis lane-right';
    }
    const blLeft = document.getElementById('cockpitBlinkerLeft');
    const blRight = document.getElementById('cockpitBlinkerRight');
    if (blLeft) blLeft.classList.remove('blinking');
    if (blRight) blRight.classList.remove('blinking');

    const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setEl('hudRoadTypeBadge', scenario.roadBadge);
    setEl('hudRouteName', scenario.title);
    setEl('hudFleetVal', scenario.fleetText);
    setEl('hudCostVal', scenario.costText);
    setEl('hudEtaVal', scenario.etaText);
    setEl('hudCargoVal', scenario.cargoText);
    setEl('hudTollVal', scenario.tollText);
    setEl('hudDistLeftVal', `${scenario.totalDistance} km`);
    setEl('hudFuelVal', scenario.fuelText);

    // Plaka & Takograf & Tasarruf
    const cleanPlate = scenario.plate ? scenario.plate.split('•')[0].trim() : '34 KRG 102';
    setEl('cockpitPlateTag', cleanPlate);
    setEl('hudTachoRemain', scenario.tachoRemain || '02 sa 45 dk');
    setEl('hudSavingsText', scenario.savingsText || '🌱 38 kg CO₂ • ₺550 Köprü Tasarrufu');
    const tachoFill = document.getElementById('hudTachoFill');
    if (tachoFill) tachoFill.style.width = '35%';

    // Canlı Hava Durumu & Hareketli Parçacıklar
    renderCockpitWeather(scenario);

    const banner = document.getElementById('simCompleteBanner');
    if (banner) banner.style.display = 'none';

    // Harita Üzerindeki Araç İşareti
    const isDevlet = scenario.roadType === 'devlet_yolu';
    const truckIcon = L.divIcon({
        className: 'sim-truck-marker',
        html: `
            <div class="sim-truck-beacon">
                <div class="sim-truck-circle ${isDevlet ? 'road-devlet' : 'road-otoyol'}">
                    <i class="fas fa-truck-moving"></i>
                </div>
                <div class="sim-truck-badge-bar">
                    <span class="sim-truck-plate-tag">${cleanPlate}</span>
                    <span class="sim-truck-speed-tag" id="markerLiveSpeed">⚡ ${scenario.speedRange[0]} km/s</span>
                </div>
            </div>
        `,
        iconSize: [110, 80],
        iconAnchor: [55, 30]
    });

    curatedSimState.marker = L.marker(curatedSimState.interpolatedPoints[0], { icon: truckIcon }).addTo(mainMap);

    // Buton Durumları: Çalışıyor -> 'Durdur'
    const btnSim = document.getElementById('btnSimulate');
    if (btnSim) {
        btnSim.classList.add('active');
        btnSim.innerHTML = '<i class="fas fa-stop"></i> Durdur';
    }
    const btnStop = document.getElementById('btnSimStop');
    if (btnStop) {
        btnStop.className = 'btn btn-danger btn-sm';
        btnStop.innerHTML = '<i class="fas fa-stop"></i> Durdur';
    }
    const btnPause = document.getElementById('btnSimPause');
    if (btnPause) {
        btnPause.innerHTML = '<i class="fas fa-pause"></i>';
    }

    const selectEl = document.getElementById('curatedScenarioSelect');
    if (selectEl) selectEl.value = scenarioKey;

    startSimTimer();
}

function startSimTimer() {
    if (curatedSimState.intervalId) clearInterval(curatedSimState.intervalId);

    const baseDelay = Math.max(25, Math.floor(160 / curatedSimState.speedMultiplier));

    curatedSimState.intervalId = setInterval(() => {
        if (curatedSimState.isPaused) return;

        const pts = curatedSimState.interpolatedPoints;
        if (!pts || pts.length === 0) return;

        curatedSimState.step++;
        curatedSimState.laneStepCount++;

        // Şerit Değiştirme Animasyonu:
        // Araç sağ şerittedir, sol sinyali yakar, direksiyonu kırıp sol şeride TAMAMEN girer.
        // Bir süre sonra sağ sinyali yakar, direksiyonu kırıp sağ şeride TAMAMEN geri döner.
        if (curatedSimState.laneStepCount >= 16) {
            curatedSimState.laneStepCount = 0;
            const carChassis = document.getElementById('cockpitCarChassis');
            const blLeft = document.getElementById('cockpitBlinkerLeft');
            const blRight = document.getElementById('cockpitBlinkerRight');

            if (curatedSimState.laneState === 'right') {
                // 1. Sol Sinyali Yak
                if (blLeft) blLeft.classList.add('blinking');
                setTimeout(() => {
                    if (curatedSimState.isPaused) return;
                    // 2. Sola Direksiyon Kır ve Sol Şeride Geç
                    if (carChassis) {
                        carChassis.className = 'cockpit-car-chassis lane-left steering-left';
                    }
                    setTimeout(() => {
                        // 3. Direksiyonu Düzelt ve Sol Şeride Otur
                        if (carChassis) {
                            carChassis.className = 'cockpit-car-chassis lane-left';
                        }
                        if (blLeft) blLeft.classList.remove('blinking');
                        curatedSimState.laneState = 'left';
                    }, 800);
                }, 400);
            } else {
                // 1. Sağ Sinyali Yak
                if (blRight) blRight.classList.add('blinking');
                setTimeout(() => {
                    if (curatedSimState.isPaused) return;
                    // 2. Sağa Direksiyon Kır ve Sağ Şeride Dön
                    if (carChassis) {
                        carChassis.className = 'cockpit-car-chassis lane-right steering-right';
                    }
                    setTimeout(() => {
                        // 3. Direksiyonu Düzelt ve Sağ Şeride Otur
                        if (carChassis) {
                            carChassis.className = 'cockpit-car-chassis lane-right';
                        }
                        if (blRight) blRight.classList.remove('blinking');
                        curatedSimState.laneState = 'right';
                    }, 800);
                }, 400);
            }
        }

        // Rota sonuna ulaşıldığında
        if (curatedSimState.step >= pts.length) {
            const banner = document.getElementById('simCompleteBanner');
            if (banner) banner.style.display = 'block';

            const speedDig = document.getElementById('hudSpeedDigital');
            if (speedDig) speedDig.textContent = '0';
            const markerSpeed = document.getElementById('markerLiveSpeed');
            if (markerSpeed) markerSpeed.textContent = '⚡ 0 km/s (Varış)';

            // Yol ve araç animasyonlarını DONDUR
            const hudView = document.getElementById('hudCockpitView');
            if (hudView) hudView.classList.add('is-paused');
            const hud = document.getElementById('simTelemetryHud');
            if (hud) hud.classList.add('sim-paused');
            const carChassis = document.getElementById('cockpitCarChassis');
            if (carChassis) carChassis.classList.add('brake-active');

            curatedSimState.isRunning = false;
            const btnStop = document.getElementById('btnSimStop');
            if (btnStop) {
                btnStop.className = 'btn btn-success btn-sm';
                btnStop.innerHTML = '<i class="fas fa-play"></i> Yeniden Başlat';
            }
            const btnSim = document.getElementById('btnSimulate');
            if (btnSim) {
                btnSim.innerHTML = '<i class="fas fa-play"></i> Simülasyon';
            }

            clearInterval(curatedSimState.intervalId);
            curatedSimState.intervalId = null;
            return;
        }

        const currentCoord = pts[curatedSimState.step];
        curatedSimState.marker.setLatLng(currentCoord);

        const scenario = curatedSimState.scenario;
        const speedMin = scenario.speedRange[0];
        const speedMax = scenario.speedRange[1];
        const curSpeed = Math.floor(speedMin + Math.random() * (speedMax - speedMin + 1));
        const curRpm = Math.floor(scenario.rpmRange[0] + Math.random() * (scenario.rpmRange[1] - scenario.rpmRange[0]));

        // İlerledikçe kalan mesafe ve süreyi dinamik eksilt
        const progressFrac = curatedSimState.step / pts.length;

        // Otomatik Kaza & Yol Tıkanıklığı Tespiti (Senaryo ilerleyişine göre)
        if (!curatedSimState.incidentTriggered && scenario && scenario.incident && progressFrac >= (scenario.incident.triggerStepRatio || 0.28)) {
            triggerSimIncident(scenario.incident);
        }

        // Kaza patladıysa ama henüz alternatif rotaya sapılmadıysa araç yavaşlasın (tıkanıklık/kuyruk hissi)
        let displaySpeed = curSpeed;
        if (curatedSimState.incidentTriggered && !curatedSimState.rerouted) {
            displaySpeed = Math.max(18, Math.floor(curSpeed * 0.42));
        }

        const distLeft = Math.max(0, Math.round(scenario.totalDistance * (1 - progressFrac)));
        const minsLeft = Math.max(0, Math.round(scenario.etaMinutes * (1 - progressFrac)));
        const hoursLeft = Math.floor(minsLeft / 60);
        const remMins = minsLeft % 60;

        const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
        setEl('hudSpeedDigital', displaySpeed);
        setEl('hudRpmVal', `${curRpm.toLocaleString('tr-TR')} RPM`);
        setEl('hudDistLeftVal', `${distLeft} km`);
        
        if (curatedSimState.incidentTriggered && !curatedSimState.rerouted) {
            setEl('hudEtaVal', `${hoursLeft > 0 ? hoursLeft + ' sa ' : ''}${remMins} dk (+${scenario.incident ? scenario.incident.delayMinutes : 45} dk Kaza Gecikmesi)`);
        } else {
            setEl('hudEtaVal', `${hoursLeft > 0 ? hoursLeft + ' sa ' : ''}${remMins} dk`);
        }

        const tachoFill = document.getElementById('hudTachoFill');
        if (tachoFill) {
            tachoFill.style.width = `${Math.min(95, Math.round(35 + progressFrac * 60))}%`;
        }

        const markerSpeed = document.getElementById('markerLiveSpeed');
        if (markerSpeed) {
            if (curatedSimState.incidentTriggered && !curatedSimState.rerouted) {
                markerSpeed.textContent = `⚠️ ${displaySpeed} km/s (Trafik Tıkalı)`;
            } else {
                markerSpeed.textContent = `⚡ ${displaySpeed} km/s`;
            }
        }
    }, baseDelay);
}

// Durdur / Başlat: Paneli ve rotayı silmeden SADECE yol akışını ve aracı durdurur/başlatır
function toggleSimStopPlay() {
    if (!curatedSimState.key) {
        startCuratedSimulation('marmara_d100');
        return;
    }

    const hudView = document.getElementById('hudCockpitView');
    const hud = document.getElementById('simTelemetryHud');
    const carChassis = document.getElementById('cockpitCarChassis');
    const btnStop = document.getElementById('btnSimStop');
    const btnSim = document.getElementById('btnSimulate');
    const btnPause = document.getElementById('btnSimPause');
    const speedDig = document.getElementById('hudSpeedDigital');

    if (curatedSimState.isRunning && !curatedSimState.isPaused) {
        // Durdura basıldı -> YOL VE ARAÇ DURUR, FREN LAMBALARI YANAR, HIZ 0 OLUR, PANEL KAPANMAZ!
        curatedSimState.isPaused = true;
        curatedSimState.isRunning = false;
        if (curatedSimState.intervalId) {
            clearInterval(curatedSimState.intervalId);
            curatedSimState.intervalId = null;
        }

        if (hudView) hudView.classList.add('is-paused');
        if (hud) hud.classList.add('sim-paused');
        if (carChassis) carChassis.classList.add('brake-active');
        if (speedDig) speedDig.textContent = '0';

        if (btnStop) {
            btnStop.className = 'btn btn-success btn-sm';
            btnStop.innerHTML = '<i class="fas fa-play"></i> Başlat';
        }
        if (btnSim) {
            btnSim.className = 'btn-map-control active';
            btnSim.innerHTML = '<i class="fas fa-play"></i> Başlat';
        }
        if (btnPause) {
            btnPause.innerHTML = '<i class="fas fa-play"></i>';
        }
    } else {
        // Başlat'a basıldı -> Yol tekrar akar, araç hareket eder, fren lambaları söner!
        curatedSimState.isPaused = false;
        curatedSimState.isRunning = true;

        if (hudView) hudView.classList.remove('is-paused');
        if (hud) hud.classList.remove('sim-paused');
        if (carChassis) carChassis.classList.remove('brake-active');

        if (btnStop) {
            btnStop.className = 'btn btn-danger btn-sm';
            btnStop.innerHTML = '<i class="fas fa-stop"></i> Durdur';
        }
        if (btnSim) {
            btnSim.className = 'btn-map-control active';
            btnSim.innerHTML = '<i class="fas fa-stop"></i> Durdur';
        }
        if (btnPause) {
            btnPause.innerHTML = '<i class="fas fa-pause"></i>';
        }

        startSimTimer();
    }
}

function toggleSimPause() {
    toggleSimStopPlay();
}

function restartSim() {
    curatedSimState.step = 0;
    curatedSimState.isPaused = false;
    curatedSimState.isRunning = true;
    curatedSimState.laneState = 'right';
    curatedSimState.laneStepCount = 0;

    const banner = document.getElementById('simCompleteBanner');
    if (banner) banner.style.display = 'none';

    const btnPause = document.getElementById('btnSimPause');
    if (btnPause) btnPause.innerHTML = '<i class="fas fa-pause"></i>';

    const btnStop = document.getElementById('btnSimStop');
    if (btnStop) {
        btnStop.className = 'btn btn-danger btn-sm';
        btnStop.innerHTML = '<i class="fas fa-stop"></i> Durdur';
    }

    const hudView = document.getElementById('hudCockpitView');
    if (hudView) hudView.classList.remove('is-paused');
    const hud = document.getElementById('simTelemetryHud');
    if (hud) hud.classList.remove('sim-paused');
    const carChassis = document.getElementById('cockpitCarChassis');
    if (carChassis) {
        carChassis.className = 'cockpit-car-chassis lane-right';
    }

    if (curatedSimState.marker && curatedSimState.interpolatedPoints.length > 0) {
        curatedSimState.marker.setLatLng(curatedSimState.interpolatedPoints[0]);
    }
    startSimTimer();
}

function setSimSpeed(multiplier) {
    curatedSimState.speedMultiplier = multiplier;
    document.querySelectorAll('.btn-sim-speed').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('id') === `btnSim${multiplier}x`);
    });

    const hudView = document.getElementById('hudCockpitView');
    if (hudView) {
        hudView.classList.remove('speed-1x', 'speed-2x', 'speed-5x');
        hudView.classList.add(`speed-${multiplier}x`);
    }

    if (curatedSimState.intervalId) {
        startSimTimer();
    }
}

// Üst Bardaki Simülasyon Butonu
function toggleVehicleSimulation() {
    if (curatedSimState.key) {
        toggleSimStopPlay();
    } else {
        const sel = document.getElementById('curatedScenarioSelect');
        const key = (sel && sel.value) ? sel.value : 'marmara_d100';
        startCuratedSimulation(key);
    }
}

// Sağ Üstteki Kapat (X) Butonu: Paneli ve haritayı tamamen temizler
function closeTelemetryHud() {
    if (curatedSimState.intervalId) {
        clearInterval(curatedSimState.intervalId);
        curatedSimState.intervalId = null;
    }
    if (curatedSimState.marker && mainMap) {
        mainMap.removeLayer(curatedSimState.marker);
        curatedSimState.marker = null;
    }
    if (curatedSimState.polyline && mainMap) {
        mainMap.removeLayer(curatedSimState.polyline);
        curatedSimState.polyline = null;
    }
    if (curatedSimState.polylineCasing && mainMap) {
        mainMap.removeLayer(curatedSimState.polylineCasing);
        curatedSimState.polylineCasing = null;
    }
    if (curatedSimState.incidentMarker && mainMap) {
        mainMap.removeLayer(curatedSimState.incidentMarker);
        curatedSimState.incidentMarker = null;
    }
    if (curatedSimState.altPolyline && mainMap) {
        mainMap.removeLayer(curatedSimState.altPolyline);
        curatedSimState.altPolyline = null;
    }

    const alertCard = document.getElementById('hudIncidentAlertCard');
    if (alertCard) alertCard.style.display = 'none';

    const hud = document.getElementById('simTelemetryHud');
    if (hud) {
        hud.classList.remove('active', 'sim-paused');
        hud.style.display = 'none';
    }

    const hudView = document.getElementById('hudCockpitView');
    if (hudView) {
        hudView.classList.remove('is-paused');
    }

    const btnSim = document.getElementById('btnSimulate');
    if (btnSim) {
        btnSim.classList.remove('active');
        btnSim.innerHTML = '<i class="fas fa-play"></i> Simülasyon';
    }

    const selectEl = document.getElementById('curatedScenarioSelect');
    if (selectEl) selectEl.value = '';

    curatedSimState.key = null;
    curatedSimState.isRunning = false;
    curatedSimState.isPaused = false;
    curatedSimState.incidentTriggered = false;
    curatedSimState.rerouted = false;
}

function stopVehicleSimulation() {
    toggleSimStopPlay();
}

// =========================================================================
// DİNAMİK TRAFİK, KAZA ALARMI & ALTERNATİF KAÇIŞ ROTASI (REROUTE) MOTORU
// =========================================================================

function triggerSimIncident(incident) {
    if (!incident || curatedSimState.incidentTriggered) return;
    curatedSimState.incidentTriggered = true;

    // 1. HUD İçindeki Kırmızı Alarm Kartını Aç
    const alertCard = document.getElementById('hudIncidentAlertCard');
    if (alertCard) {
        alertCard.style.display = 'block';
        const hl = document.getElementById('incidentHeadline');
        if (hl) hl.textContent = incident.headline;
        const sub = document.getElementById('incidentSubText');
        if (sub) sub.textContent = incident.subText;
        const byp = document.getElementById('incidentBypassText');
        if (byp) byp.textContent = `Önerilen Kaçış: ${incident.bypassTitle}`;
        const btnAction = document.getElementById('btnRerouteAction');
        if (btnAction) {
            btnAction.className = 'btn-reroute-action';
            btnAction.innerHTML = '<i class="fas fa-route"></i> Alternatif Rotaya Sap (Dinamik Reroute)';
        }
    }

    // 2. Haritada Kaza Noktası İkonu & Pulse Ring Yerleştir
    if (incident.blockedPoint && mainMap) {
        if (curatedSimState.incidentMarker && mainMap.hasLayer(curatedSimState.incidentMarker)) {
            mainMap.removeLayer(curatedSimState.incidentMarker);
        }

        const incIcon = L.divIcon({
            className: 'traffic-incident-marker',
            html: `
                <div class="traffic-incident-beacon type-accident" title="${incident.title}">
                    <div class="pulse-ring"></div>
                    <i class="fas fa-triangle-exclamation"></i>
                </div>
            `,
            iconSize: [36, 36],
            iconAnchor: [18, 18]
        });

        curatedSimState.incidentMarker = L.marker(incident.blockedPoint, { icon: incIcon }).addTo(mainMap);
        curatedSimState.incidentMarker.bindPopup(`
            <div class="traffic-popup-box">
                <div class="traffic-popup-header text-danger">
                    <i class="fas fa-car-burst"></i> ${incident.headline}
                </div>
                <div class="traffic-popup-desc">${incident.subText}</div>
                <div class="traffic-popup-tag bg-danger text-white">Bekleme: +${incident.delayMinutes} Dk</div>
            </div>
        `).openPopup();
    }

    // 3. Önerilen Alternatif Kaçış Çizgisini Haritada Çiz (Yeşil Kesikli Çizgi)
    if (curatedSimState.scenario && curatedSimState.scenario.alternativePath && mainMap) {
        if (curatedSimState.altPolyline && mainMap.hasLayer(curatedSimState.altPolyline)) {
            mainMap.removeLayer(curatedSimState.altPolyline);
        }
        curatedSimState.altPolyline = L.polyline(curatedSimState.scenario.alternativePath, {
            color: '#10b981',
            weight: 6,
            opacity: 0.95,
            dashArray: '8, 8'
        }).addTo(mainMap);
    }
}

// Kullanıcı "Alternatif Rotaya Sap" Butonuna Bastığında:
function applyAlternativeReroute() {
    if (!curatedSimState.scenario) return;
    const scenario = curatedSimState.scenario;
    const incident = scenario.incident || {
        headline: 'ALTERNATİF GÜZERGAH AKTİF',
        savingsInfo: '🌱 35 dk Süre ve Rölanti Tasarrufu',
        alternativeBadge: 'Alternatif Kaçış Koridoru'
    };

    // 1. Araç Kokpit Sinyal & Kaçış Direksiyon Hareketi (Sola viraj alıp şerit değiştirme)
    const carChassis = document.getElementById('cockpitCarChassis');
    const blLeft = document.getElementById('cockpitBlinkerLeft');
    if (blLeft) blLeft.classList.add('blinking');
    if (carChassis) carChassis.className = 'cockpit-car-chassis lane-left steering-left';

    setTimeout(() => {
        if (carChassis) carChassis.className = 'cockpit-car-chassis lane-left';
        if (blLeft) blLeft.classList.remove('blinking');
    }, 1200);

    // 2. Buton Durumunu Başarılıya Çevir
    const btnAction = document.getElementById('btnRerouteAction');
    if (btnAction) {
        btnAction.className = 'btn-reroute-action btn-reroute-success';
        btnAction.innerHTML = '<i class="fas fa-check-circle"></i> ALTERNATİF GÜZERGAHA SAPILDI (REROUTE AKTİF)';
    }

    // 3. Haritadaki Rota Çizgilerini Yenile:
    // Mevcut rota kırmızımsı kesikli "Kilitli Rota" olarak arkada kalır
    if (curatedSimState.polyline) {
        curatedSimState.polyline.setStyle({
            color: '#ef4444',
            opacity: 0.45,
            dashArray: '4, 8'
        });
    }

    // Alternatif yol ana rota haline gelir
    const altPath = scenario.alternativePath || scenario.path;
    if (curatedSimState.altPolyline) {
        curatedSimState.altPolyline.setStyle({
            color: '#10b981',
            weight: 6,
            opacity: 1.0,
            dashArray: null
        });
    }

    // 4. Aracın Simülasyon Noktalarını Alternatif Yol Koordinatlarıyla Güncelle!
    const altInterp = interpolatePath(altPath, 16);
    curatedSimState.interpolatedPoints = altInterp;
    curatedSimState.step = 0; // Yeni rotanın başından devam et
    curatedSimState.rerouted = true;

    // 5. Telemetri Rozetleri ve Bilgilerini Güncelle
    const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setEl('hudRoadTypeBadge', incident.alternativeBadge || 'ALTERNATİF KAÇIŞ HATTI');
    setEl('hudSavingsText', incident.savingsInfo || '🌱 42 dk Süre ve Yakıt Tasarrufu');
    setEl('hudRouteName', `${scenario.title.split('(')[0].trim()} (Bypass Aktif)`);
    const badge = document.getElementById('hudRoadTypeBadge');
    if (badge) {
        badge.style.borderColor = '#10b981';
        badge.style.color = '#10b981';
    }

    // Haritayı yeni rotaya yumuşakça odakla
    if (mainMap && altInterp.length > 0) {
        mainMap.panTo(altInterp[0], { animate: true, duration: 1.2 });
    }
}

// HUD Kontrol Barındaki "🚨" Butonu ile Manuel Test
function triggerSimIncidentTest() {
    if (!curatedSimState.key) {
        startCuratedSimulation('baskent_anadolu');
        setTimeout(() => {
            const sc = curatedSimState.scenario;
            if (sc && sc.incident) triggerSimIncident(sc.incident);
        }, 600);
        return;
    }

    const scenario = curatedSimState.scenario;
    if (scenario && scenario.incident) {
        triggerSimIncident(scenario.incident);
    } else {
        // Varsayılan kaza olayı oluştur
        const curPts = curatedSimState.interpolatedPoints;
        const midPoint = curPts && curPts.length > 0 ? curPts[Math.min(curPts.length - 1, curatedSimState.step + 10)] : [40.75, 30.5];
        triggerSimIncident({
            title: 'Trafik Yoğunluğu & Şerit Kapanması',
            headline: 'İLERİDE ZİNCİRLEME KAZA: YOL KİLİTLENDİ',
            subText: '2 Şerit Trafiğe Kapandı • +45 Dk Bekleme Süresi',
            delayMinutes: 45,
            blockedPoint: midPoint,
            bypassTitle: 'D-100 Alternatif Yan Yol Kaçışı (35 Dk Kazanç)',
            savingsInfo: '⚡ 35 dk süre kurtarıldı • ₺180 TL Tasarruf',
            alternativeBadge: 'D-100 Alternatif Kaçış Koridoru'
        });
    }
}

// =========================================================================
// TÜM TÜRKİYE CANLI KARAYOLLARI TRAFİK & OLAY KATMANI (TOGGLE)
// =========================================================================
function toggleTrafficIncidentLayer() {
    if (!mainMap) return;
    const btn = document.getElementById('btnTrafficLayer');

    if (isTrafficLayerActive) {
        // Kapat
        if (trafficLayerGroup) {
            mainMap.removeLayer(trafficLayerGroup);
            trafficLayerGroup = null;
        }
        isTrafficLayerActive = false;
        if (btn) btn.classList.remove('active');
        return;
    }

    // Aç
    trafficLayerGroup = L.layerGroup();

    // 1. Karayolu Trafik Akış Çizgileri
    TURKEY_TRAFFIC_FLOW_LINES.forEach(flow => {
        const line = L.polyline(flow.coords, {
            color: flow.color,
            weight: flow.weight,
            opacity: flow.opacity,
            dashArray: flow.dashArray || null
        });
        line.bindTooltip(`<strong>${flow.title}</strong>`, { sticky: true });
        trafficLayerGroup.addLayer(line);
    });

    // 2. Noktasal Kaza & Yol Çalışması Olay Marker'ları
    TURKEY_TRAFFIC_INCIDENTS_DATA.forEach(inc => {
        const beaconClass = inc.type === 'accident' ? 'type-accident' : (inc.type === 'works' ? 'type-works' : 'type-jam');
        const iconName = inc.type === 'accident' ? 'fa-car-burst' : (inc.type === 'works' ? 'fa-person-digging' : 'fa-traffic-light');

        const mIcon = L.divIcon({
            className: 'traffic-incident-marker',
            html: `
                <div class="traffic-incident-beacon ${beaconClass}" title="${inc.headline}">
                    <div class="pulse-ring"></div>
                    <i class="fas ${iconName}"></i>
                </div>
            `,
            iconSize: [34, 34],
            iconAnchor: [17, 17]
        });

        const marker = L.marker(inc.coords, { icon: mIcon });
        marker.bindPopup(`
            <div class="traffic-popup-box">
                <div class="traffic-popup-header ${inc.type === 'accident' ? 'text-danger' : (inc.type === 'works' ? 'text-warning' : 'text-danger')}">
                    <i class="fas ${iconName}"></i> ${inc.headline}
                </div>
                <div class="traffic-popup-desc">${inc.sub}</div>
                <div style="font-size:10px; color:#10b981; margin-bottom:5px; font-weight:700;">
                    <i class="fas fa-shield-halved"></i> ${inc.bypass}
                </div>
                <span class="traffic-popup-tag bg-danger text-white">Bekleme: +${inc.delay} Dk</span>
            </div>
        `);
        trafficLayerGroup.addLayer(marker);
    });

    trafficLayerGroup.addTo(mainMap);
    isTrafficLayerActive = true;
    if (btn) btn.classList.add('active');
}

function openUetdsModal() {
    const scenario = curatedSimState.scenario || CURATED_SCENARIOS['marmara_d100'];
    if (!scenario) return;

    const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setEl('uetdsDocCode', scenario.uetdsCode || 'UETDS-2026-TR-418029');
    setEl('uetdsDocPlate', scenario.plate ? scenario.plate.split('•')[0].trim() : '34 KRG 102');
    setEl('uetdsDocDriver', scenario.driver || 'Mustafa Çelik (SRC-4 Belgesi Onaylı)');
    setEl('uetdsDocRoute', scenario.title);
    setEl('uetdsDocDistEta', `${scenario.totalDistance} km • ${scenario.etaText}`);
    setEl('uetdsDocRoadType', scenario.roadBadge);
    setEl('uetdsDocCargo', scenario.cargoText);

    const now = new Date();
    const dateStr = now.toLocaleDateString('tr-TR') + ' ' + now.toLocaleTimeString('tr-TR');
    setEl('uetdsDocDateTime', dateStr);

    const modal = document.getElementById('uetdsModal');
    if (modal) modal.classList.add('active');
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
        const roadType = document.getElementById('roadTypePreference')?.value || 'otoyol';

        const res = await fetch('/api/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: problemType,
                optimize_for: optimizeFor,
                delivery_date: deliveryDate || null,
                cargo_ids: cargoIds,
                road_type: roadType
            })
        });

        const result = await res.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        lastOptimizationResult = result;

        alert(`✅ Rota planlamasi tamamlandi!\n\n📦 ${result.total_cargos} kargo planlandi\n🚚 ${result.routes.length} rota olusturuldu\n🛣️ Güzergah Tipi: ${roadType === 'devlet_yolu' ? 'D-100 Devlet Yolu (0 TL Geçiş)' : 'Otoyol (HGS)'}\n📏 Toplam mesafe: ${result.routes.reduce((sum, r) => sum + r.distance, 0).toFixed(1)} km\n💰 Toplam maliyet: ${result.total_cost.toFixed(0)} TL`);

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

    document.getElementById('resultTotalCost').textContent = result.total_cost.toFixed(0) + ' TL';
    document.getElementById('resultTotalCargos').textContent = result.total_cargos;
    document.getElementById('resultTotalWeight').textContent = result.total_weight.toFixed(0) + ' kg';

    if (result.total_fuel_cost) {
        document.getElementById('fuelCostInfo').style.display = 'block';
        document.getElementById('resultFuelCost').textContent = result.total_fuel_cost.toFixed(0) + ' TL';
    } else {
        document.getElementById('fuelCostInfo').style.display = 'none';
    }

    if (result.rented_vehicles > 0) {
        document.getElementById('rentedInfo').style.display = 'block';
        document.getElementById('resultRentedVehicles').textContent = result.rented_vehicles + ` (${result.rental_cost} TL)`;
    } else {
        document.getElementById('rentedInfo').style.display = 'none';
    }

    const detailsDiv = document.getElementById('routeDetails');
    detailsDiv.innerHTML = result.routes.map((route, i) => {
        let usersHtml = '';
        if (route.cargo_users && route.cargo_users.length > 0) {
            usersHtml = `<div class="cargo-users"><strong>Kargo Sahipleri:</strong><ul>${route.cargo_users.map(u => `<li>${u.username || 'Anonim'} - ${u.weight}kg (${u.station})</li>`).join('')}</ul></div>`;
        }
        const roadBadge = route.road_type_label || (route.road_type === 'devlet_yolu' ? '🚗 D-100 / E-5 (0 TL Geçiş)' : '🛣️ Otoyol (HGS)');
        const durationText = route.duration_formatted || (route.duration_hours ? `${route.duration_hours.toFixed(1)} sa` : '-');
        const tollText = route.toll_cost ? `${route.toll_cost.toFixed(0)} TL` : '0 TL (Ücretsiz)';

        return `
        <div class="route-card ${route.is_rented ? 'rented' : ''}">
            <h4>
                <i class="fas fa-truck" style="color:${routeColors[i % routeColors.length]}"></i>
                ${route.vehicle.name}
                <span style="display:inline-block; font-size:11px; background:#1e293b; color:#38bdf8; padding:2px 8px; border-radius:6px; margin-left:8px; border:1px solid #334155;">${roadBadge}</span>
                ${route.is_rented ? '<span class="status status-pending">Kiralık</span>' : ''}
            </h4>
            <div class="route-info">
                <span>Tahmini Süre: <strong style="color:#f59e0b;">${durationText}</strong></span>
                <span>Mesafe: <strong>${route.distance} km</strong></span>
                <span>Geçiş Ücreti: <strong>${tollText}</strong></span>
                <span>Yakıt: <strong>${route.fuel_cost || 0} TL</strong></span>
                <span>Toplam Maliyet: <strong>${route.cost} TL</strong></span>
                <span>Ağırlık: <strong>${route.weight} kg</strong></span>
                <span>Kargo: <strong>${route.cargo_count} adet</strong></span>
            </div>
            <div class="route-path">
                <strong>Güzergah:</strong> ${route.route_names.join(' <i class="fas fa-arrow-right"></i> ')}
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
                <td>
                    <strong>${r.vehicle_name || 'Kiralık'}</strong>
                    ${r.road_type_label ? `<br><small style="color:#0284c7; font-weight:600;">${r.road_type_label}</small>` : ''}
                    ${r.duration_formatted ? `<br><small style="color:#d97706; font-weight:600;"><i class="fas fa-clock"></i> ${r.duration_formatted}</small>` : ''}
                </td>
                <td>${routeStations}</td>
                <td>${r.total_distance?.toFixed(1) || '-'}</td>
                <td>${r.total_cost?.toFixed(0) || '-'} TL</td>
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

// Global Klavye Kısayolları (Ctrl+K Arama Odaklanma)
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        const input = document.getElementById('mapSearchInput');
        if (input) {
            e.preventDefault();
            input.focus();
            input.select();
        }
    }
});

