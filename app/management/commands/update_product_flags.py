"""Management command to update all product flags."""

from django.core.management.base import BaseCommand
from app.models import Product


class Command(BaseCommand):
    help = 'Update all product flags (trending, new, controversial, popular)'

    def handle(self, *args, **options):
        products = Product.objects.all()
        updated_count = 0

        for product in products:
            # Update all flags for this product
            product.update_all_flags(save=True)
            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated flags for {updated_count} products'
            )
        )
