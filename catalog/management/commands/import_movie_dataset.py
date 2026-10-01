import csv
import os
from django.core.management.base import BaseCommand
from catalog.models import MovieDatasetRecord
from django.conf import settings
from decimal import Decimal, InvalidOperation

class Command(BaseCommand):
    help = 'Imports exactly 50,000 records into MovieDatasetRecord from the verified CSV'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'docs', 'dataset', 'mediamerge_movies_50000.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        if MovieDatasetRecord.objects.count() >= 50000:
            self.stdout.write(self.style.WARNING("Dataset already imported (>= 50,000 records exist). Skipping import to prevent duplicates."))
            return

        # Expected headers
        expected_headers = [
            "source_id", "title", "original_title", "media_type",
            "release_year", "runtime_minutes", "language", "genre",
            "rating", "vote_count", "description"
        ]

        records_to_create = []
        batch_size = 5000
        total_imported = 0
        skipped = 0

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

            if headers != expected_headers:
                self.stderr.write(self.style.ERROR(f"Column mismatch.\nExpected: {expected_headers}\nGot: {headers}"))
                return

            rows = list(reader)
            if len(rows) != 50000:
                self.stderr.write(self.style.ERROR(f"Row count mismatch. Expected exactly 50000, got {len(rows)}."))
                return

            self.stdout.write("Validating rows and preparing objects...")

            for row in rows:
                if len(row) != 11:
                    skipped += 1
                    continue
                    
                row_dict = dict(zip(headers, row))

                # Handle numeric conversions carefully
                release_year = int(row_dict['release_year']) if row_dict['release_year'].strip() else None
                runtime_minutes = int(row_dict['runtime_minutes']) if row_dict['runtime_minutes'].strip() else None
                vote_count = int(row_dict['vote_count']) if row_dict['vote_count'].strip() else None
                
                try:
                    rating = Decimal(row_dict['rating']) if row_dict['rating'].strip() else None
                except InvalidOperation:
                    rating = None

                records_to_create.append(
                    MovieDatasetRecord(
                        source_id=row_dict['source_id'][:50],
                        title=row_dict['title'][:500],
                        original_title=row_dict['original_title'][:500],
                        media_type=row_dict['media_type'][:50],
                        release_year=release_year,
                        runtime_minutes=runtime_minutes,
                        language=row_dict['language'][:100],
                        genre=row_dict['genre'][:255],
                        rating=rating,
                        vote_count=vote_count,
                        description=row_dict['description']
                    )
                )

        self.stdout.write("Starting bulk insert (this may take a few seconds)...")
        
        # Insert in batches
        MovieDatasetRecord.objects.bulk_create(records_to_create, batch_size=batch_size)
        total_imported = len(records_to_create)

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {total_imported} records. Skipped {skipped} records."))
