# Generated by Django 4.1.5 on 2023-01-09 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_auctionlisting_category_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
