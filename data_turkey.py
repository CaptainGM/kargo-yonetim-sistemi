# -*- coding: utf-8 -*-
"""
Türkiye Geneli 81 İl ve Stratejik 350+ Lojistik İstasyonu, Çeşitlendirilmiş Araç Filosu
ve Gerçekçi Güncel Akaryakıt/Operasyonel Maliyet Veri Modeli
"""

TURKEY_STATIONS = [
    {
        "name": "Marmara Lojistik Ana Hub (Kocaeli)",
        "city": "Kocaeli",
        "district": "İzmit",
        "latitude": 40.8225,
        "longitude": 29.9213,
        "is_depot": True,
        "station_type": "hub",
        "daily_capacity": 50000
    },
    {
        "name": "Kocaeli - İzmit Merkez Şube",
        "city": "Kocaeli",
        "district": "İzmit",
        "latitude": 40.7654,
        "longitude": 29.9408,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Gebze GOSB Lojistik Üssü",
        "city": "Kocaeli",
        "district": "Gebze",
        "latitude": 40.8027,
        "longitude": 29.4307,
        "station_type": "hub",
        "daily_capacity": 35000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Darıca Şube",
        "city": "Kocaeli",
        "district": "Darıca",
        "latitude": 40.7692,
        "longitude": 29.3753,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Çayırova Lojistik Park",
        "city": "Kocaeli",
        "district": "Çayırova",
        "latitude": 40.8261,
        "longitude": 29.3711,
        "station_type": "hub",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Dilovası Liman Aktarma",
        "city": "Kocaeli",
        "district": "Dilovası",
        "latitude": 40.7833,
        "longitude": 29.5333,
        "station_type": "hub",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Körfez Petrokimya Şube",
        "city": "Kocaeli",
        "district": "Körfez",
        "latitude": 40.7625,
        "longitude": 29.7773,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Derince Liman Terminali",
        "city": "Kocaeli",
        "district": "Derince",
        "latitude": 40.755,
        "longitude": 29.8314,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Başiskele Şube",
        "city": "Kocaeli",
        "district": "Başiskele",
        "latitude": 40.714,
        "longitude": 29.9284,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Gölcük Tersane Şube",
        "city": "Kocaeli",
        "district": "Gölcük",
        "latitude": 40.72,
        "longitude": 29.82,
        "station_type": "branch",
        "daily_capacity": 8500,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Karamürsel Şube",
        "city": "Kocaeli",
        "district": "Karamürsel",
        "latitude": 40.6917,
        "longitude": 29.6167,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Kartepe Lojistik Köyü",
        "city": "Kocaeli",
        "district": "Kartepe",
        "latitude": 40.7533,
        "longitude": 30.0224,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "Kocaeli - Kandıra Şube",
        "city": "Kocaeli",
        "district": "Kandıra",
        "latitude": 41.0711,
        "longitude": 30.1528,
        "station_type": "branch",
        "daily_capacity": 4000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Kadıköy Aktarma Merkezi",
        "city": "İstanbul",
        "district": "Kadıköy",
        "latitude": 40.9927,
        "longitude": 29.0277,
        "station_type": "hub",
        "daily_capacity": 30000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Üsküdar Şube",
        "city": "İstanbul",
        "district": "Üsküdar",
        "latitude": 41.0267,
        "longitude": 29.0153,
        "station_type": "branch",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Pendik Kurtköy Lojistik Üssü",
        "city": "İstanbul",
        "district": "Pendik",
        "latitude": 40.8767,
        "longitude": 29.2344,
        "station_type": "hub",
        "daily_capacity": 45000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Tuzla Lojistik & Antrepo",
        "city": "İstanbul",
        "district": "Tuzla",
        "latitude": 40.8167,
        "longitude": 29.3,
        "station_type": "hub",
        "daily_capacity": 40000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Kartal Şube",
        "city": "İstanbul",
        "district": "Kartal",
        "latitude": 40.89,
        "longitude": 29.19,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Maltepe Dağıtım Şubesi",
        "city": "İstanbul",
        "district": "Maltepe",
        "latitude": 40.93,
        "longitude": 29.14,
        "station_type": "branch",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Ataşehir Finans & Kargo",
        "city": "İstanbul",
        "district": "Ataşehir",
        "latitude": 40.985,
        "longitude": 29.11,
        "station_type": "branch",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Ümraniye Şube",
        "city": "İstanbul",
        "district": "Ümraniye",
        "latitude": 41.0256,
        "longitude": 29.1167,
        "station_type": "branch",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Sancaktepe Lojistik Noktası",
        "city": "İstanbul",
        "district": "Sancaktepe",
        "latitude": 41.0,
        "longitude": 29.23,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Çekmeköy Dağıtım",
        "city": "İstanbul",
        "district": "Çekmeköy",
        "latitude": 41.035,
        "longitude": 29.18,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Beşiktaş Levent Hub",
        "city": "İstanbul",
        "district": "Beşiktaş",
        "latitude": 41.0422,
        "longitude": 29.0067,
        "station_type": "branch",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Şişli Mecidiyeköy Şube",
        "city": "İstanbul",
        "district": "Şişli",
        "latitude": 41.06,
        "longitude": 28.9878,
        "station_type": "branch",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Fatih Tarihi Yarımada",
        "city": "İstanbul",
        "district": "Fatih",
        "latitude": 41.018,
        "longitude": 28.945,
        "station_type": "branch",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Bakırköy Şube",
        "city": "İstanbul",
        "district": "Bakırköy",
        "latitude": 40.9801,
        "longitude": 28.8725,
        "station_type": "branch",
        "daily_capacity": 17000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Zeytinburnu Tekstil Lojistik",
        "city": "İstanbul",
        "district": "Zeytinburnu",
        "latitude": 41.0,
        "longitude": 28.9,
        "station_type": "branch",
        "daily_capacity": 19000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Bağcılar Dağıtım",
        "city": "İstanbul",
        "district": "Bağcılar",
        "latitude": 41.035,
        "longitude": 28.84,
        "station_type": "branch",
        "daily_capacity": 24000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Başakşehir İkitelli OSB Hub",
        "city": "İstanbul",
        "district": "Başakşehir",
        "latitude": 41.0794,
        "longitude": 28.8028,
        "station_type": "hub",
        "daily_capacity": 48000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Esenyurt Lojistik Vadisi",
        "city": "İstanbul",
        "district": "Esenyurt",
        "latitude": 41.0342,
        "longitude": 28.68,
        "station_type": "hub",
        "daily_capacity": 55000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Beylikdüzü Şube",
        "city": "İstanbul",
        "district": "Beylikdüzü",
        "latitude": 41.0,
        "longitude": 28.65,
        "station_type": "branch",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Avcılar Liman Şube",
        "city": "İstanbul",
        "district": "Avcılar",
        "latitude": 40.98,
        "longitude": 28.72,
        "station_type": "branch",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Büyükçekmece Şube",
        "city": "İstanbul",
        "district": "Büyükçekmece",
        "latitude": 41.02,
        "longitude": 28.58,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Sarıyer Maslak Lojistik",
        "city": "İstanbul",
        "district": "Sarıyer",
        "latitude": 41.11,
        "longitude": 29.02,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Silivri Sanayi Dağıtım",
        "city": "İstanbul",
        "district": "Silivri",
        "latitude": 41.07,
        "longitude": 28.25,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "İstanbul - Çatalca Lojistik Köyü",
        "city": "İstanbul",
        "district": "Çatalca",
        "latitude": 41.14,
        "longitude": 28.46,
        "station_type": "hub",
        "daily_capacity": 25000,
        "is_depot": False
    },
    {
        "name": "Ankara - Çankaya Merkez Hub",
        "city": "Ankara",
        "district": "Çankaya",
        "latitude": 39.9208,
        "longitude": 32.8541,
        "station_type": "hub",
        "daily_capacity": 42000,
        "is_depot": False
    },
    {
        "name": "Ankara - Yenimahalle OSTİM OSB",
        "city": "Ankara",
        "district": "Yenimahalle",
        "latitude": 39.97,
        "longitude": 32.74,
        "station_type": "hub",
        "daily_capacity": 38000,
        "is_depot": False
    },
    {
        "name": "Ankara - Keçiören Dağıtım",
        "city": "Ankara",
        "district": "Keçiören",
        "latitude": 40.0,
        "longitude": 32.86,
        "station_type": "branch",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Ankara - Mamak Şube",
        "city": "Ankara",
        "district": "Mamak",
        "latitude": 39.93,
        "longitude": 32.92,
        "station_type": "branch",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Ankara - Sincan 1. OSB Aktarma",
        "city": "Ankara",
        "district": "Sincan",
        "latitude": 39.97,
        "longitude": 32.58,
        "station_type": "hub",
        "daily_capacity": 28000,
        "is_depot": False
    },
    {
        "name": "Ankara - Etimesgut Şube",
        "city": "Ankara",
        "district": "Etimesgut",
        "latitude": 39.95,
        "longitude": 32.68,
        "station_type": "branch",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Ankara - Gölbaşı Lojistik Park",
        "city": "Ankara",
        "district": "Gölbaşı",
        "latitude": 39.79,
        "longitude": 32.81,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Ankara - Kahramankazan Lojistik Üssü",
        "city": "Ankara",
        "district": "Kahramankazan",
        "latitude": 40.2,
        "longitude": 32.68,
        "station_type": "hub",
        "daily_capacity": 40000,
        "is_depot": False
    },
    {
        "name": "Ankara - Pursaklar Dağıtım",
        "city": "Ankara",
        "district": "Pursaklar",
        "latitude": 40.04,
        "longitude": 32.9,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Ankara - Altındağ İskitler",
        "city": "Ankara",
        "district": "Altındağ",
        "latitude": 39.95,
        "longitude": 32.86,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "İzmir - Konak Liman Hub",
        "city": "İzmir",
        "district": "Konak",
        "latitude": 38.4192,
        "longitude": 27.1287,
        "station_type": "hub",
        "daily_capacity": 36000,
        "is_depot": False
    },
    {
        "name": "İzmir - Bornova Lojistik Köyü",
        "city": "İzmir",
        "district": "Bornova",
        "latitude": 38.4697,
        "longitude": 27.2181,
        "station_type": "hub",
        "daily_capacity": 32000,
        "is_depot": False
    },
    {
        "name": "İzmir - Karşıyaka Dağıtım Şubesi",
        "city": "İzmir",
        "district": "Karşıyaka",
        "latitude": 38.4556,
        "longitude": 27.1125,
        "station_type": "branch",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "İzmir - Çiğli Atatürk OSB",
        "city": "İzmir",
        "district": "Çiğli",
        "latitude": 38.49,
        "longitude": 27.05,
        "station_type": "hub",
        "daily_capacity": 24000,
        "is_depot": False
    },
    {
        "name": "İzmir - Gaziemir Ege Serbest Bölge",
        "city": "İzmir",
        "district": "Gaziemir",
        "latitude": 38.32,
        "longitude": 27.13,
        "station_type": "hub",
        "daily_capacity": 26000,
        "is_depot": False
    },
    {
        "name": "İzmir - Buca Dağıtım",
        "city": "İzmir",
        "district": "Buca",
        "latitude": 38.38,
        "longitude": 27.18,
        "station_type": "branch",
        "daily_capacity": 17000,
        "is_depot": False
    },
    {
        "name": "İzmir - Torbalı OSB Lojistik",
        "city": "İzmir",
        "district": "Torbalı",
        "latitude": 38.16,
        "longitude": 27.36,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "İzmir - Aliağa Rafineri & Liman Hub",
        "city": "İzmir",
        "district": "Aliağa",
        "latitude": 38.8,
        "longitude": 26.97,
        "station_type": "hub",
        "daily_capacity": 28000,
        "is_depot": False
    },
    {
        "name": "İzmir - Menemen Plastik İhtisas",
        "city": "İzmir",
        "district": "Menemen",
        "latitude": 38.6,
        "longitude": 27.07,
        "station_type": "branch",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "İzmir - Kemalpaşa Lojistik Vadisi",
        "city": "İzmir",
        "district": "Kemalpaşa",
        "latitude": 38.43,
        "longitude": 27.42,
        "station_type": "hub",
        "daily_capacity": 30000,
        "is_depot": False
    },
    {
        "name": "Bursa - Nilüfer NOSAB Ana Hub",
        "city": "Bursa",
        "district": "Nilüfer",
        "latitude": 40.21,
        "longitude": 28.98,
        "station_type": "hub",
        "daily_capacity": 35000,
        "is_depot": False
    },
    {
        "name": "Bursa - Osmangazi Merkez Şube",
        "city": "Bursa",
        "district": "Osmangazi",
        "latitude": 40.1885,
        "longitude": 29.061,
        "station_type": "branch",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Bursa - Yıldırım Dağıtım",
        "city": "Bursa",
        "district": "Yıldırım",
        "latitude": 40.19,
        "longitude": 29.11,
        "station_type": "branch",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Bursa - Gemlik Serbest Bölge Liman",
        "city": "Bursa",
        "district": "Gemlik",
        "latitude": 40.43,
        "longitude": 29.15,
        "station_type": "hub",
        "daily_capacity": 26000,
        "is_depot": False
    },
    {
        "name": "Bursa - İnegöl Mobilya Sanayi OSB",
        "city": "Bursa",
        "district": "İnegöl",
        "latitude": 40.08,
        "longitude": 29.51,
        "station_type": "hub",
        "daily_capacity": 24000,
        "is_depot": False
    },
    {
        "name": "Bursa - Mudanya İskele Şube",
        "city": "Bursa",
        "district": "Mudanya",
        "latitude": 40.37,
        "longitude": 28.88,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Bursa - Kestel Sanayi",
        "city": "Bursa",
        "district": "Kestel",
        "latitude": 40.2,
        "longitude": 29.21,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Bursa - Karacabey Tarım & Lojistik",
        "city": "Bursa",
        "district": "Karacabey",
        "latitude": 40.21,
        "longitude": 28.36,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Antalya - Muratpaşa Lojistik Hub",
        "city": "Antalya",
        "district": "Muratpaşa",
        "latitude": 36.8841,
        "longitude": 30.7056,
        "station_type": "hub",
        "daily_capacity": 30000,
        "is_depot": False
    },
    {
        "name": "Antalya - Kepez Dağıtım",
        "city": "Antalya",
        "district": "Kepez",
        "latitude": 36.93,
        "longitude": 30.68,
        "station_type": "branch",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Antalya - Konyaaltı Şube",
        "city": "Antalya",
        "district": "Konyaaltı",
        "latitude": 36.87,
        "longitude": 30.63,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Antalya - Alanya Aktarma Merkezi",
        "city": "Antalya",
        "district": "Alanya",
        "latitude": 36.5444,
        "longitude": 31.9954,
        "station_type": "hub",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Antalya - Manavgat Şube",
        "city": "Antalya",
        "district": "Manavgat",
        "latitude": 36.79,
        "longitude": 31.44,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Antalya - Serik Dağıtım",
        "city": "Antalya",
        "district": "Serik",
        "latitude": 36.92,
        "longitude": 31.1,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Antalya - Kumluca Toptancı Hal Lojistik",
        "city": "Antalya",
        "district": "Kumluca",
        "latitude": 36.37,
        "longitude": 30.29,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Antalya - Kaş Dağıtım",
        "city": "Antalya",
        "district": "Kaş",
        "latitude": 36.2,
        "longitude": 29.64,
        "station_type": "branch",
        "daily_capacity": 5000,
        "is_depot": False
    },
    {
        "name": "Adana - Seyhan Merkez Hub",
        "city": "Adana",
        "district": "Seyhan",
        "latitude": 37.0,
        "longitude": 35.3213,
        "station_type": "hub",
        "daily_capacity": 32000,
        "is_depot": False
    },
    {
        "name": "Adana - Yüreğir Dağıtım",
        "city": "Adana",
        "district": "Yüreğir",
        "latitude": 36.98,
        "longitude": 35.35,
        "station_type": "branch",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Adana - Çukurova Şube",
        "city": "Adana",
        "district": "Çukurova",
        "latitude": 37.04,
        "longitude": 35.27,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Adana - Ceyhan Enerji İhtisas Limanı",
        "city": "Adana",
        "district": "Ceyhan",
        "latitude": 37.03,
        "longitude": 35.82,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Mersin - Akdeniz Uluslararası Liman Hub",
        "city": "Mersin",
        "district": "Akdeniz",
        "latitude": 36.8,
        "longitude": 34.6333,
        "station_type": "hub",
        "daily_capacity": 40000,
        "is_depot": False
    },
    {
        "name": "Mersin - Yenişehir Dağıtım",
        "city": "Mersin",
        "district": "Yenişehir",
        "latitude": 36.78,
        "longitude": 34.58,
        "station_type": "branch",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Mersin - Toroslar Şube",
        "city": "Mersin",
        "district": "Toroslar",
        "latitude": 36.83,
        "longitude": 34.6,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Mersin - Tarsus OSB Aktarma",
        "city": "Mersin",
        "district": "Tarsus",
        "latitude": 36.92,
        "longitude": 34.89,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "Mersin - Erdemli Narenciye Lojistik",
        "city": "Mersin",
        "district": "Erdemli",
        "latitude": 36.6,
        "longitude": 34.31,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Mersin - Silifke Şube",
        "city": "Mersin",
        "district": "Silifke",
        "latitude": 36.38,
        "longitude": 33.93,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Konya - Selçuklu Sanayi Hub",
        "city": "Konya",
        "district": "Selçuklu",
        "latitude": 37.8667,
        "longitude": 32.4833,
        "station_type": "hub",
        "daily_capacity": 28000,
        "is_depot": False
    },
    {
        "name": "Konya - Karatay Marangozlar Sanayi",
        "city": "Konya",
        "district": "Karatay",
        "latitude": 37.87,
        "longitude": 32.53,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "Konya - Meram Şube",
        "city": "Konya",
        "district": "Meram",
        "latitude": 37.84,
        "longitude": 32.45,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Konya - Akşehir Dağıtım",
        "city": "Konya",
        "district": "Akşehir",
        "latitude": 38.36,
        "longitude": 31.42,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Konya - Ereğli Şube",
        "city": "Konya",
        "district": "Ereğli",
        "latitude": 37.51,
        "longitude": 34.05,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Kayseri - Melikgazi OSB Hub",
        "city": "Kayseri",
        "district": "Melikgazi",
        "latitude": 38.7312,
        "longitude": 35.4787,
        "station_type": "hub",
        "daily_capacity": 28000,
        "is_depot": False
    },
    {
        "name": "Kayseri - Kocasinan Dağıtım",
        "city": "Kayseri",
        "district": "Kocasinan",
        "latitude": 38.75,
        "longitude": 35.45,
        "station_type": "branch",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Kayseri - Talas Şube",
        "city": "Kayseri",
        "district": "Talas",
        "latitude": 38.69,
        "longitude": 35.55,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Eskişehir - Tepebaşı Lojistik Hub",
        "city": "Eskişehir",
        "district": "Tepebaşı",
        "latitude": 39.7767,
        "longitude": 30.5206,
        "station_type": "hub",
        "daily_capacity": 24000,
        "is_depot": False
    },
    {
        "name": "Eskişehir - Odunpazarı OSB",
        "city": "Eskişehir",
        "district": "Odunpazarı",
        "latitude": 39.76,
        "longitude": 30.55,
        "station_type": "hub",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Eskişehir - Sivrihisar Kavşağı",
        "city": "Eskişehir",
        "district": "Sivrihisar",
        "latitude": 39.45,
        "longitude": 31.53,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Gaziantep - Şehitkamil 1-5 OSB Hub",
        "city": "Gaziantep",
        "district": "Şehitkamil",
        "latitude": 37.0662,
        "longitude": 37.3833,
        "station_type": "hub",
        "daily_capacity": 38000,
        "is_depot": False
    },
    {
        "name": "Gaziantep - Şahinbey Dağıtım",
        "city": "Gaziantep",
        "district": "Şahinbey",
        "latitude": 37.03,
        "longitude": 37.36,
        "station_type": "branch",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Gaziantep - Nizip Fıstık Lojistik",
        "city": "Gaziantep",
        "district": "Nizip",
        "latitude": 37.01,
        "longitude": 37.79,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Haliliye Merkez Hub",
        "city": "Şanlıurfa",
        "district": "Haliliye",
        "latitude": 37.1591,
        "longitude": 38.7969,
        "station_type": "hub",
        "daily_capacity": 24000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Eyyübiye Dağıtım",
        "city": "Şanlıurfa",
        "district": "Eyyübiye",
        "latitude": 37.13,
        "longitude": 38.78,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Karaköprü Şube",
        "city": "Şanlıurfa",
        "district": "Karaköprü",
        "latitude": 37.19,
        "longitude": 38.81,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Siverek Aktarma",
        "city": "Şanlıurfa",
        "district": "Siverek",
        "latitude": 37.7556,
        "longitude": 39.3178,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Birecik Şube",
        "city": "Şanlıurfa",
        "district": "Birecik",
        "latitude": 37.03,
        "longitude": 37.98,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Diyarbakır - Bağlar Lojistik Hub",
        "city": "Diyarbakır",
        "district": "Bağlar",
        "latitude": 37.9144,
        "longitude": 40.2306,
        "station_type": "hub",
        "daily_capacity": 26000,
        "is_depot": False
    },
    {
        "name": "Diyarbakır - Kayapınar Dağıtım",
        "city": "Diyarbakır",
        "district": "Kayapınar",
        "latitude": 37.95,
        "longitude": 40.18,
        "station_type": "branch",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Diyarbakır - Yenişehir Şube",
        "city": "Diyarbakır",
        "district": "Yenişehir",
        "latitude": 37.92,
        "longitude": 40.21,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Diyarbakır - Ergani Şube",
        "city": "Diyarbakır",
        "district": "Ergani",
        "latitude": 38.27,
        "longitude": 39.76,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Diyarbakır - Bismil Pamuk Lojistik",
        "city": "Diyarbakır",
        "district": "Bismil",
        "latitude": 37.85,
        "longitude": 40.66,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Batman - Merkez Hub",
        "city": "Batman",
        "district": "Merkez",
        "latitude": 37.8812,
        "longitude": 41.1293,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Mardin - Artuklu Hub",
        "city": "Mardin",
        "district": "Artuklu",
        "latitude": 37.3212,
        "longitude": 40.7245,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Mardin - Kızıltepe Hub",
        "city": "Mardin",
        "district": "Kızıltepe",
        "latitude": 37.1944,
        "longitude": 40.5878,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Mardin - Nusaybin Sınır Kapısı",
        "city": "Mardin",
        "district": "Nusaybin",
        "latitude": 37.07,
        "longitude": 41.21,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Samsun - İlkadım Liman Hub",
        "city": "Samsun",
        "district": "İlkadım",
        "latitude": 41.2928,
        "longitude": 36.3313,
        "station_type": "hub",
        "daily_capacity": 28000,
        "is_depot": False
    },
    {
        "name": "Samsun - Tekkeköy Lojistik Köyü",
        "city": "Samsun",
        "district": "Tekkeköy",
        "latitude": 41.23,
        "longitude": 36.45,
        "station_type": "hub",
        "daily_capacity": 30000,
        "is_depot": False
    },
    {
        "name": "Samsun - Atakum Dağıtım",
        "city": "Samsun",
        "district": "Atakum",
        "latitude": 41.33,
        "longitude": 36.27,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Samsun - Bafra Şube",
        "city": "Samsun",
        "district": "Bafra",
        "latitude": 41.56,
        "longitude": 35.9,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Samsun - Çarşamba Şube",
        "city": "Samsun",
        "district": "Çarşamba",
        "latitude": 41.2,
        "longitude": 36.72,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Trabzon - Ortahisar Liman Hub",
        "city": "Trabzon",
        "district": "Ortahisar",
        "latitude": 41.0027,
        "longitude": 39.7167,
        "station_type": "hub",
        "daily_capacity": 24000,
        "is_depot": False
    },
    {
        "name": "Trabzon - Akçaabat Dağıtım",
        "city": "Trabzon",
        "district": "Akçaabat",
        "latitude": 41.02,
        "longitude": 39.57,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Trabzon - Yomra Lojistik Park",
        "city": "Trabzon",
        "district": "Yomra",
        "latitude": 40.96,
        "longitude": 39.85,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Ordu - Altınordu Dağıtım Hub",
        "city": "Ordu",
        "district": "Altınordu",
        "latitude": 40.9839,
        "longitude": 37.8764,
        "station_type": "hub",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Ordu - Ünye Liman Şube",
        "city": "Ordu",
        "district": "Ünye",
        "latitude": 41.13,
        "longitude": 37.28,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Ordu - Fatsa Sanayi",
        "city": "Ordu",
        "district": "Fatsa",
        "latitude": 41.03,
        "longitude": 37.5,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Giresun - Merkez Hub",
        "city": "Giresun",
        "district": "Merkez",
        "latitude": 40.9128,
        "longitude": 38.3895,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Rize - Merkez Liman Hub",
        "city": "Rize",
        "district": "Merkez",
        "latitude": 41.0201,
        "longitude": 40.5234,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Rize - Çayeli Dağıtım",
        "city": "Rize",
        "district": "Çayeli",
        "latitude": 41.09,
        "longitude": 40.72,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Artvin - Merkez Şube",
        "city": "Artvin",
        "district": "Merkez",
        "latitude": 41.1828,
        "longitude": 41.8183,
        "station_type": "branch",
        "daily_capacity": 5000,
        "is_depot": False
    },
    {
        "name": "Artvin - Hopa Liman Sınır Hub",
        "city": "Artvin",
        "district": "Hopa",
        "latitude": 41.4,
        "longitude": 41.43,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Zonguldak - Merkez Liman",
        "city": "Zonguldak",
        "district": "Merkez",
        "latitude": 41.4564,
        "longitude": 31.7987,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Zonguldak - Kdz. Ereğli Erdemir Hub",
        "city": "Zonguldak",
        "district": "Kdz. Ereğli",
        "latitude": 41.28,
        "longitude": 31.42,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Karabük - Safranbolu & KARDEMİR",
        "city": "Karabük",
        "district": "Merkez",
        "latitude": 41.2061,
        "longitude": 32.6204,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Bartın - Merkez Liman",
        "city": "Bartın",
        "district": "Merkez",
        "latitude": 41.6344,
        "longitude": 32.3375,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Kastamonu - Merkez Hub",
        "city": "Kastamonu",
        "district": "Merkez",
        "latitude": 41.3887,
        "longitude": 33.7827,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Sinop - Merkez Şube",
        "city": "Sinop",
        "district": "Merkez",
        "latitude": 42.0231,
        "longitude": 35.1531,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Bolu - Merkez Dağıtım Hub",
        "city": "Bolu",
        "district": "Merkez",
        "latitude": 40.7392,
        "longitude": 31.6089,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Bolu - Gerede Kavşak Deposu",
        "city": "Bolu",
        "district": "Gerede",
        "latitude": 40.8,
        "longitude": 32.2,
        "station_type": "hub",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Düzce - Merkez OSB Hub",
        "city": "Düzce",
        "district": "Merkez",
        "latitude": 40.8438,
        "longitude": 31.1565,
        "station_type": "hub",
        "daily_capacity": 17000,
        "is_depot": False
    },
    {
        "name": "Amasya - Merkez",
        "city": "Amasya",
        "district": "Merkez",
        "latitude": 40.6501,
        "longitude": 35.8353,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Çorum - Merkez OSB",
        "city": "Çorum",
        "district": "Merkez",
        "latitude": 40.5506,
        "longitude": 34.9556,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Tokat - Merkez",
        "city": "Tokat",
        "district": "Merkez",
        "latitude": 40.3167,
        "longitude": 36.55,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Gümüşhane - Merkez",
        "city": "Gümüşhane",
        "district": "Merkez",
        "latitude": 40.46,
        "longitude": 39.47,
        "station_type": "branch",
        "daily_capacity": 4000,
        "is_depot": False
    },
    {
        "name": "Bayburt - Merkez",
        "city": "Bayburt",
        "district": "Merkez",
        "latitude": 40.2552,
        "longitude": 40.2249,
        "station_type": "branch",
        "daily_capacity": 3000,
        "is_depot": False
    },
    {
        "name": "Manisa - Yunusemre MOSB Ana Hub",
        "city": "Manisa",
        "district": "Yunusemre",
        "latitude": 38.6191,
        "longitude": 27.4289,
        "station_type": "hub",
        "daily_capacity": 30000,
        "is_depot": False
    },
    {
        "name": "Manisa - Şehzadeler Dağıtım",
        "city": "Manisa",
        "district": "Şehzadeler",
        "latitude": 38.61,
        "longitude": 27.44,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Manisa - Turgutlu OSB",
        "city": "Manisa",
        "district": "Turgutlu",
        "latitude": 38.5,
        "longitude": 27.7,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Manisa - Salihli Şube",
        "city": "Manisa",
        "district": "Salihli",
        "latitude": 38.48,
        "longitude": 28.14,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Manisa - Akhisar Zeytin & Gıda",
        "city": "Manisa",
        "district": "Akhisar",
        "latitude": 38.92,
        "longitude": 27.84,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Manisa - Soma Sanayi",
        "city": "Manisa",
        "district": "Soma",
        "latitude": 39.18,
        "longitude": 27.61,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Aydın - Efeler Dağıtım Hub",
        "city": "Aydın",
        "district": "Efeler",
        "latitude": 37.856,
        "longitude": 27.8416,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Aydın - Kuşadası Liman Şube",
        "city": "Aydın",
        "district": "Kuşadası",
        "latitude": 37.86,
        "longitude": 27.26,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Aydın - Nazilli Ticaret Merkezi",
        "city": "Aydın",
        "district": "Nazilli",
        "latitude": 37.91,
        "longitude": 28.32,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Aydın - Söke Tarım & Sanayi",
        "city": "Aydın",
        "district": "Söke",
        "latitude": 37.75,
        "longitude": 27.41,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Aydın - Didim Turizm Şube",
        "city": "Aydın",
        "district": "Didim",
        "latitude": 37.38,
        "longitude": 27.26,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Denizli - Pamukkale Tekstil Hub",
        "city": "Denizli",
        "district": "Pamukkale",
        "latitude": 37.7765,
        "longitude": 29.0864,
        "station_type": "hub",
        "daily_capacity": 26000,
        "is_depot": False
    },
    {
        "name": "Denizli - Merkezefendi Sanayi",
        "city": "Denizli",
        "district": "Merkezefendi",
        "latitude": 37.78,
        "longitude": 29.04,
        "station_type": "branch",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Denizli - Sarayköy Jeotermal",
        "city": "Denizli",
        "district": "Sarayköy",
        "latitude": 37.92,
        "longitude": 28.93,
        "station_type": "branch",
        "daily_capacity": 5000,
        "is_depot": False
    },
    {
        "name": "Muğla - Menteşe Merkez",
        "city": "Muğla",
        "district": "Menteşe",
        "latitude": 37.2153,
        "longitude": 28.3636,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Muğla - Bodrum Lojistik Hub",
        "city": "Muğla",
        "district": "Bodrum",
        "latitude": 37.0344,
        "longitude": 27.4305,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "Muğla - Fethiye Aktarma",
        "city": "Muğla",
        "district": "Fethiye",
        "latitude": 36.65,
        "longitude": 29.12,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Muğla - Marmaris Marina Şube",
        "city": "Muğla",
        "district": "Marmaris",
        "latitude": 36.85,
        "longitude": 28.27,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Muğla - Milas Sanayi",
        "city": "Muğla",
        "district": "Milas",
        "latitude": 37.31,
        "longitude": 27.78,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Balıkesir - Altıeylül Merkez Hub",
        "city": "Balıkesir",
        "district": "Altıeylül",
        "latitude": 39.6484,
        "longitude": 27.8826,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Balıkesir - Bandırma Liman Lojistik",
        "city": "Balıkesir",
        "district": "Bandırma",
        "latitude": 40.3522,
        "longitude": 27.9767,
        "station_type": "hub",
        "daily_capacity": 24000,
        "is_depot": False
    },
    {
        "name": "Balıkesir - Edremit Körfez Şube",
        "city": "Balıkesir",
        "district": "Edremit",
        "latitude": 39.59,
        "longitude": 27.02,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Balıkesir - Ayvalık Şube",
        "city": "Balıkesir",
        "district": "Ayvalık",
        "latitude": 39.32,
        "longitude": 26.69,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Çanakkale - Merkez Şube",
        "city": "Çanakkale",
        "district": "Merkez",
        "latitude": 40.1553,
        "longitude": 26.4142,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Çanakkale - Biga Sanayi Hub",
        "city": "Çanakkale",
        "district": "Biga",
        "latitude": 40.23,
        "longitude": 27.24,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Afyonkarahisar - Merkez Mermer Hub",
        "city": "Afyonkarahisar",
        "district": "Merkez",
        "latitude": 38.7507,
        "longitude": 30.5567,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Afyonkarahisar - Sandıklı Şube",
        "city": "Afyonkarahisar",
        "district": "Sandıklı",
        "latitude": 38.46,
        "longitude": 30.27,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Kütahya - Merkez Porselen Hub",
        "city": "Kütahya",
        "district": "Merkez",
        "latitude": 39.4167,
        "longitude": 29.9833,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Kütahya - Tavşanlı Linyit",
        "city": "Kütahya",
        "district": "Tavşanlı",
        "latitude": 39.54,
        "longitude": 29.49,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Uşak - Merkez Tekstil Hub",
        "city": "Uşak",
        "district": "Merkez",
        "latitude": 38.6823,
        "longitude": 29.4082,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Erzurum - Yakutiye Bölge Hub",
        "city": "Erzurum",
        "district": "Yakutiye",
        "latitude": 39.9,
        "longitude": 41.27,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "Erzurum - Palandöken Dağıtım",
        "city": "Erzurum",
        "district": "Palandöken",
        "latitude": 39.87,
        "longitude": 41.25,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Malatya - Yeşilyurt OSB Hub",
        "city": "Malatya",
        "district": "Yeşilyurt",
        "latitude": 38.3552,
        "longitude": 38.3095,
        "station_type": "hub",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Malatya - Battalgazi Şube",
        "city": "Malatya",
        "district": "Battalgazi",
        "latitude": 38.36,
        "longitude": 38.36,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Elazığ - Merkez OSB Hub",
        "city": "Elazığ",
        "district": "Merkez",
        "latitude": 38.681,
        "longitude": 39.2264,
        "station_type": "hub",
        "daily_capacity": 17000,
        "is_depot": False
    },
    {
        "name": "Van - İpekyolu Bölge Hub",
        "city": "Van",
        "district": "İpekyolu",
        "latitude": 38.4891,
        "longitude": 43.4089,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "Van - Tuşba Dağıtım",
        "city": "Van",
        "district": "Tuşba",
        "latitude": 38.55,
        "longitude": 43.37,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Van - Erciş Şube",
        "city": "Van",
        "district": "Erciş",
        "latitude": 39.03,
        "longitude": 43.36,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Erzincan - Merkez Hub",
        "city": "Erzincan",
        "district": "Merkez",
        "latitude": 39.75,
        "longitude": 39.5,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Kars - Merkez Lojistik Köy Hub",
        "city": "Kars",
        "district": "Merkez",
        "latitude": 40.6167,
        "longitude": 43.1,
        "station_type": "hub",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Ağrı - Merkez Dağıtım",
        "city": "Ağrı",
        "district": "Merkez",
        "latitude": 39.7191,
        "longitude": 43.0503,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Ağrı - Doğubayazıt Gürbulak Hub",
        "city": "Ağrı",
        "district": "Doğubayazıt",
        "latitude": 39.55,
        "longitude": 44.08,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Iğdır - Merkez Dilucu Hub",
        "city": "Iğdır",
        "district": "Merkez",
        "latitude": 39.9167,
        "longitude": 44.0333,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Ardahan - Merkez",
        "city": "Ardahan",
        "district": "Merkez",
        "latitude": 41.1105,
        "longitude": 42.7022,
        "station_type": "branch",
        "daily_capacity": 4000,
        "is_depot": False
    },
    {
        "name": "Muş - Merkez",
        "city": "Muş",
        "district": "Merkez",
        "latitude": 38.7432,
        "longitude": 41.5064,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Bitlis - Tatvan Feribot & Hub",
        "city": "Bitlis",
        "district": "Tatvan",
        "latitude": 38.5,
        "longitude": 42.28,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Bingöl - Merkez",
        "city": "Bingöl",
        "district": "Merkez",
        "latitude": 38.8854,
        "longitude": 40.4983,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Tunceli - Merkez",
        "city": "Tunceli",
        "district": "Merkez",
        "latitude": 39.1079,
        "longitude": 39.5401,
        "station_type": "branch",
        "daily_capacity": 4000,
        "is_depot": False
    },
    {
        "name": "Hakkari - Yüksekova Sınır Hub",
        "city": "Hakkari",
        "district": "Yüksekova",
        "latitude": 37.5736,
        "longitude": 44.2872,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Hakkari - Merkez",
        "city": "Hakkari",
        "district": "Merkez",
        "latitude": 37.58,
        "longitude": 43.74,
        "station_type": "branch",
        "daily_capacity": 5000,
        "is_depot": False
    },
    {
        "name": "Şırnak - Cizre İpekyolu Hub",
        "city": "Şırnak",
        "district": "Cizre",
        "latitude": 37.33,
        "longitude": 42.19,
        "station_type": "hub",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Şırnak - Silopi Habur Kapısı Hub",
        "city": "Şırnak",
        "district": "Silopi",
        "latitude": 37.17,
        "longitude": 42.47,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Siirt - Merkez",
        "city": "Siirt",
        "district": "Merkez",
        "latitude": 37.9333,
        "longitude": 41.95,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Adıyaman - Merkez OSB",
        "city": "Adıyaman",
        "district": "Merkez",
        "latitude": 37.7648,
        "longitude": 38.2786,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Adıyaman - Kahta Şube",
        "city": "Adıyaman",
        "district": "Kahta",
        "latitude": 37.78,
        "longitude": 38.62,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Kilis - Öncüpınar Sınır Hub",
        "city": "Kilis",
        "district": "Merkez",
        "latitude": 36.7184,
        "longitude": 37.1212,
        "station_type": "hub",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Osmaniye - Merkez OSB Hub",
        "city": "Osmaniye",
        "district": "Merkez",
        "latitude": 37.0742,
        "longitude": 36.2478,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Osmaniye - Kadirli Şube",
        "city": "Osmaniye",
        "district": "Kadirli",
        "latitude": 37.37,
        "longitude": 36.1,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Kahramanmaraş - Onikişubat Tekstil Hub",
        "city": "Kahramanmaraş",
        "district": "Onikişubat",
        "latitude": 37.5858,
        "longitude": 36.9371,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "Kahramanmaraş - Dulkadiroğlu Dağıtım",
        "city": "Kahramanmaraş",
        "district": "Dulkadiroğlu",
        "latitude": 37.58,
        "longitude": 36.96,
        "station_type": "branch",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Kahramanmaraş - Elbistan Şube",
        "city": "Kahramanmaraş",
        "district": "Elbistan",
        "latitude": 38.2,
        "longitude": 37.19,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Hatay - Antakya Merkez",
        "city": "Hatay",
        "district": "Antakya",
        "latitude": 36.2023,
        "longitude": 36.1606,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Hatay - İskenderun Demir Çelik Liman",
        "city": "Hatay",
        "district": "İskenderun",
        "latitude": 36.5872,
        "longitude": 36.1736,
        "station_type": "hub",
        "daily_capacity": 25000,
        "is_depot": False
    },
    {
        "name": "Hatay - Dörtyol Petrol Terminali",
        "city": "Hatay",
        "district": "Dörtyol",
        "latitude": 36.85,
        "longitude": 36.22,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Hatay - Samandağ Şube",
        "city": "Hatay",
        "district": "Samandağ",
        "latitude": 36.08,
        "longitude": 35.98,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Tekirdağ - Çorlu Havalimanı Lojistik Üssü",
        "city": "Tekirdağ",
        "district": "Çorlu",
        "latitude": 41.16,
        "longitude": 27.8,
        "station_type": "hub",
        "daily_capacity": 32000,
        "is_depot": False
    },
    {
        "name": "Tekirdağ - Çerkezköy Sanayi Hub",
        "city": "Tekirdağ",
        "district": "Çerkezköy",
        "latitude": 41.29,
        "longitude": 28.0,
        "station_type": "hub",
        "daily_capacity": 28000,
        "is_depot": False
    },
    {
        "name": "Tekirdağ - Süleymanpaşa Asyaport Liman",
        "city": "Tekirdağ",
        "district": "Süleymanpaşa",
        "latitude": 40.9781,
        "longitude": 27.5117,
        "station_type": "hub",
        "daily_capacity": 22000,
        "is_depot": False
    },
    {
        "name": "Tekirdağ - Kapaklı Şube",
        "city": "Tekirdağ",
        "district": "Kapaklı",
        "latitude": 41.32,
        "longitude": 27.97,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Edirne - Kapıkule Tır Parkı & Hub",
        "city": "Edirne",
        "district": "Merkez",
        "latitude": 41.6772,
        "longitude": 26.5557,
        "station_type": "hub",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Edirne - Keşan Kavşak Şube",
        "city": "Edirne",
        "district": "Keşan",
        "latitude": 40.85,
        "longitude": 26.63,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Kırklareli - Lüleburgaz Tekstil Sanayi",
        "city": "Kırklareli",
        "district": "Lüleburgaz",
        "latitude": 41.405,
        "longitude": 27.355,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Kırklareli - Dereköy Sınır Kapısı",
        "city": "Kırklareli",
        "district": "Merkez",
        "latitude": 41.7355,
        "longitude": 27.2252,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Yalova - Tersaneler & Ro-Ro Liman",
        "city": "Yalova",
        "district": "Merkez",
        "latitude": 40.655,
        "longitude": 29.2769,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Yalova - Altınova Tersaneler",
        "city": "Yalova",
        "district": "Altınova",
        "latitude": 40.7,
        "longitude": 29.5,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Bilecik - Bozüyük Seramik Hub",
        "city": "Bilecik",
        "district": "Bozüyük",
        "latitude": 39.91,
        "longitude": 30.04,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Bilecik - Merkez",
        "city": "Bilecik",
        "district": "Merkez",
        "latitude": 40.1426,
        "longitude": 29.9793,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Sakarya - Adapazarı Merkez Hub",
        "city": "Sakarya",
        "district": "Adapazarı",
        "latitude": 40.7731,
        "longitude": 30.4028,
        "station_type": "hub",
        "daily_capacity": 26000,
        "is_depot": False
    },
    {
        "name": "Sakarya - Serdivan Dağıtım",
        "city": "Sakarya",
        "district": "Serdivan",
        "latitude": 40.76,
        "longitude": 30.36,
        "station_type": "branch",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Sakarya - Hendek 2. OSB",
        "city": "Sakarya",
        "district": "Hendek",
        "latitude": 40.8,
        "longitude": 30.75,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Sakarya - Arifiye YHT & Otomotiv Hub",
        "city": "Sakarya",
        "district": "Arifiye",
        "latitude": 40.71,
        "longitude": 30.36,
        "station_type": "hub",
        "daily_capacity": 20000,
        "is_depot": False
    },
    {
        "name": "Sakarya - Akyazı Şube",
        "city": "Sakarya",
        "district": "Akyazı",
        "latitude": 40.68,
        "longitude": 30.62,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Sakarya - Karasu Liman & Serbest Bölge",
        "city": "Sakarya",
        "district": "Karasu",
        "latitude": 41.07,
        "longitude": 30.69,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Sivas - Merkez OSB Hub",
        "city": "Sivas",
        "district": "Merkez",
        "latitude": 39.7477,
        "longitude": 37.0179,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Aksaray - Merkez Mercedes Kamyon Hub",
        "city": "Aksaray",
        "district": "Merkez",
        "latitude": 38.3687,
        "longitude": 34.037,
        "station_type": "hub",
        "daily_capacity": 18000,
        "is_depot": False
    },
    {
        "name": "Kırıkkale - MKEK Sanayi Hub",
        "city": "Kırıkkale",
        "district": "Merkez",
        "latitude": 39.8468,
        "longitude": 33.5153,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Kırşehir - Petlas Lastik Hub",
        "city": "Kırşehir",
        "district": "Merkez",
        "latitude": 39.1425,
        "longitude": 34.1709,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Nevşehir - Kapadokya Lojistik",
        "city": "Nevşehir",
        "district": "Merkez",
        "latitude": 38.6244,
        "longitude": 34.7144,
        "station_type": "branch",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Niğde - Merkez OSB",
        "city": "Niğde",
        "district": "Merkez",
        "latitude": 37.9667,
        "longitude": 34.6833,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Karaman - Bisküvi & Gıda Sanayi Hub",
        "city": "Karaman",
        "district": "Merkez",
        "latitude": 37.1759,
        "longitude": 33.2287,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Yozgat - Merkez",
        "city": "Yozgat",
        "district": "Merkez",
        "latitude": 39.8181,
        "longitude": 34.8147,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Çankırı - Sumitomo Lastik Hub",
        "city": "Çankırı",
        "district": "Merkez",
        "latitude": 40.6013,
        "longitude": 33.6134,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Isparta - Merkez Gül Lojistik",
        "city": "Isparta",
        "district": "Merkez",
        "latitude": 37.7648,
        "longitude": 30.5566,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Burdur - Merkez Mermer",
        "city": "Burdur",
        "district": "Merkez",
        "latitude": 37.7203,
        "longitude": 30.2908,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "İzmir - Bergama Batı Anadolu OSB",
        "city": "İzmir",
        "district": "Bergama",
        "latitude": 39.12,
        "longitude": 27.18,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "İzmir - Dikili Liman",
        "city": "İzmir",
        "district": "Dikili",
        "latitude": 39.07,
        "longitude": 26.89,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "İzmir - Foça Şube",
        "city": "İzmir",
        "district": "Foça",
        "latitude": 38.67,
        "longitude": 26.76,
        "station_type": "branch",
        "daily_capacity": 5000,
        "is_depot": False
    },
    {
        "name": "Manisa - Kula Jeopark",
        "city": "Manisa",
        "district": "Kula",
        "latitude": 38.54,
        "longitude": 28.65,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Aydın - Çine Maden Lojistik",
        "city": "Aydın",
        "district": "Çine",
        "latitude": 37.61,
        "longitude": 28.06,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Muğla - Yatağan Termik & Mermer",
        "city": "Muğla",
        "district": "Yatağan",
        "latitude": 37.34,
        "longitude": 28.14,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Muğla - Ortaca & Dalaman Kargo",
        "city": "Muğla",
        "district": "Ortaca",
        "latitude": 36.83,
        "longitude": 28.77,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Antalya - Finike Narenciye Hub",
        "city": "Antalya",
        "district": "Finike",
        "latitude": 36.29,
        "longitude": 30.14,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Antalya - Gazipaşa Havalimanı Lojistik",
        "city": "Antalya",
        "district": "Gazipaşa",
        "latitude": 36.27,
        "longitude": 32.31,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Mersin - Anamur Muz & Yaş Meyve",
        "city": "Mersin",
        "district": "Anamur",
        "latitude": 36.07,
        "longitude": 32.83,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Hatay - Reyhanlı Cilvegözü Sınır Hub",
        "city": "Hatay",
        "district": "Reyhanlı",
        "latitude": 36.27,
        "longitude": 36.57,
        "station_type": "hub",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Hatay - Payas Liman & Haddehane",
        "city": "Hatay",
        "district": "Payas",
        "latitude": 36.75,
        "longitude": 36.21,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Gaziantep - Oğuzeli Havalimanı Kargo",
        "city": "Gaziantep",
        "district": "Oğuzeli",
        "latitude": 36.96,
        "longitude": 37.51,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Kilis - Elbeyli Çobanbey Kapısı",
        "city": "Kilis",
        "district": "Elbeyli",
        "latitude": 36.67,
        "longitude": 37.47,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Kayseri - İncesu OSB",
        "city": "Kayseri",
        "district": "İncesu",
        "latitude": 38.63,
        "longitude": 35.19,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Afyonkarahisar - Dinar Kavşak Şube",
        "city": "Afyonkarahisar",
        "district": "Dinar",
        "latitude": 38.06,
        "longitude": 30.16,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Balıkesir - Gönen Deri & Gıda",
        "city": "Balıkesir",
        "district": "Gönen",
        "latitude": 40.1,
        "longitude": 27.65,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Balıkesir - Burhaniye Şube",
        "city": "Balıkesir",
        "district": "Burhaniye",
        "latitude": 39.5,
        "longitude": 26.97,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Çanakkale - Çan Seramik Sanayi",
        "city": "Çanakkale",
        "district": "Çan",
        "latitude": 40.03,
        "longitude": 27.05,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Çanakkale - Gelibolu İskele",
        "city": "Çanakkale",
        "district": "Gelibolu",
        "latitude": 40.41,
        "longitude": 26.67,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Yalova - Çınarcık Şube",
        "city": "Yalova",
        "district": "Çınarcık",
        "latitude": 40.64,
        "longitude": 29.12,
        "station_type": "branch",
        "daily_capacity": 5000,
        "is_depot": False
    },
    {
        "name": "Düzce - Akçakoca Liman",
        "city": "Düzce",
        "district": "Akçakoca",
        "latitude": 41.08,
        "longitude": 31.11,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Bolu - Mengen Şube",
        "city": "Bolu",
        "district": "Mengen",
        "latitude": 40.95,
        "longitude": 32.06,
        "station_type": "branch",
        "daily_capacity": 4000,
        "is_depot": False
    },
    {
        "name": "Kastamonu - Tosya Ahşap & Sanayi Hub",
        "city": "Kastamonu",
        "district": "Tosya",
        "latitude": 41.01,
        "longitude": 34.04,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Samsun - Havza OSB",
        "city": "Samsun",
        "district": "Havza",
        "latitude": 40.97,
        "longitude": 35.66,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Rize - Ardeşen Dağıtım",
        "city": "Rize",
        "district": "Ardeşen",
        "latitude": 41.19,
        "longitude": 40.98,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Trabzon - Sürmene Tersaneler",
        "city": "Trabzon",
        "district": "Sürmene",
        "latitude": 40.91,
        "longitude": 40.12,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Erzurum - Oltu Şube",
        "city": "Erzurum",
        "district": "Oltu",
        "latitude": 40.55,
        "longitude": 41.99,
        "station_type": "branch",
        "daily_capacity": 5000,
        "is_depot": False
    },
    {
        "name": "Konya - Beyşehir Hub",
        "city": "Konya",
        "district": "Beyşehir",
        "latitude": 37.68,
        "longitude": 31.72,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Konya - Seydişehir Alüminyum Hub",
        "city": "Konya",
        "district": "Seydişehir",
        "latitude": 37.42,
        "longitude": 31.84,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Konya - Cihanbeyli Tuz & Lojistik",
        "city": "Konya",
        "district": "Cihanbeyli",
        "latitude": 38.65,
        "longitude": 32.92,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Konya - Kulu Ankara Yolu Hub",
        "city": "Konya",
        "district": "Kulu",
        "latitude": 39.09,
        "longitude": 33.08,
        "station_type": "hub",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Konya - Karapınar Güneş Enerjisi & Tarım",
        "city": "Konya",
        "district": "Karapınar",
        "latitude": 37.71,
        "longitude": 33.55,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Konya - Çumra Şeker & Tarım Hub",
        "city": "Konya",
        "district": "Çumra",
        "latitude": 37.57,
        "longitude": 32.77,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Konya - Ilgın Termal & Dağıtım",
        "city": "Konya",
        "district": "Ilgın",
        "latitude": 38.28,
        "longitude": 31.91,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Konya - Kadınhanı Hub",
        "city": "Konya",
        "district": "Kadınhanı",
        "latitude": 38.24,
        "longitude": 32.21,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Konya - Çeltik Dağıtım",
        "city": "Konya",
        "district": "Çeltik",
        "latitude": 39.03,
        "longitude": 31.78,
        "station_type": "branch",
        "daily_capacity": 5000,
        "is_depot": False
    },
    {
        "name": "Sivas - Şarkışla Canlı Hayvan & Tarım Hub",
        "city": "Sivas",
        "district": "Şarkışla",
        "latitude": 39.42,
        "longitude": 36.41,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Sivas - Divriği Maden Hub",
        "city": "Sivas",
        "district": "Divriği",
        "latitude": 39.37,
        "longitude": 38.12,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Sivas - Suşehri Doğu Karadeniz Geçişi",
        "city": "Sivas",
        "district": "Suşehri",
        "latitude": 40.16,
        "longitude": 38.08,
        "station_type": "hub",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Sivas - Kangal Termik & Lojistik",
        "city": "Sivas",
        "district": "Kangal",
        "latitude": 39.23,
        "longitude": 37.39,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Sivas - Zara Bal & Dağıtım",
        "city": "Sivas",
        "district": "Zara",
        "latitude": 39.89,
        "longitude": 37.76,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Sivas - Gemerek OSB",
        "city": "Sivas",
        "district": "Gemerek",
        "latitude": 39.18,
        "longitude": 36.07,
        "station_type": "branch",
        "daily_capacity": 6500,
        "is_depot": False
    },
    {
        "name": "Yozgat - Sorgun OSB & Dağıtım Hub",
        "city": "Yozgat",
        "district": "Sorgun",
        "latitude": 39.81,
        "longitude": 35.18,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Yozgat - Yerköy Hızlı Tren Lojistik",
        "city": "Yozgat",
        "district": "Yerköy",
        "latitude": 39.64,
        "longitude": 34.47,
        "station_type": "hub",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Yozgat - Boğazlıyan Şeker & Sanayi",
        "city": "Yozgat",
        "district": "Boğazlıyan",
        "latitude": 39.19,
        "longitude": 35.25,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Yozgat - Akdağmadeni Orman Ürünleri",
        "city": "Yozgat",
        "district": "Akdağmadeni",
        "latitude": 39.66,
        "longitude": 35.88,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Aksaray - Ortaköy Tarım Dağıtım",
        "city": "Aksaray",
        "district": "Ortaköy",
        "latitude": 38.74,
        "longitude": 34.04,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Aksaray - Eskil Tuz Gölü Hub",
        "city": "Aksaray",
        "district": "Eskil",
        "latitude": 38.58,
        "longitude": 33.41,
        "station_type": "branch",
        "daily_capacity": 6500,
        "is_depot": False
    },
    {
        "name": "Aksaray - Sultanhanı İpekyolu Kervanı",
        "city": "Aksaray",
        "district": "Sultanhanı",
        "latitude": 38.25,
        "longitude": 33.54,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Niğde - Bor Karma OSB Hub",
        "city": "Niğde",
        "district": "Bor",
        "latitude": 37.89,
        "longitude": 34.56,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Niğde - Ulukışla Lojistik Kavşağı",
        "city": "Niğde",
        "district": "Ulukışla",
        "latitude": 37.54,
        "longitude": 34.48,
        "station_type": "hub",
        "daily_capacity": 9500,
        "is_depot": False
    },
    {
        "name": "Nevşehir - Ürgüp Turizm & Kargo Hub",
        "city": "Nevşehir",
        "district": "Ürgüp",
        "latitude": 38.63,
        "longitude": 34.91,
        "station_type": "hub",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Nevşehir - Avanos Seramik & Sanayi",
        "city": "Nevşehir",
        "district": "Avanos",
        "latitude": 38.71,
        "longitude": 34.84,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Nevşehir - Derinkuyu Patates Depoları",
        "city": "Nevşehir",
        "district": "Derinkuyu",
        "latitude": 38.37,
        "longitude": 34.73,
        "station_type": "branch",
        "daily_capacity": 7500,
        "is_depot": False
    },
    {
        "name": "Kırşehir - Kaman Ceviz & Dağıtım Hub",
        "city": "Kırşehir",
        "district": "Kaman",
        "latitude": 39.36,
        "longitude": 33.72,
        "station_type": "hub",
        "daily_capacity": 8500,
        "is_depot": False
    },
    {
        "name": "Kırşehir - Mucur Hub",
        "city": "Kırşehir",
        "district": "Mucur",
        "latitude": 39.06,
        "longitude": 34.37,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Karaman - Ermenek Maden & Tarım",
        "city": "Karaman",
        "district": "Ermenek",
        "latitude": 36.63,
        "longitude": 32.89,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Karaman - Kazımkarabekir Hub",
        "city": "Karaman",
        "district": "Kazımkarabekir",
        "latitude": 37.23,
        "longitude": 33.02,
        "station_type": "branch",
        "daily_capacity": 5500,
        "is_depot": False
    },
    {
        "name": "Ankara - Polatlı Tahıl Borsası Hub",
        "city": "Ankara",
        "district": "Polatlı",
        "latitude": 39.58,
        "longitude": 32.14,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Ankara - Şereflikoçhisar Tuz & Lojistik",
        "city": "Ankara",
        "district": "Şereflikoçhisar",
        "latitude": 38.94,
        "longitude": 33.54,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Ankara - Beypazarı Maden Suyu & Sanayi",
        "city": "Ankara",
        "district": "Beypazarı",
        "latitude": 40.16,
        "longitude": 31.92,
        "station_type": "hub",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Ankara - Çubuk Dağıtım",
        "city": "Ankara",
        "district": "Çubuk",
        "latitude": 40.24,
        "longitude": 33.03,
        "station_type": "branch",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Kırıkkale - Yahşihan Sanayi Hub",
        "city": "Kırıkkale",
        "district": "Yahşihan",
        "latitude": 39.83,
        "longitude": 33.45,
        "station_type": "hub",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Kırıkkale - Keskin Hub",
        "city": "Kırıkkale",
        "district": "Keskin",
        "latitude": 39.67,
        "longitude": 33.61,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Çankırı - Ilgaz Dağı Geçişi Hub",
        "city": "Çankırı",
        "district": "Ilgaz",
        "latitude": 40.92,
        "longitude": 33.62,
        "station_type": "hub",
        "daily_capacity": 9000,
        "is_depot": False
    },
    {
        "name": "Çankırı - Çerkeş Hayvancılık & OSB",
        "city": "Çankırı",
        "district": "Çerkeş",
        "latitude": 40.81,
        "longitude": 32.89,
        "station_type": "branch",
        "daily_capacity": 7500,
        "is_depot": False
    },
    {
        "name": "Eskişehir - Çifteler Tarım Hub",
        "city": "Eskişehir",
        "district": "Çifteler",
        "latitude": 39.38,
        "longitude": 31.13,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Eskişehir - Alpu Dağıtım",
        "city": "Eskişehir",
        "district": "Alpu",
        "latitude": 39.77,
        "longitude": 31.18,
        "station_type": "branch",
        "daily_capacity": 6000,
        "is_depot": False
    },
    {
        "name": "Afyonkarahisar - Sandıklı Jeotermal & Hub",
        "city": "Afyonkarahisar",
        "district": "Sandıklı",
        "latitude": 38.46,
        "longitude": 30.27,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Afyonkarahisar - Dinar Kavşak Lojistik Hub",
        "city": "Afyonkarahisar",
        "district": "Dinar",
        "latitude": 38.06,
        "longitude": 30.16,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Afyonkarahisar - Bolvadin Hub",
        "city": "Afyonkarahisar",
        "district": "Bolvadin",
        "latitude": 38.71,
        "longitude": 31.05,
        "station_type": "branch",
        "daily_capacity": 8500,
        "is_depot": False
    },
    {
        "name": "Afyonkarahisar - Emirdağ Gurbetçi & Dağıtım",
        "city": "Afyonkarahisar",
        "district": "Emirdağ",
        "latitude": 39.02,
        "longitude": 31.15,
        "station_type": "hub",
        "daily_capacity": 9500,
        "is_depot": False
    },
    {
        "name": "Kütahya - Tavşanlı OSB & Linyit Hub",
        "city": "Kütahya",
        "district": "Tavşanlı",
        "latitude": 39.54,
        "longitude": 29.49,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Kütahya - Simav Jeotermal & Sera Hub",
        "city": "Kütahya",
        "district": "Simav",
        "latitude": 39.09,
        "longitude": 28.98,
        "station_type": "branch",
        "daily_capacity": 7500,
        "is_depot": False
    },
    {
        "name": "Kütahya - Gediz Dağıtım",
        "city": "Kütahya",
        "district": "Gediz",
        "latitude": 38.99,
        "longitude": 29.57,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Uşak - Banaz OSB Hub",
        "city": "Uşak",
        "district": "Banaz",
        "latitude": 38.74,
        "longitude": 29.75,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Uşak - Eşme Kilim & Tarım",
        "city": "Uşak",
        "district": "Eşme",
        "latitude": 38.4,
        "longitude": 28.97,
        "station_type": "branch",
        "daily_capacity": 6500,
        "is_depot": False
    },
    {
        "name": "Burdur - Bucak Mermer & Taşımacılık Hub",
        "city": "Burdur",
        "district": "Bucak",
        "latitude": 37.46,
        "longitude": 30.59,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Isparta - Yalvaç Sanayi & Dağıtım",
        "city": "Isparta",
        "district": "Yalvaç",
        "latitude": 38.3,
        "longitude": 31.18,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Isparta - Eğirdir Elma & Soğuk Hava Deposu",
        "city": "Isparta",
        "district": "Eğirdir",
        "latitude": 37.87,
        "longitude": 30.85,
        "station_type": "hub",
        "daily_capacity": 9500,
        "is_depot": False
    },
    {
        "name": "Çorum - Sungurlu OSB & Kavşak Hub",
        "city": "Çorum",
        "district": "Sungurlu",
        "latitude": 40.16,
        "longitude": 34.37,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Çorum - Osmancık İpekyolu Çeltik Hub",
        "city": "Çorum",
        "district": "Osmancık",
        "latitude": 40.97,
        "longitude": 34.8,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Çorum - Alaca Dağıtım",
        "city": "Çorum",
        "district": "Alaca",
        "latitude": 40.17,
        "longitude": 34.84,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Tokat - Erbaa Yaprak & Sanayi Hub",
        "city": "Tokat",
        "district": "Erbaa",
        "latitude": 40.67,
        "longitude": 36.57,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Tokat - Turhal Şeker & Lojistik",
        "city": "Tokat",
        "district": "Turhal",
        "latitude": 40.39,
        "longitude": 36.08,
        "station_type": "hub",
        "daily_capacity": 10500,
        "is_depot": False
    },
    {
        "name": "Tokat - Niksar Su & Ceviz Dağıtım",
        "city": "Tokat",
        "district": "Niksar",
        "latitude": 40.59,
        "longitude": 36.95,
        "station_type": "branch",
        "daily_capacity": 8500,
        "is_depot": False
    },
    {
        "name": "Tokat - Zile Hub",
        "city": "Tokat",
        "district": "Zile",
        "latitude": 40.3,
        "longitude": 35.89,
        "station_type": "branch",
        "daily_capacity": 7500,
        "is_depot": False
    },
    {
        "name": "Amasya - Merzifon Lojistik & Havalimanı Hub",
        "city": "Amasya",
        "district": "Merzifon",
        "latitude": 40.87,
        "longitude": 35.46,
        "station_type": "hub",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Amasya - Suluova Et & Biyogaz Sanayi",
        "city": "Amasya",
        "district": "Suluova",
        "latitude": 40.83,
        "longitude": 35.65,
        "station_type": "hub",
        "daily_capacity": 9500,
        "is_depot": False
    },
    {
        "name": "Kastamonu - Tosya Ahşap & Kapı Sanayi Hub",
        "city": "Kastamonu",
        "district": "Tosya",
        "latitude": 41.02,
        "longitude": 34.04,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Kastamonu - Taşköprü Sarımsak Hub",
        "city": "Kastamonu",
        "district": "Taşköprü",
        "latitude": 41.51,
        "longitude": 34.21,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Sinop - Boyabat Tuğla & Toprak Sanayi Hub",
        "city": "Sinop",
        "district": "Boyabat",
        "latitude": 41.47,
        "longitude": 34.77,
        "station_type": "hub",
        "daily_capacity": 10000,
        "is_depot": False
    },
    {
        "name": "Kahramanmaraş - Elbistan Termik & Lojistik Hub",
        "city": "Kahramanmaraş",
        "district": "Elbistan",
        "latitude": 38.2,
        "longitude": 37.19,
        "station_type": "hub",
        "daily_capacity": 13500,
        "is_depot": False
    },
    {
        "name": "Kahramanmaraş - Afşin Hub",
        "city": "Kahramanmaraş",
        "district": "Afşin",
        "latitude": 38.25,
        "longitude": 36.91,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Kahramanmaraş - Göksun Karayolu Geçişi",
        "city": "Kahramanmaraş",
        "district": "Göksun",
        "latitude": 38.02,
        "longitude": 36.49,
        "station_type": "branch",
        "daily_capacity": 7500,
        "is_depot": False
    },
    {
        "name": "Malatya - Yeşilyurt 2. OSB Hub",
        "city": "Malatya",
        "district": "Yeşilyurt",
        "latitude": 38.31,
        "longitude": 38.24,
        "station_type": "hub",
        "daily_capacity": 16000,
        "is_depot": False
    },
    {
        "name": "Malatya - Battalgazi Kayısı Dağıtım",
        "city": "Malatya",
        "district": "Battalgazi",
        "latitude": 38.42,
        "longitude": 38.36,
        "station_type": "branch",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Malatya - Darende İpekyolu Geçişi",
        "city": "Malatya",
        "district": "Darende",
        "latitude": 38.56,
        "longitude": 37.5,
        "station_type": "branch",
        "daily_capacity": 7000,
        "is_depot": False
    },
    {
        "name": "Elazığ - Kovancılar Kavşağı Hub",
        "city": "Elazığ",
        "district": "Kovancılar",
        "latitude": 38.71,
        "longitude": 39.85,
        "station_type": "hub",
        "daily_capacity": 9500,
        "is_depot": False
    },
    {
        "name": "Erzincan - Tercan Dağıtım",
        "city": "Erzincan",
        "district": "Tercan",
        "latitude": 39.78,
        "longitude": 40.38,
        "station_type": "branch",
        "daily_capacity": 6500,
        "is_depot": False
    },
    {
        "name": "Erzurum - Pasinler Hub",
        "city": "Erzurum",
        "district": "Pasinler",
        "latitude": 39.98,
        "longitude": 41.67,
        "station_type": "branch",
        "daily_capacity": 7500,
        "is_depot": False
    },
    {
        "name": "Erzurum - Horasan İpekyolu Bağlantısı Hub",
        "city": "Erzurum",
        "district": "Horasan",
        "latitude": 40.04,
        "longitude": 42.17,
        "station_type": "hub",
        "daily_capacity": 9500,
        "is_depot": False
    },
    {
        "name": "Ağrı - Doğubayazıt Gürbulak Sınır Kapısı Hub",
        "city": "Ağrı",
        "district": "Doğubayazıt",
        "latitude": 39.55,
        "longitude": 44.08,
        "station_type": "hub",
        "daily_capacity": 15000,
        "is_depot": False
    },
    {
        "name": "Ağrı - Patnos Hub",
        "city": "Ağrı",
        "district": "Patnos",
        "latitude": 39.23,
        "longitude": 42.86,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Kars - Sarıkamış Dağıtım",
        "city": "Kars",
        "district": "Sarıkamış",
        "latitude": 40.33,
        "longitude": 42.57,
        "station_type": "branch",
        "daily_capacity": 6500,
        "is_depot": False
    },
    {
        "name": "Van - Erciş Lojistik Hub",
        "city": "Van",
        "district": "Erciş",
        "latitude": 39.03,
        "longitude": 43.36,
        "station_type": "hub",
        "daily_capacity": 12500,
        "is_depot": False
    },
    {
        "name": "Van - Edremit Dağıtım",
        "city": "Van",
        "district": "Edremit",
        "latitude": 38.42,
        "longitude": 43.25,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Siverek Hub",
        "city": "Şanlıurfa",
        "district": "Siverek",
        "latitude": 37.75,
        "longitude": 39.31,
        "station_type": "hub",
        "daily_capacity": 14000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Viranşehir Hub",
        "city": "Şanlıurfa",
        "district": "Viranşehir",
        "latitude": 37.23,
        "longitude": 39.76,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Birecik Fıstık & Lojistik",
        "city": "Şanlıurfa",
        "district": "Birecik",
        "latitude": 37.03,
        "longitude": 37.98,
        "station_type": "hub",
        "daily_capacity": 11000,
        "is_depot": False
    },
    {
        "name": "Şanlıurfa - Suruç Dağıtım",
        "city": "Şanlıurfa",
        "district": "Suruç",
        "latitude": 36.98,
        "longitude": 38.42,
        "station_type": "branch",
        "daily_capacity": 8500,
        "is_depot": False
    },
    {
        "name": "Mardin - Midyat Taş Vadisi Hub",
        "city": "Mardin",
        "district": "Midyat",
        "latitude": 37.42,
        "longitude": 41.34,
        "station_type": "hub",
        "daily_capacity": 11500,
        "is_depot": False
    },
    {
        "name": "Mardin - Nusaybin İpekyolu Sınır Hub",
        "city": "Mardin",
        "district": "Nusaybin",
        "latitude": 37.07,
        "longitude": 41.21,
        "station_type": "hub",
        "daily_capacity": 13000,
        "is_depot": False
    },
    {
        "name": "Gaziantep - Nizip Zeytin & Sabun Hub",
        "city": "Gaziantep",
        "district": "Nizip",
        "latitude": 37.01,
        "longitude": 37.79,
        "station_type": "hub",
        "daily_capacity": 13500,
        "is_depot": False
    },
    {
        "name": "Gaziantep - İslahiye Dağıtım",
        "city": "Gaziantep",
        "district": "İslahiye",
        "latitude": 37.03,
        "longitude": 36.63,
        "station_type": "branch",
        "daily_capacity": 8000,
        "is_depot": False
    },
    {
        "name": "Diyarbakır - Ergani Maden Yolu Hub",
        "city": "Diyarbakır",
        "district": "Ergani",
        "latitude": 38.27,
        "longitude": 39.76,
        "station_type": "hub",
        "daily_capacity": 12000,
        "is_depot": False
    },
    {
        "name": "Diyarbakır - Bismil Pamuk & Tarım",
        "city": "Diyarbakır",
        "district": "Bismil",
        "latitude": 37.85,
        "longitude": 40.67,
        "station_type": "branch",
        "daily_capacity": 9500,
        "is_depot": False
    }
]

EXPANDED_VEHICLES = [
    {
        "id": 1,
        "name": "Moto Kurye - Honda CBF 150 (Express)",
        "plate": "41 MTO 101",
        "type": "courier",
        "category": "Express Dağıtım",
        "capacity": 50,
        "volume_m3": 0.3,
        "fuel_type": "gasoline",
        "fuel_liters_per_100km": 3.5,
        "fuel_consumption": 2.99,
        "rental_cost": 180.0,
        "speed_factor": 1.25,
        "co2_g_per_km": 80.8,
        "is_owned": 1,
        "icon": "fa-motorcycle",
        "color": "#10b981",
        "description": "Acil evrak ve hafif paketler için maksimum çeviklik."
    },
    {
        "id": 2,
        "name": "Panelvan - Fiat Doblo Maxi (Hafif Ticari)",
        "plate": "41 PNV 202",
        "type": "van",
        "category": "Hafif Ticari",
        "capacity": 400,
        "volume_m3": 4.2,
        "fuel_type": "diesel",
        "fuel_liters_per_100km": 7.8,
        "fuel_consumption": 7.22,
        "rental_cost": 380.0,
        "speed_factor": 1.1,
        "co2_g_per_km": 209.0,
        "is_owned": 1,
        "icon": "fa-van-shuttle",
        "color": "#06b6d4",
        "description": "Şehir içi sokak aralarında seri e-ticaret dağıtımı."
    },
    {
        "id": 3,
        "name": "Dağıtım Kamyoneti - Ford Transit 350L",
        "plate": "41 TRN 303",
        "type": "light_truck",
        "category": "Şehir İçi Kamyonet",
        "capacity": 1000,
        "volume_m3": 12.5,
        "fuel_type": "diesel",
        "fuel_liters_per_100km": 11.5,
        "fuel_consumption": 10.64,
        "rental_cost": 580.0,
        "speed_factor": 1.0,
        "co2_g_per_km": 308.2,
        "is_owned": 1,
        "icon": "fa-truck-pickup",
        "color": "#6366f1",
        "description": "Standart koli ve orta hacimli kargo taşımacılığı."
    },
    {
        "id": 4,
        "name": "Bölgesel Kamyon - Isuzu NPR Long",
        "plate": "41 KAM 404",
        "type": "medium_truck",
        "category": "Bölgesel Dağıtım Kamyonu",
        "capacity": 2500,
        "volume_m3": 28.0,
        "fuel_type": "diesel",
        "fuel_liters_per_100km": 21.0,
        "fuel_consumption": 19.43,
        "rental_cost": 950.0,
        "speed_factor": 0.95,
        "co2_g_per_km": 562.8,
        "is_owned": 1,
        "icon": "fa-truck",
        "color": "#f59e0b",
        "description": "İller arası ve sanayi bölgeleri için ideal taşıma kapasitesi."
    },
    {
        "id": 5,
        "name": "Ağır Hizmet Kamyonu - Mercedes-Benz Axor 1840",
        "plate": "41 AXO 505",
        "type": "heavy_truck",
        "category": "Şehirlerarası Ağır Vasıta",
        "capacity": 6000,
        "volume_m3": 50.0,
        "fuel_type": "diesel",
        "fuel_liters_per_100km": 29.5,
        "fuel_consumption": 27.29,
        "rental_cost": 1600.0,
        "speed_factor": 0.9,
        "co2_g_per_km": 790.6,
        "is_owned": 1,
        "icon": "fa-truck-moving",
        "color": "#8b5cf6",
        "description": "Büyük aktarma merkezleri arası toplu yük transferi."
    },
    {
        "id": 6,
        "name": "Mega Treyler TIR - Scania R450 Highline",
        "plate": "41 TIR 606",
        "type": "trailer",
        "category": "Mega Lojistik Tır",
        "capacity": 15000,
        "volume_m3": 95.0,
        "fuel_type": "diesel",
        "fuel_liters_per_100km": 33.5,
        "fuel_consumption": 31.56,
        "rental_cost": 2400.0,
        "speed_factor": 0.85,
        "co2_g_per_km": 897.8,
        "is_owned": 1,
        "icon": "fa-trailer",
        "color": "#ef4444",
        "description": "Türkiye geneli ana hat (linehaul) konteyner ve paletli sevkiyat."
    }
]

LOGISTICS_PARAMS = {
    "fuel_prices": {
        "diesel_per_liter": 92.5,
        "gasoline_per_liter": 85.5,
        "adblue_per_liter": 36.5,
        "lpg_per_liter": 45.0
    },
    "toll_rates": {
        "osmangazi_bridge": 980.0,
        "canakkale_1915": 740.0,
        "yavuz_sultan_selim": 180.0,
        "highway_per_km": 1.8
    },
    "driver_daily_wage": 2500.0,
    "co2_emission_factors": {
        "diesel": 2.68,
        "gasoline": 2.31
    }
}

TURKEY_REGIONS = {
    "Marmara": [
        "Kocaeli",
        "İstanbul",
        "Bursa",
        "Sakarya",
        "Yalova",
        "Tekirdağ",
        "Edirne",
        "Kırklareli",
        "Balıkesir",
        "Çanakkale",
        "Bilecik"
    ],
    "Ege": [
        "İzmir",
        "Manisa",
        "Aydın",
        "Denizli",
        "Muğla",
        "Afyonkarahisar",
        "Kütahya",
        "Uşak"
    ],
    "İç Anadolu": [
        "Ankara",
        "Konya",
        "Eskişehir",
        "Kayseri",
        "Sivas",
        "Aksaray",
        "Kırıkkale",
        "Kırşehir",
        "Nevşehir",
        "Niğde",
        "Karaman",
        "Yozgat",
        "Çankırı"
    ],
    "Akdeniz": [
        "Antalya",
        "Adana",
        "Mersin",
        "Hatay",
        "Kahramanmaraş",
        "Osmaniye",
        "Isparta",
        "Burdur"
    ],
    "Karadeniz": [
        "Samsun",
        "Trabzon",
        "Ordu",
        "Giresun",
        "Rize",
        "Artvin",
        "Zonguldak",
        "Bolu",
        "Düzce",
        "Karabük",
        "Bartın",
        "Kastamonu",
        "Sinop",
        "Amasya",
        "Çorum",
        "Tokat",
        "Gümüşhane",
        "Bayburt"
    ],
    "Güneydoğu Anadolu": [
        "Gaziantep",
        "Diyarbakır",
        "Şanlıurfa",
        "Batman",
        "Mardin",
        "Adıyaman",
        "Siirt",
        "Şırnak",
        "Kilis"
    ],
    "Doğu Anadolu": [
        "Malatya",
        "Elazığ",
        "Erzurum",
        "Van",
        "Erzincan",
        "Kars",
        "Ağrı",
        "Muş",
        "Bitlis",
        "Bingöl",
        "Tunceli",
        "Iğdır",
        "Ardahan",
        "Hakkari"
    ]
}
