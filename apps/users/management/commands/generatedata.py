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
        "image": "places/kbtu.jpg",
        "category": 1,
        "address": "Almaty, Tole Bi 59",
        "link": "https://kbtu.edu.kz"
    }
]

PLACE_TRANSLATIONS_DATA = [
    {
        "id": 1,
        "place_id": 1,
        "language_id": 1,  # English
        "name": "Kazakh-British Technical University (KBTU)",
        "timetable": "09:00 - 18:00",
        "description": "Kazakh-British Technical University (KBTU) is one of the leading technical universities in Kazakhstan, located in the center of Almaty. The university is well known for its programs in information technology, engineering, business, and energy industries. KBTU is situated in a historic building and provides modern education, international partnerships, research opportunities, and innovative learning environments for students.",
    },
    {
        "id": 2,
        "place_id": 1,
        "language_id": 2,  # Russian
        "name": "Казахстанско-Британский технический университет (КБТУ)",
        "timetable": "09:00 - 18:00",
        "description": "Казахстанско-Британский технический университет (КБТУ) — один из ведущих технических университетов Казахстана, расположенный в центре Алматы. Университет известен своими программами в области информационных технологий, инженерии, бизнеса и энергетики. КБТУ находится в историческом здании и предоставляет современное образование, международные партнерства, исследовательские возможности и инновационную образовательную среду для студентов.",
    },
    {
        "id": 3,
        "place_id": 1,
        "language_id": 3,  # Kazakh
        "name": "Қазақстан-Британ техникалық университеті (ҚБТУ)",
        "timetable": "09:00 - 18:00",
        "description": "Қазақстан-Британ техникалық университеті (ҚБТУ) — Алматы қаласының орталығында орналасқан Қазақстандағы жетекші техникалық жоғары оқу орындарының бірі. Университет ақпараттық технологиялар, инженерия, бизнес және энергетика салаларындағы білім беру бағдарламаларымен танымал. ҚБТУ тарихи ғимаратта орналасқан және студенттерге заманауи білім, халықаралық серіктестік, ғылыми-зерттеу мүмкіндіктері мен инновациялық оқу ортасын ұсынады.",
    },
]

EVENTS_DATA = [
    {
        "id": 1,
        "image": "https://sxodim.com/uploads/posts/2026/01/15/optimized/eadbbf33219d4f446982451ce810c21f_545x305-q-85.jpg",
        "date": date(2026, 2, 20),
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
        "date": date(2026, 2, 24),
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
        "date": date(2026, 4, 17),
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
        "date": date(2026, 3, 27),
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
        "date": date(2026, 2, 17),
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
        "date": date(2026, 2, 19),
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
        "date": date(2026, 2, 20),
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
        "date": date(2026, 2, 20),
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
        "date": date(2026, 2, 21),
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
        "date": date(2026, 2, 21),
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
        "date": date(2026, 2, 21),
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
        "date": date(2026, 2, 22),
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
        "date": date(2026, 2, 23),
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
        "date": date(2026, 2, 24),
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
        "date": date(2026, 2, 25),
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
        "date": date(2026, 2, 26),
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
        "date": date(2026, 2, 27),
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
        "date": date(2026, 2, 27),
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
        "date": date(2026, 2, 28),
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
        "date": date(2026, 2, 28),
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
        "date": date(2026, 3, 1),
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
        "date": date(2026, 3, 1),
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
        "date": date(2026, 3, 6),
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
        "date": date(2026, 3, 7),
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
        "date": date(2026, 3, 8),
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
        "date": date(2026, 3, 8),
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
        "date": date(2026, 3, 10),
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
        "date": date(2026, 3, 11),
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
        "date": date(2026, 3, 17),
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
        "date": date(2026, 3, 18),
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
        "date": date(2026, 3, 21),
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
        "date": date(2026, 3, 20),
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
        "date": date(2026, 2, 28),          # первый день выставки (28.02–01.03)
        "start_time": dtime(12, 0),         
        "duration": 480, 
        "artist": "Wedding Fair 2026 в Алматы",
        "cost": 9990,                       # от 9 990 ₸ на сайте
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
        "name": "Сувенирная тарелка «Қазақ хандығына 550 жыл»",
        "address": "ул. Шевченко 133Б, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/suvjen-rnyje-tarjelk/",
        "image": "https://ademi-ai.kz/image/catalog/suv/plate-khanate550.jpg",
    },
    {
        "id": 2,
        "name": "Тарелка Абай",
        "address": "ул. Шевченко 133Б, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/suvjen-rnyje-tarjelk/",
        "image": "https://ademi-ai.kz/image/catalog/suv/plate-abai.jpg",
    },
    {
        "id": 3,
        "name": "Плакетка Абай",
        "address": "ул. Шевченко 133Б, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/suvjen-rnyje-tarjelk/",
        "image": "https://ademi-ai.kz/image/catalog/suv/plaque-abai.jpg",
    },
    {
        "id": 4,
        "name": "Книга Абай Кунанбаев (подарочная тарелка)",
        "address": "ул. Шевченко 133Б, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/suvjen-rnyje-tarjelk/",
        "image": "https://ademi-ai.kz/image/catalog/suv/book-abai.jpg",
    },
    {
        "id": 5,
        "name": "Брелок Албан",
        "address": "ул. Шевченко 133Б, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/brelok-alban.jpg",
    },
    {
        "id": 6,
        "name": "Брелок Беріш",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/brelok-berish.jpg",
    },
    {
        "id": 7,
        "name": "Брелок Жаппас",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/brelok-zhappas.jpg",
    },
    {
        "id": 8,
        "name": "Брелок Шанышқылы",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/brelok-shanyshkyly.jpg",
    },
    {
        "id": 9,
        "name": "Брелок Шекті",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/brelok-shekti.jpg",
    },
    {
        "id": 10,
        "name": "Брелок Шөмекей",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/brelok-shomekey.jpg",
    },
    {
        "id": 11,
        "name": "Брелок Қаракесек",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/brelok-karakesek.jpg",
    },
    {
        "id": 12,
        "name": "Брелок Қызылқұрт",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/brelok-kyzylqurt.jpg",
    },
    {
        "id": 13,
        "name": "Магнитка Бесик той",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/magnit-besik-toy.jpg",
    },
    {
        "id": 14,
        "name": "Мягкая игрушка Куат",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/myagkaya-igrushka-kuat.jpg",
    },
    {
        "id": 15,
        "name": "Мягкая игрушка Молдир",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/myagkaya-igrushka-moldir.jpg",
    },
    {
        "id": 16,
        "name": "Мягкая игрушка Сауле",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/myagkaya-igrushka-saule.jpg",
    },
    {
        "id": 17,
        "name": "Набор аксессуаров Новый Казахстан",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/noviy-kazakhstan-set.jpg",
    },
    {
        "id": 18,
        "name": "Сувенир Асык в мешочке",
        "address": "ул. Шевченко 133B, Алматы, Казахстан",
        "link": "https://ademi-ai.kz/aksessuary/",
        "image": "https://ademi-ai.kz/image/catalog/aksessuary/asyk-v-meshochke.jpg",
    },
    {
        "id": 19,
        "name": "Almaty Pen",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/almaty_pen.jpg",
    },
    {
        "id": 20,
        "name": "Altyn Adam statuette (big)",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/altyn_adam_statuette.jpg",
    },
    {
        "id": 21,
        "name": "Almaty Gift Set",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/almaty_gift_set.jpg",
    },
    {
        "id": 22,
        "name": "Trolley Almaty",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/almaty_trolley.jpg",
    },
    {
        "id": 23,
        "name": "Almaty Umbrella",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/almaty_umbrella.jpg",
    },
    {
        "id": 24,
        "name": "Alma Cosmetic Bag",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/alma_cosmetic_bag.jpg",
    },
    {
        "id": 25,
        "name": "Alma Scarf",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/alma_scarf.jpg",
    },
    {
        "id": 26,
        "name": "Almaty Musical Box Figurine",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/almaty_musical_box.jpg",
    },
    {
        "id": 27,
        "name": "Wall Panel Almaty",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/wall_panel_almaty.jpg",
    },
    {
        "id": 28,
        "name": "Altyn Alma Mug (1 person)",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/altyn_alma_mug.jpg",
    },
    {
        "id": 29,
        "name": "Altyn Alma Tea Pair (1 person)",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/altyn_alma_tea_pair.jpg",
    },
    {
        "id": 30,
        "name": "Almaly Tea Set for 6 Persons",
        "address": "пр. Аль-Фараби, 5, PFC \"Нурлы Тау\", блок 2A, 7 этаж, офис 702, Алматы, Казахстан",
        "link": "https://empire.kz/ru/collections/almaty/",
        "image": "https://empire.kz/image/collection/almaty/almaly_tea_set.jpg",
    }
]

APPS_DATA = [
    {
        "id": 1,
        "name": "ONAY",
        "image": "apps/onay.png",
        "description": "Приложение для оплаты общественного транспорта и управления транспортной картой в Алматы.",
    },
    {
        "id": 2,
        "name": "Uber",
        "image": "apps/uber.png",
        "description": "Международный сервис такси, доступный в Алматы.",
    },
    {
        "id": 3,
        "name": "inDrive",
        "image": "apps/indrive.png",
        "description": "Сервис такси, где пользователь может предложить свою цену поездки.",
    },
    {
        "id": 4,
        "name": "Yandex Go",
        "image": "apps/yandexgo.png",
        "description": "Популярный сервис такси и доставки в Казахстане.",
    },
    {
        "id": 5,
        "name": "2GIS",
        "image": "apps/2gis.png",
        "description": "Офлайн-карты города, навигация и справочник организаций Алматы.",
    },
    {
        "id": 6,
        "name": "Google Maps",
        "image": "apps/googlemaps.png",
        "description": "Навигация, маршруты общественного транспорта и отзывы о местах.",
    },
    {
        "id": 7,
        "name": "Booking.com",
        "image": "apps/booking.png",
        "description": "Платформа для бронирования отелей и жилья.",
    },
    {
        "id": 8,
        "name": "Airbnb",
        "image": "apps/airbnb.png",
        "description": "Сервис краткосрочной аренды квартир и домов.",
    },
    {
        "id": 9,
        "name": "Glovo",
        "image": "apps/glovo.png",
        "description": "Сервис доставки еды и товаров в Алматы.",
    },
    {
        "id": 10,
        "name": "Wolt",
        "image": "apps/wolt.png",
        "description": "Приложение для заказа еды и продуктов.",
    },
    {
        "id": 11,
        "name": "Kaspi.kz",
        "image": "apps/kaspi.png",
        "description": "Мобильный банкинг и QR-оплата, широко используемая в Казахстане.",
    },
    {
        "id": 12,
        "name": "Google Translate",
        "image": "apps/googletranslate.png",
        "description": "Приложение для перевода текста, речи и с помощью камеры.",
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
