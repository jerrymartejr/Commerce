# Generated by Django 4.1.5 on 2023-01-09 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_bid_highest_bid_auctionlisting_highest_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
