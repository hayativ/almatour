# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Any
from datetime import date, time as dtime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from apps.users.models import CustomUser 
from apps.places.models import Place, PlaceTranslation
from apps.info.models import Souvenir, App, Advertisement, AdvertisementTranslation
from apps.events.models import Event, EventTranslation, CalendarEvent

NOW = timezone.now


# ============================================================
# ===================== НАЧАЛО =================
# ============================================================

USERS_DATA = [
    {
        "id": 1,
        "email": "admin@example.com",
        "phone": "+77010000001",
        "password": make_password("AdminStrongPass123"),
        "is_superuser": True,
        "username": "admin",
        "is_active": True, #проставить везде True
    }
]

PLACES_DATA = [
    {
        "id": 1,
        "image": "images/places/tselinny-center.jpg",
        "category": 1,
        "address": "Улица Масанчи, 59",
        "link": "https://www.tselinny.org/en",
        'lat': 43.248545,
        'lng': 76.929537,
    },
    {
        "id": 2,
        "image": "images/places/ascension-cathedral.jpg",
        "category": 2,
        "address": "​Парк им. 28 гвардейцев-панфиловцев​Улица Гоголя, 40в",
        "link": "https://cathedral.kz/en",
        'lat': 43.258742,
        'lng': 76.952983,
    },
    {
        "id": 3,
        "image": "images/places/almaty-museum-of-arts.jpg",
        "category": 1,
        "address": "Проспект Аль-Фараби, 28",
        "link": "https://www.almaty.art/museum",
        'lat': 43.227494,
        'lng': 76.949053,
    },
    {
        "id": 4,
        "image": "images/places/kazakhstan-hotel.jpg",
        "category": 0,
        "address": "Проспект Достык, 52",
        "link": "https://kazakhstanhotel.kz/en/",
        'lat': 43.244935,
        'lng': 76.957131,
    },
    {
        "id": 5,
        "image": "images/places/almaty-hotel.jpg",
        "category": 0,
        "address": "Улица Кабанбай батыра, 85",
        "link": "https://hotelalmaty.kz/en/",
        'lat': 43.250145,
        'lng': 76.94451,
    },
    {
        "id": 6,
        "image": "images/places/lermontov-drama-theater.jpg",
        "category": 1,
        "address": "​Улица Байсеитовой, 43",
        "link": "https://www.tl.kz/content/",
        'lat': 43.242915,
        'lng': 76.943938,
    },
    {
        "id": 7,
        "image": "images/places/kasteev-museum.jpg",
        "category": 1,
        "address": "Микрорайон Коктем-3, 22/1",
        "link": "https://www.gmirk.kz/en/",
        'lat': 43.235747,
        'lng': 76.918624,
    },
    {
        "id": 8,
        "image": "images/places/green-bazaar.jpg",
        "category": 0,
        "address": "​Проспект Жибек Жолы, 53",
        "link": "",
        'lat': 43.262771,
        'lng': 76.955205,
    },
    {
        "id": 9,
        "image": "images/places/botanical-garden.jpg",
        "category": 3,
        "address": "Улица Тимирязева, 36д",
        "link": "",
        'lat': 43.226243,
        'lng': 76.91321,
    },
    {
        "id": 10,
        "image": "images/places/terrenkur.jpg",
        "category": 3,
        "address": "Терренкур",
        "link": "",
        'lat': 43.193935,
        'lng': 76.983724,
    },
    {
        "id": 11,
        "image": "images/places/republic-square.jpg",
        "category": 3,
        "address": "Площадь Республики",
        "link": "",
        'lat': 43.237902,
        'lng': 76.945387,
    },
    {
        "id": 12,
        "image": "images/places/kbtu.jpg",
        "category": 0,
        "address": "​Улица Толе би, 59",
        "link": "https://kbtu.edu.kz/en/",
        'lat': 43.255102,
        'lng': 76.943183,
    },
    {
        "id": 13,
        "image": "images/places/arasan-spa.jpg",
        "category": 0,
        "address": "​Улица Тулебаева, 78",
        "link": "https://arasan-spa.kz/",
        'lat': 43.258649,
        'lng': 76.948621,
    },
    {
        "id": 14,
        "image": "images/places/abai-opera-ballet.jpg",
        "category": 1,
        "address": "Улица Кабанбай батыра, 110",
        "link": "https://abaykazntob.kz/en/home-page/",
        'lat': 43.249368,
        'lng': 76.945622,
    },
    {
        "id": 15,
        "image": "images/places/central-mosque.jpg",
        "category": 2,
        "address": "​Улица Пушкина, 16",
        "link": "",
        'lat': 43.268385,
        'lng': 76.953602,
    },
    {
        "id": 16,
        "image": "images/places/central-recreation-park.jpg",
        "category": 0,
        "address": "Улица Гоголя, 1",
        "link": "https://almatycentralpark.kz/",
        'lat': 43.261331,
        'lng': 76.965178,
    },
]

PLACE_TRANSLATIONS_DATA = [
    {
        "id": 1,
        "place_id": 1,
        "language_id": 1,  
        "name": "Tselinny Center of Contemporary Culture",
        "timetable": "Varies by exhibition and event",
        "description": "Tselinny Center of Contemporary Culture is one of Almaty’s important cultural spaces dedicated to contemporary art, exhibitions, public programs, lectures, and creative initiatives. Located in the city center, it serves as a platform for dialogue between artists, researchers, and visitors, combining historical significance with a modern cultural vision.",
    },
    {
        "id": 2,
        "place_id": 1,
        "language_id": 2,
        "name": "Центр современной культуры «Целинный»",
        "timetable": "Зависит от выставок и мероприятий",
        "description": "Одно из важных культурных пространств Алматы, посвящённое современному искусству, выставкам, публичным программам, лекциям и творческим инициативам. Расположенный в центре города, он служит площадкой для диалога между художниками, исследователями и посетителями, сочетая историческую значимость с современным культурным видением.",
    },
    {
        "id": 3,
        "place_id": 1,
        "language_id": 3, 
        "name": "«Целинный» заманауи мәдениет орталығы",
        "timetable": "Көрме мен іс-шараға байланысты",
        "description": "«Алматыдағы заманауи өнерге, көрмелерге, жария бағдарламаларға, дәрістер мен шығармашылық бастамаларға арналған маңызды мәдени кеңістіктердің бірі. Қала орталығында орналасқан бұл орын суретшілер, зерттеушілер және келушілер арасындағы диалог алаңы болып, тарихи маңыз бен заманауи мәдени көзқарасты ұштастырады.",
    },

    {
        "id": 4,
        "place_id": 2,
        "language_id": 1,
        "name": "Ascension Cathedral",
        "timetable": "Daily",
        "description": "Ascension Cathedral is one of the most famous architectural and religious landmarks in Almaty. Located in Panfilov Park, the cathedral is well known for its colorful exterior, wooden construction, and historical significance. It attracts both worshippers and tourists interested in the city’s cultural heritage and православие architecture.",
    },
    {
        "id": 5,
        "place_id": 2,
        "language_id": 2,
        "name": "Вознесенский собор",
        "timetable": "Ежедневно",
        "description": "Одна из самых известных архитектурных и религиозных достопримечательностей Алматы. Расположенный в Парке имени 28 гвардейцев-панфиловцев, собор известен своим ярким обликом, деревянной конструкцией и исторической значимостью. Он привлекает как верующих, так и туристов, интересующихся культурным наследием города и православной архитектурой.",
    },
    {
        "id": 6,
        "place_id": 2,
        "language_id": 3,
        "name": "Вознесение соборы",
        "timetable": "Күн сайын",
        "description": "Алматыдағы ең танымал сәулет және діни көрнекі орындардың бірі. 28 гвардияшы-панфиловшылар саябағында орналасқан бұл собор өзінің жарқын келбетімен, ағаштан салынған құрылысымен және тарихи маңызымен ерекшеленеді. Ол қала мәдени мұрасы мен православ сәулетіне қызығатын келушілер мен туристерді тартады.",
    },

    {
        "id": 7,
        "place_id": 3,
        "language_id": 1,
        "name": "Almaty Museum of Arts",
        "timetable": "Varies by exhibition schedule",
        "description": "Almaty Museum of Arts is a modern cultural venue presenting exhibitions, artistic projects, and educational programs. The museum introduces visitors to contemporary and classical visual art, supporting creative dialogue and expanding the artistic life of the city. It is a destination for those interested in culture, design, and modern museum spaces.",
    },
    {
        "id": 8,
        "place_id": 3,
        "language_id": 2,
        "name": "Almaty Museum of Arts",
        "timetable": "Зависит от расписания выставок",
        "description": "Современное культурное пространство, представляющее выставки, художественные проекты и образовательные программы. Музей знакомит посетителей с современным и классическим визуальным искусством, поддерживает творческий диалог и расширяет художественную жизнь города. Это место для всех, кто интересуется культурой, дизайном и современными музейными пространствами.",
    },
    {
        "id": 9,
        "place_id": 3,
        "language_id": 3,
        "name": "Almaty Museum of Arts",
        "timetable": "Көрме кестесіне байланысты",
        "description": "Көрмелерді, көркем жобаларды және білім беру бағдарламаларын ұсынатын заманауи мәдени кеңістік. Мұражай келушілерді заманауи және классикалық бейнелеу өнерімен таныстырып, шығармашылық диалогты қолдайды және қаланың көркем өмірін байытады. Бұл мәдениетке, дизайнға және заманауи мұражай кеңістіктеріне қызығатындар үшін маңызды орын.",
    },

    {
        "id": 10,
        "place_id": 4,
        "language_id": 1,
        "name": "Hotel Kazakhstan",
        "timetable": "Open 24/7",
        "description": "Hotel Kazakhstan is one of the most recognizable symbols of Almaty and an important landmark of the city skyline. Located on Dostyk Avenue, the hotel is known for its high-rise architecture, panoramic views, and central location. It remains a popular place for accommodation, meetings, and sightseeing.",
    },
    {
        "id": 11,
        "place_id": 4,
        "language_id": 2,
        "name": "Гостиница «Казахстан»",
        "timetable": "Круглосуточно",
        "description": "Один из самых узнаваемых символов Алматы и важная часть городского силуэта. Расположенная на проспекте Достык, гостиница известна своей высотной архитектурой, панорамными видами и удобным центральным расположением. Она остаётся популярным местом для проживания, встреч и знакомства с городом.",
    },
    {
        "id": 12,
        "place_id": 4,
        "language_id": 3,
        "name": "«Қазақстан» қонақ үйі",
        "timetable": "Тәулік бойы",
        "description": "«Алматының ең танымал нышандарының бірі және қала келбетінің маңызды бөлігі. Достық даңғылында орналасқан бұл қонақ үй өзінің биік сәулетімен, панорамалық көріністерімен және қала орталығындағы ыңғайлы орналасуымен белгілі. Ол тұруға, кездесулер өткізуге және қаламен танысуға арналған танымал орын болып қала береді.",
    },

    {
        "id": 13,
        "place_id": 5,
        "language_id": 1,
        "name": "Almaty Hotel",
        "timetable": "Open 24/7",
        "description": "Almaty Hotel is a historic hotel located in the heart of the city. It is known for its classic atmosphere, central location, and proximity to major streets, theaters, restaurants, and business areas. The hotel reflects the urban character of Almaty and remains one of the recognizable places in the city center.",
    },
    {
        "id": 14,
        "place_id": 5,
        "language_id": 2,
        "name": "Гостиница «Алматы»",
        "timetable": "Круглосуточно",
        "description": "Исторический отель, расположенный в самом центре города. Она известна своей классической атмосферой, удобным расположением и близостью к главным улицам, театрам, ресторанам и деловым районам. Отель отражает городской характер Алматы и остаётся одним из узнаваемых мест центра.",
    },
    {
        "id": 15,
        "place_id": 5,
        "language_id": 3,
        "name": "«Алматы» қонақ үйі",
        "timetable": "Тәулік бойы",
        "description": "Қаланың қақ ортасында орналасқан тарихи қонақ үй. Ол өзінің классикалық атмосферасымен, ыңғайлы орналасуымен және басты көшелерге, театрларға, мейрамханаларға және іскерлік аудандарға жақындығымен танымал. Бұл қонақ үй Алматының қалалық келбетін көрсетіп, орталықтағы танымал орындардың бірі болып саналады.",
    },

    {
        "id": 16,
        "place_id": 6,
        "language_id": 1,
        "name": "M. Lermontov Russian Drama Theatre",
        "timetable": "Varies by performance schedule",
        "description": "The M. Lermontov Russian Drama Theatre is one of the leading theatrical institutions in Almaty. It is known for its dramatic productions, classical and modern repertoire, and long-standing contribution to the cultural life of the city. The theater attracts audiences with its artistic traditions and central location.",
    },
    {
        "id": 17,
        "place_id": 6,
        "language_id": 2,
        "name": "Театр драмы им. М. Лермонтова",
        "timetable": "Зависит от репертуара",
        "description": "Один из ведущих театров Алматы. Он известен своими драматическими постановками, классическим и современным репертуаром, а также значительным вкладом в культурную жизнь города. Театр привлекает зрителей своими художественными традициями и центральным расположением.",
    },
    {
        "id": 18,
        "place_id": 6,
        "language_id": 3,
        "name": "М. Лермонтов атындағы драма театры",
        "timetable": "Репертуарға байланысты",
        "description": "Алматыдағы жетекші театрлардың бірі. Театр драмалық қойылымдарымен, классикалық және заманауи репертуарымен, сондай-ақ қаланың мәдени өміріне қосқан үлесімен танымал. Оның көркем дәстүрлері мен орталықтағы орналасуы көрермендерді тартады.",
    },

    {
        "id": 19,
        "place_id": 7,
        "language_id": 1,
        "name": "A. Kasteev State Museum of Arts",
        "timetable": "Varies by museum schedule",
        "description": "The A. Kasteev State Museum of Arts is one of the largest and most important art museums in Kazakhstan. Its collections include Kazakh, Russian, European, and Asian art, as well as temporary exhibitions and educational programs. The museum is a key destination for learning about the artistic heritage of the country.",
    },
    {
        "id": 20,
        "place_id": 7,
        "language_id": 2,
        "name": "Государственный музей искусств РК им. А. Кастеева",
        "timetable": "Зависит от расписания музея",
        "description": "Один из крупнейших и важнейших художественных музеев Казахстана. Его коллекции включают казахское, русское, европейское и азиатское искусство, а также временные выставки и образовательные программы. Музей является важным местом для знакомства с художественным наследием страны.",
    },
    {
        "id": 21,
        "place_id": 7,
        "language_id": 3,
        "name": "Ә. Қастеев атындағы ҚР Мемлекеттік өнер музейі",
        "timetable": "Мұражай кестесіне байланысты",
        "description": "Қазақстандағы ең ірі және маңызды өнер музейлерінің бірі. Оның қорында қазақ, орыс, еуропалық және азиялық өнер туындылары, сондай-ақ уақытша көрмелер мен білім беру бағдарламалары бар. Бұл музей елдің көркем мұрасымен танысуға арналған маңызды орын.",
    },

    {
        "id": 22,
        "place_id": 8,
        "language_id": 1,
        "name": "Green Bazaar",
        "timetable": "Daily",
        "description": "Green Bazaar is one of the most famous markets in Almaty and a lively place where visitors can experience the atmosphere of local trade. The market offers fresh fruits, vegetables, spices, traditional foods, household goods, and souvenirs. It is a popular destination for both residents and tourists who want to explore everyday city life.",
    },
    {
        "id": 23,
        "place_id": 8,
        "language_id": 2,
        "name": "Зелёный базар",
        "timetable": "Ежедневно",
        "description": "Один из самых известных рынков Алматы и живое место, где можно почувствовать атмосферу местной торговли. На рынке представлены свежие фрукты, овощи, специи, традиционные продукты, товары для дома и сувениры. Это популярное место как среди жителей города, так и среди туристов, желающих увидеть повседневную жизнь Алматы.",
    },
    {
        "id": 24,
        "place_id": 8,
        "language_id": 3,
        "name": "Жасыл базар",
        "timetable": "Күн сайын",
        "description": "Алматыдағы ең танымал базарлардың бірі және жергілікті сауда атмосферасын сезінуге болатын жанданған орын. Мұнда жаңа піскен жемістер, көкөністер, дәмдеуіштер, ұлттық тағамдар, тұрмыстық тауарлар мен кәдесыйлар сатылады. Бұл орын қала тұрғындары мен күнделікті өмірді көргісі келетін туристер арасында танымал.",
    },

    {
        "id": 25,
        "place_id": 9,
        "language_id": 1,
        "name": "Botanical Garden",
        "timetable": "Daily",
        "description": "The Botanical Garden in Almaty is a green recreational area and an important scientific and educational space. It is known for its diverse plant collections, walking paths, seasonal scenery, and peaceful atmosphere. The garden is popular for прогулки, outdoor relaxation, and enjoying nature within the city.",
    },
    {
        "id": 26,
        "place_id": 9,
        "language_id": 2,
        "name": "Ботанический сад",
        "timetable": "Ежедневно",
        "description": "Зелёная зона отдыха и важное научно-образовательное пространство. Он известен разнообразием растений, прогулочными аллеями, сезонными пейзажами и спокойной атмосферой. Сад популярен для прогулок, отдыха на свежем воздухе и знакомства с природой в городской среде.",
    },
    {
        "id": 27,
        "place_id": 9,
        "language_id": 3,
        "name": "Ботаникалық бақ",
        "timetable": "Күн сайын",
        "description": "Демалысқа арналған жасыл аймақ әрі маңызды ғылыми-білім беру кеңістігі. Ол өсімдіктердің алуан түрлілігімен, серуендеуге арналған жолдарымен, маусымдық көріністерімен және тыныш атмосферасымен танымал. Бұл бақ табиғатты тамашалау, серуендеу және қала ішінде демалу үшін танымал орын.",
    },

    {
        "id": 28,
        "place_id": 10,
        "language_id": 1,
        "name": "Terrenkur",
        "timetable": "Open 24/7",
        "description": "Terrenkur is a popular walking and recreational route in Almaty, stretching through a scenic green area near the foothills. It is valued for its fresh air, natural surroundings, and suitability for walking, jogging, and light outdoor activity. The route is especially popular among residents seeking quiet rest and exercise.",
    },
    {
        "id": 29,
        "place_id": 10,
        "language_id": 2,
        "name": "Терренкур",
        "timetable": "Круглосуточно",
        "description": "Популярный прогулочный и рекреационный маршрут в Алматы, проходящий через живописную зелёную зону у подножия гор. Он ценится за свежий воздух, природное окружение и удобство для прогулок, пробежек и лёгкой физической активности. Маршрут особенно популярен среди жителей, которые ищут спокойный отдых и движение на свежем воздухе.",
    },
    {
        "id": 30,
        "place_id": 10,
        "language_id": 3,
        "name": "Терренкур",
        "timetable": "Тәулік бойы",
        "description": "Алматыдағы тауға жақын көркем жасыл аймақ арқылы өтетін танымал серуендеу және демалыс бағыты. Ол таза ауасымен, табиғи ортасымен және серуендеуге, жүгіруге, жеңіл дене белсенділігіне қолайлылығымен бағаланады. Бұл бағыт тыныш демалыс пен қозғалысты қалайтын тұрғындар арасында ерекше танымал.",
    },

    {
        "id": 31,
        "place_id": 11,
        "language_id": 1,
        "name": "Republic Square",
        "timetable": "Open 24/7",
        "description": "Republic Square is one of the main public spaces in Almaty and an important symbolic center of the city. It is associated with official events, urban gatherings, and the nearby Independence Monument. The square is a recognizable landmark and a popular point for walking and city views.",
    },
    {
        "id": 32,
        "place_id": 11,
        "language_id": 2,
        "name": "Площадь Республики",
        "timetable": "Круглосуточно",
        "description": "Одно из главных общественных пространств Алматы и важный символический центр города. Она связана с официальными мероприятиями, городскими собраниями и расположенным рядом Монументом Независимости. Площадь является узнаваемой достопримечательностью и популярным местом для прогулок и знакомства с городом.",
    },
    {
        "id": 33,
        "place_id": 11,
        "language_id": 3,
        "name": "Республика алаңы",
        "timetable": "Тәулік бойы",
        "description": "Алматыдағы басты қоғамдық кеңістіктердің бірі және қаланың маңызды нышандық орталығы. Ол ресми іс-шаралармен, қалалық жиналыстармен және маңындағы Тәуелсіздік монументімен байланысты. Бұл алаң серуендеуге және қаланың көрнекті орындарын тамашалауға арналған танымал орын.",
    },

    {
        "id": 34,
        "place_id": 12,
        "language_id": 1,
        "name": "Kazakh-British Technical University (KBTU)",
        "timetable": "09:00 - 18:00",
        "description": "Kazakh-British Technical University is one of the leading technical universities in Kazakhstan, located in the center of Almaty. The university is well known for its programs in information technology, engineering, business, and energy industries. KBTU is situated in a historic building and provides modern education, international partnerships, research opportunities, and innovative learning environments for students.",
    },
    {
        "id": 35,
        "place_id": 12,
        "language_id": 2,
        "name": "Казахстанско-Британский технический университет (КБТУ)",
        "timetable": "09:00 - 18:00",
        "description": "Один из ведущих технических университетов Казахстана, расположенный в центре Алматы. Университет известен своими программами в области информационных технологий, инженерии, бизнеса и энергетики. КБТУ находится в историческом здании и предоставляет современное образование, международные партнёрства, исследовательские возможности и инновационную образовательную среду для студентов.",
    },
    {
        "id": 36,
        "place_id": 12,
        "language_id": 3,
        "name": "Қазақстан-Британ техникалық университеті (ҚБТУ)",
        "timetable": "09:00 - 18:00",
        "description": "Алматы қаласының орталығында орналасқан Қазақстандағы жетекші техникалық жоғары оқу орындарының бірі. Университет ақпараттық технологиялар, инженерия, бизнес және энергетика салаларындағы бағдарламаларымен танымал. ҚБТУ тарихи ғимаратта орналасқан және студенттерге заманауи білім, халықаралық серіктестік, ғылыми-зерттеу мүмкіндіктері мен инновациялық оқу ортасын ұсынады.",
    },

    {
        "id": 37,
        "place_id": 13,
        "language_id": 1,
        "name": "Arasan Wellness & Spa",
        "timetable": "Varies by complex schedule",
        "description": "Arasan Wellness & Spa is a well-known bath and wellness complex in Almaty. It offers spaces for relaxation, spa procedures, and traditional bathing experiences, making it a popular destination for both residents and visitors. The complex is recognized as one of the iconic leisure locations in the city center.",
    },
    {
        "id": 38,
        "place_id": 13,
        "language_id": 2,
        "name": "Arasan Wellness & Spa",
        "timetable": "Зависит от расписания комплекса",
        "description": "Известный банно-оздоровительный комплекс в Алматы. Он предлагает пространство для отдыха, спа-процедуры и традиционные банные форматы, что делает его популярным местом как среди жителей, так и среди гостей города. Комплекс считается одним из знаковых мест отдыха в центре Алматы.",
    },
    {
        "id": 39,
        "place_id": 13,
        "language_id": 3,
        "name": "Arasan Wellness & Spa",
        "timetable": "Кешен кестесіне байланысты",
        "description": "Алматыдағы танымал монша және сауықтыру кешені. Мұнда демалысқа, спа рәсімдеріне және дәстүрлі монша қызметтеріне арналған жағдай жасалған, сондықтан ол қала тұрғындары мен қонақтары арасында кең сұранысқа ие. Бұл кешен қала орталығындағы әйгілі демалыс орындарының бірі болып саналады.",
    },

    {
        "id": 40,
        "place_id": 14,
        "language_id": 1,
        "name": "Abai Opera and Ballet Theatre",
        "timetable": "Varies by performance schedule",
        "description": "The Abai Opera and Ballet Theatre is one of the main cultural symbols of Almaty and Kazakhstan. It is renowned for its opera and ballet productions, elegant architecture, and contribution to the development of performing arts. The theater is an important destination for those interested in music, stage performance, and classical culture.",
    },
    {
        "id": 41,
        "place_id": 14,
        "language_id": 2,
        "name": "Театр оперы и балета им. Абая",
        "timetable": "Зависит от репертуара",
        "description": "Один из главных культурных символов Алматы и Казахстана. Он известен своими оперными и балетными постановками, изящной архитектурой и вкладом в развитие сценического искусства. Театр является важным местом для всех, кто интересуется музыкой, сценой и классической культурой.",
    },
    {
        "id": 42,
        "place_id": 14,
        "language_id": 3,
        "name": "Абай атындағы опера және балет театры",
        "timetable": "Репертуарға байланысты",
        "description": "Алматы мен Қазақстанның басты мәдени нышандарының бірі. Ол опера және балет қойылымдарымен, әсем сәулетімен және сахна өнерін дамытуға қосқан үлесімен танымал. Театр музыкаға, сахна өнеріне және классикалық мәдениетке қызығатындар үшін маңызды орын болып табылады.",
    },

    {
        "id": 43,
        "place_id": 15,
        "language_id": 1,
        "name": "Central Mosque",
        "timetable": "Daily",
        "description": "The Central Mosque of Almaty is one of the largest and most important Islamic religious sites in the city. It is known for its grand architecture, spacious prayer halls, and spiritual significance for the Muslim community. The mosque also stands out as a notable architectural landmark in Almaty.",
    },
    {
        "id": 44,
        "place_id": 15,
        "language_id": 2,
        "name": "Центральная мечеть",
        "timetable": "Ежедневно",
        "description": "Одна из крупнейших и важнейших исламских религиозных площадок города. Она известна своей монументальной архитектурой, просторными молитвенными залами и духовным значением для мусульманской общины. Мечеть также является заметной архитектурной достопримечательностью Алматы.",
    },
    {
        "id": 45,
        "place_id": 15,
        "language_id": 3,
        "name": "Орталық мешіт",
        "timetable": "Күн сайын",
        "description": "Қаладағы ең ірі әрі маңызды исламдық діни орындардың бірі. Ол өзінің еңселі сәулетімен, кең намаз залдарымен және мұсылман қауымы үшін рухани маңызымен танымал. Сонымен қатар мешіт Алматының көрнекті сәулет ескерткіштерінің бірі болып саналады.",
    },

    {
        "id": 46,
        "place_id": 16,
        "language_id": 1,
        "name": "Central Recreation Park",
        "timetable": "Daily",
        "description": "Central Recreation Park is one of the most popular leisure areas in Almaty for families, children, and visitors. The park offers green walking spaces, amusement facilities, and a relaxed urban atmosphere. It is a convenient place for outdoor recreation, entertainment, and spending time with friends or family.",
    },
    {
        "id": 47,
        "place_id": 16,
        "language_id": 2,
        "name": "Центральный парк отдыха",
        "timetable": "Ежедневно",
        "description": "Одна из самых популярных зон досуга в Алматы для семей, детей и гостей города. Парк предлагает зелёные прогулочные пространства, развлекательные объекты и спокойную городскую атмосферу. Это удобное место для отдыха на свежем воздухе, развлечений и времяпрепровождения с друзьями или семьёй.",
    },
    {
        "id": 48,
        "place_id": 16,
        "language_id": 3,
        "name": "Орталық демалыс саябағы",
        "timetable": "Күн сайын",
        "description": "Алматыдағы отбасылар, балалар және қала қонақтары арасында ең танымал демалыс орындарының бірі. Саябақта жасыл серуендеу аймақтары, ойын-сауық нысандары және жайлы қалалық атмосфера бар. Бұл ашық ауада демалуға, көңіл көтеруге және достармен не отбасымен уақыт өткізуге ыңғайлы орын.",
    },
]

EVENTS_DATA = [
    {
        "id": 1,
        "image": "https://sxodim.com/uploads/posts/2026/01/15/optimized/eadbbf33219d4f446982451ce810c21f_545x305-q-85.jpg",
        "date": date(2026, 4, 15),
        "start_time": dtime(20, 0),
        "duration": 120,
        "artist": "Контркультура: Чёрная Экономика",
        "cost": 9000,
        "currency": "KZT",
        "category": 1,
        "address": "Ginger, пр. Достык, 132Б",
        "link": "https://sxodim.com/almaty/event/koncert-kontrkultura-chernaya-ekonomika",
    },
    {
        "id": 2,
        "image": "https://sxodim.com/uploads/posts/2025/12/05/optimized/ebabe72cacfa99f8640097f8214aa31b_545x305-q-85.jpg",
        "date": date(2026, 4, 15),
        "start_time": dtime(19, 0),
        "duration": 90,
        "artist": "«Алматы махаббатым» концерт-спектаклі",
        "cost": 3000,
        "currency": "KZT",
        "category": 1,
        "address": "Республика сарайы, пр. Достык, 56",
        "link": "https://sxodim.com/almaty/event/almaty-mahabbatym-koncert-spektakli",
    },
    {
        "id": 3,
        "image": "https://sxodim.com/uploads/posts/2025/07/24/optimized/6b0643b02517289c42c53f581588dc08_545x305-q-85.jpg",
        "date": date(2026, 4, 16),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "LUCAVEROS",
        "cost": 8500,
        "currency": "KZT",
        "category": 1,
        "address": "Motor club, пр-т. Назарбаева, 50",
        "link": "https://sxodim.com/almaty/event/koncert-lucaveros-1",
    },
    {
        "id": 4,
        "image": "https://sxodim.com/uploads/posts/2026/01/15/optimized/eadbbf33219d4f446982451ce810c21f_545x305-q-85.jpg",
        "date": date(2026, 4, 17),
        "start_time": dtime(20, 0),
        "duration": 90,
        "artist": "Jay Sean & Nana (The Darkman)",
        "cost": 10000,
        "currency": "KZT",
        "category": 1,
        "address": "Дворец Республики, пр. Достык, 56",
        "link": "https://sxodim.com/almaty/event/koncert-jay-sean-i-nana-darkman",
    },
    {
        "id": 5,
        "image": "https://sxodim.com/uploads/posts/2025/12/05/optimized/ebabe72cacfa99f8640097f8214aa31b_545x305-q-85.jpg",
        "date": date(2026, 4, 18),
        "start_time": dtime(20, 0),
        "duration": 10,
        "artist": "Трио Shestero — Акустический блюз",
        "cost": 2000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40Б",
        "link": "https://sxodim.com/almaty/event/duet-shestero-akusticheskiy-blyuz",
    },
    {
        "id": 6,
        "image": "https://sxodim.com/uploads/posts/2025/10/29/optimized/4425210afb398173bece8058a8f24b5f_545x305-q-85.jpg",
        "date": date(2026, 4, 19),
        "start_time": dtime(20, 0),
        "duration": 90,
        "artist": "Квартет Екатерины Хоменковой — Our favorite things",
        "cost": 2000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40Б",
        "link": "https://sxodim.com/almaty/event/kvartet-ekateriny-homenkovoy-our-favorite-things-1",
    },
    {
        "id": 7,
        "image": "https://sxodim.com/uploads/posts/2026/01/30/optimized/1c76eb5b0385b166cb9ed6ebdac7d75c_545x305-q-85.jpg",
        "date": date(2026, 4, 21),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "Посвящение Уэсу Монтгомери — джаз, проверенный временем",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40Б",
        "link": "https://sxodim.com/almaty/event/posvyashchenie-uesu-montgomeri-dzhaz-proverennyy-vremenem-1",
    },
    {
        "id": 8,
        "image": "https://sxodim.com/uploads/posts/2026/02/02/optimized/7249af96e8203866704e164277a2672d_545x305-q-85.jpg",
        "date": date(2026, 4, 22),
        "start_time": dtime(19, 30),
        "duration": 90,
        "artist": "Галымжан Мейрам — «Золотые хиты Сан-Ремо»",
        "cost": 5000,
        "currency": "KZT",
        "category": 1,
        "address": "Театр La Bohême, ул. Валиханова, 43, уг. ул. Жибек Жолы",
        "link": "https://sxodim.com/almaty/event/kvartirnik-galymzhana-meyrama-zolotye-hity-san-remo-1",
    },
    {
        "id": 9,
        "image": "https://sxodim.com/uploads/posts/2026/02/16/optimized/7256e2c92dcb433a6ea32b66cec6798b_545x305-q-85.jpg",
        "date": date(2026, 4, 23),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "La Bohême — «Февральская точка»",
        "cost": 5000,
        "currency": "KZT",
        "category": 1,
        "address": "La Bohême Театр, ул. Валиханова, 43, уг. ул. Жибек Жолы",
        "link": "https://sxodim.com/almaty/event/kvartirnik-v-teatre-la-boheme-fevralskaya-tochka",
    },
    {
        "id": 10,
        "image": "https://sxodim.com/uploads/posts/2026/02/02/optimized/c3fc714bdcd9831bfa483048b855bb0a_545x305-q-85.jpg",
        "date": date(2026, 4, 23),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "Jazz Colours & Сурья — Good bye, Winter!",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/jazz-colours-surya-good-bye-winter",
    },
    {
        "id": 11,
        "image": "https://sxodim.com/uploads/posts/2026/02/02/optimized/d71b9ef6ea84244c98cfd428fd0aa364_545x305-q-85.jpg",
        "date": date(2026, 4, 21),
        "start_time": dtime(22, 0),
        "duration": 90,
        "artist": "Dair Ard — Кельтский фолк",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/dair-ard-etno-dzhaz",
    },
    {
        "id": 12,
        "image": "https://sxodim.com/uploads/posts/2025/04/28/optimized/3d18b515325c18bbcff765c59671d5bf_545x305-q-85.jpg",
        "date": date(2026, 4, 22),
        "start_time": dtime(18, 0),
        "duration": 120,
        "artist": "Bugarabu & Рамхи — «Аура ритма»",
        "cost": 7000,
        "currency": "KZT",
        "category": 1,
        "address": "Театр La Bohême, ул. Валиханова, 43, уг. ул. Жибек Жолы",
        "link": "https://sxodim.com/almaty/event/koncert-retrit-bugarabu-i-ramhi-aura-ritma",
    },
    {
        "id": 13,
        "image": "https://sxodim.com/uploads/posts/2026/01/26/optimized/b579c38c6c9d53206e35e8b0690dc240_545x305-q-85.jpg",
        "date": date(2026, 4, 23),
        "start_time": dtime(20, 0),
        "duration": 120,
        "artist": "All stars jam session — Джазовая музыка и импровизация",
        "cost": 2000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/vecher-dzhaza-i-improvizacii-all-stars-jam-session-v-everjazz",
    },
    {
        "id": 14,
        "image": "https://sxodim.com/uploads/posts/2026/02/02/optimized/278ca14931fcadb22cfe860453dbaadf_545x305-q-85.jpg",
        "date": date(2026, 4, 24),
        "start_time": dtime(20, 0),
        "duration": 90,
        "artist": "Раушан Абишева — River of Love",
        "cost": 2000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/raushan-abisheva-river-of-love",
    },
    {
        "id": 15,
        "image": "https://sxodim.com/uploads/posts/2026/02/02/optimized/278ca14931fcadb22cfe860453dbaadf_545x305-q-85.jpg",
        "date": date(2026, 4, 25),
        "start_time": dtime(20, 0),
        "duration": 60,
        "artist": "Pop Queens — Dua Lipa & Rihanna Night (Юлия Яковлева и резиденты EverJazz)",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/pop-queens-dua-lipa-rihanna-night-yuliya-yakovleva-i-rezidenty-everjazz",
    },
    {
        "id": 16,
        "image": "https://sxodim.com/uploads/posts/2026/01/30/optimized/6e362e301137ae506245155b0631b00c_1522x570-q-85.jpg",
        "date": date(2026, 4, 26),
        "start_time": dtime(20, 0),
        "duration": 60,
        "artist": "Eric B. Turner (США) — Джаз и блюз из сердца Америки",
        "cost": 8000,   # минимальная цена
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40Б",
        "link": "https://sxodim.com/almaty/event/eric-b-turner-ssha-dzhaz-i-blyuz-iz-serdca-ameriki",
    },
    {
        "id": 17,
        "image": "https://sxodim.com/uploads/posts/2026/02/02/optimized/64cfdb0076e988cb7f809635aa947d10_545x305-q-85.jpg",
        "date": date(2026, 4, 27),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "Диана Макина",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/avtorskiy-koncert-diany-makiny-esli-by-lyudi-imeli-krylya",
    },
    {
        "id": 18,
        "image": "https://sxodim.com/uploads/posts/2025/10/29/optimized/7451b6f5f2f099a59dc10d82016ba721_545x305-q-85.jpg",
        "date": date(2026, 4, 27),
        "start_time": dtime(22, 0),
        "duration": 120,
        "artist": "Гаухар Саттарова & STEPS",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/gauhar-sattarova-i-gruppa-steps-hot-jazz-funk",
    },
    {
        "id": 19,
        "image": "https://sxodim.com/uploads/posts/2026/01/30/optimized/861895f89773b9af3a8deed08e0f092f_545x305-q-85.jpg",
        "date": date(2026, 4, 28),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "Tribute to Wes Montgomery",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40Б",
        "link": "https://sxodim.com/almaty/event/posvyashchenie-uesu-montgomeri-dzhaz-proverennyy-vremenem-2",
    },
    {
        "id": 20,
        "image": "https://sxodim.com/uploads/posts/2026/02/02/optimized/ca95740af6b538fb97bdb421fb789a3b_545x305-q-85.jpg",
        "date": date(2026, 4, 28),
        "start_time": dtime(22, 0),
        "duration": 120,
        "artist": "Ирэна Аравина & Jazz House",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/irena-aravina-i-jazz-house-goodbye-winter",
    },
    {
        "id": 21,
        "image": "https://sxodim.com/uploads/posts/2026/02/02/optimized/55457a38a37be8dac37a81b8ae32572c_545x305-q-85.jpg",
        "date": date(2026, 4, 15),
        "start_time": dtime(13, 0),
        "duration": 120,
        "artist": "Гульнара Бертисбаева & Friends",
        "cost": 3000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40б",
        "link": "https://sxodim.com/almaty/event/gulnara-bertisbaeva-friends-happy-day",
    },
    {
        "id": 22,
        "image": "https://sxodim.com/uploads/posts/2026/01/30/optimized/0273ec078d00ee460ce8504788f2328d_545x305-q-85.jpg",
        "date": date(2026, 4, 15),
        "start_time": dtime(18, 0),
        "duration": 120,
        "artist": "Игорь Ананьев & Akko band",
        "cost": 4000,
        "currency": "KZT",
        "category": 1,
        "address": "Джаз-клуб EverJazz, ул. Гоголя, 40Б",
        "link": "https://sxodim.com/almaty/event/igor-ananev-i-akko-band-noche-de-acordeon-1",
    },
    {
        "id": 23,
        "image": "https://sxodim.com/uploads/posts/2026/01/29/optimized/3ed0615fd9d19f142265f9eeb03d1bd9_545x305-q-85.jpg",
        "date": date(2026, 4, 16),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "Айқын Төлепберген",
        "cost": 11000,
        "currency": "KZT",
        "category": 1,
        "address": "Дворец спорта им. Балуана Шолака, пр. Абая, 44",
        "link": "https://sxodim.com/almaty/event/ay-yn-t-lepbergenni-sen-koncerti",
    },
    {
        "id": 24,
        "image": "https://sxodim.com/uploads/posts/2026/02/13/optimized/28e7b62c91c42d441409c1bcff5576eb_545x305-q-85.jpg",
        "date": date(2026, 4, 17),
        "start_time": dtime(20, 0),
        "duration": 120,
        "artist": "Нұрболат Абдуллин",
        "cost": 7000,
        "currency": "KZT",
        "category": 1,
        "address": "Республика Сарайы, Достық даңғылы, 56",
        "link": "https://sxodim.com/almaty/event/n-rbolat-abdullin-koncerti",
    },
    {
        "id": 25,
        "image": "https://sxodim.com/uploads/posts/2026/02/11/optimized/4272d273d97fde3f188216a8c23b1d5d_545x305-q-85.jpg",
        "date": date(2026, 4, 25),
        "start_time": dtime(16, 0),
        "duration": 120,
        "artist": "Мақпал Жүнісова",
        "cost": 6000,
        "currency": "KZT",
        "category": 1,
        "address": "Республика Сарайы, Достық даңғылы, 56",
        "link": "https://sxodim.com/almaty/event/ma-pal-zh-nisovany-merekelik-koncerti-8-nauryz-16-00",
    },
    {
        "id": 26,
        "image": "https://sxodim.com/uploads/posts/2026/02/11/optimized/e7197e2ac187d71a8bc2963012e7472a_545x305-q-85.jpg",
        "date": date(2026, 4, 17),  
        "start_time": dtime(20, 0),
        "duration": 120,
        "artist": "Мақпал Жүнісова",
        "cost": 6000,
        "currency": "KZT",
        "category": 1,
        "address": "Республика Сарайы, Достық даңғылы, 56",
        "link": "https://sxodim.com/almaty/event/ma-pal-zh-nisovany-merekelik-koncerti-8-nauryz-20-00",
    },
    {
        "id": 27,
        "image": "https://sxodim.com/uploads/posts/2026/01/08/optimized/63905982bded619034f7d6cceec49020_545x305-q-85.jpg",
        "date": date(2026, 4, 26),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "«Жігіттер»",
        "cost": 5000,
        "currency": "KZT",
        "category": 1,
        "address": "Республика сарайы, Достык, 56",
        "link": "https://sxodim.com/almaty/event/zhigitter-tobyny-koncerti",
    },
    {
        "id": 28,
        "image": "https://sxodim.com/uploads/posts/2026/02/11/optimized/458a06c995a62a85e83892428cce5824_545x305-q-85.jpg",
        "date": date(2026, 4, 27),
        "start_time": dtime(19, 30),
        "duration": 120,
        "artist": "Nauryz Fest (сборный концерт)",
        "cost": 7000,
        "currency": "KZT",
        "category": 1,
        "address": "Республика Сарайы, Достық даңғылы, 56",
        "link": "https://sxodim.com/almaty/event/nauryz-fest-koncerti",
    },
    {
        "id": 29,
        "image": "https://sxodim.com/uploads/posts/2025/12/11/optimized/0e56967cc4902fa018850a0c5d06b6fd_545x305-q-85.jpg",
        "date": date(2026, 4, 15),
        "start_time": dtime(20, 0),
        "duration": 120,
        "artist": "Anton Belyaev & Therr Maitz",
        "cost": 25000,
        "currency": "KZT",
        "category": 1,
        "address": "Дворец Республики, пр. Достык, 56",
        "link": "https://sxodim.com/almaty/event/colnyy-koncert-antona-belyaeva-i-gruppy-therr-maitz",
    },
    {
        "id": 30,
        "image": "https://sxodim.com/uploads/posts/2026/02/11/optimized/26dcccf30b8614fc1ced38ef819265c2_545x305-q-85.jpg",
        "date": date(2026, 4, 16),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "«Ән мен әнші»",
        "cost": 7000,
        "currency": "KZT",
        "category": 1,
        "address": "Республика Сарайы, Достық даңғылы, 56",
        "link": "https://sxodim.com/almaty/event/n-men-nshi-koncerti",
    },
    {
        "id": 31,
        "image": "https://sxodim.com/uploads/posts/2026/02/11/optimized/26dcccf30b8614fc1ced38ef819265c2_545x305-q-85.jpg",
        "date": date(2026, 4, 18),
        "start_time": dtime(20, 0),
        "duration": 120,
        "artist": "Концерт Антоха МС в Алматы",
        "cost": 15000,
        "currency": "KZT",
        "category": 1,
        "address": "Motor club, ул. Назарбаева, 50",
        "link": "https://sxodim.com/almaty/event/koncert-antoha-ms-v-almaty",
    },
    {
        "id": 32,
        "image": "https://sxodim.com/uploads/posts/2026/02/11/optimized/ff236953535e6d55993ee3dbe5d35127_1522x570-q-85.jpg",
        "date": date(2026, 4, 20),
        "start_time": dtime(19, 0),
        "duration": 120,
        "artist": "Конкурс Mrs Kazakhstan",
        "cost": 8000,
        "currency": "KZT",
        "category": 1,
        "address": "Дворец Республики, пр. Достык, 56",
        "link": "https://sxodim.com/almaty/event/konkurs-mrs-kazakhstan",
    },
    {
        "id": 33,
        "image": "https://ticketon.kz/media/upload/54864u57013_afisha-2.jpg",
        "date": date(2026, 4, 28),      
        "start_time": dtime(12, 0),         
        "duration": 480, 
        "artist": "Wedding Fair 2026 в Алматы",
        "cost": 9990,                     
        "currency": "KZT",
        "category": 2,              
        "address": "The Ritz-Carlton Almaty, Esentai Towers, пр. Аль-Фараби, 77/7",
        "link": "https://ticketon.kz/event/wedding-fair-2026-v-almaty",
    },
]


EVENT_TRANSLATIONS_DATA = [
    # 1
    {"id": 1, "event_id": 1, "language_id": 1, "name": "Kontrkultura: Black Economy", "description": "Concert in Almaty. Venue: Ginger (Dostyk Ave., 132B)."},
    {"id": 2, "event_id": 1, "language_id": 2, "name": "Контркультура: Чёрная Экономика", "description": "Концерт в Алматы. Площадка: Ginger (пр. Достык, 132Б)."},
    {"id": 3, "event_id": 1, "language_id": 3, "name": "Контркультура: Қара Экономика", "description": "Алматыдағы концерт. Өтетін орны: Ginger (Достық даңғ., 132Б)."},

    # 2
    {"id": 4, "event_id": 2, "language_id": 1, "name": "‘Almaty, My Love’ Concert-Performance", "description": "Concert-performance in Almaty. Venue: Republic Palace (Dostyk Ave., 56)."},
    {"id": 5, "event_id": 2, "language_id": 2, "name": "«Алматы махаббатым» концерт-спектакль", "description": "Концерт-спектакль в Алматы. Место: Республика сарайы (пр. Достык, 56)."},
    {"id": 6, "event_id": 2, "language_id": 3, "name": "«Алматы махаббатым» концерт-спектаклі", "description": "Алматыдағы концерт-спектакль. Өтетін орны: Республика сарайы (Достық даңғ., 56)."},

    # 3
    {"id": 7, "event_id": 3, "language_id": 1, "name": "LUCAVEROS Live in Almaty", "description": "Live concert at Motor club (Nazarbayev Ave., 50)."},
    {"id": 8, "event_id": 3, "language_id": 2, "name": "LUCAVEROS", "description": "Концерт в Motor club (пр-т Назарбаева, 50)."},
    {"id": 9, "event_id": 3, "language_id": 3, "name": "LUCAVEROS", "description": "Motor club-та концерт (Назарбаев даңғ., 50)."},

    # 4
    {"id": 10, "event_id": 4, "language_id": 1, "name": "Jay Sean & Nana (The Darkman) Live", "description": "Live show at the Republic Palace (Dostyk Ave., 56). Duration: 90 minutes."},
    {"id": 11, "event_id": 4, "language_id": 2, "name": "Jay Sean & Nana (The Darkman)", "description": "Концерт во Дворце Республики (пр. Достык, 56). Длительность: 90 минут."},
    {"id": 12, "event_id": 4, "language_id": 3, "name": "Jay Sean & Nana (The Darkman)", "description": "Республика сарайындағы концерт (Достық даңғ., 56). Ұзақтығы: 90 минут."},

    # 5
    {"id": 13, "event_id": 5, "language_id": 1, "name": "Shestero Trio — Acoustic Blues", "description": "Acoustic blues night at EverJazz (Gogol St., 40B)."},
    {"id": 14, "event_id": 5, "language_id": 2, "name": "Трио Shestero — Акустический блюз", "description": "Вечер акустического блюза в EverJazz (ул. Гоголя, 40Б)."},
    {"id": 15, "event_id": 5, "language_id": 3, "name": "Shestero триосы — акустикалық блюз", "description": "EverJazz-та акустикалық блюз кеші (Гоголь к-сі, 40Б)."},

    # 6
    {"id": 16, "event_id": 6, "language_id": 1, "name": "Ekaterina Khomenkova Quartet — Our Favorite Things", "description": "Jazz concert at EverJazz (Gogol St., 40B)."},
    {"id": 17, "event_id": 6, "language_id": 2, "name": "Квартет Екатерины Хоменковой — Our favorite things", "description": "Джаз-концерт в EverJazz (ул. Гоголя, 40Б)."},
    {"id": 18, "event_id": 6, "language_id": 3, "name": "Екатерина Хоменкова квартеті — Our Favorite Things", "description": "EverJazz-та джаз концерті (Гоголь к-сі, 40Б)."},

    # 7
    {"id": 19, "event_id": 7, "language_id": 1, "name": "Tribute to Wes Montgomery — Timeless Jazz", "description": "Tribute concert at EverJazz (Gogol St., 40B)."},
    {"id": 20, "event_id": 7, "language_id": 2, "name": "Посвящение Уэсу Монтгомери — джаз, проверенный временем", "description": "Трибьют-концерт в EverJazz (ул. Гоголя, 40Б)."},
    {"id": 21, "event_id": 7, "language_id": 3, "name": "Уэс Монтгомериге арналған кеш — уақытпен сыналған джаз", "description": "EverJazz-та трибьют-концерт (Гоголь к-сі, 40Б)."},

    # 8
    {"id": 22, "event_id": 8, "language_id": 1, "name": "Galymzhan Meiram — ‘Golden Sanremo Hits’", "description": "Music evening at La Bohême Theatre (43 Valikhanov St., corner of Zhibek Zholy)."},
    {"id": 23, "event_id": 8, "language_id": 2, "name": "Галымжан Мейрам — «Золотые хиты Сан-Ремо»", "description": "Музыкальный вечер в театре La Bohême (ул. Валиханова, 43, уг. ул. Жибек Жолы)."},
    {"id": 24, "event_id": 8, "language_id": 3, "name": "Ғалымжан Мейрам — «Сан-Ремоның алтын хиттері»", "description": "La Bohême театрындағы музыкалық кеш (Валиханов к-сі, 43, Жібек Жолы қиылысы)."},

    # 9
    {"id": 25, "event_id": 9, "language_id": 1, "name": "La Bohême — ‘February Point’", "description": "Evening event at La Bohême Theatre (43 Valikhanov St., corner of Zhibek Zholy)."},
    {"id": 26, "event_id": 9, "language_id": 2, "name": "La Bohême — «Февральская точка»", "description": "Вечер в театре La Bohême (ул. Валиханова, 43, уг. ул. Жибек Жолы)."},
    {"id": 27, "event_id": 9, "language_id": 3, "name": "La Bohême — «Ақпан нүктесі»", "description": "La Bohême театрындағы кеш (Валиханов к-сі, 43, Жібек Жолы қиылысы)."},

    # 10
    {"id": 28, "event_id": 10, "language_id": 1, "name": "Jazz Colours & Surya — Good Bye, Winter!", "description": "Live jazz show at EverJazz (Gogol St., 40B)."},
    {"id": 29, "event_id": 10, "language_id": 2, "name": "Jazz Colours & Сурья — Good bye, Winter!", "description": "Джаз-концерт в EverJazz (ул. Гоголя, 40Б)."},
    {"id": 30, "event_id": 10, "language_id": 3, "name": "Jazz Colours & Сурья — Goodbye, Winter!", "description": "EverJazz-та джаз кеші (Гоголь к-сі, 40Б)."},

    # 11
    {"id": 31, "event_id": 11, "language_id": 1, "name": "Dair Ard — Celtic Folk", "description": "Celtic folk night at EverJazz (Gogol St., 40B)."},
    {"id": 32, "event_id": 11, "language_id": 2, "name": "Dair Ard — Кельтский фолк", "description": "Вечер кельтского фолка в EverJazz (ул. Гоголя, 40Б)."},
    {"id": 33, "event_id": 11, "language_id": 3, "name": "Dair Ard — кельт фолкі", "description": "EverJazz-та кельт фолк кеші (Гоголь к-сі, 40Б)."},

    # 12
    {"id": 34, "event_id": 12, "language_id": 1, "name": "Bugarabu & Ramkhi — ‘Aura of Rhythm’", "description": "Concert-retreat at La Bohême Theatre (43 Valikhanov St., corner of Zhibek Zholy)."},
    {"id": 35, "event_id": 12, "language_id": 2, "name": "Bugarabu & Рамхи — «Аура ритма»", "description": "Концерт-ретрит в театре La Bohême (ул. Валиханова, 43, уг. ул. Жибек Жолы)."},
    {"id": 36, "event_id": 12, "language_id": 3, "name": "Bugarabu & Рамхи — «Ырғақ аурасы»", "description": "La Bohême театрындағы концерт-ретрит (Валиханов к-сі, 43, Жібек Жолы қиылысы)."},

    # 13
    {"id": 37, "event_id": 13, "language_id": 1, "name": "All Stars Jam Session — Jazz & Improvisation", "description": "Jam session night at EverJazz (Gogol St., 40B)."},
    {"id": 38, "event_id": 13, "language_id": 2, "name": "All stars jam session — Джазовая музыка и импровизация", "description": "Джем-сейшн в EverJazz (ул. Гоголя, 40Б)."},
    {"id": 39, "event_id": 13, "language_id": 3, "name": "All Stars Jam Session — джаз және импровизация", "description": "EverJazz-та джем-сейшн (Гоголь к-сі, 40Б)."},

    # 14
    {"id": 40, "event_id": 14, "language_id": 1, "name": "Raushan Abisheva — River of Love", "description": "Live performance at EverJazz (Gogol St., 40B)."},
    {"id": 41, "event_id": 14, "language_id": 2, "name": "Раушан Абишева — River of Love", "description": "Концерт в EverJazz (ул. Гоголя, 40Б)."},
    {"id": 42, "event_id": 14, "language_id": 3, "name": "Раушан Әбішева — River of Love", "description": "EverJazz-та концерт (Гоголь к-сі, 40Б)."},

    # 15
    {"id": 43, "event_id": 15, "language_id": 1, "name": "Pop Queens — Dua Lipa & Rihanna Night", "description": "Pop hits night with EverJazz residents (Gogol St., 40B)."},
    {"id": 44, "event_id": 15, "language_id": 2, "name": "Pop Queens — Dua Lipa & Rihanna Night (Юлия Яковлева и резиденты EverJazz)", "description": "Вечер поп-хитов с резидентами EverJazz (ул. Гоголя, 40Б)."},
    {"id": 45, "event_id": 15, "language_id": 3, "name": "Pop Queens — Dua Lipa & Rihanna Night", "description": "EverJazz резиденттерімен поп-хиттер кеші (Гоголь к-сі, 40Б)."},

    # 16
    {"id": 46, "event_id": 16, "language_id": 1, "name": "Eric B. Turner (USA) — Jazz & Blues from the Heart of America", "description": "Live jazz & blues at EverJazz (Gogol St., 40B)."},
    {"id": 47, "event_id": 16, "language_id": 2, "name": "Eric B. Turner (США) — Джаз и блюз из сердца Америки", "description": "Концерт в EverJazz (ул. Гоголя, 40Б)."},
    {"id": 48, "event_id": 16, "language_id": 3, "name": "Eric B. Turner (АҚШ) — Американың жүрегінен джаз және блюз", "description": "EverJazz-та концерт (Гоголь к-сі, 40Б)."},

    # 17
    {"id": 49, "event_id": 17, "language_id": 1, "name": "Diana Makina — Author’s Concert", "description": "Live concert at EverJazz (Gogol St., 40B). Duration: 120 minutes."},
    {"id": 50, "event_id": 17, "language_id": 2, "name": "Диана Макина", "description": "Авторский концерт в EverJazz (ул. Гоголя, 40Б). Длительность: 120 минут."},
    {"id": 51, "event_id": 17, "language_id": 3, "name": "Диана Макина", "description": "EverJazz-та авторлық концерт (Гоголь к-сі, 40Б). Ұзақтығы: 120 минут."},

    # 18
    {"id": 52, "event_id": 18, "language_id": 1, "name": "Gaukhar Sattarova & STEPS — Hot Jazz Funk", "description": "Hot jazz-funk night at EverJazz (Gogol St., 40B). Duration: 120 minutes."},
    {"id": 53, "event_id": 18, "language_id": 2, "name": "Гаухар Саттарова & STEPS", "description": "Hot jazz-funk в EverJazz (ул. Гоголя, 40Б). Длительность: 120 минут."},
    {"id": 54, "event_id": 18, "language_id": 3, "name": "Гаухар Саттарова & STEPS", "description": "EverJazz-та hot jazz-funk кеші (Гоголь к-сі, 40Б). Ұзақтығы: 120 минут."},

    # 19
    {"id": 55, "event_id": 19, "language_id": 1, "name": "Tribute to Wes Montgomery", "description": "Tribute concert at EverJazz (Gogol St., 40B). Duration: 120 minutes."},
    {"id": 56, "event_id": 19, "language_id": 2, "name": "Tribute to Wes Montgomery", "description": "Трибьют-концерт в EverJazz (ул. Гоголя, 40Б). Длительность: 120 минут."},
    {"id": 57, "event_id": 19, "language_id": 3, "name": "Wes Montgomery-ге трибьют", "description": "EverJazz-та трибьют-концерт (Гоголь к-сі, 40Б). Ұзақтығы: 120 минут."},

    # 20
    {"id": 58, "event_id": 20, "language_id": 1, "name": "Irena Aravina & Jazz House — Goodbye Winter", "description": "Live jazz at EverJazz (Gogol St., 40B). Duration: 120 minutes."},
    {"id": 59, "event_id": 20, "language_id": 2, "name": "Ирэна Аравина & Jazz House", "description": "Джаз-концерт в EverJazz (ул. Гоголя, 40Б). Длительность: 120 минут."},
    {"id": 60, "event_id": 20, "language_id": 3, "name": "Ирэна Аравина & Jazz House", "description": "EverJazz-та джаз концерті (Гоголь к-сі, 40Б). Ұзақтығы: 120 минут."},

    # 21
    {"id": 61, "event_id": 21, "language_id": 1, "name": "Gulnara Bertisbaeva & Friends — Happy Day", "description": "Live concert at EverJazz (Gogol St., 40B). Duration: 120 minutes."},
    {"id": 62, "event_id": 21, "language_id": 2, "name": "Гульнара Бертисбаева & Friends", "description": "Концерт в EverJazz (ул. Гоголя, 40Б). Длительность: 120 минут."},
    {"id": 63, "event_id": 21, "language_id": 3, "name": "Гульнара Бертисбаева & Friends", "description": "EverJazz-та концерт (Гоголь к-сі, 40Б). Ұзақтығы: 120 минут."},

    # 22
    {"id": 64, "event_id": 22, "language_id": 1, "name": "Igor Ananyev & Akko Band — Noche de Acordeon", "description": "Accordion night at EverJazz (Gogol St., 40B). Duration: 120 minutes."},
    {"id": 65, "event_id": 22, "language_id": 2, "name": "Игорь Ананьев & Akko band", "description": "Вечер аккордеона в EverJazz (ул. Гоголя, 40Б). Длительность: 120 минут."},
    {"id": 66, "event_id": 22, "language_id": 3, "name": "Игорь Ананьев & Akko band", "description": "EverJazz-та аккордеон кеші (Гоголь к-сі, 40Б). Ұзақтығы: 120 минут."},

    # 23
    {"id": 67, "event_id": 23, "language_id": 1, "name": "Aikyn Tolepbergen — Live in Almaty", "description": "Concert at Baluan Sholak Sports Palace (Abay Ave., 44). Duration: 120 minutes."},
    {"id": 68, "event_id": 23, "language_id": 2, "name": "Айқын Төлепберген", "description": "Концерт во Дворце спорта им. Балуана Шолака (пр. Абая, 44). Длительность: 120 минут."},
    {"id": 69, "event_id": 23, "language_id": 3, "name": "Айқын Төлепберген", "description": "Балуан Шолақ атындағы спорт сарайындағы концерт (Абай даңғ., 44). Ұзақтығы: 120 минут."},

    # 24
    {"id": 70, "event_id": 24, "language_id": 1, "name": "Nurbulat Abdullin — Live Concert", "description": "Concert at Republic Palace (Dostyk Ave., 56). Duration: 120 minutes."},
    {"id": 71, "event_id": 24, "language_id": 2, "name": "Нұрболат Абдуллин", "description": "Концерт в Республика Сарайы (пр. Достык, 56). Длительность: 120 минут."},
    {"id": 72, "event_id": 24, "language_id": 3, "name": "Нұрболат Абдуллин", "description": "Республика сарайындағы концерт (Достық даңғ., 56). Ұзақтығы: 120 минут."},

    # 25
    {"id": 73, "event_id": 25, "language_id": 1, "name": "Makpal Zhunusova — Holiday Concert (16:00)", "description": "Holiday concert at Republic Palace (Dostyk Ave., 56). Duration: 120 minutes."},
    {"id": 74, "event_id": 25, "language_id": 2, "name": "Мақпал Жүнісова", "description": "Мерекелік концерт (16:00) в Республика Сарайы (пр. Достык, 56). Длительность: 120 минут."},
    {"id": 75, "event_id": 25, "language_id": 3, "name": "Мақпал Жүнісова — мерекелік концерт (16:00)", "description": "Республика сарайындағы мерекелік концерт (16:00) (Достық даңғ., 56). Ұзақтығы: 120 минут."},

    # 26
    {"id": 76, "event_id": 26, "language_id": 1, "name": "Makpal Zhunusova — Holiday Concert (20:00)", "description": "Holiday concert at Republic Palace (Dostyk Ave., 56). Duration: 120 minutes."},
    {"id": 77, "event_id": 26, "language_id": 2, "name": "Мақпал Жүнісова", "description": "Мерекелік концерт (20:00) в Республика Сарайы (пр. Достык, 56). Длительность: 120 минут."},
    {"id": 78, "event_id": 26, "language_id": 3, "name": "Мақпал Жүнісова — мерекелік концерт (20:00)", "description": "Республика сарайындағы мерекелік концерт (20:00) (Достық даңғ., 56). Ұзақтығы: 120 минут."},

    # 27
    {"id": 79, "event_id": 27, "language_id": 1, "name": "‘Zhigitter’ Live Concert", "description": "Live concert at Republic Palace (Dostyk Ave., 56). Duration: 120 minutes."},
    {"id": 80, "event_id": 27, "language_id": 2, "name": "«Жігіттер»", "description": "Концерт в Республика сарайы (пр. Достык, 56). Длительность: 120 минут."},
    {"id": 81, "event_id": 27, "language_id": 3, "name": "«Жігіттер»", "description": "Республика сарайындағы концерт (Достық даңғ., 56). Ұзақтығы: 120 минут."},

    # 28
    {"id": 82, "event_id": 28, "language_id": 1, "name": "Nauryz Fest — Gala Concert", "description": "Gala concert at Republic Palace (Dostyk Ave., 56). Starts at 19:30. Duration: 120 minutes."},
    {"id": 83, "event_id": 28, "language_id": 2, "name": "Nauryz Fest (сборный концерт)", "description": "Сборный концерт в Республика Сарайы (пр. Достык, 56). Начало в 19:30. Длительность: 120 минут."},
    {"id": 84, "event_id": 28, "language_id": 3, "name": "Nauryz Fest (құрама концерт)", "description": "Республика сарайындағы құрама концерт (Достық даңғ., 56). Басталуы 19:30. Ұзақтығы: 120 минут."},

    # 29
    {"id": 85, "event_id": 29, "language_id": 1, "name": "Anton Belyaev & Therr Maitz — Solo Concert", "description": "Solo concert at the Republic Palace (Dostyk Ave., 56). Duration: 120 minutes."},
    {"id": 86, "event_id": 29, "language_id": 2, "name": "Anton Belyaev & Therr Maitz", "description": "Сольный концерт во Дворце Республики (пр. Достык, 56). Длительность: 120 минут."},
    {"id": 87, "event_id": 29, "language_id": 3, "name": "Anton Belyaev & Therr Maitz", "description": "Республика сарайындағы жеке концерт (Достық даңғ., 56). Ұзақтығы: 120 минут."},

    # 30
    {"id": 88, "event_id": 30, "language_id": 1, "name": "‘Song and Singer’ Concert", "description": "Concert at Republic Palace (Dostyk Ave., 56). Duration: 120 minutes."},
    {"id": 89, "event_id": 30, "language_id": 2, "name": "«Ән мен әнші»", "description": "Концерт в Республика Сарайы (пр. Достык, 56). Длительность: 120 минут."},
    {"id": 90, "event_id": 30, "language_id": 3, "name": "«Ән мен әнші»", "description": "Республика сарайындағы концерт (Достық даңғ., 56). Ұзақтығы: 120 минут."},

    # 31
    {"id": 91, "event_id": 31, "language_id": 1, "name": "Antoha MC Live in Almaty", "description": "Live concert at Motor club (Nazarbayev Ave., 50). Duration: 120 minutes."},
    {"id": 92, "event_id": 31, "language_id": 2, "name": "Концерт Антоха МС в Алматы", "description": "Концерт в Motor club (ул. Назарбаева, 50). Длительность: 120 минут."},
    {"id": 93, "event_id": 31, "language_id": 3, "name": "Алматыдағы Антоха МС концерті", "description": "Motor club-та концерт (Назарбаев даңғ., 50). Ұзақтығы: 120 минут."},

    # 32
    {"id": 94, "event_id": 32, "language_id": 1, "name": "Mrs Kazakhstan Contest", "description": "Beauty contest at the Republic Palace (Dostyk Ave., 56). Duration: 120 minutes."},
    {"id": 95, "event_id": 32, "language_id": 2, "name": "Конкурс Mrs Kazakhstan", "description": "Конкурс во Дворце Республики (пр. Достык, 56). Длительность: 120 минут."},
    {"id": 96, "event_id": 32, "language_id": 3, "name": "Mrs Kazakhstan байқауы", "description": "Республика сарайындағы байқау (Достық даңғ., 56). Ұзақтығы: 120 минут."},

    # 33
    {"id": 97, "event_id": 33, "language_id": 1, "name": "Wedding Fair 2026 in Almaty", "description": "Wedding expo at The Ritz-Carlton Almaty (Al-Farabi Ave., 77/7). First day of the fair (Feb 28 – Mar 1)."},
    {"id": 98, "event_id": 33, "language_id": 2, "name": "Wedding Fair 2026 в Алматы", "description": "Свадебная выставка в The Ritz-Carlton Almaty (пр. Аль-Фараби, 77/7). Первый день выставки (28.02–01.03)."},
    {"id": 99, "event_id": 33, "language_id": 3, "name": "Алматыдағы Wedding Fair 2026", "description": "The Ritz-Carlton Almaty-дегі үйлену тойы көрмесі (Әл-Фараби даңғ., 77/7). Көрменің алғашқы күні (28.02–01.03)."},
]


CALENDAR_EVENTS_DATA = [
    {"id": 1, "user_id": 1, "event_id": 1, "status": 1}, # проставить везде 1
    {"id": 2, "user_id": 1, "event_id": 2, "status": 1},
    {"id": 3, "user_id": 1, "event_id": 3, "status": 1},
    {"id": 4, "user_id": 1, "event_id": 4, "status": 1},
    {"id": 5, "user_id": 1, "event_id": 5, "status": 1},
    {"id": 6, "user_id": 1, "event_id": 6, "status": 1},
    {"id": 7, "user_id": 1, "event_id": 7, "status": 1},
    {"id": 8, "user_id": 1, "event_id": 8, "status": 1},
    {"id": 9, "user_id": 1, "event_id": 9, "status": 1},
    {"id": 10, "user_id": 1, "event_id": 10, "status": 1},
    {"id": 11, "user_id": 1, "event_id": 11, "status": 1},
    {"id": 12, "user_id": 1, "event_id": 12, "status": 1},
    {"id": 13, "user_id": 1, "event_id": 13, "status": 1},
    {"id": 14, "user_id": 1, "event_id": 14, "status": 1},
    {"id": 15, "user_id": 1, "event_id": 15, "status": 1},
    {"id": 16, "user_id": 1, "event_id": 16, "status": 1},
    {"id": 17, "user_id": 1, "event_id": 17, "status": 1},
    {"id": 18, "user_id": 1, "event_id": 18, "status": 1},
    {"id": 19, "user_id": 1, "event_id": 19, "status": 1},
    {"id": 20, "user_id": 1, "event_id": 20, "status": 1},
    {"id": 21, "user_id": 1, "event_id": 21, "status": 1},
    {"id": 22, "user_id": 1, "event_id": 22, "status": 1},
    {"id": 23, "user_id": 1, "event_id": 23, "status": 1},
    {"id": 24, "user_id": 1, "event_id": 24, "status": 1},
    {"id": 25, "user_id": 1, "event_id": 25, "status": 1},
    {"id": 26, "user_id": 1, "event_id": 26, "status": 1},
    {"id": 27, "user_id": 1, "event_id": 27, "status": 1},
    {"id": 28, "user_id": 1, "event_id": 28, "status": 1},
    {"id": 29, "user_id": 1, "event_id": 29, "status": 1},
    {"id": 30, "user_id": 1, "event_id": 30, "status": 1},
    {"id": 31, "user_id": 1, "event_id": 31, "status": 1},
    {"id": 32, "user_id": 1, "event_id": 32, "status": 1},
    {"id": 33, "user_id": 1, "event_id": 33, "status": 1},
]

SOUVENIRS_DATA = [
    {
        "id": 1,
        "name": "JER Ceramics",
        "address": "​Микрорайон Таугуль-1, 47",
        "link": "https://www.instagram.com/jer.community/",
        "image": "images/info/souvenirs/jer.jpg",
    },
    {
        "id": 2,
        "name": "Tartpa",
        "address": "​Улица Байсеитовой, 45",
        "link": "https://tartpa.kz/",
        "image": "images/info/souvenirs/tartpa.jpg",
    },
    {
        "id": 3,
        "name": "Sinichki Store",
        "address": "​Улица Айтеке би, 53",
        "link": "https://www.instagram.com/sinichki.store/",
        "image": "images/info/souvenirs/sinichki-store.jpg",
    },
    {
        "id": 4,
        "name": "Quraq Korpe",
        "address": "​Улица Панфилова, 92",
        "link": "https://www.instagram.com/kurak_korpe/",
        "image": "images/info/souvenirs/quraq-korpe.jpg",
    },
    {
        "id": 5,
        "name": "BEEPL",
        "address": "Кармысова 82/1",
        "link": "https://www.instagram.com/beepl_space/",
        "image": "images/info/souvenirs/beepl.jpg",
    },
    {
        "id": 6,
        "name": "Meloman",
        "address": "​Улица Гоголя, 58",
        "link": "https://www.meloman.kz/",
        "image": "images/info/souvenirs/meloman.jpg",
    },
]

APPS_DATA = [
    {
        "id": 1,
        "name": "ONAY",
        "image": "images/info/apps/onay.jpg",
        "description": "An app for paying for public transportation and managing your transit card in Almaty.",
    },
    {
        "id": 2,
        "name": "Uber",
        "image": "images/info/apps/uber.jpg",
        "description": "An international taxi service available in Almaty.",
    },
    {
        "id": 3,
        "name": "inDrive",
        "image": "images/info/apps/indrive.jpg",
        "description": "A taxi service where users can suggest their own fare.",
    },
    {
        "id": 4,
        "name": "Yandex Go",
        "image": "images/info/apps/yandexgo.jpg",
        "description": "A popular taxi and delivery service in Kazakhstan.",
    },
    {
        "id": 5,
        "name": "2GIS",
        "image": "images/info/apps/2gis.jpg",
        "description": "Offline city maps, navigation, and a directory of businesses in Almaty.",
    },
    {
        "id": 6,
        "name": "Google Maps",
        "image": "images/info/apps/google-maps.jpg",
        "description": "Navigation, public transportation routes, and reviews of places.",
    },
    {
        "id": 7,
        "name": "Booking.com",
        "image": "images/info/apps/booking.jpg",
        "description": "A platform for booking hotels and accommodations.",
    },
    {
        "id": 8,
        "name": "Airbnb",
        "image": "images/info/apps/airbnb.jpg",
        "description": "A service for short-term rentals of apartments and houses.",
    },
    {
        "id": 9,
        "name": "Glovo",
        "image": "images/info/apps/glovo.jpg",
        "description": "Food and grocery delivery service in Almaty.",
    },
    {
        "id": 10,
        "name": "Wolt",
        "image": "images/info/apps/wolt.jpg",
        "description": "An app for ordering food and groceries.",
    },
    {
        "id": 11,
        "name": "Kaspi.kz",
        "image": "images/info/apps/kaspi.jpg",
        "description": "Mobile banking and QR payments, which are widely used in Kazakhstan.",
    },
    {
        "id": 12,
        "name": "Google Translate",
        "image": "images/info/apps/google-translate.jpg",
        "description": "An app for translating text, speech, and using the camera.",
    }
]

ADVERTISEMENTS_DATA = [
    {
        "id": 1,
        "image": "ads/banner.jpg",
        "is_active": True,
        "priority": 1,
    }
]

ADVERTISEMENT_TRANSLATIONS_DATA = [
    {
        "id": 1,
        "advertisement_id": 1,
        "language_id": 1,  # От 0 до 3
        "name": "Winter Sale",
        "description": "Up to 50% discount",
    }
]


class Command(BaseCommand):
    help = "Load production initial data into database"

    @transaction.atomic
    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        started = NOW()

        self.load_users()
        self.load_places()
        self.load_place_translations()
        self.load_events()
        self.load_event_translations()
        self.load_calendar_events()
        self.load_souvenirs()
        self.load_apps()
        self.load_advertisements()
        self.load_advertisement_translations()

        self.stdout.write(
            self.style.SUCCESS(
                f"Data successfully loaded in {(NOW() - started).total_seconds()} sec"
            )
        )

    # ========================================================
    # ===================== КОНЕЦ ======================
    # ========================================================

    def load_users(self):
        for user in USERS_DATA:
            CustomUser.objects.update_or_create(
                id=user["id"],
                defaults={
                    "email": user["email"],
                    "phone": user["phone"],
                    "password": user["password"],
                    "is_superuser": bool(user["is_superuser"]),
                    "username": user["username"],
                    # date_joined по схеме DEFAULT CURRENT_TIMESTAMP, но можно проставить явно:
                    "date_joined": NOW(),
                    "last_login": NOW(),
                    "is_active": bool(user["is_active"]),
                },
            )

    def load_places(self):
        for place in PLACES_DATA:
            Place.objects.update_or_create(
                id=place["id"],
                defaults={
                    "image": place["image"],
                    "category": place["category"],
                    "address": place["address"],
                    "link": place["link"],
                    "lat": place["lat"],
                    "lng": place["lng"],
                    # created_at по схеме DEFAULT CURRENT_TIMESTAMP — можно не трогать,
                    # но при update лучше обновлять updated_at:
                    "updated_at": NOW(),
                    # deleted_at в новой схеме DATETIME NULL, НЕ 0:
                    "deleted_at": None,
                },
            )

    def load_place_translations(self):
        """
        Важно: в схеме UNIQUE(place_id, language_id)
        Поэтому лучше искать по (place_id, language_id), а не по id,
        чтобы не ловить дубли при изменении сидов.
        """
        for tr in PLACE_TRANSLATIONS_DATA:
            PlaceTranslation.objects.update_or_create(
                place_id=tr["place_id"],
                language_id=tr["language_id"],
                defaults={
                    "name": tr["name"],
                    "timetable": tr["timetable"],
                    "description": tr["description"],
                },
            )

    def load_events(self):
        for event in EVENTS_DATA:
            Event.objects.update_or_create(
                id=event["id"],
                defaults={
                    "image": event["image"],
                    "date": event["date"],                 # DATE
                    "start_time": event["start_time"],     # TIME
                    "duration": event["duration"],
                    "artist": event["artist"],
                    "cost": event["cost"],
                    "currency": event.get("currency", "KZT"),
                    "category": event["category"],
                    "address": event["address"],
                    "link": event["link"],
                    "updated_at": NOW(),
                    "deleted_at": None,
                },
            )

    def load_event_translations(self):
        """
        UNIQUE(event_id, language_id) -> ищем по этим полям.
        """
        for tr in EVENT_TRANSLATIONS_DATA:
            EventTranslation.objects.update_or_create(
                event_id=tr["event_id"],
                language_id=tr["language_id"],
                defaults={
                    "name": tr["name"],
                    "description": tr["description"],
                },
            )

    def load_calendar_events(self):
        """
        В новой схеме нет поля date.
        UNIQUE(user_id, event_id) -> ищем по (user_id, event_id).
        """
        for item in CALENDAR_EVENTS_DATA:
            CalendarEvent.objects.update_or_create(
                user_id=item["user_id"],
                event_id=item["event_id"],
                defaults={
                    "status": item["status"],
                },
            )

    def load_souvenirs(self):
        for item in SOUVENIRS_DATA:
            Souvenir.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "address": item["address"],
                    "link": item["link"],
                    "image": item.get("image"),  # image nullable
                },
            )

    def load_apps(self):
        for item in APPS_DATA:
            App.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "image": item["image"],
                    "description": item["description"],
                },
            )

    def load_advertisements(self):
        for ad in ADVERTISEMENTS_DATA:
            Advertisement.objects.update_or_create(
                id=ad["id"],
                defaults={
                    "image": ad["image"],
                    "updated_at": NOW(),
                    "is_active": bool(ad["is_active"]),
                    "priority": ad["priority"],
                },
            )

    def load_advertisement_translations(self):
        """
        UNIQUE(advertisement_id, language_id) -> ищем по этим полям.
        """
        for tr in ADVERTISEMENT_TRANSLATIONS_DATA:
            AdvertisementTranslation.objects.update_or_create(
                advertisement_id=tr["advertisement_id"],
                language_id=tr["language_id"],
                defaults={
                    "name": tr["name"],
                    "description": tr["description"],
                },
            )
