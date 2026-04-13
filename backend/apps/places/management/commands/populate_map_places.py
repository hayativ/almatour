from django.core.management.base import BaseCommand
from apps.places.models import Place, PlaceTranslation

class Command(BaseCommand):
    help = 'Populate the database with the initial 19 places for the map.'

    def handle(self, *args, **kwargs):
        places_data = [
            {
                'id': 1001,
                'slug': 'tselinny-center',
                'name': 'The Tselinny Center for Contemporary Culture',
                'description': 'The Tselinny Center for Contemporary Culture is one of the most iconic cultural hubs in Almaty, Kazakhstan.',
                'address': 'Abay Ave 117/6, Almaty 050000',
                'lat': 43.2387,
                'lng': 76.9504,
                'category': 1,
            },
            {
                'id': 1002,
                'slug': 'ascension-cathedral',
                'name': 'Ascension Cathedral',
                'description': 'The Ascension Cathedral (Zenkov Cathedral) is a Russian Orthodox cathedral located in Panfilov Park.',
                'address': '97 Gogol St, Almaty 050000',
                'lat': 43.2578,
                'lng': 76.9533,
                'category': 0,
            },
            {
                'id': 1003,
                'slug': 'almaty-museum-of-arts',
                'name': 'Almaty Museum of Arts',
                'description': 'The Almaty Museum of Arts houses an extensive collection of Kazakh fine art.',
                'address': 'Satpaev Ave 22A, Almaty 050040',
                'lat': 43.2399,
                'lng': 76.9365,
                'category': 1,
            },
            {
                'id': 1004,
                'slug': 'kazakhstan-hotel',
                'name': 'Kazakhstan Hotel',
                'description': 'The Kazakhstan Hotel is a landmark building in Almaty, recognizable by its distinctive crown-shaped top.',
                'address': 'Dostyk Ave 52/2, Almaty 050010',
                'lat': 43.2369,
                'lng': 76.9455,
                'category': 0,
            },
            {
                'id': 1005,
                'slug': 'almaty-hotel',
                'name': 'Almaty Hotel',
                'description': 'Almaty Hotel is a classic hotel located in the heart of the city.',
                'address': 'Kabanbay Batyr St 85, Almaty 050000',
                'lat': 43.2573,
                'lng': 76.9407,
                'category': 0,
            },
            {
                'id': 1006,
                'slug': 'lermontov-drama-theater',
                'name': 'Lermontov Drama Theater',
                'description': 'The Russian Academic Drama Theater named after M. Lermontov is one of the oldest theaters in Kazakhstan.',
                'address': 'Abay Ave 43, Almaty 050000',
                'lat': 43.2541,
                'lng': 76.9374,
                'category': 1,
            },
            {
                'id': 1007,
                'slug': 'kasteev-museum',
                'name': 'State Museum of Arts of the Republic of Kazakhstan named after A. Kasteev',
                'description': 'The A. Kasteev State Museum of Arts is the largest art museum in Kazakhstan.',
                'address': 'Satpaev Ave 22, Almaty 050040',
                'lat': 43.2330,
                'lng': 76.9580,
                'category': 1,
            },
            {
                'id': 1008,
                'slug': 'green-bazaar',
                'name': 'Green Bazaar',
                'description': 'The Green Bazaar (Zelyony Bazar) is one of Almaty\'s most famous and oldest marketplaces.',
                'address': 'Zhibek Zholy Ave 53, Almaty 050000',
                'lat': 43.2564,
                'lng': 76.9435,
                'category': 0,
            },
            {
                'id': 1009,
                'slug': 'memorial-of-glory',
                'name': 'Memorial of Glory',
                'description': 'The Memorial of Glory in Almaty is a monument dedicated to the heroes and soldiers who fought during WWII.',
                'address': 'Dosmuhamedov St, Almaty 050000',
                'lat': 43.2724,
                'lng': 76.9717,
                'category': 0,
            },
            {
                'id': 1010,
                'slug': 'botanical-garden',
                'name': 'Botanical Garden',
                'description': 'The Main Botanical Garden of Almaty is a large green oasis spanning over 103 hectares.',
                'address': 'Timiryazev St 36, Almaty 050040',
                'lat': 43.2248,
                'lng': 76.9380,
                'category': 2,
            },
            {
                'id': 1011,
                'slug': 'terrencourt',
                'name': 'Terrencourt',
                'description': 'Terrencourt is a popular health trail and walking route in the foothills of the Tien Shan mountains.',
                'address': 'Medeu District, Almaty',
                'lat': 43.2290,
                'lng': 76.9585,
                'category': 2,
            },
            {
                'id': 1012,
                'slug': 'panfilov-park',
                'name': 'Park named after 28 Panfilov Guards',
                'description': 'The Park of 28 Panfilov Guardsmen is one of the most beautiful and historic parks in Almaty.',
                'address': 'Gogol St, Almaty 050000',
                'lat': 43.2580,
                'lng': 76.9530,
                'category': 2,
            },
            {
                'id': 1013,
                'slug': 'republic-square',
                'name': 'Republic Square',
                'description': 'Republic Square is the central square of Almaty and one of the main public spaces in the city.',
                'address': 'Satpaev Ave, Almaty 050000',
                'lat': 43.2390,
                'lng': 76.9505,
                'category': 0,
            },
            {
                'id': 1014,
                'slug': 'kbtu',
                'name': 'Kazakh-British Technical University',
                'description': 'Kazakh-British Technical University (KBTU) is one of the leading technical universities in Kazakhstan.',
                'address': 'Tole Bi St 59, Almaty 050000',
                'lat': 43.2485,
                'lng': 76.9365,
                'category': 1,
            },
            {
                'id': 1015,
                'slug': 'arasan-spa',
                'name': 'Arasan Wellness & Spa',
                'description': 'Arasan Baths is one of the most famous bathhouses in Central Asia.',
                'address': 'Tulebaev St 78, Almaty 050000',
                'lat': 43.2570,
                'lng': 76.9445,
                'category': 0,
            },
            {
                'id': 1016,
                'slug': 'nedelka-fountain',
                'name': 'Nedelka Fountain',
                'description': 'The Nedelka Fountain (also known as the "Week" Fountain) is a charming public fountain in Almaty.',
                'address': 'Panfilov Park, Almaty 050000',
                'lat': 43.2575,
                'lng': 76.9538,
                'category': 0,
            },
            {
                'id': 1017,
                'slug': 'abai-opera-ballet',
                'name': 'Abai Opera and Ballet Theater',
                'description': 'The Abai State Academic Opera and Ballet Theater is the leading opera and ballet institution in Kazakhstan.',
                'address': 'Kabanbay Batyr Ave 110, Almaty 050000',
                'lat': 43.2425,
                'lng': 76.9390,
                'category': 1,
            },
            {
                'id': 1018,
                'slug': 'central-mosque',
                'name': 'Central Mosque',
                'description': 'The Central Mosque of Almaty is one of the largest mosques in Kazakhstan.',
                'address': 'Pushkin St 16, Almaty 050000',
                'lat': 43.2685,
                'lng': 76.9305,
                'category': 0,
            },
            {
                'id': 1019,
                'slug': 'central-recreation-park',
                'name': 'Central Recreation Park of Almaty',
                'description': 'The Central Park of Culture and Recreation in Almaty is the largest park in the city.',
                'address': 'Gogol St 1, Almaty 050040',
                'lat': 43.2295,
                'lng': 76.9620,
                'category': 2,
            },
        ]

        for item in places_data:
            place, created = Place.objects.get_or_create(
                id=item['id'],
                defaults={
                    'category': item['category'],
                    'address': item['address'],
                    'latitude': item['lat'],
                    'longitude': item['lng'],
                    'image': f"https://picsum.photos/seed/{item['slug']}/800/600",
                    'link': 'https://almatour.kz',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created place: {item['name']}"))
            else:
                place.latitude = item['lat']
                place.longitude = item['lng']
                place.save()
                self.stdout.write(self.style.WARNING(f"Updated place coordinates: {item['name']}"))

            # Create translations
            for lang_id, lang_code in [(0, 'en'), (1, 'ru'), (2, 'kz')]:
                PlaceTranslation.objects.update_or_create(
                    place=place,
                    language_id=lang_id,
                    defaults={
                        'name': f"{item['name']} ({lang_code})",
                        'description': f"{item['description']} ({lang_code})",
                        'timetable': '9:00 - 18:00',
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated places for map.'))
