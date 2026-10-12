# -*- coding: utf-8 -*-
"""
Türkiye Geneli 81 İl ve Önemli İlçe İstasyonları & Genişletilmiş Araç Filosu Verisi
Lojistik Rota Yönetim ve Optimizasyon Sistemi
"""

# Türkiye 81 İl Merkezi ve Önemli Lojistik / Sanayi İlçe İstasyonları
TURKEY_STATIONS = [
    # --- Ana Lojistik Hub (Merkez Depo) ---
    {
        "name": "Marmara Lojistik Ana Hub (Kocaeli)",
        "city": "Kocaeli",
        "district": "İzmit",
        "latitude": 40.8225,
        "longitude": 29.9213,
        "is_depot": True
    },

    # --- 1) Marmara Bölgesi İl ve İlçeleri ---
    {"name": "Kocaeli - İzmit Merkez", "city": "Kocaeli", "district": "İzmit", "latitude": 40.7654, "longitude": 29.9408, "is_depot": False},
    {"name": "Kocaeli - Gebze Organize Sanayi", "city": "Kocaeli", "district": "Gebze", "latitude": 40.8027, "longitude": 29.4307, "is_depot": False},
    {"name": "Kocaeli - Darıca", "city": "Kocaeli", "district": "Darıca", "latitude": 40.7692, "longitude": 29.3753, "is_depot": False},
    {"name": "Kocaeli - Çayırova", "city": "Kocaeli", "district": "Çayırova", "latitude": 40.8261, "longitude": 29.3711, "is_depot": False},
    {"name": "Kocaeli - Dilovası Liman", "city": "Kocaeli", "district": "Dilovası", "latitude": 40.7833, "longitude": 29.5333, "is_depot": False},
    {"name": "Kocaeli - Körfez", "city": "Kocaeli", "district": "Körfez", "latitude": 40.7625, "longitude": 29.7773, "is_depot": False},
    {"name": "Kocaeli - Derince Liman", "city": "Kocaeli", "district": "Derince", "latitude": 40.7550, "longitude": 29.8314, "is_depot": False},
    {"name": "Kocaeli - Başiskele", "city": "Kocaeli", "district": "Başiskele", "latitude": 40.7140, "longitude": 29.9284, "is_depot": False},
    {"name": "Kocaeli - Gölcük", "city": "Kocaeli", "district": "Gölcük", "latitude": 40.7200, "longitude": 29.8200, "is_depot": False},
    {"name": "Kocaeli - Karamürsel", "city": "Kocaeli", "district": "Karamürsel", "latitude": 40.6917, "longitude": 29.6167, "is_depot": False},
    {"name": "Kocaeli - Kartepe Lojistik", "city": "Kocaeli", "district": "Kartepe", "latitude": 40.7533, "longitude": 30.0224, "is_depot": False},
    {"name": "Kocaeli - Kandıra", "city": "Kocaeli", "district": "Kandıra", "latitude": 41.0711, "longitude": 30.1528, "is_depot": False},

    # İstanbul İlçeleri
    {"name": "İstanbul - Kadıköy Aktarma", "city": "İstanbul", "district": "Kadıköy", "latitude": 40.9927, "longitude": 29.0277, "is_depot": False},
    {"name": "İstanbul - Üsküdar", "city": "İstanbul", "district": "Üsküdar", "latitude": 41.0267, "longitude": 29.0153, "is_depot": False},
    {"name": "İstanbul - Pendik Kurtköy Lojistik", "city": "İstanbul", "district": "Pendik", "latitude": 40.8767, "longitude": 29.2344, "is_depot": False},
    {"name": "İstanbul - Ümraniye", "city": "İstanbul", "district": "Ümraniye", "latitude": 41.0256, "longitude": 29.1167, "is_depot": False},
    {"name": "İstanbul - Beşiktaş", "city": "İstanbul", "district": "Beşiktaş", "latitude": 41.0422, "longitude": 29.0067, "is_depot": False},
    {"name": "İstanbul - Şişli", "city": "İstanbul", "district": "Şişli", "latitude": 41.0600, "longitude": 28.9878, "is_depot": False},
    {"name": "İstanbul - Bakırköy", "city": "İstanbul", "district": "Bakırköy", "latitude": 40.9801, "longitude": 28.8725, "is_depot": False},
    {"name": "İstanbul - Başakşehir İkitelli OSB", "city": "İstanbul", "district": "Başakşehir", "latitude": 41.0794, "longitude": 28.8028, "is_depot": False},
    {"name": "İstanbul - Esenyurt Lojistik Park", "city": "İstanbul", "district": "Esenyurt", "latitude": 41.0342, "longitude": 28.6800, "is_depot": False},
    {"name": "İstanbul - Tuzla Tersaneler", "city": "İstanbul", "district": "Tuzla", "latitude": 40.8167, "longitude": 29.3000, "is_depot": False},

    # Bursa İlçeleri
    {"name": "Bursa - Nilüfer OSB", "city": "Bursa", "district": "Nilüfer", "latitude": 40.2100, "longitude": 28.9800, "is_depot": False},
    {"name": "Bursa - Osmangazi Merkez", "city": "Bursa", "district": "Osmangazi", "latitude": 40.1885, "longitude": 29.0610, "is_depot": False},
    {"name": "Bursa - Gemlik Serbest Bölge Liman", "city": "Bursa", "district": "Gemlik", "latitude": 40.4300, "longitude": 29.1500, "is_depot": False},
    {"name": "Bursa - İnegöl Mobilya Sanayi", "city": "Bursa", "district": "İnegöl", "latitude": 40.0800, "longitude": 29.5100, "is_depot": False},

    # Sakarya, Yalova, Trakya
    {"name": "Sakarya - Adapazarı Merkez", "city": "Sakarya", "district": "Adapazarı", "latitude": 40.7731, "longitude": 30.4028, "is_depot": False},
    {"name": "Sakarya - Serdivan", "city": "Sakarya", "district": "Serdivan", "latitude": 40.7600, "longitude": 30.3600, "is_depot": False},
    {"name": "Sakarya - Hendek OSB", "city": "Sakarya", "district": "Hendek", "latitude": 40.8000, "longitude": 30.7500, "is_depot": False},
    {"name": "Yalova - Merkez Liman", "city": "Yalova", "district": "Merkez", "latitude": 40.6550, "longitude": 29.2769, "is_depot": False},
    {"name": "Tekirdağ - Çorlu Lojistik Üssü", "city": "Tekirdağ", "district": "Çorlu", "latitude": 41.1600, "longitude": 27.8000, "is_depot": False},
    {"name": "Tekirdağ - Süleymanpaşa", "city": "Tekirdağ", "district": "Süleymanpaşa", "latitude": 40.9781, "longitude": 27.5117, "is_depot": False},
    {"name": "Edirne - Merkez", "city": "Edirne", "district": "Merkez", "latitude": 41.6772, "longitude": 26.5557, "is_depot": False},
    {"name": "Kırklareli - Lüleburgaz", "city": "Kırklareli", "district": "Lüleburgaz", "latitude": 41.4050, "longitude": 27.3550, "is_depot": False},
    {"name": "Kırklareli - Merkez", "city": "Kırklareli", "district": "Merkez", "latitude": 41.7355, "longitude": 27.2252, "is_depot": False},
    {"name": "Balıkesir - Merkez", "city": "Balıkesir", "district": "Altıeylül", "latitude": 39.6484, "longitude": 27.8826, "is_depot": False},
    {"name": "Balıkesir - Bandırma Liman", "city": "Balıkesir", "district": "Bandırma", "latitude": 40.3522, "longitude": 27.9767, "is_depot": False},
    {"name": "Çanakkale - Merkez", "city": "Çanakkale", "district": "Merkez", "latitude": 40.1553, "longitude": 26.4142, "is_depot": False},
    {"name": "Bilecik - Merkez", "city": "Bilecik", "district": "Merkez", "latitude": 40.1426, "longitude": 29.9793, "is_depot": False},

    # --- 2) Ege Bölgesi İl ve İlçeleri ---
    {"name": "İzmir - Konak Liman Hub", "city": "İzmir", "district": "Konak", "latitude": 38.4192, "longitude": 27.1287, "is_depot": False},
    {"name": "İzmir - Bornova Lojistik", "city": "İzmir", "district": "Bornova", "latitude": 38.4697, "longitude": 27.2181, "is_depot": False},
    {"name": "İzmir - Karşıyaka", "city": "İzmir", "district": "Karşıyaka", "latitude": 38.4556, "longitude": 27.1125, "is_depot": False},
    {"name": "İzmir - Çiğli Atatürk OSB", "city": "İzmir", "district": "Çiğli", "latitude": 38.4900, "longitude": 27.0500, "is_depot": False},
    {"name": "İzmir - Buca", "city": "İzmir", "district": "Buca", "latitude": 38.3889, "longitude": 27.1778, "is_depot": False},
    {"name": "İzmir - Gaziemir Serbest Bölge", "city": "İzmir", "district": "Gaziemir", "latitude": 38.3200, "longitude": 27.1300, "is_depot": False},
    {"name": "Manisa - Yunusemre OSB", "city": "Manisa", "district": "Yunusemre", "latitude": 38.6191, "longitude": 27.4289, "is_depot": False},
    {"name": "Aydın - Efeler Merkez", "city": "Aydın", "district": "Efeler", "latitude": 37.8481, "longitude": 27.8453, "is_depot": False},
    {"name": "Aydın - Kuşadası", "city": "Aydın", "district": "Kuşadası", "latitude": 37.8579, "longitude": 27.2610, "is_depot": False},
    {"name": "Denizli - Pamukkale Sanayi", "city": "Denizli", "district": "Pamukkale", "latitude": 37.7765, "longitude": 29.0864, "is_depot": False},
    {"name": "Muğla - Menteşe Merkez", "city": "Muğla", "district": "Menteşe", "latitude": 37.2153, "longitude": 28.3636, "is_depot": False},
    {"name": "Muğla - Bodrum Lojistik", "city": "Muğla", "district": "Bodrum", "latitude": 37.0344, "longitude": 27.4305, "is_depot": False},
    {"name": "Muğla - Fethiye", "city": "Muğla", "district": "Fethiye", "latitude": 36.6217, "longitude": 29.1164, "is_depot": False},
    {"name": "Afyonkarahisar - Merkez", "city": "Afyonkarahisar", "district": "Merkez", "latitude": 38.7569, "longitude": 30.5387, "is_depot": False},
    {"name": "Kütahya - Merkez", "city": "Kütahya", "district": "Merkez", "latitude": 39.4242, "longitude": 29.9833, "is_depot": False},
    {"name": "Uşak - Merkez", "city": "Uşak", "district": "Merkez", "latitude": 38.6742, "longitude": 29.4059, "is_depot": False},

    # --- 3) İç Anadolu Bölgesi İl ve İlçeleri ---
    {"name": "Ankara - Çankaya Merkez Hub", "city": "Ankara", "district": "Çankaya", "latitude": 39.9208, "longitude": 32.8541, "is_depot": False},
    {"name": "Ankara - Yenimahalle OSTİM OSB", "city": "Ankara", "district": "Yenimahalle", "latitude": 39.9700, "longitude": 32.7400, "is_depot": False},
    {"name": "Ankara - Keçiören", "city": "Ankara", "district": "Keçiören", "latitude": 40.0167, "longitude": 32.8667, "is_depot": False},
    {"name": "Ankara - Sincan OSB", "city": "Ankara", "district": "Sincan", "latitude": 39.9600, "longitude": 32.5800, "is_depot": False},
    {"name": "Ankara - Etimesgut Lojistik", "city": "Ankara", "district": "Etimesgut", "latitude": 39.9500, "longitude": 32.6833, "is_depot": False},
    {"name": "Ankara - Gölbaşı", "city": "Ankara", "district": "Gölbaşı", "latitude": 39.7894, "longitude": 32.8086, "is_depot": False},
    {"name": "Konya - Selçuklu Sanayi Hub", "city": "Konya", "district": "Selçuklu", "latitude": 37.8667, "longitude": 32.4833, "is_depot": False},
    {"name": "Konya - Karatay", "city": "Konya", "district": "Karatay", "latitude": 37.8744, "longitude": 32.5311, "is_depot": False},
    {"name": "Eskişehir - Odunpazarı", "city": "Eskişehir", "district": "Odunpazarı", "latitude": 39.7610, "longitude": 30.5283, "is_depot": False},
    {"name": "Eskişehir - Tepebaşı OSB", "city": "Eskişehir", "district": "Tepebaşı", "latitude": 39.7767, "longitude": 30.5206, "is_depot": False},
    {"name": "Kayseri - Melikgazi OSB", "city": "Kayseri", "district": "Melikgazi", "latitude": 38.7205, "longitude": 35.4826, "is_depot": False},
    {"name": "Sivas - Merkez", "city": "Sivas", "district": "Merkez", "latitude": 39.7477, "longitude": 37.0179, "is_depot": False},
    {"name": "Aksaray - Merkez", "city": "Aksaray", "district": "Merkez", "latitude": 38.3687, "longitude": 34.0370, "is_depot": False},
    {"name": "Kırıkkale - Merkez", "city": "Kırıkkale", "district": "Merkez", "latitude": 39.8468, "longitude": 33.5153, "is_depot": False},
    {"name": "Kırşehir - Merkez", "city": "Kırşehir", "district": "Merkez", "latitude": 39.1425, "longitude": 34.1709, "is_depot": False},
    {"name": "Nevşehir - Kapadokya Lojistik", "city": "Nevşehir", "district": "Merkez", "latitude": 38.6244, "longitude": 34.7144, "is_depot": False},
    {"name": "Niğde - Merkez", "city": "Niğde", "district": "Merkez", "latitude": 37.9667, "longitude": 34.6833, "is_depot": False},
    {"name": "Karaman - Merkez", "city": "Karaman", "district": "Merkez", "latitude": 37.1759, "longitude": 33.2287, "is_depot": False},
    {"name": "Yozgat - Merkez", "city": "Yozgat", "district": "Merkez", "latitude": 39.8181, "longitude": 34.8147, "is_depot": False},
    {"name": "Çankırı - Merkez", "city": "Çankırı", "district": "Merkez", "latitude": 40.6013, "longitude": 33.6134, "is_depot": False},

    # --- 4) Akdeniz Bölgesi İl ve İlçeleri ---
    {"name": "Antalya - Muratpaşa Lojistik Hub", "city": "Antalya", "district": "Muratpaşa", "latitude": 36.8841, "longitude": 30.7056, "is_depot": False},
    {"name": "Antalya - Kepez", "city": "Antalya", "district": "Kepez", "latitude": 36.9300, "longitude": 30.6800, "is_depot": False},
    {"name": "Antalya - Alanya", "city": "Antalya", "district": "Alanya", "latitude": 36.5438, "longitude": 31.9998, "is_depot": False},
    {"name": "Antalya - Manavgat", "city": "Antalya", "district": "Manavgat", "latitude": 36.7869, "longitude": 31.4422, "is_depot": False},
    {"name": "Adana - Seyhan Lojistik Hub", "city": "Adana", "district": "Seyhan", "latitude": 36.9914, "longitude": 35.3308, "is_depot": False},
    {"name": "Adana - Yüreğir OSB", "city": "Adana", "district": "Yüreğir", "latitude": 36.9856, "longitude": 35.3528, "is_depot": False},
    {"name": "Mersin - Akdeniz Liman Hub", "city": "Mersin", "district": "Akdeniz", "latitude": 36.8000, "longitude": 34.6333, "is_depot": False},
    {"name": "Mersin - Tarsus", "city": "Mersin", "district": "Tarsus", "latitude": 36.9167, "longitude": 34.8958, "is_depot": False},
    {"name": "Hatay - Antakya Merkez", "city": "Hatay", "district": "Antakya", "latitude": 36.2023, "longitude": 36.1606, "is_depot": False},
    {"name": "Hatay - İskenderun Liman", "city": "Hatay", "district": "İskenderun", "latitude": 36.5872, "longitude": 36.1736, "is_depot": False},
    {"name": "Kahramanmaraş - Onikişubat Sanayi", "city": "Kahramanmaraş", "district": "Onikişubat", "latitude": 37.5858, "longitude": 36.9371, "is_depot": False},
    {"name": "Osmaniye - Merkez", "city": "Osmaniye", "district": "Merkez", "latitude": 37.0742, "longitude": 36.2478, "is_depot": False},
    {"name": "Isparta - Merkez", "city": "Isparta", "district": "Merkez", "latitude": 37.7648, "longitude": 30.5566, "is_depot": False},
    {"name": "Burdur - Merkez", "city": "Burdur", "district": "Merkez", "latitude": 37.7203, "longitude": 30.2908, "is_depot": False},

    # --- 5) Karadeniz Bölgesi İl ve İlçeleri ---
    {"name": "Samsun - İlkadım Liman Hub", "city": "Samsun", "district": "İlkadım", "latitude": 41.2867, "longitude": 36.3300, "is_depot": False},
    {"name": "Samsun - Tekkeköy Lojistik", "city": "Samsun", "district": "Tekkeköy", "latitude": 41.2294, "longitude": 36.4464, "is_depot": False},
    {"name": "Trabzon - Ortahisar Liman Hub", "city": "Trabzon", "district": "Ortahisar", "latitude": 41.0027, "longitude": 39.7167, "is_depot": False},
    {"name": "Ordu - Altınordu", "city": "Ordu", "district": "Altınordu", "latitude": 40.9839, "longitude": 37.8764, "is_depot": False},
    {"name": "Giresun - Merkez", "city": "Giresun", "district": "Merkez", "latitude": 40.9128, "longitude": 38.3895, "is_depot": False},
    {"name": "Rize - Merkez", "city": "Rize", "district": "Merkez", "latitude": 41.0201, "longitude": 40.5234, "is_depot": False},
    {"name": "Artvin - Merkez", "city": "Artvin", "district": "Merkez", "latitude": 41.1828, "longitude": 41.8183, "is_depot": False},
    {"name": "Zonguldak - Merkez Liman", "city": "Zonguldak", "district": "Merkez", "latitude": 41.4564, "longitude": 31.7987, "is_depot": False},
    {"name": "Zonguldak - Ereğli Erdemir", "city": "Zonguldak", "district": "Karadeniz Ereğli", "latitude": 41.2847, "longitude": 31.4286, "is_depot": False},
    {"name": "Bolu - Merkez Lojistik", "city": "Bolu", "district": "Merkez", "latitude": 40.7350, "longitude": 31.6061, "is_depot": False},
    {"name": "Düzce - Merkez", "city": "Düzce", "district": "Merkez", "latitude": 40.8438, "longitude": 31.1565, "is_depot": False},
    {"name": "Karabük - Safranbolu Sanayi", "city": "Karabük", "district": "Merkez", "latitude": 41.2061, "longitude": 32.6204, "is_depot": False},
    {"name": "Bartın - Merkez Liman", "city": "Bartın", "district": "Merkez", "latitude": 41.6344, "longitude": 32.3375, "is_depot": False},
    {"name": "Kastamonu - Merkez", "city": "Kastamonu", "district": "Merkez", "latitude": 41.3887, "longitude": 33.7827, "is_depot": False},
    {"name": "Sinop - Merkez Liman", "city": "Sinop", "district": "Merkez", "latitude": 42.0231, "longitude": 35.1531, "is_depot": False},
    {"name": "Amasya - Merkez", "city": "Amasya", "district": "Merkez", "latitude": 40.6501, "longitude": 35.8353, "is_depot": False},
    {"name": "Çorum - Merkez", "city": "Çorum", "district": "Merkez", "latitude": 40.5506, "longitude": 34.9556, "is_depot": False},
    {"name": "Tokat - Merkez", "city": "Tokat", "district": "Merkez", "latitude": 40.3167, "longitude": 36.5500, "is_depot": False},
    {"name": "Gümüşhane - Merkez", "city": "Gümüşhane", "district": "Merkez", "latitude": 40.4600, "longitude": 39.4814, "is_depot": False},
    {"name": "Bayburt - Merkez", "city": "Bayburt", "district": "Merkez", "latitude": 40.2552, "longitude": 40.2249, "is_depot": False},

    # --- 6) Güneydoğu Anadolu Bölgesi İl ve İlçeleri ---
    {"name": "Gaziantep - Şehitkamil OSB Hub", "city": "Gaziantep", "district": "Şehitkamil", "latitude": 37.0662, "longitude": 37.3833, "is_depot": False},
    {"name": "Gaziantep - Şahinbey", "city": "Gaziantep", "district": "Şahinbey", "latitude": 37.0428, "longitude": 37.3603, "is_depot": False},
    {"name": "Diyarbakır - Kayapınar Lojistik", "city": "Diyarbakır", "district": "Kayapınar", "latitude": 37.9144, "longitude": 40.2306, "is_depot": False},
    {"name": "Şanlıurfa - Haliliye", "city": "Şanlıurfa", "district": "Haliliye", "latitude": 37.1674, "longitude": 38.7955, "is_depot": False},
    {"name": "Batman - Merkez Petrol Sanayi", "city": "Batman", "district": "Merkez", "latitude": 37.8812, "longitude": 41.1293, "is_depot": False},
    {"name": "Mardin - Artuklu Lojistik", "city": "Mardin", "district": "Artuklu", "latitude": 37.3212, "longitude": 40.7245, "is_depot": False},
    {"name": "Adıyaman - Merkez", "city": "Adıyaman", "district": "Merkez", "latitude": 37.7648, "longitude": 38.2786, "is_depot": False},
    {"name": "Siirt - Merkez", "city": "Siirt", "district": "Merkez", "latitude": 37.9333, "longitude": 41.9500, "is_depot": False},
    {"name": "Şırnak - Cizre Lojistik", "city": "Şırnak", "district": "Cizre", "latitude": 37.3272, "longitude": 42.1856, "is_depot": False},
    {"name": "Kilis - Merkez", "city": "Kilis", "district": "Merkez", "latitude": 36.7184, "longitude": 37.1212, "is_depot": False},

    # --- 7) Doğu Anadolu Bölgesi İl ve İlçeleri ---
    {"name": "Malatya - Yeşilyurt OSB", "city": "Malatya", "district": "Yeşilyurt", "latitude": 38.3552, "longitude": 38.3095, "is_depot": False},
    {"name": "Elazığ - Merkez", "city": "Elazığ", "district": "Merkez", "latitude": 38.6810, "longitude": 39.2264, "is_depot": False},
    {"name": "Erzurum - Yakutiye Lojistik Hub", "city": "Erzurum", "district": "Yakutiye", "latitude": 39.9043, "longitude": 41.2678, "is_depot": False},
    {"name": "Van - İpekyolu Lojistik", "city": "Van", "district": "İpekyolu", "latitude": 38.4891, "longitude": 43.4089, "is_depot": False},
    {"name": "Erzincan - Merkez", "city": "Erzincan", "district": "Merkez", "latitude": 39.7500, "longitude": 39.5000, "is_depot": False},
    {"name": "Kars - Merkez", "city": "Kars", "district": "Merkez", "latitude": 40.6167, "longitude": 43.1000, "is_depot": False},
    {"name": "Ağrı - Merkez", "city": "Ağrı", "district": "Merkez", "latitude": 39.7191, "longitude": 43.0503, "is_depot": False},
    {"name": "Muş - Merkez", "city": "Muş", "district": "Merkez", "latitude": 38.7432, "longitude": 41.5064, "is_depot": False},
    {"name": "Bitlis - Tatvan Liman", "city": "Bitlis", "district": "Tatvan", "latitude": 38.5008, "longitude": 42.2817, "is_depot": False},
    {"name": "Bingöl - Merkez", "city": "Bingöl", "district": "Merkez", "latitude": 38.8853, "longitude": 40.4983, "is_depot": False},
    {"name": "Tunceli - Merkez", "city": "Tunceli", "district": "Merkez", "latitude": 39.1079, "longitude": 39.5401, "is_depot": False},
    {"name": "Iğdır - Merkez", "city": "Iğdır", "district": "Merkez", "latitude": 39.9237, "longitude": 44.0450, "is_depot": False},
    {"name": "Ardahan - Merkez", "city": "Ardahan", "district": "Merkez", "latitude": 41.1105, "longitude": 42.7022, "is_depot": False},
    {"name": "Hakkari - Yüksekova", "city": "Hakkari", "district": "Yüksekova", "latitude": 37.5736, "longitude": 44.2872, "is_depot": False}
]

# Çok Sınıflı, Gerçekçi ve Genişletilmiş Araç Filosu
EXPANDED_VEHICLES = [
    {
        "name": "Moto Kurye - Honda CBF 150 (Express)",
        "plate": "41 MTO 101",
        "type": "courier",
        "category": "Express Dağıtım",
        "capacity": 50,
        "volume_m3": 0.3,
        "rental_cost": 80.0,
        "fuel_consumption": 0.35,  # TL/km
        "speed_factor": 1.25,
        "is_owned": 1,
        "icon": "fa-motorcycle",
        "color": "#10b981",
        "description": "Acil evrak ve hafif paketler için maksimum çeviklik."
    },
    {
        "name": "Panelvan - Fiat Doblo Maxi (Hafif Ticari)",
        "plate": "41 PNV 202",
        "type": "van",
        "category": "Hafif Ticari",
        "capacity": 400,
        "volume_m3": 4.2,
        "rental_cost": 180.0,
        "fuel_consumption": 0.75,
        "speed_factor": 1.10,
        "is_owned": 1,
        "icon": "fa-van-shuttle",
        "color": "#06b6d4",
        "description": "Şehir içi sokak aralarında seri dağıtım."
    },
    {
        "name": "Dağıtım Kamyoneti - Ford Transit 350L",
        "plate": "41 TRN 303",
        "type": "light_truck",
        "category": "Şehir İçi Kamyonet",
        "capacity": 1000,
        "volume_m3": 12.5,
        "rental_cost": 280.0,
        "fuel_consumption": 1.15,
        "speed_factor": 1.00,
        "is_owned": 1,
        "icon": "fa-truck-pickup",
        "color": "#6366f1",
        "description": "Standart koli ve orta hacimli kargo taşımacılığı."
    },
    {
        "name": "Bölgesel Kamyon - Isuzu NPR Long",
        "plate": "41 KAM 404",
        "type": "medium_truck",
        "category": "Bölgesel Dağıtım Kamyonu",
        "capacity": 2500,
        "volume_m3": 28.0,
        "rental_cost": 450.0,
        "fuel_consumption": 1.85,
        "speed_factor": 0.95,
        "is_owned": 1,
        "icon": "fa-truck",
        "color": "#f59e0b",
        "description": "İller arası ve sanayi bölgeleri için ideal taşıma kapasitesi."
    },
    {
        "name": "Ağır Hizmet Kamyonu - Mercedes-Benz Axor 1840",
        "plate": "41 AXO 505",
        "type": "heavy_truck",
        "category": "Şehirlerarası Ağır Vasıta",
        "capacity": 6000,
        "volume_m3": 50.0,
        "rental_cost": 750.0,
        "fuel_consumption": 3.10,
        "speed_factor": 0.90,
        "is_owned": 1,
        "icon": "fa-truck-moving",
        "color": "#8b5cf6",
        "description": "Büyük aktarma merkezleri arası toplu yük transferi."
    },
    {
        "name": "Mega Treyler TIR - Scania R450 Highline",
        "plate": "41 TIR 606",
        "type": "trailer",
        "category": "Mega Lojistik Tır",
        "capacity": 15000,
        "volume_m3": 95.0,
        "rental_cost": 1200.0,
        "fuel_consumption": 4.60,
        "speed_factor": 0.85,
        "is_owned": 1,
        "icon": "fa-trailer",
        "color": "#ef4444",
        "description": "Türkiye geneli ana hat (linehaul) konteyner ve paletli sevkiyat."
    }
]

# Türkiye Coğrafi Bölgeleri ve İl Listeleri (Frontend ve Filtreleme İçin)
TURKEY_REGIONS = {
    "Marmara": ["Kocaeli", "İstanbul", "Bursa", "Sakarya", "Yalova", "Tekirdağ", "Edirne", "Kırklareli", "Balıkesir", "Çanakkale", "Bilecik"],
    "Ege": ["İzmir", "Manisa", "Aydın", "Denizli", "Muğla", "Afyonkarahisar", "Kütahya", "Uşak"],
    "İç Anadolu": ["Ankara", "Konya", "Eskişehir", "Kayseri", "Sivas", "Aksaray", "Kırıkkale", "Kırşehir", "Nevşehir", "Niğde", "Karaman", "Yozgat", "Çankırı"],
    "Akdeniz": ["Antalya", "Adana", "Mersin", "Hatay", "Kahramanmaraş", "Osmaniye", "Isparta", "Burdur"],
    "Karadeniz": ["Samsun", "Trabzon", "Ordu", "Giresun", "Rize", "Artvin", "Zonguldak", "Bolu", "Düzce", "Karabük", "Bartın", "Kastamonu", "Sinop", "Amasya", "Çorum", "Tokat", "Gümüşhane", "Bayburt"],
    "Güneydoğu Anadolu": ["Gaziantep", "Diyarbakır", "Şanlıurfa", "Batman", "Mardin", "Adıyaman", "Siirt", "Şırnak", "Kilis"],
    "Doğu Anadolu": ["Malatya", "Elazığ", "Erzurum", "Van", "Erzincan", "Kars", "Ağrı", "Muş", "Bitlis", "Bingöl", "Tunceli", "Iğdır", "Ardahan", "Hakkari"]
}
