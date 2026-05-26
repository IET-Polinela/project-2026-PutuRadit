import random
from django.core.management.base import BaseCommand
from faker import Faker
from reports.models import Report

fake = Faker('id_ID')


class Command(BaseCommand):
    help = 'Generate fake reports'

    def add_arguments(self, parser):
        parser.add_argument('num_records', type=int)

    def handle(self, *args, **kwargs):
        num_records = kwargs['num_records']

        context_data = {
            'Jalan Rusak': [
                'Lubang Besar di Tengah Jalan',
                'Aspal Mengelupas Parah',
                'Jalan Bergelombang'
            ],
            'Sampah': [
                'Tumpukan Sampah Liar',
                'Bau Menyengat',
                'TPS Penuh'
            ],
            'Lampu Mati': [
                'Lampu Jalan Mati Total',
                'Lampu Berkedip'
            ],
            'Drainase': [
                'Saluran Air Mampet',
                'Drainase Meluap'
            ],
            'Keamanan': [
                'Vandalisme Fasilitas Umum',
                'Kerumunan Mencurigakan'
            ],
        }

        status_choices = [
            'REPORTED',
            'VERIFIED',
            'IN_PROGRESS',
            'RESOLVED'
        ]

        for _ in range(num_records):
            category = random.choice(list(context_data.keys()))
            title = random.choice(context_data[category])

            Report.objects.create(
                title=f"{title} - {fake.street_name()}",
                description=f"Lokasi: {fake.address()}",
                location=f"{fake.city()} - {fake.street_address()}",
                category=category,
                status=random.choice(status_choices),
            )

        self.stdout.write(
            self.style.SUCCESS(f'{num_records} data berhasil dibuat!')
        )